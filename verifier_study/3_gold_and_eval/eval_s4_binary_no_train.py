"""
eval_s4_binary_no_train.py

Evaluate a saved S4/DeBERTa-style binary verifier on binary val/gold JSONL
without training.

Threshold is selected on validation by max F1, then applied unchanged to gold.

Run examples from /workspace/project3:

  python -u eval_s4_binary_no_train.py \
    --model-path signal4_model_scifact_healthver \
    --val-jsonl data/distill_arxiv_v2/binary_val.jsonl \
    --gold-jsonl data/distill_arxiv/gold_binary_eval.jsonl \
    --out-dir eval_base_scifact_healthver \
    --batch-size 16 \
    --max-length 512 \
    --bf16

  python -u eval_s4_binary_no_train.py \
    --model-path /workspace/signal4_model \
    --val-jsonl data/distill_arxiv_v2/binary_val.jsonl \
    --gold-jsonl data/distill_arxiv/gold_binary_eval.jsonl \
    --out-dir eval_base_original_s4 \
    --batch-size 16 \
    --max-length 512 \
    --bf16
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np
import torch
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    precision_recall_fscore_support,
    roc_auc_score,
)
from torch.utils.data import Dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer, DataCollatorWithPadding, Trainer, TrainingArguments


LABEL_NAMES = {0: "SUPPORTED", 1: "UNSUPPORTED"}


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


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


class ClaimEvidenceDataset(Dataset):
    def __init__(self, rows: list[dict[str, Any]], tokenizer, max_length: int):
        self.rows = rows
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, idx: int) -> dict[str, Any]:
        r = self.rows[idx]
        claim = str(r.get("claim") or r.get("claim_text") or "").strip()
        evidence = str(r.get("evidence_text") or r.get("evidence_text_for_verifier") or "").strip()
        enc = self.tokenizer(
            claim,
            evidence,
            truncation=True,
            max_length=self.max_length,
        )
        enc["labels"] = int(r["label"])
        return enc


def softmax_np(logits: np.ndarray) -> np.ndarray:
    x = logits - np.max(logits, axis=1, keepdims=True)
    e = np.exp(x)
    return e / np.sum(e, axis=1, keepdims=True)


def safe_auc(y_true: np.ndarray, probs_pos: np.ndarray) -> float | None:
    try:
        if len(set(y_true.tolist())) < 2:
            return None
        return float(roc_auc_score(y_true, probs_pos))
    except Exception:
        return None


def safe_auprc(y_true: np.ndarray, probs_pos: np.ndarray) -> float | None:
    try:
        if len(set(y_true.tolist())) < 2:
            return None
        return float(average_precision_score(y_true, probs_pos))
    except Exception:
        return None


def ece_score(y_true: np.ndarray, probs_pos: np.ndarray, n_bins: int = 10) -> float:
    y_pred = (probs_pos >= 0.5).astype(int)
    conf = np.where(y_pred == 1, probs_pos, 1.0 - probs_pos)
    correct = (y_pred == y_true).astype(float)

    bins = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    n = len(y_true)
    if n == 0:
        return 0.0

    for i in range(n_bins):
        lo, hi = bins[i], bins[i + 1]
        if i == n_bins - 1:
            mask = (conf >= lo) & (conf <= hi)
        else:
            mask = (conf >= lo) & (conf < hi)
        if not mask.any():
            continue
        ece += mask.mean() * abs(correct[mask].mean() - conf[mask].mean())

    return float(ece)


def metrics_at_threshold(y_true: np.ndarray, probs_pos: np.ndarray, threshold: float) -> dict[str, Any]:
    y_pred = (probs_pos >= threshold).astype(int)

    p, r, f1, _ = precision_recall_fscore_support(
        y_true,
        y_pred,
        labels=[1],
        average="binary",
        zero_division=0,
    )

    tp = int(((y_true == 1) & (y_pred == 1)).sum())
    fp = int(((y_true == 0) & (y_pred == 1)).sum())
    fn = int(((y_true == 1) & (y_pred == 0)).sum())
    tn = int(((y_true == 0) & (y_pred == 0)).sum())

    return {
        "threshold": float(threshold),
        "n": int(len(y_true)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(p),
        "recall": float(r),
        "f1": float(f1),
        "auroc": safe_auc(y_true, probs_pos),
        "auprc": safe_auprc(y_true, probs_pos),
        "ece_10": ece_score(y_true, probs_pos, n_bins=10),
        "confusion": {"tn": tn, "fp": fp, "fn": fn, "tp": tp},
        "label_counts": {
            "SUPPORTED": int((y_true == 0).sum()),
            "UNSUPPORTED": int((y_true == 1).sum()),
        },
        "pred_counts": {
            "SUPPORTED": int((y_pred == 0).sum()),
            "UNSUPPORTED": int((y_pred == 1).sum()),
        },
    }


def choose_best_threshold(y_true: np.ndarray, probs_pos: np.ndarray) -> dict[str, Any]:
    best = None
    for t in np.round(np.arange(0.05, 0.951, 0.01), 2):
        m = metrics_at_threshold(y_true, probs_pos, float(t))
        key = (m["f1"], m["recall"], m["precision"])
        if best is None or key > best["key"]:
            best = {"threshold": float(t), "metrics": m, "key": key}
    assert best is not None
    return {
        "selected_threshold": best["threshold"],
        "selection_metric": "max_val_f1_then_recall_then_precision",
        "val_metrics_at_selected_threshold": best["metrics"],
    }


def compute_slices(rows: list[dict[str, Any]], y_true: np.ndarray, probs_pos: np.ndarray, threshold: float) -> dict[str, Any]:
    slice_defs = {
        "question_type": defaultdict(list),
        "answer_variant": defaultdict(list),
        "question_type_x_answer_variant": defaultdict(list),
    }

    for i, r in enumerate(rows):
        qt = str(r.get("question_type") or r.get("train_source") or "unknown")
        av = str(r.get("answer_variant") or "unknown")
        slice_defs["question_type"][qt].append(i)
        slice_defs["answer_variant"][av].append(i)
        slice_defs["question_type_x_answer_variant"][f"{qt}::{av}"].append(i)

    out: dict[str, Any] = {}
    for group_name, group_map in slice_defs.items():
        out[group_name] = {}
        for name, idxs in sorted(group_map.items()):
            idx = np.array(idxs, dtype=int)
            out[group_name][name] = metrics_at_threshold(y_true[idx], probs_pos[idx], threshold)
    return out


def make_prediction_rows(rows: list[dict[str, Any]], probs_pos: np.ndarray, threshold: float) -> list[dict[str, Any]]:
    out = []
    for r, p in zip(rows, probs_pos):
        pred = int(p >= threshold)
        rr = dict(r)
        rr["prob_unsupported"] = float(p)
        rr["pred_label"] = pred
        rr["pred_label_name"] = LABEL_NAMES[pred]
        rr["threshold"] = float(threshold)
        out.append(rr)
    return out


def evaluate(trainer: Trainer, dataset: ClaimEvidenceDataset, rows: list[dict[str, Any]], threshold: float | None = None) -> dict[str, Any]:
    pred = trainer.predict(dataset)
    logits = np.asarray(pred.predictions)
    y_true = np.array([int(r["label"]) for r in rows], dtype=int)
    probs_pos = softmax_np(logits)[:, 1]

    threshold_selection = None
    if threshold is None:
        threshold_selection = choose_best_threshold(y_true, probs_pos)
        threshold = threshold_selection["selected_threshold"]

    return {
        "threshold_selection": threshold_selection,
        "overall": metrics_at_threshold(y_true, probs_pos, threshold),
        "slices": compute_slices(rows, y_true, probs_pos, threshold),
        "pred_rows": make_prediction_rows(rows, probs_pos, threshold),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-path", required=True)
    ap.add_argument("--val-jsonl", type=Path, required=True)
    ap.add_argument("--gold-jsonl", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--max-length", type=int, default=512)
    ap.add_argument("--bf16", action="store_true")
    ap.add_argument("--fp16", action="store_true")
    args = ap.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)

    val_rows = read_jsonl(args.val_jsonl)
    gold_rows = read_jsonl(args.gold_jsonl)

    tokenizer = AutoTokenizer.from_pretrained(args.model_path, use_fast=True)
    model = AutoModelForSequenceClassification.from_pretrained(
        args.model_path,
        num_labels=2,
        id2label={0: "SUPPORTED", 1: "UNSUPPORTED"},
        label2id={"SUPPORTED": 0, "UNSUPPORTED": 1},
        ignore_mismatched_sizes=True,
    )

    val_ds = ClaimEvidenceDataset(val_rows, tokenizer, max_length=args.max_length)
    gold_ds = ClaimEvidenceDataset(gold_rows, tokenizer, max_length=args.max_length)

    training_args = TrainingArguments(
        output_dir=str(args.out_dir / "_tmp_trainer"),
        per_device_eval_batch_size=args.batch_size,
        report_to=[],
        bf16=args.bf16,
        fp16=args.fp16,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        tokenizer=tokenizer,
        data_collator=DataCollatorWithPadding(tokenizer=tokenizer),
    )

    val_eval = evaluate(trainer, val_ds, val_rows, threshold=None)
    threshold = val_eval["threshold_selection"]["selected_threshold"]
    gold_eval = evaluate(trainer, gold_ds, gold_rows, threshold=threshold)

    write_jsonl(args.out_dir / "val_predictions.jsonl", val_eval["pred_rows"])
    write_jsonl(args.out_dir / "gold_predictions.jsonl", gold_eval["pred_rows"])

    summary = {
        "model_path": args.model_path,
        "selected_threshold_from_val": threshold,
        "val": {
            "overall": val_eval["overall"],
            "slices": val_eval["slices"],
        },
        "gold": {
            "overall": gold_eval["overall"],
            "slices": gold_eval["slices"],
        },
        "notes": [
            "No training performed.",
            "Threshold selected on validation and applied unchanged to gold.",
        ],
    }

    save_json(args.out_dir / "metrics_summary.json", summary)

    print("\nFinished no-train evaluation")
    print("=" * 72)
    print(f"Model path: {args.model_path}")
    print(f"Selected threshold from val: {threshold}")
    print("\nVAL overall:")
    print(json.dumps(val_eval["overall"], ensure_ascii=False, indent=2))
    print("\nGOLD overall:")
    print(json.dumps(gold_eval["overall"], ensure_ascii=False, indent=2))
    print("\nGOLD question_type slices:")
    print(json.dumps(gold_eval["slices"]["question_type"], ensure_ascii=False, indent=2))
    print("\nWrote:")
    print(f"  {args.out_dir / 'metrics_summary.json'}")
    print(f"  {args.out_dir / 'val_predictions.jsonl'}")
    print(f"  {args.out_dir / 'gold_predictions.jsonl'}")


if __name__ == "__main__":
    main()
