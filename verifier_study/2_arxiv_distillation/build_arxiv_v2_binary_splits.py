"""
backend/app/services/build_arxiv_v2_binary_splits.py

Build binary train/validation/gold files for arXiv S4 fine-tuning.

Train input:
  data/distill_arxiv_v2/train_teacher_labeled_non_opus.json

Gold input:
  data/distill_arxiv/gold_final_human_reviewed.json

Binary mapping:
  SUPPORTED   -> 0
  UNSUPPORTED -> 1
  ABSTENTION  -> excluded from binary train/eval

Train/val:
  - question-disjoint split using train_row_id/qid groups
  - validation is teacher-labeled only
  - gold is never used for early stopping or threshold selection

Outputs:
  data/distill_arxiv_v2/binary_train.jsonl
  data/distill_arxiv_v2/binary_val.jsonl
  data/distill_arxiv_v2/binary_train_val_split_summary.json
  data/distill_arxiv/gold_binary_eval.jsonl
  data/distill_arxiv/gold_binary_eval_summary.json

Run:
  python -m app.services.build_arxiv_v2_binary_splits --val-frac 0.15 --seed 2908
"""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


V2_DIR = Path("data") / "distill_arxiv_v2"
GOLD_DIR = Path("data") / "distill_arxiv"

TRAIN_LABELED_IN = V2_DIR / "train_teacher_labeled_non_opus.json"
GOLD_FINAL_IN = GOLD_DIR / "gold_final_human_reviewed.json"

TRAIN_OUT = V2_DIR / "binary_train.jsonl"
VAL_OUT = V2_DIR / "binary_val.jsonl"
SPLIT_SUMMARY_OUT = V2_DIR / "binary_train_val_split_summary.json"

GOLD_BINARY_OUT = GOLD_DIR / "gold_binary_eval.jsonl"
GOLD_SUMMARY_OUT = GOLD_DIR / "gold_binary_eval_summary.json"

LABEL_MAP = {
    "SUPPORTED": 0,
    "UNSUPPORTED": 1,
}


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
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def norm_label(x: Any) -> str:
    return str(x or "").strip().upper()


def group_id_train(row: dict[str, Any]) -> str:
    # train_row_id is best because plain/cited claims from the same generated answer stay together.
    for k in ["train_row_id", "global_qid", "qid", "id"]:
        if row.get(k) is not None and str(row.get(k)).strip():
            return str(row[k])
    return str(row.get("claim_id"))


def to_binary_train(row: dict[str, Any]) -> dict[str, Any] | None:
    label = norm_label(row.get("teacher_label"))
    if label not in LABEL_MAP:
        return None

    evidence_text = str(row.get("evidence_text_for_verifier") or "").strip()
    claim = str(row.get("claim") or row.get("claim_text") or "").strip()

    return {
        "claim_id": row.get("claim_id"),
        "group_id": group_id_train(row),
        "qid": row.get("qid"),
        "train_row_id": row.get("train_row_id"),
        "question": row.get("question"),
        "claim": claim,
        "claim_text": claim,
        "evidence_text": evidence_text,
        "evidence_text_for_verifier": evidence_text,
        "label": LABEL_MAP[label],
        "label_name": label,
        "teacher_label": label,
        "teacher_confidence": row.get("teacher_confidence"),
        "teacher_model": row.get("teacher_model"),
        "teacher_rationale": row.get("teacher_rationale"),
        "question_type": row.get("question_type"),
        "train_source": row.get("train_source"),
        "answer_variant": row.get("answer_variant"),
        "evidence_scope": row.get("evidence_scope"),
        "source_file": str(TRAIN_LABELED_IN),
    }


