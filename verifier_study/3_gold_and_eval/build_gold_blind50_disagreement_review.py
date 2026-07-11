"""
backend/app/services/build_gold_blind50_disagreement_review.py

Build a readable review file for blind-50 disagreement cases.

Inputs:
  data/distill_arxiv/gold_blind50_review_labeled.jsonl
  data/distill_arxiv/gold_eval_teacher_drafted_opus.json
  data/distill_arxiv/gold_eval_teacher_labeled_llama70b_closed.json

Outputs:
  data/distill_arxiv/gold_blind50_disagreement_review.md
  data/distill_arxiv/gold_blind50_disagreement_review.jsonl

Use after blind-50 labels are completed and teacher audit has been run.

Run:
  python -m app.services.build_gold_blind50_disagreement_review
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from collections import Counter


GOLD_DIR = Path("data") / "distill_arxiv"

HUMAN_IN = GOLD_DIR / "gold_blind50_review_labeled.jsonl"
OPUS_IN = GOLD_DIR / "gold_eval_teacher_drafted_opus.json"
LLAMA_IN = GOLD_DIR / "gold_eval_teacher_labeled_llama70b_closed.json"

OUT_MD = GOLD_DIR / "gold_blind50_disagreement_review.md"
OUT_JSONL = GOLD_DIR / "gold_blind50_disagreement_review.jsonl"

LABEL_KEYS = [
    "gold_draft_label",
    "teacher_label",
    "draft_label",
    "label",
    "pred_label",
]

RATIONALE_KEYS = [
    "gold_draft_rationale",
    "teacher_rationale",
    "draft_rationale",
    "rationale",
]

CONF_KEYS = [
    "gold_draft_confidence",
    "teacher_confidence",
    "draft_confidence",
    "confidence",
]


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
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


def load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def norm_label(x: Any) -> str:
    s = str(x or "").strip().upper()
    if s in {"SUPPORTED", "UNSUPPORTED", "ABSTENTION"}:
        return s
    return ""


def by_claim_id(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out = {}
    for r in rows:
        cid = str(r.get("claim_id") or "").strip()
        if cid:
            out[cid] = r
    return out


def get_first(row: dict[str, Any], keys: list[str]) -> Any:
    for k in keys:
        if k in row and row.get(k) not in [None, ""]:
            return row.get(k)
    return ""


def model_label(row: dict[str, Any] | None) -> str:
    if not row:
        return ""
    return norm_label(get_first(row, LABEL_KEYS))


def model_rationale(row: dict[str, Any] | None) -> str:
    if not row:
        return ""
    return str(get_first(row, RATIONALE_KEYS) or "").strip()


def model_conf(row: dict[str, Any] | None) -> Any:
    if not row:
        return ""
    return get_first(row, CONF_KEYS)


def bq(text: Any) -> str:
    s = str(text or "").strip()
    if not s:
        return "> "
    return "\n".join("> " + line for line in s.splitlines())


def short_reason(h: str, o: str, l: str) -> list[str]:
    reasons = []
    if o and h != o:
        reasons.append("human_vs_opus")
    if l and h != l:
        reasons.append("human_vs_llama")
    if o and l and o != l:
        reasons.append("opus_vs_llama")
    if "ABSTENTION" in {h, o, l} and len({x for x in [h, o, l] if x}) > 1:
        reasons.append("abstention_boundary")
    if "UNSUPPORTED" in {h, o, l} and len({x for x in [h, o, l] if x}) > 1:
        reasons.append("unsupported_boundary")
    return reasons


def main() -> None:
    human_rows = read_jsonl(HUMAN_IN)
    opus_rows = load_json(OPUS_IN) if OPUS_IN.exists() else []
    llama_rows = load_json(LLAMA_IN) if LLAMA_IN.exists() else []

    opus_by_id = by_claim_id(opus_rows if isinstance(opus_rows, list) else [])
    llama_by_id = by_claim_id(llama_rows if isinstance(llama_rows, list) else [])

    disagreements = []
    all_rows = []

    for r in human_rows:
        cid = str(r.get("claim_id"))
        human = norm_label(r.get("human_label"))
        opus = model_label(opus_by_id.get(cid))
        llama = model_label(llama_by_id.get(cid))

        reasons = short_reason(human, opus, llama)

        rec = {
            "blind_id": r.get("blind_id"),
            "claim_id": cid,
            "question_type": r.get("question_type"),
            "answer_variant": r.get("answer_variant"),
            "evidence_scope": r.get("evidence_scope"),
            "human_label": human,
            "human_notes": r.get("human_notes"),
            "opus_label": opus,
            "opus_confidence": model_conf(opus_by_id.get(cid)),
            "opus_rationale": model_rationale(opus_by_id.get(cid)),
            "llama70b_label": llama,
            "llama70b_confidence": model_conf(llama_by_id.get(cid)),
            "llama70b_rationale": model_rationale(llama_by_id.get(cid)),
            "disagreement_reasons": reasons,
            "question": r.get("question"),
            "claim": r.get("claim"),
            "evidence_text_for_verifier": r.get("evidence_text_for_verifier"),
            "review_final_label": "",
            "review_notes": "",
        }

        all_rows.append(rec)
        if reasons:
            disagreements.append(rec)

    write_jsonl(OUT_JSONL, disagreements)

    md = []
    md.append("# Gold Blind-50 Disagreement Review")
    md.append("")
    md.append("Review only these cases first. Fill `REVIEW_FINAL_LABEL` if you decide your blind label should change.")
    md.append("")
    md.append("Allowed labels: `SUPPORTED`, `UNSUPPORTED`, `ABSTENTION`.")
    md.append("")
    md.append("## Summary")
    md.append("")
    md.append(f"- Blind rows: **{len(human_rows)}**")
    md.append(f"- Disagreement rows: **{len(disagreements)}**")
    md.append(f"- Human labels: `{dict(Counter(x['human_label'] for x in all_rows))}`")
    md.append(f"- Opus labels on blind rows: `{dict(Counter(x['opus_label'] for x in all_rows))}`")
    md.append(f"- Llama labels on blind rows: `{dict(Counter(x['llama70b_label'] for x in all_rows))}`")
    md.append("")
    md.append("Disagreement reasons:")
    md.append("")
    reason_counter = Counter()
    for d in disagreements:
        reason_counter.update(d["disagreement_reasons"])
    for k, v in reason_counter.most_common():
        md.append(f"- **{k}:** {v}")
    md.append("")
    md.append("---")
    md.append("")

    # Sort boundary cases first, then by blind ID.
    def sort_key(x):
        priority = 0
        if "abstention_boundary" in x["disagreement_reasons"]:
            priority -= 2
        if "unsupported_boundary" in x["disagreement_reasons"]:
            priority -= 1
        return (priority, str(x.get("blind_id")))

    for d in sorted(disagreements, key=sort_key):
        md.append(f"## {d['blind_id']} — {d['claim_id']}")
        md.append("")
        md.append(f"**question_type:** `{d.get('question_type')}`  ")
        md.append(f"**answer_variant:** `{d.get('answer_variant')}`  ")
        md.append(f"**evidence_scope:** `{d.get('evidence_scope')}`")
        md.append("")
        md.append("### Labels")
        md.append("")
        md.append(f"- **Human blind:** `{d['human_label']}`")
        if d.get("human_notes"):
            md.append(f"  - Human notes: {d.get('human_notes')}")
        md.append(f"- **Opus:** `{d['opus_label']}` confidence=`{d['opus_confidence']}`")
        if d.get("opus_rationale"):
            md.append(f"  - Opus rationale: {d.get('opus_rationale')}")
        md.append(f"- **Llama-70B:** `{d['llama70b_label']}` confidence=`{d['llama70b_confidence']}`")
        if d.get("llama70b_rationale"):
            md.append(f"  - Llama rationale: {d.get('llama70b_rationale')}")
        md.append("")
        md.append(f"**Disagreement reasons:** `{', '.join(d['disagreement_reasons'])}`")
        md.append("")
        md.append("**REVIEW_FINAL_LABEL:** ")
        md.append("")
        md.append("**REVIEW_NOTES:** ")
        md.append("")
        md.append("### Question")
        md.append("")
        md.append(bq(d.get("question")))
        md.append("")
        md.append("### Claim")
        md.append("")
        md.append(bq(d.get("claim")))
        md.append("")
        md.append("### Evidence")
        md.append("")
        md.append(bq(d.get("evidence_text_for_verifier")))
        md.append("")
        md.append("---")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    print("\nBuilt blind-50 disagreement review")
    print("=" * 64)
    print(f"Blind rows:        {len(human_rows)}")
    print(f"Disagreement rows: {len(disagreements)}")
    print(f"Reason counts:     {dict(reason_counter)}")
    print(f"Wrote:             {OUT_MD}")
    print(f"Wrote:             {OUT_JSONL}")


if __name__ == "__main__":
    main()
