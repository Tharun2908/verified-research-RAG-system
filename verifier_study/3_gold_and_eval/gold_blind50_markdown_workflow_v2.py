"""
backend/app/services/gold_blind50_markdown_workflow_v2.py

More robust blind-50 Markdown workflow.

Use this if the first importer reports blank labels even though you filled the Markdown.
It accepts labels on the same line or next line after HUMAN_LABEL.

Commands from backend/:
  python -m app.services.gold_blind50_markdown_workflow_v2 export
  python -m app.services.gold_blind50_markdown_workflow_v2 import-labels
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

GOLD_DIR = Path("data") / "distill_arxiv"
DEFAULT_JSONL = GOLD_DIR / "gold_blind50_review.jsonl"
DEFAULT_MD = GOLD_DIR / "gold_blind50_review_readable.md"
DEFAULT_LABELED_JSONL = GOLD_DIR / "gold_blind50_review_labeled.jsonl"
ALLOWED = {"SUPPORTED", "UNSUPPORTED", "ABSTENTION"}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with open(path, encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise SystemExit(f"Invalid JSONL at {path}:{line_no}: {e}") from e
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def blockquote(text: Any) -> str:
    s = str(text or "").strip()
    if not s:
        return "> "
    return "\n".join("> " + line for line in s.splitlines())


def export_markdown(args: argparse.Namespace) -> None:
    rows = read_jsonl(args.input)
    lines = []
    lines.append("# Gold Blind-50 Review")
    lines.append("")
    lines.append("Fill `HUMAN_LABEL` with exactly one of: `SUPPORTED`, `UNSUPPORTED`, `ABSTENTION`.")
    lines.append("")
    lines.append("Do not open the hidden key or model draft files until all 50 labels are filled.")
    lines.append("")
    lines.append("---")
    lines.append("")

    for r in rows:
        blind_id = r.get("blind_id", "")
        claim_id = r.get("claim_id", "")
        human_label = str(r.get("human_label") or "").strip()
        human_notes = str(r.get("human_notes") or "").strip()
        lines.append(f"## {blind_id}")
        lines.append("")
        lines.append(f"**claim_id:** `{claim_id}`")
        lines.append("")
        lines.append(f"**question_type:** `{r.get('question_type', '')}`  ")
        lines.append(f"**answer_variant:** `{r.get('answer_variant', '')}`  ")
        lines.append(f"**evidence_scope:** `{r.get('evidence_scope', '')}`")
        lines.append("")
        lines.append("**HUMAN_LABEL:** " + human_label)
        lines.append("")
        lines.append("**HUMAN_NOTES:** " + human_notes)
        lines.append("")
        lines.append("### Question")
        lines.append("")
        lines.append(blockquote(r.get("question")))
        lines.append("")
        lines.append("### Claim")
        lines.append("")
        lines.append(blockquote(r.get("claim")))
        lines.append("")
        lines.append("### Evidence")
        lines.append("")
        lines.append(blockquote(r.get("evidence_text_for_verifier")))
        lines.append("")
        lines.append("### Label rules")
        lines.append("")
        rules = r.get("labeling_rules", {})
        if isinstance(rules, dict):
            for label in ["SUPPORTED", "UNSUPPORTED", "ABSTENTION"]:
                lines.append(f"- **{label}:** {rules.get(label, '')}")
        else:
            lines.append("- **SUPPORTED:** Evidence directly supports the claim.")
            lines.append("- **UNSUPPORTED:** Claim is contradicted, unverifiable, or adds details not in evidence.")
            lines.append("- **ABSTENTION:** Refusal/no substantive factual answer claim/insufficient-evidence statement.")
        lines.append("")
        lines.append("---")
        lines.append("")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print("\nExported readable blind-50 markdown")
    print("=" * 56)
    print(f"Rows:  {len(rows)}")
    print(f"Wrote: {args.output}")


def clean_candidate_label(s: str) -> str:
    s = str(s or "").strip()
    s = re.sub(r"^[>*#\-\s]+", "", s).strip()
    s = s.strip("`*_ ").strip()
    s = s.upper().replace("-", "_").replace(" ", "_")
    s = re.sub(r"[^A-Z_]", "", s)
    return s


def extract_field_block(section: str, field: str) -> str:
    marker_re = re.compile(
        rf"(?:\*\*)?{re.escape(field)}\s*:\s*(?:\*\*)?\s*",
        flags=re.IGNORECASE,
    )
    m = marker_re.search(section)
    if not m:
        return ""
    rest = section[m.end():]
    stop_patterns = [
        r"\n\s*(?:\*\*)?HUMAN_LABEL\s*:",
        r"\n\s*(?:\*\*)?HUMAN_NOTES\s*:",
        r"\n\s*###\s+Question",
        r"\n\s*###\s+Claim",
        r"\n\s*###\s+Evidence",
        r"\n\s*###\s+Label rules",
        r"\n\s*---\s*",
        r"\n\s*##\s+B\d+",
    ]
    stop = len(rest)
    for pat in stop_patterns:
        sm = re.search(pat, rest, flags=re.IGNORECASE)
        if sm:
            stop = min(stop, sm.start())
    return rest[:stop].strip()


def extract_label_from_section(section: str) -> str:
    block = extract_field_block(section, "HUMAN_LABEL")
    cand = clean_candidate_label(block)
    if cand in ALLOWED:
        return cand
    for line in block.splitlines():
        cand = clean_candidate_label(line)
        if cand in ALLOWED:
            return cand
    upper = block.upper()
    for label in ["SUPPORTED", "UNSUPPORTED", "ABSTENTION"]:
        if re.search(rf"\b{label}\b", upper):
            return label
    return ""


def extract_notes_from_section(section: str) -> str:
    block = extract_field_block(section, "HUMAN_NOTES")
    return block.strip()


def parse_markdown_labels(path: Path) -> dict[str, dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(r"^##\s+(B\d+)\s*$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    labels: dict[str, dict[str, str]] = {}
    for i, m in enumerate(matches):
        blind_id = m.group(1)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        section = text[start:end]
        labels[blind_id] = {
            "human_label": extract_label_from_section(section),
            "human_notes": extract_notes_from_section(section),
        }
    return labels


def import_labels(args: argparse.Namespace) -> None:
    rows = read_jsonl(args.input)
    labels = parse_markdown_labels(args.markdown)
    missing_sections = []
    blank_labels = []
    invalid_labels = []
    updated = []

    for r in rows:
        blind_id = str(r.get("blind_id"))
        parsed = labels.get(blind_id)
        if parsed is None:
            missing_sections.append(blind_id)
            updated.append(r)
            continue
        label = parsed["human_label"]
        notes = parsed["human_notes"]
        if not label:
            blank_labels.append(blind_id)
        elif label not in ALLOWED:
            invalid_labels.append((blind_id, label))
        rr = dict(r)
        rr["human_label"] = label
        rr["human_notes"] = notes
        updated.append(rr)

    if missing_sections:
        raise SystemExit(f"Missing markdown sections for blind IDs: {missing_sections[:10]}")
    if invalid_labels:
        raise SystemExit(f"Invalid labels: {invalid_labels[:10]}")

    out_path = args.input if args.overwrite_original else args.output
    write_jsonl(out_path, updated)

    print("\nImported blind-50 markdown labels")
    print("=" * 56)
    print(f"Rows:          {len(updated)}")
    print(f"Blank labels:  {len(blank_labels)}")
    if blank_labels:
        print(f"Blank IDs:      {blank_labels[:20]}")
    print(f"Wrote:         {out_path}")
    if blank_labels:
        print("\nStill blank. Accepted examples:")
        print("  **HUMAN_LABEL:** SUPPORTED")
        print("  HUMAN_LABEL: UNSUPPORTED")
        print("  **HUMAN_LABEL:**")
        print("  ABSTENTION")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    ep = sub.add_parser("export")
    ep.add_argument("--input", type=Path, default=DEFAULT_JSONL)
    ep.add_argument("--output", type=Path, default=DEFAULT_MD)

    ip = sub.add_parser("import-labels")
    ip.add_argument("--input", type=Path, default=DEFAULT_JSONL)
    ip.add_argument("--markdown", type=Path, default=DEFAULT_MD)
    ip.add_argument("--output", type=Path, default=DEFAULT_LABELED_JSONL)
    ip.add_argument("--overwrite-original", action="store_true")

    args = ap.parse_args()
    if args.cmd == "export":
        export_markdown(args)
    elif args.cmd == "import-labels":
        import_labels(args)
    else:
        raise SystemExit(f"Unknown command: {args.cmd}")


if __name__ == "__main__":
    main()