def to_binary_gold(row: dict[str, Any]) -> dict[str, Any] | None:
    label = norm_label(row.get("final_label") or row.get("human_final_label"))
    if label not in LABEL_MAP:
        return None

    evidence_text = str(row.get("evidence_text_for_verifier") or "").strip()
    claim = str(row.get("claim") or row.get("claim_text") or "").strip()

    return {
        "claim_id": row.get("claim_id"),
        "review_id": row.get("review_id"),
        "question": row.get("question"),
        "claim": claim,
        "claim_text": claim,
        "evidence_text": evidence_text,
        "evidence_text_for_verifier": evidence_text,
        "label": LABEL_MAP[label],
        "label_name": label,
        "human_final_label": label,
        "final_label": label,
        "final_notes": row.get("final_notes"),
        "question_type": row.get("question_type"),
        "answer_variant": row.get("answer_variant"),
        "evidence_scope": row.get("evidence_scope"),
        "is_blind50": row.get("is_blind50", False),
        "opus_label": row.get("opus_label"),
        "llama70b_label": row.get("llama70b_label"),
        "warning_flags": row.get("warning_flags", []),
        "source_file": str(GOLD_FINAL_IN),
    }


def counts(rows: list[dict[str, Any]]) -> dict[str, Any]:
    label_counts = Counter(r["label_name"] for r in rows)
    source_counts = Counter(r.get("train_source") or r.get("question_type") or "unknown" for r in rows)
    arm_counts = Counter(r.get("answer_variant") or "unknown" for r in rows)
    source_label = Counter((r.get("train_source") or r.get("question_type") or "unknown", r["label_name"]) for r in rows)
    arm_label = Counter((r.get("answer_variant") or "unknown", r["label_name"]) for r in rows)

    return {
        "n": len(rows),
        "label_counts": dict(label_counts),
        "positive_unsupported": label_counts.get("UNSUPPORTED", 0),
        "negative_supported": label_counts.get("SUPPORTED", 0),
        "positive_rate": round(label_counts.get("UNSUPPORTED", 0) / len(rows), 4) if rows else 0,
        "source_or_qtype_counts": dict(source_counts),
        "answer_variant_counts": dict(arm_counts),
        "source_or_qtype_by_label": {f"{k[0]}::{k[1]}": v for k, v in source_label.items()},
        "answer_variant_by_label": {f"{k[0]}::{k[1]}": v for k, v in arm_label.items()},
    }


