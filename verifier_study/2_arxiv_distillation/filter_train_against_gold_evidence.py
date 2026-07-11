"""
backend/app/services/filter_train_against_gold_evidence.py

Repair evidence-paper contamination by protecting the gold set and filtering TRAIN claims.

Why:
  The train/gold question split was top-1-paper-disjoint, but actual generation used top-k evidence.
  A direct check showed most gold claims use evidence papers that also appear somewhere in train.
  Dropping gold would destroy evaluation size, so this script keeps gold intact and removes any
  train claim whose actual evidence-paper keys overlap the gold evidence-paper keys.

Inputs by default:
  data/distill_arxiv/distill_train_claims.json
  data/distill_arxiv/distill_train_teacher_labeled.json
  data/distill_arxiv/gold_eval_claims.json
  data/distill_arxiv/gold_eval_teacher_drafted.json

Outputs by default:
  data/distill_arxiv/distill_train_claims_gold_evidence_clean.json
  data/distill_arxiv/distill_train_teacher_labeled_gold_evidence_clean.json
  data/distill_arxiv/train_gold_evidence_filter_report.json

Run from backend/:
  python -m app.services.filter_train_against_gold_evidence
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


DISTILL_DIR = Path("data") / "distill_arxiv"

TRAIN_CLAIMS = DISTILL_DIR / "distill_train_claims.json"
TRAIN_LABELED = DISTILL_DIR / "distill_train_teacher_labeled.json"
GOLD_CLAIMS = DISTILL_DIR / "gold_eval_claims.json"
GOLD_DRAFTED = DISTILL_DIR / "gold_eval_teacher_drafted.json"

OUT_TRAIN_CLAIMS = DISTILL_DIR / "distill_train_claims_gold_evidence_clean.json"
OUT_TRAIN_LABELED = DISTILL_DIR / "distill_train_teacher_labeled_gold_evidence_clean.json"
OUT_REPORT = DISTILL_DIR / "train_gold_evidence_filter_report.json"


def load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def norm_title(title: Any) -> str:
    return " ".join(str(title or "").lower().strip().split())


def evidence_keys(record: dict[str, Any]) -> set[str]:
    keys: set[str] = set()
    evidence = record.get("evidence", [])

    if not isinstance(evidence, list):
        return keys

    for ev in evidence:
        if not isinstance(ev, dict):
            continue

        pid = (
            ev.get("resolved_corpus_paper_id")
            if ev.get("resolved_corpus_paper_id") is not None
            else ev.get("corpus_paper_id")
            if ev.get("corpus_paper_id") is not None
            else ev.get("paper_id")
        )

        if pid is not None and str(pid).strip() != "":
            keys.add(f"pid:{pid}")
            continue

        title = norm_title(ev.get("title"))
        if title:
            keys.add(f"title:{title}")

    return keys


def claim_id(record: dict[str, Any]) -> str:
    if record.get("claim_id"):
        return str(record["claim_id"])

    split = record.get("split", "unknown")
    qid = record.get("qid", "q")
    variant = record.get("answer_variant", "answer")
    idx = record.get("claim_index", 0)
    return f"{split}_q{qid}_{variant}_c{idx}"


def label_of(record: dict[str, Any]) -> str:
    return str(record.get("teacher_label") or record.get("distill_label") or record.get("label") or "MISSING")


def summarize_labels(rows: list[dict[str, Any]]) -> dict[str, int]:
    return dict(Counter(label_of(r) for r in rows))


def summarize_field(rows: list[dict[str, Any]], field: str) -> dict[str, int]:
    return dict(Counter(str(r.get(field) or "unknown") for r in rows))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--train-claims", type=Path, default=TRAIN_CLAIMS)
    ap.add_argument("--train-labeled", type=Path, default=TRAIN_LABELED)
    ap.add_argument("--gold-claims", type=Path, default=GOLD_CLAIMS)
    ap.add_argument("--gold-drafted", type=Path, default=GOLD_DRAFTED)
    ap.add_argument("--out-train-claims", type=Path, default=OUT_TRAIN_CLAIMS)
    ap.add_argument("--out-train-labeled", type=Path, default=OUT_TRAIN_LABELED)
    ap.add_argument("--out-report", type=Path, default=OUT_REPORT)
    args = ap.parse_args()

    train_claims = load_json(args.train_claims)
    train_labeled = load_json(args.train_labeled)
    gold_claims = load_json(args.gold_claims)
    gold_drafted = load_json(args.gold_drafted) if args.gold_drafted.exists() else []

    if not isinstance(train_claims, list) or not isinstance(train_labeled, list) or not isinstance(gold_claims, list):
        raise SystemExit("Input files must be JSON lists.")

    gold_keys: set[str] = set()
    for r in gold_claims:
        gold_keys.update(evidence_keys(r))

    train_claim_ids_to_keep: set[str] = set()
    train_claim_ids_to_drop: set[str] = set()

    dropped_train_claims: list[dict[str, Any]] = []
    kept_train_claims: list[dict[str, Any]] = []

    drop_reason_counts: Counter[str] = Counter()
    dropped_label_counts: Counter[str] = Counter()

    for r in train_claims:
        cid = claim_id(r)
        overlap = evidence_keys(r) & gold_keys

        if overlap:
            train_claim_ids_to_drop.add(cid)
            rr = {
                "claim_id": cid,
                "qid": r.get("qid"),
                "question_type": r.get("question_type") or r.get("type"),
                "answer_variant": r.get("answer_variant"),
                "evidence_scope": r.get("evidence_scope"),
                "overlapping_gold_evidence_keys": sorted(overlap),
                "claim": r.get("claim") or r.get("claim_text"),
            }
            dropped_train_claims.append(rr)
            for k in overlap:
                drop_reason_counts[k] += 1
        else:
            train_claim_ids_to_keep.add(cid)
            kept_train_claims.append(r)

    # Filter labeled file using the same claim ids.
    kept_labeled: list[dict[str, Any]] = []
    dropped_labeled: list[dict[str, Any]] = []
    labeled_missing_from_claims: list[str] = []

    known_ids = train_claim_ids_to_keep | train_claim_ids_to_drop

    for r in train_labeled:
        cid = claim_id(r)
        if cid not in known_ids:
            labeled_missing_from_claims.append(cid)
            # Conservative: keep unknown rows out of the clean training file.
            continue

        if cid in train_claim_ids_to_keep:
            kept_labeled.append(r)
        else:
            dropped_labeled.append(r)
            dropped_label_counts[label_of(r)] += 1

    # Check resulting overlap.
    kept_train_keys: set[str] = set()
    for r in kept_train_claims:
        kept_train_keys.update(evidence_keys(r))

    gold_overlap_after = set()
    for r in gold_claims:
        gold_overlap_after.update(evidence_keys(r) & kept_train_keys)

    report = {
        "inputs": {
            "train_claims": str(args.train_claims),
            "train_labeled": str(args.train_labeled),
            "gold_claims": str(args.gold_claims),
            "gold_drafted": str(args.gold_drafted),
        },
        "outputs": {
            "train_claims_clean": str(args.out_train_claims),
            "train_labeled_clean": str(args.out_train_labeled),
            "report": str(args.out_report),
        },
        "summary": {
            "gold_claims": len(gold_claims),
            "gold_drafted": len(gold_drafted) if isinstance(gold_drafted, list) else None,
            "gold_unique_evidence_keys": len(gold_keys),
            "train_claims_original": len(train_claims),
            "train_claims_kept": len(kept_train_claims),
            "train_claims_dropped": len(dropped_train_claims),
            "train_claim_drop_rate": round(len(dropped_train_claims) / len(train_claims), 4) if train_claims else 0.0,
            "train_labeled_original": len(train_labeled),
            "train_labeled_kept": len(kept_labeled),
            "train_labeled_dropped": len(dropped_labeled),
            "labeled_rows_missing_from_claims": len(labeled_missing_from_claims),
            "gold_train_evidence_overlap_after_filter": len(gold_overlap_after),
        },
        "kept_train_label_counts": summarize_labels(kept_labeled),
        "dropped_train_label_counts": dict(dropped_label_counts),
        "kept_train_by_answer_variant": summarize_field(kept_labeled, "answer_variant"),
        "kept_train_by_question_type": {
            k: v for k, v in Counter(str(r.get("question_type") or r.get("type") or "unknown") for r in kept_labeled).items()
        },
        "dropped_train_by_answer_variant": summarize_field(dropped_labeled, "answer_variant"),
        "dropped_train_by_question_type": {
            k: v for k, v in Counter(str(r.get("question_type") or r.get("type") or "unknown") for r in dropped_labeled).items()
        },
        "top_overlapping_gold_evidence_keys_causing_train_drops": dict(drop_reason_counts.most_common(30)),
        "dropped_train_claims_preview": dropped_train_claims[:50],
        "labeled_rows_missing_from_claims_preview": labeled_missing_from_claims[:50],
    }

    save_json(args.out_train_claims, kept_train_claims)
    save_json(args.out_train_labeled, kept_labeled)
    save_json(args.out_report, report)

    print("\nTrain filtering against gold evidence")
    print("=" * 64)
    print(f"Gold claims:                         {len(gold_claims)}")
    print(f"Gold unique evidence keys:            {len(gold_keys)}")
    print(f"Original train claims:                {len(train_claims)}")
    print(f"Kept train claims:                    {len(kept_train_claims)}")
    print(f"Dropped train claims:                 {len(dropped_train_claims)}")
    if train_claims:
        print(f"Train claim drop rate:                {100 * len(dropped_train_claims) / len(train_claims):.1f}%")
    print(f"Original labeled train rows:          {len(train_labeled)}")
    print(f"Kept labeled train rows:              {len(kept_labeled)}")
    print(f"Dropped labeled train rows:           {len(dropped_labeled)}")
    print(f"Overlap after filter:                 {len(gold_overlap_after)} evidence keys")
    print("\nKept train label counts:")
    for lab, n in sorted(summarize_labels(kept_labeled).items()):
        print(f"  {lab:12s} {n}")
    print("\nDropped train label counts:")
    for lab, n in sorted(dict(dropped_label_counts).items()):
        print(f"  {lab:12s} {n}")
    print(f"\nWrote clean train claims:             {args.out_train_claims}")
    print(f"Wrote clean labeled train:            {args.out_train_labeled}")
    print(f"Wrote report:                         {args.out_report}")


if __name__ == "__main__":
    main()
