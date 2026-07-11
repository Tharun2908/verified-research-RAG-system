"""
backend/app/services/check_distill_evidence_overlap.py

Check actual evidence-paper overlap between distillation train claims and gold claims.

Why this exists:
  The question split was made top-1-paper-disjoint, but generation inputs used top-k=3 evidence.
  This script checks the actual evidence attached to extracted claims. If gold claims use evidence
  from any train-side evidence paper, they are flagged for dropping or separate reporting.

Inputs by default:
  data/distill_arxiv/distill_train_claims.json
  data/distill_arxiv/gold_eval_claims.json

Outputs by default:
  data/distill_arxiv/evidence_overlap_report.json
  data/distill_arxiv/gold_eval_claims_no_overlap.json

Run from backend/:
  python -m app.services.check_distill_evidence_overlap
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


DISTILL_DIR = Path("data") / "distill_arxiv"

DEFAULT_TRAIN = DISTILL_DIR / "distill_train_claims.json"
DEFAULT_GOLD = DISTILL_DIR / "gold_eval_claims.json"
DEFAULT_REPORT = DISTILL_DIR / "evidence_overlap_report.json"
DEFAULT_FILTERED_GOLD = DISTILL_DIR / "gold_eval_claims_no_overlap.json"


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
    """
    Return stable evidence-paper keys for one claim record.

    Preferred:
      pid:<resolved_corpus_paper_id>

    Fallbacks:
      pid:<corpus_paper_id>
      pid:<paper_id>
      title:<normalized title>

    The fallback exists only because older artifacts may not have resolved IDs.
    """
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


def evidence_titles(record: dict[str, Any]) -> list[str]:
    titles: list[str] = []
    for ev in record.get("evidence", []) or []:
        if isinstance(ev, dict) and ev.get("title"):
            t = str(ev["title"]).strip()
            if t and t not in titles:
                titles.append(t)
    return titles


def short_record(record: dict[str, Any], overlap: set[str] | None = None) -> dict[str, Any]:
    return {
        "claim_id": record.get("claim_id"),
        "qid": record.get("qid"),
        "split": record.get("split"),
        "question_type": record.get("question_type") or record.get("type"),
        "answer_variant": record.get("answer_variant"),
        "claim_index": record.get("claim_index"),
        "evidence_scope": record.get("evidence_scope"),
        "evidence_keys": sorted(evidence_keys(record)),
        "overlapping_evidence_keys": sorted(overlap or []),
        "evidence_titles": evidence_titles(record),
        "question": record.get("question"),
        "claim": record.get("claim") or record.get("claim_text"),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", type=Path, default=DEFAULT_TRAIN)
    ap.add_argument("--gold", type=Path, default=DEFAULT_GOLD)
    ap.add_argument("--report-out", type=Path, default=DEFAULT_REPORT)
    ap.add_argument("--filtered-gold-out", type=Path, default=DEFAULT_FILTERED_GOLD)
    ap.add_argument("--no-filtered-file", action="store_true")
    args = ap.parse_args()

    train = load_json(args.train)
    gold = load_json(args.gold)

    if not isinstance(train, list) or not isinstance(gold, list):
        raise SystemExit("Both train and gold inputs must be JSON lists.")

    train_keys: set[str] = set()
    train_key_to_examples: dict[str, list[dict[str, Any]]] = defaultdict(list)

    train_missing_keys = 0
    for r in train:
        keys = evidence_keys(r)
        if not keys:
            train_missing_keys += 1
            continue
        train_keys.update(keys)
        for k in keys:
            if len(train_key_to_examples[k]) < 5:
                train_key_to_examples[k].append(short_record(r))

    contaminated_gold: list[dict[str, Any]] = []
    clean_gold: list[dict[str, Any]] = []
    gold_missing_keys = 0

    overlap_key_counts: Counter[str] = Counter()
    by_question_type: Counter[str] = Counter()
    by_answer_variant: Counter[str] = Counter()
    by_evidence_scope: Counter[str] = Counter()

    for r in gold:
        keys = evidence_keys(r)
        if not keys:
            gold_missing_keys += 1

        overlap = keys & train_keys

        if overlap:
            contaminated_gold.append(short_record(r, overlap=overlap))
            for k in overlap:
                overlap_key_counts[k] += 1
            by_question_type[str(r.get("question_type") or r.get("type") or "unknown")] += 1
            by_answer_variant[str(r.get("answer_variant") or "unknown")] += 1
            by_evidence_scope[str(r.get("evidence_scope") or "unknown")] += 1
        else:
            clean_gold.append(r)

    contaminated_qids = sorted({str(r.get("qid")) for r in contaminated_gold})
    clean_qids = sorted({str(r.get("qid")) for r in clean_gold})

    report = {
        "inputs": {
            "train": str(args.train),
            "gold": str(args.gold),
        },
        "summary": {
            "train_claims": len(train),
            "gold_claims": len(gold),
            "train_unique_evidence_keys": len(train_keys),
            "gold_clean_claims": len(clean_gold),
            "gold_contaminated_claims": len(contaminated_gold),
            "gold_contaminated_claim_rate": round(len(contaminated_gold) / len(gold), 4) if gold else 0.0,
            "gold_clean_qids": len(clean_qids),
            "gold_contaminated_qids": len(contaminated_qids),
            "train_claims_missing_evidence_keys": train_missing_keys,
            "gold_claims_missing_evidence_keys": gold_missing_keys,
        },
        "contamination_breakdown": {
            "by_question_type": dict(by_question_type),
            "by_answer_variant": dict(by_answer_variant),
            "by_evidence_scope": dict(by_evidence_scope),
            "overlap_key_counts": dict(overlap_key_counts.most_common()),
        },
        "contaminated_gold_claims": contaminated_gold,
        "train_examples_for_overlap_keys": {
            k: train_key_to_examples[k]
            for k, _ in overlap_key_counts.most_common()
        },
    }

    save_json(args.report_out, report)

    if not args.no_filtered_file:
        save_json(args.filtered_gold_out, clean_gold)

    print("\nEvidence-overlap check")
    print("=" * 56)
    print(f"Train claims:              {len(train)}")
    print(f"Gold claims:               {len(gold)}")
    print(f"Train evidence keys:        {len(train_keys)}")
    print(f"Gold contaminated claims:   {len(contaminated_gold)}")
    print(f"Gold clean claims:          {len(clean_gold)}")
    if gold:
        print(f"Contaminated claim rate:    {100 * len(contaminated_gold) / len(gold):.1f}%")
    print(f"Gold contaminated qids:     {len(contaminated_qids)}")
    print(f"Train missing evidence ids: {train_missing_keys}")
    print(f"Gold missing evidence ids:  {gold_missing_keys}")

    if contaminated_gold:
        print("\nContamination breakdown:")
        print(f"  by_question_type: {dict(by_question_type)}")
        print(f"  by_answer_variant: {dict(by_answer_variant)}")
        print(f"  by_evidence_scope: {dict(by_evidence_scope)}")
        print("\nFirst contaminated gold claim:")
        print(json.dumps(contaminated_gold[0], ensure_ascii=False, indent=2)[:3000])
        print("\nRecommendation: inspect the report, then drop contaminated gold claims or report them separately.")
    else:
        print("\nNo actual evidence-paper overlap found between train and gold claims.")

    print(f"\nWrote report: {args.report_out}")
    if not args.no_filtered_file:
        print(f"Wrote filtered gold claims: {args.filtered_gold_out}")


if __name__ == "__main__":
    main()
