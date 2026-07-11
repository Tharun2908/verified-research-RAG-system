"""
backend/app/services/build_arxiv_gold_blind50_review.py

Build a blind-50 human review file from Opus-drafted gold claims WITHOUT exposing draft labels.

Input:
  data/distill_arxiv/gold_eval_teacher_drafted_opus.json

Outputs:
  data/distill_arxiv/gold_blind50_review.jsonl
  data/distill_arxiv/gold_blind50_manifest_hidden.json
  data/distill_arxiv/gold_blind50_build_report.json

Protocol:
  - The script may internally stratify by Opus draft label.
  - The review JSONL intentionally hides gold_draft_label/confidence/rationale.
  - Do NOT open the hidden manifest or Opus draft file until blind labels are completed.

Run from backend/:
  python -m app.services.build_arxiv_gold_blind50_review --n 50 --seed 2908
"""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


GOLD_DIR = Path("data") / "distill_arxiv"
DEFAULT_DRAFTS = GOLD_DIR / "gold_eval_teacher_drafted_opus.json"
OUT_REVIEW = GOLD_DIR / "gold_blind50_review.jsonl"
OUT_HIDDEN = GOLD_DIR / "gold_blind50_manifest_hidden.json"
OUT_REPORT = GOLD_DIR / "gold_blind50_build_report.json"

LABELS = ["SUPPORTED", "UNSUPPORTED", "ABSTENTION"]


def load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def evidence_text_from_list(evidence: Any) -> str:
    if not isinstance(evidence, list):
        return ""
    parts = []
    for i, ev in enumerate(evidence, start=1):
        if not isinstance(ev, dict):
            continue
        n = ev.get("number", ev.get("rank", i))
        title = str(ev.get("title") or "").strip()
        text = str(ev.get("text") or "").strip()
        parts.append(f"[{n}] {title}\n{text}".strip())
    return "\n\n".join([p for p in parts if p])


def evidence_text(row: dict[str, Any]) -> str:
    txt = str(row.get("evidence_text_for_verifier") or "").strip()
    if txt:
        return txt
    return evidence_text_from_list(row.get("evidence"))


def sample_stratified(rows: list[dict[str, Any]], n: int, rng: random.Random) -> list[dict[str, Any]]:
    """Stratify primarily by draft label, then fill remaining slots from all rows."""
    buckets = defaultdict(list)
    for r in rows:
        buckets[str(r.get("gold_draft_label", "UNKNOWN"))].append(r)
    for b in buckets.values():
        rng.shuffle(b)

    selected = []
    selected_ids = set()

    label_counts = Counter(r.get("gold_draft_label", "UNKNOWN") for r in rows)
    available_labels = [lab for lab in LABELS if label_counts.get(lab, 0) > 0]

    # Ensure minority labels are represented where possible.
    base_min = min(8, max(1, n // 6))
    for lab in available_labels:
        take = min(base_min, len(buckets[lab]), n - len(selected))
        for r in buckets[lab][:take]:
            selected.append(r)
            selected_ids.add(r.get("claim_id"))

    # Then proportional fill from all remaining rows.
    remaining = [r for r in rows if r.get("claim_id") not in selected_ids]
    rng.shuffle(remaining)
    for r in remaining:
        if len(selected) >= n:
            break
        selected.append(r)
        selected_ids.add(r.get("claim_id"))

    rng.shuffle(selected)
    return selected[:n]


def blind_row(row: dict[str, Any], blind_id: int) -> dict[str, Any]:
    return {
        "blind_id": f"B{blind_id:03d}",
        "claim_id": row.get("claim_id"),
        "question": row.get("question"),
        "answer_variant": row.get("answer_variant"),
        "question_type": row.get("question_type") or row.get("type"),
        "claim": row.get("claim") or row.get("claim_text"),
        "evidence_scope": row.get("evidence_scope"),
        "evidence_text_for_verifier": evidence_text(row),
        "human_label": "",
        "human_notes": "",
        "allowed_labels": ["SUPPORTED", "UNSUPPORTED", "ABSTENTION"],
        "labeling_rules": {
            "SUPPORTED": "Evidence directly supports the claim.",
            "UNSUPPORTED": "Claim is contradicted, unverifiable, or adds details not in evidence.",
            "ABSTENTION": "Refusal/no substantive factual answer claim/insufficient-evidence statement.",
        },
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--drafts", type=Path, default=DEFAULT_DRAFTS)
    ap.add_argument("--n", type=int, default=50)
    ap.add_argument("--seed", type=int, default=2908)
    args = ap.parse_args()

    rows = load_json(args.drafts)
    if not isinstance(rows, list):
        raise SystemExit(f"{args.drafts} must be a JSON list.")

    rng = random.Random(args.seed)
    selected = sample_stratified(rows, n=args.n, rng=rng)

    blind_rows = [blind_row(r, i) for i, r in enumerate(selected, start=1)]
    hidden_rows = [
        {
            "blind_id": blind_rows[i]["blind_id"],
            "claim_id": r.get("claim_id"),
            "gold_draft_label": r.get("gold_draft_label"),
            "gold_draft_confidence": r.get("gold_draft_confidence"),
            "gold_draft_rationale": r.get("gold_draft_rationale"),
            "answer_variant": r.get("answer_variant"),
            "question_type": r.get("question_type") or r.get("type"),
        }
        for i, r in enumerate(selected)
    ]

    report = {
        "input": str(args.drafts),
        "blind_review_output": str(OUT_REVIEW),
        "hidden_manifest_output": str(OUT_HIDDEN),
        "n_requested": args.n,
        "n_written": len(blind_rows),
        "seed": args.seed,
        "full_draft_label_counts": dict(Counter(r.get("gold_draft_label", "UNKNOWN") for r in rows)),
        "blind50_hidden_draft_label_counts": dict(Counter(r.get("gold_draft_label", "UNKNOWN") for r in selected)),
        "protocol_warning": "Do not open hidden manifest or Opus draft file until blind human labels are completed.",
    }

    write_jsonl(OUT_REVIEW, blind_rows)
    save_json(OUT_HIDDEN, hidden_rows)
    save_json(OUT_REPORT, report)

    print("\nBuilt blind-50 gold review file")
    print("=" * 64)
    print(f"Gold drafts loaded: {len(rows)}")
    print(f"Blind rows written: {len(blind_rows)}")
    print(f"Wrote review file:  {OUT_REVIEW}")
    print(f"Wrote hidden key:   {OUT_HIDDEN}")
    print(f"Wrote report:       {OUT_REPORT}")
    print("\nDO NOT open the hidden key/report draft-label counts until blind labels are completed.")


if __name__ == "__main__":
    main()
