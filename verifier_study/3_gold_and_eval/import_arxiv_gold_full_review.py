"""
backend/app/services/import_arxiv_gold_full_review.py

Import final human labels from the full gold assisted-review markdown and build
the frozen human-reviewed gold file.

Inputs:
  data/distill_arxiv/gold_full_assisted_review.md
  data/distill_arxiv/gold_full_assisted_review.jsonl

Outputs:
  data/distill_arxiv/gold_full_assisted_review_labeled.jsonl
  data/distill_arxiv/gold_final_human_reviewed.json
  data/distill_arxiv/gold_final_human_review_summary.json

Run from backend/:
  python -m app.services.import_arxiv_gold_full_review
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


GOLD_DIR = Path("data") / "distill_arxiv"

DEFAULT_MD = GOLD_DIR / "gold_full_assisted_review.md"
DEFAULT_BASE_JSONL = GOLD_DIR / "gold_full_assisted_review.jsonl"

OUT_LABELED_JSONL = GOLD_DIR / "gold_full_assisted_review_labeled.jsonl"
OUT_FINAL_JSON = GOLD_DIR / "gold_final_human_reviewed.json"
OUT_SUMMARY = GOLD_DIR / "gold_final_human_review_summary.json"

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


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def clean_label(s: Any) -> str:
    s = str(s or "").strip()
    s = re.sub(r"^[>*#\-\s]+", "", s).strip()
    s = s.strip("`*_ ").strip()
    s = s.upper()
    s = s.replace("-", "_").replace(" ", "_")
    s = re.sub(r"[^A-Z_]", "", s)
    return s if s in ALLOWED else ""


def extract_field_block(section: str, field: str) -> str:
    marker_re = re.compile(
        rf"(?:\*\*)?{re.escape(field)}\s*:\s*(?:\*\*)?\s*",
        flags=re.IGNORECASE,
    )
    m = marker_re.search(section)
    if not m:
        return ""

    start = m.end()
    rest = section[start:]

    stop_patterns = [
        r"\n\s*(?:\*\*)?FINAL_LABEL\s*:",
        r"\n\s*(?:\*\*)?FINAL_NOTES\s*:",
        r"\n\s*###\s+Drafts",
        r"\n\s*###\s+Question",
        r"\n\s*###\s+Claim",
        r"\n\s*###\s+Evidence",
        r"\n\s*---\s*",
        r"\n\s*##\s+G\d+",
    ]

    stop = len(rest)
    for pat in stop_patterns:
        sm = re.search(pat, rest, flags=re.IGNORECASE)
        if sm:
            stop = min(stop, sm.start())

    return rest[:stop].strip()


def extract_label(section: str) -> str:
    block = extract_field_block(section, "FINAL_LABEL")

    cand = clean_label(block)
    if cand:
        return cand

    for line in block.splitlines():
        cand = clean_label(line)
        if cand:
            return cand

    upper = block.upper()
    for label in ALLOWED:
        if re.search(rf"\b{label}\b", upper):
            return label

    return ""


def extract_notes(section: str) -> str:
    block = extract_field_block(section, "FINAL_NOTES")
    return block.strip()


def parse_markdown(path: Path) -> dict[str, dict[str, str]]:
    text = path.read_text(encoding="utf-8")

    pattern = re.compile(r"^##\s+(G\d+)\s+—\s+([^\s]+)\s*$", re.MULTILINE)
    matches = list(pattern.finditer(text))

    parsed: dict[str, dict[str, str]] = {}

    for i, m in enumerate(matches):
        review_id = m.group(1)
        claim_id = m.group(2)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        section = text[start:end]

        parsed[review_id] = {
            "review_id": review_id,
            "claim_id": claim_id,
            "final_label": extract_label(section),
            "final_notes": extract_notes(section),
        }

    return parsed


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--markdown", type=Path, default=DEFAULT_MD)
    ap.add_argument("--base-jsonl", type=Path, default=DEFAULT_BASE_JSONL)
    ap.add_argument("--out-labeled-jsonl", type=Path, default=OUT_LABELED_JSONL)
    ap.add_argument("--out-final-json", type=Path, default=OUT_FINAL_JSON)
    ap.add_argument("--out-summary", type=Path, default=OUT_SUMMARY)
    ap.add_argument("--allow-blanks", action="store_true")
    args = ap.parse_args()

    rows = read_jsonl(args.base_jsonl)
    parsed = parse_markdown(args.markdown)

    if not parsed:
        raise SystemExit(f"No review sections parsed from {args.markdown}")

    updated = []
    missing_sections = []
    blank_labels = []
    invalid_claim_mismatch = []

    for r in rows:
        review_id = str(r.get("review_id") or "")
        claim_id = str(r.get("claim_id") or "")

        p = parsed.get(review_id)
        if p is None:
            missing_sections.append(review_id)
            updated.append(r)
            continue

        if p.get("claim_id") != claim_id:
            invalid_claim_mismatch.append({
                "review_id": review_id,
                "jsonl_claim_id": claim_id,
                "markdown_claim_id": p.get("claim_id"),
            })

        label = clean_label(p.get("final_label"))
        notes = p.get("final_notes", "")

        if not label:
            blank_labels.append(review_id)

        rr = dict(r)
        rr["final_label"] = label
        rr["final_notes"] = notes
        rr["human_final_label"] = label
        rr["human_final_notes"] = notes
        rr["gold_label_source"] = "human_full_review"
        updated.append(rr)

    if missing_sections:
        raise SystemExit(f"Missing markdown sections for review IDs: {missing_sections[:20]}")
    if invalid_claim_mismatch:
        raise SystemExit(f"Claim ID mismatches: {invalid_claim_mismatch[:5]}")
    if blank_labels and not args.allow_blanks:
        raise SystemExit(
            f"Blank FINAL_LABEL for {len(blank_labels)} rows. First blanks: {blank_labels[:20]}\n"
            "Fill them in the markdown, or rerun with --allow-blanks only for debugging."
        )

    write_jsonl(args.out_labeled_jsonl, updated)

    final_rows = []
    for r in updated:
        final_rows.append({
            "claim_id": r.get("claim_id"),
            "review_id": r.get("review_id"),
            "question": r.get("question"),
            "question_type": r.get("question_type"),
            "answer_variant": r.get("answer_variant"),
            "evidence_scope": r.get("evidence_scope"),
            "claim": r.get("claim"),
            "claim_text": r.get("claim"),
            "evidence_text_for_verifier": r.get("evidence_text_for_verifier"),
            "final_label": r.get("final_label"),
            "human_final_label": r.get("human_final_label"),
            "final_notes": r.get("final_notes"),
            "is_blind50": r.get("is_blind50", False),
            "opus_label": r.get("opus_label"),
            "opus_confidence": r.get("opus_confidence"),
            "opus_rationale": r.get("opus_rationale"),
            "llama70b_label": r.get("llama70b_label"),
            "llama70b_confidence": r.get("llama70b_confidence"),
            "llama70b_rationale": r.get("llama70b_rationale"),
            "warning_flags": r.get("warning_flags", []),
        })

    save_json(args.out_final_json, final_rows)

    counts = Counter(r.get("final_label", "") for r in updated)
    by_qtype = {}
    for qt in sorted(set(str(r.get("question_type") or "unknown") for r in updated)):
        by_qtype[qt] = dict(Counter(r.get("final_label", "") for r in updated if str(r.get("question_type") or "unknown") == qt))

    by_arm = {}
    for arm in sorted(set(str(r.get("answer_variant") or "unknown") for r in updated)):
        by_arm[arm] = dict(Counter(r.get("final_label", "") for r in updated if str(r.get("answer_variant") or "unknown") == arm))

    by_qtype_arm_counter: dict[str, Counter] = {}
    for r in updated:
        key = f"{r.get('question_type') or 'unknown'}::{r.get('answer_variant') or 'unknown'}"
        by_qtype_arm_counter.setdefault(key, Counter())
        by_qtype_arm_counter[key][r.get("final_label", "")] += 1
    by_qtype_arm = {k: dict(v) for k, v in sorted(by_qtype_arm_counter.items())}

    supported = counts.get("SUPPORTED", 0)
    unsupported = counts.get("UNSUPPORTED", 0)
    abstention = counts.get("ABSTENTION", 0)

    summary = {
        "inputs": {
            "markdown": str(args.markdown),
            "base_jsonl": str(args.base_jsonl),
        },
        "outputs": {
            "labeled_jsonl": str(args.out_labeled_jsonl),
            "final_json": str(args.out_final_json),
            "summary": str(args.out_summary),
        },
        "rows_total": len(updated),
        "label_counts": dict(counts),
        "label_counts_by_question_type": by_qtype,
        "label_counts_by_answer_variant": by_arm,
        "label_counts_by_question_type_and_answer_variant": by_qtype_arm,
        "binary_usable_supported_unsupported": supported + unsupported,
        "confirmed_gold_unsupported": unsupported,
        "confirmed_gold_abstention": abstention,
        "gold_positive_gate_threshold_low": 50,
        "gold_positive_gate_threshold_high": 60,
        "gold_positive_gate_pass_50": unsupported >= 50,
        "gold_positive_gate_pass_60": unsupported >= 60,
        "second_gold_tranche_needed": unsupported < 50,
        "blank_labels": len(blank_labels),
        "notes": [
            "ABSTENTION rows should be excluded from binary supported-vs-unsupported evaluation.",
            "If confirmed gold UNSUPPORTED is below 50, generate a second gold tranche before final eval.",
        ],
    }

    save_json(args.out_summary, summary)

    print("\nImported full gold review")
    print("=" * 72)
    print(f"Rows total:                   {len(updated)}")
    print(f"Label counts:                 {dict(counts)}")
    print(f"Binary usable S/U:            {supported + unsupported}")
    print(f"Confirmed UNSUPPORTED:        {unsupported}")
    print(f"Confirmed ABSTENTION:         {abstention}")
    print(f"Gold positive gate >=50:      {unsupported >= 50}")
    print(f"Gold positive gate >=60:      {unsupported >= 60}")
    print(f"Second gold tranche needed:   {unsupported < 50}")
    print("\nBy question type:")
    for k, v in by_qtype.items():
        print(f"  {k}: {v}")
    print("\nBy answer arm:")
    for k, v in by_arm.items():
        print(f"  {k}: {v}")
    print("\nWrote:")
    print(f"  {args.out_labeled_jsonl}")
    print(f"  {args.out_final_json}")
    print(f"  {args.out_summary}")


if __name__ == "__main__":
    main()
