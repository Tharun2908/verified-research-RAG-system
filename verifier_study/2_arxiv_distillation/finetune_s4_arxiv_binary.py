"""
finetune_s4_arxiv_binary.py

Fine-tune a DeBERTa-style S4 verifier on arXiv v2 binary claim-evidence data.

Binary labels:
  0 = SUPPORTED
  1 = UNSUPPORTED

Train/validation:
  - uses teacher-labeled v2 train split
  - validation is question-disjoint and teacher-labeled
  - validation selects threshold
  - gold is frozen human-reviewed and never used for threshold selection

Example on cluster from /workspace/project3:

  python -u finetune_s4_arxiv_binary.py \
    --model-path signal4_model_scifact_healthver \
    --train-jsonl data/distill_arxiv_v2/binary_train.jsonl \
    --val-jsonl data/distill_arxiv_v2/binary_val.jsonl \
    --gold-jsonl data/distill_arxiv/gold_binary_eval.jsonl \
    --out-dir arxiv_s4_from_scifact_healthver \
    --epochs 5 \
    --batch-size 8 \
    --grad-accum 2 \
    --lr 2e-5 \
    --max-length 512 \
    --weighted-loss

Outputs:
  <out-dir>/final_model/
  <out-dir>/metrics_summary.json
  <out-dir>/val_predictions.jsonl
  <out-dir>/gold_predictions.jsonl
  <out-dir>/train_config.json
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np
import torch
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    f1_score,
    precision_recall_fscore_support,
    precision_score,
    recall_score,
    roc_auc_score,
)
from torch import nn
from torch.utils.data import Dataset
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    EarlyStoppingCallback,
    Trainer,
    TrainingArguments,
    set_seed,
)


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


def set_all_seeds(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    set_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


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
        label = int(r["label"])

        enc = self.tokenizer(
            claim,
            evidence,
            truncation=True,
            max_length=self.max_length,
        )
        enc["labels"] = label
        return enc


class WeightedTrainer(Trainer):
    def __init__(self, *args, class_weights: torch.Tensor | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_weights = class_weights

    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        labels = inputs.pop("labels")
        outputs = model(**inputs)
        logits = outputs.logits

        weights = self.class_weights
        if weights is not None:
            weights = weights.to(logits.device)

        loss_fct = nn.CrossEntropyLoss(weight=weights)
        loss = loss_fct(logits.view(-1, model.config.num_labels), labels.view(-1))
        return (loss, outputs) if return_outputs else loss


def softmax_np(logits: np.ndarray) -> np.ndarray:
    x = logits - np.max(logits, axis=1, keepdims=True)
    e = np.exp(x)
    return e / np.sum(e, axis=1, keepdims=True)


def ece_score(y_true: np.ndarray, probs_pos: np.ndarray, n_bins: int = 10) -> float:
    """
    Binary ECE using confidence of predicted class.
    """
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


def metrics_at_threshold(y_true: np.ndarray, probs_pos: np.ndarray, threshold: float) -> dict[str, Any]:
    y_pred = (probs_pos >= threshold).astype(int)

    p, r, f1, _ = precision_recall_fscore_support(
        y_true,
        y_pred,
        labels=[1],
        average="binary",
        zero_division=0,
    )

    acc = accuracy_score(y_true, y_pred)

    tp = int(((y_true == 1) & (y_pred == 1)).sum())
    fp = int(((y_true == 0) & (y_pred == 1)).sum())
    fn = int(((y_true == 1) & (y_pred == 0)).sum())
    tn = int(((y_true == 0) & (y_pred == 0)).sum())

    return {
        "threshold": float(threshold),
        "n": int(len(y_true)),
        "accuracy": float(acc),
        "precision": float(p),
        "recall": float(r),
        "f1": float(f1),
        "auroc": safe_auc(y_true, probs_pos),
        "auprc": safe_auprc(y_true, probs_pos),
        "ece_10": ece_score(y_true, probs_pos, n_bins=10),
        "confusion": {
            "tn": tn,
            "fp": fp,
            "fn": fn,
            "tp": tp,
        },
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
    thresholds = np.round(np.arange(0.05, 0.951, 0.01), 2)

    best = None
    for t in thresholds:
        m = metrics_at_threshold(y_true, probs_pos, float(t))
        # Maximize F1, then recall, then precision.
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


def evaluate_split(trainer: Trainer, dataset: ClaimEvidenceDataset, rows: list[dict[str, Any]], threshold: float | None = None) -> dict[str, Any]:
    pred = trainer.predict(dataset)
    logits = pred.predictions
    y_true = np.array([int(r["label"]) for r in rows], dtype=int)
    probs = softmax_np(logits)
    probs_pos = probs[:, 1]

    if threshold is None:
        selected = choose_best_threshold(y_true, probs_pos)
        threshold = selected["selected_threshold"]
    else:
        selected = None

    overall = metrics_at_threshold(y_true, probs_pos, threshold)
    slices = compute_slices(rows, y_true, probs_pos, threshold)
    pred_rows = make_prediction_rows(rows, probs_pos, threshold)

    return {
        "threshold_selection": selected,
        "overall": overall,
        "slices": slices,
        "pred_rows": pred_rows,
        "probs_pos": probs_pos.tolist(),
        "y_true": y_true.tolist(),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-path", required=True)
    ap.add_argument("--train-jsonl", type=Path, required=True)
    ap.add_argument("--val-jsonl", type=Path, required=True)
    ap.add_argument("--gold-jsonl", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--epochs", type=float, default=5)
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--eval-batch-size", type=int, default=16)
    ap.add_argument("--grad-accum", type=int, default=2)
    ap.add_argument("--lr", type=float, default=2e-5)
    ap.add_argument("--weight-decay", type=float, default=0.01)
    ap.add_argument("--warmup-ratio", type=float, default=0.06)
    ap.add_argument("--max-length", type=int, default=512)
    ap.add_argument("--seed", type=int, default=2908)
    ap.add_argument("--weighted-loss", action="store_true")
    ap.add_argument("--fp16", action="store_true")
    ap.add_argument("--bf16", action="store_true")
    ap.add_argument("--early-stopping-patience", type=int, default=2)
    args = ap.parse_args()

    set_all_seeds(args.seed)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    train_rows = read_jsonl(args.train_jsonl)
    val_rows = read_jsonl(args.val_jsonl)
    gold_rows = read_jsonl(args.gold_jsonl)

    print("\nLoading tokenizer/model")
    print("=" * 72)
    print(f"Model path: {args.model_path}")

    tokenizer = AutoTokenizer.from_pretrained(args.model_path, use_fast=True)
    model = AutoModelForSequenceClassification.from_pretrained(
        args.model_path,
        num_labels=2,
        id2label={0: "SUPPORTED", 1: "UNSUPPORTED"},
        label2id={"SUPPORTED": 0, "UNSUPPORTED": 1},
        ignore_mismatched_sizes=True,
    )

    train_ds = ClaimEvidenceDataset(train_rows, tokenizer, max_length=args.max_length)
    val_ds = ClaimEvidenceDataset(val_rows, tokenizer, max_length=args.max_length)
    gold_ds = ClaimEvidenceDataset(gold_rows, tokenizer, max_length=args.max_length)

    label_counts = Counter(int(r["label"]) for r in train_rows)
    class_weights = None
    if args.weighted_loss:
        total = len(train_rows)
        weights = []
        for c in [0, 1]:
            weights.append(total / (2.0 * max(label_counts.get(c, 0), 1)))
        class_weights = torch.tensor(weights, dtype=torch.float)
        print(f"Using weighted loss: {class_weights.tolist()} for labels 0/1")

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        probs = softmax_np(np.asarray(logits))
        probs_pos = probs[:, 1]
        labels = np.asarray(labels, dtype=int)
        m = metrics_at_threshold(labels, probs_pos, threshold=0.5)
        out = {
            "f1": m["f1"],
            "precision": m["precision"],
            "recall": m["recall"],
            "accuracy": m["accuracy"],
            "auroc": m["auroc"] if m["auroc"] is not None else 0.0,
            "auprc": m["auprc"] if m["auprc"] is not None else 0.0,
            "ece_10": m["ece_10"],
        }
        return out

    train_args = TrainingArguments(
        output_dir=str(args.out_dir / "checkpoints"),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.eval_batch_size,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.lr,
        weight_decay=args.weight_decay,
        warmup_ratio=args.warmup_ratio,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="eval_auroc",
        greater_is_better=True,
        logging_steps=25,
        save_total_limit=2,
        report_to=[],
        fp16=args.fp16,
        bf16=args.bf16,
        seed=args.seed,
        data_seed=args.seed,
    )

    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    trainer = WeightedTrainer(
        model=model,
        args=train_args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
        class_weights=class_weights,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=args.early_stopping_patience)],
    )

    config = vars(args).copy()
    config["train_rows"] = len(train_rows)
    config["val_rows"] = len(val_rows)
    config["gold_rows"] = len(gold_rows)
    config["train_label_counts"] = dict(Counter(r["label_name"] for r in train_rows))
    config["val_label_counts"] = dict(Counter(r["label_name"] for r in val_rows))
    config["gold_label_counts"] = dict(Counter(r["label_name"] for r in gold_rows))
    config["class_weights"] = class_weights.tolist() if class_weights is not None else None
    save_json(args.out_dir / "train_config.json", config)

    print("\nTraining")
    print("=" * 72)
    print(json.dumps(config, ensure_ascii=False, indent=2, default=str))

    trainer.train()

    final_model_dir = args.out_dir / "final_model"
    trainer.save_model(str(final_model_dir))
    tokenizer.save_pretrained(str(final_model_dir))

    print("\nEvaluating validation and gold")
    print("=" * 72)

    val_eval = evaluate_split(trainer, val_ds, val_rows, threshold=None)
    selected_threshold = val_eval["threshold_selection"]["selected_threshold"]
    gold_eval = evaluate_split(trainer, gold_ds, gold_rows, threshold=selected_threshold)

    write_jsonl(args.out_dir / "val_predictions.jsonl", val_eval["pred_rows"])
    write_jsonl(args.out_dir / "gold_predictions.jsonl", gold_eval["pred_rows"])

    summary = {
        "model_path": args.model_path,
        "final_model_dir": str(final_model_dir),
        "selected_threshold_from_val": selected_threshold,
        "threshold_selection": val_eval["threshold_selection"],
        "val": {
            "overall": val_eval["overall"],
            "slices": val_eval["slices"],
        },
        "gold": {
            "overall": gold_eval["overall"],
            "slices": gold_eval["slices"],
        },
        "caveats": [
            "Gold binary positives are mostly bait; grounded::UNSUPPORTED has low n and should be interpreted descriptively.",
            "Validation is teacher-labeled and used only for early stopping/threshold selection.",
            "Gold is human-reviewed and frozen.",
        ],
    }

    save_json(args.out_dir / "metrics_summary.json", summary)

    print("\nFinal metrics")
    print("=" * 72)
    print(f"Selected threshold from val: {selected_threshold}")
    print("\nVAL overall:")
    print(json.dumps(val_eval["overall"], ensure_ascii=False, indent=2))
    print("\nGOLD overall:")
    print(json.dumps(gold_eval["overall"], ensure_ascii=False, indent=2))
    print("\nGOLD question_type slices:")
    print(json.dumps(gold_eval["slices"]["question_type"], ensure_ascii=False, indent=2))
    print("\nWrote:")
    print(f"  {final_model_dir}")
    print(f"  {args.out_dir / 'metrics_summary.json'}")
    print(f"  {args.out_dir / 'val_predictions.jsonl'}")
    print(f"  {args.out_dir / 'gold_predictions.jsonl'}")


if __name__ == "__main__":
    main()
