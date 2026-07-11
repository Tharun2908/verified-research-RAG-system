"""
backend/app/services/build_arxiv_gold_full_assisted_review.py

Build a full protected-gold assisted-review file after blind-50 is complete.

Inputs:
  data/distill_arxiv/gold_eval_teacher_drafted_opus.json
  data/distill_arxiv/gold_eval_teacher_labeled_llama70b_closed.json
  data/distill_arxiv/gold_blind50_review_labeled.jsonl

Outputs:
  data/distill_arxiv/gold_full_assisted_review.md
  data/distill_arxiv/gold_full_assisted_review.jsonl
  data/distill_arxiv/gold_full_assisted_review_report.json

Review policy:
  - Opus is the primary draft because blind-50 showed stronger alignment.
  - Llama-70B is a high-recall warning signal.
  - For the 50 blind-reviewed rows, human blind labels are carried in as existing labels.
  - For the remaining rows, FINAL_LABEL is left blank.
  - Refusal/insufficient-evidence/meta statements should be ABSTENTION, even if the meta-statement is true.

Run:
  python -m app.services.build_arxiv_gold_full_assisted_review
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


GOLD_DIR = Path("data") / "distill_arxiv"

OPUS_IN = GOLD_DIR / "gold_eval_teacher_drafted_opus.json"
LLAMA_IN = GOLD_DIR / "gold_eval_teacher_labeled_llama70b_closed.json"
BLIND_IN = GOLD_DIR / "gold_blind50_review_labeled.jsonl"

OUT_MD = GOLD_DIR / "gold_full_assisted_review.md"
OUT_JSONL = GOLD_DIR / "gold_full_assisted_review.jsonl"
OUT_REPORT = GOLD_DIR / "gold_full_assisted_review_report.json"

LABELS = {"SUPPORTED", "UNSUPPORTED", "ABSTENTION"}


def load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    if not path.exists():
        return rows
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def save_json(path: Path, obj: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def norm_label(x: Any) -> str:
    s = str(x or "").strip().upper()
    return s if s in LABELS else ""


def by_claim_id(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out = {}
    for r in rows:
        cid = str(r.get("claim_id") or "").strip()
        if cid:
            out[cid] = r
    return out


def first(row: dict[str, Any] | None, keys: list[str]) -> Any:
    if not row:
        return ""
    for k in keys:
        if k in row and row.get(k) not in [None, ""]:
            return row.get(k)
    return ""


def llama_label(row: dict[str, Any] | None) -> str:
    return norm_label(first(row, ["teacher_label", "label", "pred_label"]))


def llama_conf(row: dict[str, Any] | None) -> Any:
    return first(row, ["teacher_confidence", "confidence"])


def llama_rationale(row: dict[str, Any] | None) -> str:
    return str(first(row, ["teacher_rationale", "rationale"]) or "").strip()


def blockquote(text: Any) -> str:
    s = str(text or "").strip()
    if not s:
        return "> "
    return "\n".join("> " + line for line in s.splitlines())


def warning_flags(opus: str, llama: str, claim: str) -> list[str]:
    flags = []

    if opus and llama and opus != llama:
        flags.append("OPUS_LLAMA_DISAGREE")

    if llama == "UNSUPPORTED" and opus != "UNSUPPORTED":
        flags.append("LLAMA_UNSUPPORTED_WARNING")

    if opus == "SUPPORTED" and llama == "UNSUPPORTED":
        flags.append("SUPPORTED_VS_UNSUPPORTED_CONFLICT")

    if opus == "ABSTENTION" or llama == "ABSTENTION":
        flags.append("ABSTENTION_BOUNDARY_CHECK")

    c = (claim or "").lower()
    if any(x in c for x in [
        "do not contain information",
        "does not contain information",
        "not enough information",
        "insufficient information",
        "unable to answer",
        "unable to provide",
        "provided sources do not",
        "provided evidence does not",
    ]):
        flags.append("REFUSAL_META_STATEMENT_CHECK")

    # Short malformed fragments are often extraction errors.
    if len(str(claim or "").strip().split()) <= 6:
        flags.append("SHORT_OR_MALFORMED_CLAIM_CHECK")

    return sorted(set(flags))


def main() -> None:
    opus_rows = load_json(OPUS_IN)
    llama_rows = load_json(LLAMA_IN)
    blind_rows = read_jsonl(BLIND_IN)

    if not isinstance(opus_rows, list):
        raise SystemExit(f"{OPUS_IN} must be a JSON list.")
    if not isinstance(llama_rows, list):
        raise SystemExit(f"{LLAMA_IN} must be a JSON list.")

    llama_by_id = by_claim_id(llama_rows)
    blind_by_id = by_claim_id(blind_rows)

    review_rows = []

    for idx, o in enumerate(opus_rows, start=1):
        cid = str(o.get("claim_id") or "").strip()
        l = llama_by_id.get(cid)
        b = blind_by_id.get(cid)

        opus_lab = norm_label(o.get("gold_draft_label"))
        llab = llama_label(l)
        blind_lab = norm_label(b.get("human_label")) if b else ""

        claim = o.get("claim") or o.get("claim_text")
        flags = warning_flags(opus_lab, llab, str(claim or ""))

        final_label = blind_lab if blind_lab else ""
        final_notes = ""
        if blind_lab:
            final_notes = "Carried over from completed blind-50 review."
            if b.get("human_notes"):
                final_notes += " " + str(b.get("human_notes")).strip()

        rec = {
            "review_id": f"G{idx:03d}",
            "claim_id": cid,
            "is_blind50": bool(blind_lab),
            "question": o.get("question"),
            "question_type": o.get("question_type") or o.get("type"),
            "answer_variant": o.get("answer_variant"),
            "evidence_scope": o.get("evidence_scope"),
            "claim": claim,
            "evidence_text_for_verifier": o.get("evidence_text_for_verifier"),
            "opus_label": opus_lab,
            "opus_confidence": o.get("gold_draft_confidence"),
            "opus_rationale": o.get("gold_draft_rationale"),
            "llama70b_label": llab,
            "llama70b_confidence": llama_conf(l),
            "llama70b_rationale": llama_rationale(l),
            "warning_flags": flags,
            "final_label": final_label,
            "final_notes": final_notes,
            "allowed_labels": ["SUPPORTED", "UNSUPPORTED", "ABSTENTION"],
        }
        review_rows.append(rec)

    write_jsonl(OUT_JSONL, review_rows)

    # Put warning rows first after blind rows? For markdown, sort:
    # 1) blank final labels with warning flags
    # 2) blank final labels without warning flags
    # 3) blind rows already labeled
    def sort_key(r: dict[str, Any]):
        if r["is_blind50"]:
            group = 2
        elif r["warning_flags"]:
            group = 0
        else:
            group = 1
        return (group, r["review_id"])

    md = []
    md.append("# Full Gold Assisted Review")
    md.append("")
    md.append("Fill `FINAL_LABEL` with one of: `SUPPORTED`, `UNSUPPORTED`, `ABSTENTION`.")
    md.append("")
    md.append("Rules:")
    md.append("")
    md.append("- **SUPPORTED:** Evidence directly supports the claim.")
    md.append("- **UNSUPPORTED:** Claim asserts a factual detail not supported by evidence.")
    md.append("- **ABSTENTION:** Refusal/no-answer/insufficient-evidence/meta statement, or malformed/no substantive factual claim.")
    md.append("")
    md.append("Important boundary rule:")
    md.append("")
    md.append("> If the answer says the provided sources do not contain enough information, label it **ABSTENTION**, not SUPPORTED, even if that meta-statement is true.")
    md.append("")
    md.append("Opus is the primary draft. Llama-70B is a warning signal.")
    md.append("")
    md.append("---")
    md.append("")

    for r in sorted(review_rows, key=sort_key):
        md.append(f"## {r['review_id']} — {r['claim_id']}")
        md.append("")
        md.append(f"**blind50:** `{r['is_blind50']}`  ")
        md.append(f"**question_type:** `{r.get('question_type')}`  ")
        md.append(f"**answer_variant:** `{r.get('answer_variant')}`  ")
        md.append(f"**evidence_scope:** `{r.get('evidence_scope')}`")
        md.append("")
        md.append(f"**FINAL_LABEL:** {r.get('final_label') or ''}")
        md.append("")
        md.append(f"**FINAL_NOTES:** {r.get('final_notes') or ''}")
        md.append("")
        md.append("### Drafts")
        md.append("")
        md.append(f"- **Opus:** `{r['opus_label']}` confidence=`{r['opus_confidence']}`")
        if r.get("opus_rationale"):
            md.append(f"  - {r.get('opus_rationale')}")
        md.append(f"- **Llama-70B:** `{r['llama70b_label']}` confidence=`{r['llama70b_confidence']}`")
        if r.get("llama70b_rationale"):
            md.append(f"  - {r.get('llama70b_rationale')}")
        if r.get("warning_flags"):
            md.append(f"- **Warning flags:** `{', '.join(r['warning_flags'])}`")
        else:
            md.append("- **Warning flags:** `none`")
        md.append("")
        md.append("### Question")
        md.append("")
        md.append(blockquote(r.get("question")))
        md.append("")
        md.append("### Claim")
        md.append("")
        md.append(blockquote(r.get("claim")))
        md.append("")
        md.append("### Evidence")
        md.append("")
        md.append(blockquote(r.get("evidence_text_for_verifier")))
        md.append("")
        md.append("---")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    report = {
        "inputs": {
            "opus": str(OPUS_IN),
            "llama": str(LLAMA_IN),
            "blind50": str(BLIND_IN),
        },
        "outputs": {
            "markdown": str(OUT_MD),
            "jsonl": str(OUT_JSONL),
            "report": str(OUT_JSONL),
        },
        "summary": {
            "rows_total": len(review_rows),
            "blind50_carried_over": sum(1 for r in review_rows if r["is_blind50"]),
            "blank_final_labels": sum(1 for r in review_rows if not r["final_label"]),
            "opus_counts": dict(Counter(r["opus_label"] for r in review_rows)),
            "llama_counts": dict(Counter(r["llama70b_label"] for r in review_rows)),
            "warning_rows": sum(1 for r in review_rows if r["warning_flags"]),
            "opus_llama_disagreements": sum(1 for r in review_rows if "OPUS_LLAMA_DISAGREE" in r["warning_flags"]),
            "llama_unsupported_warnings": sum(1 for r in review_rows if "LLAMA_UNSUPPORTED_WARNING" in r["warning_flags"]),
            "refusal_meta_statement_checks": sum(1 for r in review_rows if "REFUSAL_META_STATEMENT_CHECK" in r["warning_flags"]),
            "short_or_malformed_claim_checks": sum(1 for r in review_rows if "SHORT_OR_MALFORMED_CLAIM_CHECK" in r["warning_flags"]),
        },
    }

    save_json(OUT_REPORT, report)

    print("\nBuilt full gold assisted review")
    print("=" * 72)
    for k, v in report["summary"].items():
        print(f"{k}: {v}")
    print("\nWrote:")
    print(f"  {OUT_MD}")
    print(f"  {OUT_JSONL}")
    print(f"  {OUT_REPORT}")


if __name__ == "__main__":
    main()