def stratified_group_split(rows: list[dict[str, Any]], val_frac: float, seed: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        groups[str(r["group_id"])].append(r)

    group_items = []
    for gid, items in groups.items():
        pos = sum(1 for x in items if x["label"] == 1)
        neg = sum(1 for x in items if x["label"] == 0)
        group_items.append({
            "gid": gid,
            "items": items,
            "n": len(items),
            "pos": pos,
            "neg": neg,
            "has_pos": pos > 0,
        })

    rng = random.Random(seed)

    # Put positive groups first for better val positive coverage, shuffle within strata.
    pos_groups = [g for g in group_items if g["has_pos"]]
    neg_groups = [g for g in group_items if not g["has_pos"]]
    rng.shuffle(pos_groups)
    rng.shuffle(neg_groups)

    target_n = round(len(rows) * val_frac)
    target_pos = round(sum(r["label"] == 1 for r in rows) * val_frac)

    val_gids = set()
    val_n = 0
    val_pos = 0

    # First choose positive groups until target positive count is reached or val too large.
    for g in pos_groups:
        if val_pos >= target_pos and val_n >= target_n * 0.7:
            break
        val_gids.add(g["gid"])
        val_n += g["n"]
        val_pos += g["pos"]

    # Then fill with negative/remaining groups until target n.
    remaining = [g for g in group_items if g["gid"] not in val_gids]
    rng.shuffle(remaining)

    for g in remaining:
        if val_n >= target_n:
            break
        val_gids.add(g["gid"])
        val_n += g["n"]
        val_pos += g["pos"]

    train = []
    val = []
    for r in rows:
        if str(r["group_id"]) in val_gids:
            val.append(r)
        else:
            train.append(r)

    return train, val


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--train-labeled", type=Path, default=TRAIN_LABELED_IN)
    ap.add_argument("--gold-final", type=Path, default=GOLD_FINAL_IN)
    ap.add_argument("--val-frac", type=float, default=0.15)
    ap.add_argument("--seed", type=int, default=2908)
    args = ap.parse_args()

    train_labeled = load_json(args.train_labeled)
    gold_final = load_json(args.gold_final)

    if not isinstance(train_labeled, list):
        raise SystemExit(f"{args.train_labeled} must be a JSON list.")
    if not isinstance(gold_final, list):
        raise SystemExit(f"{args.gold_final} must be a JSON list.")

    binary_train_all = [x for x in (to_binary_train(r) for r in train_labeled) if x is not None]
    binary_gold = [x for x in (to_binary_gold(r) for r in gold_final) if x is not None]

    train_rows, val_rows = stratified_group_split(binary_train_all, val_frac=args.val_frac, seed=args.seed)

    write_jsonl(TRAIN_OUT, train_rows)
    write_jsonl(VAL_OUT, val_rows)
    write_jsonl(GOLD_BINARY_OUT, binary_gold)

    train_summary = {
        "inputs": {
            "train_labeled": str(args.train_labeled),
            "gold_final": str(args.gold_final),
        },
        "outputs": {
            "binary_train": str(TRAIN_OUT),
            "binary_val": str(VAL_OUT),
            "binary_gold": str(GOLD_BINARY_OUT),
            "split_summary": str(SPLIT_SUMMARY_OUT),
            "gold_summary": str(GOLD_SUMMARY_OUT),
        },
        "label_mapping": LABEL_MAP,
        "excluded_label": "ABSTENTION",
        "seed": args.seed,
        "val_frac": args.val_frac,
        "train_all_binary_before_split": counts(binary_train_all),
        "train_split": counts(train_rows),
        "val_split": counts(val_rows),
        "question_group_overlap_train_val": len({r["group_id"] for r in train_rows} & {r["group_id"] for r in val_rows}),
        "notes": [
            "Validation is teacher-labeled only and question-disjoint from train.",
            "Gold is frozen human-reviewed and is not used for threshold selection or early stopping.",
        ],
    }

    gold_summary = {
        "input": str(args.gold_final),
        "output": str(GOLD_BINARY_OUT),
        "label_mapping": LABEL_MAP,
        "excluded_label": "ABSTENTION",
        "gold_binary": counts(binary_gold),
        "gold_full_label_counts": dict(Counter(norm_label(r.get("final_label") or r.get("human_final_label")) for r in gold_final)),
        "important_caveat": (
            "Current gold binary positives are mostly bait. Overall binary eval is valid, "
            "but grounded-overclaim recall is underpowered unless a targeted grounded-hard gold tranche is added."
        ),
    }

    save_json(SPLIT_SUMMARY_OUT, train_summary)
    save_json(GOLD_SUMMARY_OUT, gold_summary)

    print("\nBuilt arXiv v2 binary splits")
    print("=" * 72)
    print(f"Train all binary before split: {len(binary_train_all)}")
    print(f"Train rows:                   {len(train_rows)}")
    print(f"Val rows:                     {len(val_rows)}")
    print(f"Gold binary rows:             {len(binary_gold)}")
    print(f"Train/val group overlap:      {train_summary['question_group_overlap_train_val']}")
    print("\nTrain split counts:")
    print(json.dumps(train_summary["train_split"], ensure_ascii=False, indent=2))
    print("\nVal split counts:")
    print(json.dumps(train_summary["val_split"], ensure_ascii=False, indent=2))
    print("\nGold binary counts:")
    print(json.dumps(gold_summary["gold_binary"], ensure_ascii=False, indent=2))
    print("\nGold caveat:")
    print(gold_summary["important_caveat"])
    print("\nWrote:")
    print(f"  {TRAIN_OUT}")
    print(f"  {VAL_OUT}")
    print(f"  {SPLIT_SUMMARY_OUT}")
    print(f"  {GOLD_BINARY_OUT}")
    print(f"  {GOLD_SUMMARY_OUT}")


if __name__ == "__main__":
    main()
