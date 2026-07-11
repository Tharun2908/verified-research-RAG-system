"""
eval_signal2_relevance_arxiv.py

Evaluate Signal 2-style relevance scoring on the arXiv binary verifier dataset.

Idea:
  - Use a MS MARCO cross-encoder as a relevance scorer.
  - Score pair: (claim, evidence_text)
  - Higher relevance_score means the evidence is more relevant/supportive.
  - For unsupported detection, use unsupported_score = -relevance_score.
  - Select threshold on binary_val.jsonl by max F1.
  - Apply the same threshold to frozen human gold.

Labels:
  0 = SUPPORTED
  1 = UNSUPPORTED

Default model:
  cross-encoder/ms-marco-MiniLM-L-6-v2

Example:
  python -u eval_signal2_relevance_arxiv.py \
    --model-path cross-encoder/ms-marco-MiniLM-L-6-v2 \
    --val-jsonl data/distill_arxiv_v2/binary_val.jsonl \
    --gold-jsonl data/distill_arxiv/gold_binary_eval.jsonl \
    --out-dir eval_signal2_relevance \
    --batch-size 32 \
    --max-length 512 \
    --bf16 \
    > eval_signal2_relevance.log 2>&1

Outputs:
  <out-dir>/metrics_summary.json
  <out-dir>/val_predictions.jsonl
  <out-dir>/gold_predictions.jsonl
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
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
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer


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


class PairDataset(Dataset):
    def __init__(self, rows: list[dict[str, Any]]):
        self.rows = rows

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, idx: int) -> dict[str, Any]:
        r = self.rows[idx]
        claim = str(r.get("claim") or r.get("claim_text") or "").strip()
        evidence = str(r.get("evidence_text") or r.get("evidence_text_for_verifier") or "").strip()
        return {
            "claim": claim,
            "evidence": evidence,
            "label": int(r["label"]),
            "idx": idx,
        }


def collate_batch(batch: list[dict[str, Any]], tokenizer, max_length: int) -> dict[str, Any]:
    claims = [b["claim"] for b in batch]
    evidences = [b["evidence"] for b in batch]
    labels = torch.tensor([b["label"] for b in batch], dtype=torch.long)
    idxs = [b["idx"] for b in batch]

    enc = tokenizer(
        claims,
        evidences,
        padding=True,
        truncation=True,
        max_length=max_length,
        return_tensors="pt",
    )
    enc["labels"] = labels
    enc["idxs"] = idxs
    return enc


def get_relevance_scores(
    rows: list[dict[str, Any]],
    tokenizer,
    model,
    batch_size: int,
    max_length: int,
    device: torch.device,
    bf16: bool = False,
    fp16: bool = False,
) -> np.ndarray:
    ds = PairDataset(rows)
    dl = DataLoader(
        ds,
        batch_size=batch_size,
        shuffle=False,
        collate_fn=lambda b: collate_batch(b, tokenizer, max_length),
    )

    model.eval()
    scores = []

    autocast_dtype = None
    if bf16:
        autocast_dtype = torch.bfloat16
    elif fp16:
        autocast_dtype = torch.float16

    with torch.no_grad():
        for batch in dl:
            idxs = batch.pop("idxs")
            batch.pop("labels", None)
            batch = {k: v.to(device) for k, v in batch.items()}

            if autocast_dtype is not None and device.type == "cuda":
                with torch.autocast(device_type="cuda", dtype=autocast_dtype):
                    out = model(**batch)
            else:
                out = model(**batch)

            logits = out.logits.detach().float().cpu().numpy()

            # Most MS MARCO cross-encoders output shape [B, 1].
            # If a model outputs two logits, use the second logit as the positive/relevant score.
            if logits.ndim == 1:
                batch_scores = logits
            elif logits.shape[1] == 1:
                batch_scores = logits[:, 0]
            else:
                batch_scores = logits[:, 1]

            scores.extend(batch_scores.tolist())

    return np.array(scores, dtype=float)


def safe_auc(y_true: np.ndarray, scores: np.ndarray) -> float | None:
    try:
        if len(set(y_true.tolist())) < 2:
            return None
        return float(roc_auc_score(y_true, scores))
    except Exception:
        return None


def safe_auprc(y_true: np.ndarray, scores: np.ndarray) -> float | None:
    try:
        if len(set(y_true.tolist())) < 2:
            return None
        return float(average_precision_score(y_true, scores))
    except Exception:
        return None


def minmax_from_val(val_scores: np.ndarray, scores: np.ndarray) -> np.ndarray:
    lo = float(np.min(val_scores))
    hi = float(np.max(val_scores))
    if hi <= lo:
        return np.zeros_like(scores, dtype=float)
    return np.clip((scores - lo) / (hi - lo), 0.0, 1.0)


def ece_score(y_true: np.ndarray, unsupported_prob_like: np.ndarray, threshold: float, n_bins: int = 10) -> float:
    """
    ECE using confidence of the thresholded prediction.

    Since Signal 2 is not calibrated probability, this is only a rough confidence diagnostic
    after min-max scaling. Interpret cautiously.
    """
    y_pred = (unsupported_prob_like >= threshold).astype(int)
    conf = np.where(y_pred == 1, unsupported_prob_like, 1.0 - unsupported_prob_like)
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


def metrics_at_threshold(y_true: np.ndarray, unsupported_score: np.ndarray, threshold: float) -> dict[str, Any]:
    y_pred = (unsupported_score >= threshold).astype(int)

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
        "auroc": safe_auc(y_true, unsupported_score),
        "auprc": safe_auprc(y_true, unsupported_score),
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


def choose_best_threshold(y_true: np.ndarray, unsupported_score: np.ndarray) -> dict[str, Any]:
    # Search over observed score quantiles plus evenly spaced grid.
    qs = np.quantile(unsupported_score, np.linspace(0.0, 1.0, 101))
    grid = np.linspace(float(np.min(unsupported_score)), float(np.max(unsupported_score)), 101)
    thresholds = sorted(set(float(x) for x in np.concatenate([qs, grid])))

    best = None
    for t in thresholds:
        m = metrics_at_threshold(y_true, unsupported_score, t)
        key = (m["f1"], m["recall"], m["precision"])
        if best is None or key > best["key"]:
            best = {"threshold": float(t), "metrics": m, "key": key}

    assert best is not None
    return {
        "selected_threshold": best["threshold"],
        "selection_metric": "max_val_f1_then_recall_then_precision",
        "val_metrics_at_selected_threshold": best["metrics"],
    }


def compute_slices(rows: list[dict[str, Any]], y_true: np.ndarray, unsupported_score: np.ndarray, threshold: float) -> dict[str, Any]:
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
            out[group_name][name] = metrics_at_threshold(y_true[idx], unsupported_score[idx], threshold)
    return out


def make_prediction_rows(
    rows: list[dict[str, Any]],
    relevance_score: np.ndarray,
    unsupported_score: np.ndarray,
    threshold: float,
    unsupported_score_minmax: np.ndarray | None = None,
) -> list[dict[str, Any]]:
    out = []
    for i, (r, rel, unsup) in enumerate(zip(rows, relevance_score, unsupported_score)):
        pred = int(unsup >= threshold)
        rr = dict(r)
        rr["signal2_relevance_score_raw"] = float(rel)
        rr["signal2_unsupported_score_raw"] = float(unsup)
        if unsupported_score_minmax is not None:
            rr["signal2_unsupported_score_minmax_from_val"] = float(unsupported_score_minmax[i])
        rr["pred_label"] = pred
        rr["pred_label_name"] = LABEL_NAMES[pred]
        rr["threshold"] = float(threshold)
        out.append(rr)
    return out


def evaluate_split(
    rows: list[dict[str, Any]],
    relevance_score: np.ndarray,
    threshold: float | None = None,
) -> dict[str, Any]:
    y_true = np.array([int(r["label"]) for r in rows], dtype=int)
    unsupported_score = -relevance_score

    threshold_selection = None
    if threshold is None:
        threshold_selection = choose_best_threshold(y_true, unsupported_score)
        threshold = threshold_selection["selected_threshold"]

    overall = metrics_at_threshold(y_true, unsupported_score, threshold)
    slices = compute_slices(rows, y_true, unsupported_score, threshold)

    return {
        "threshold_selection": threshold_selection,
        "overall": overall,
        "slices": slices,
        "unsupported_score": unsupported_score,
        "y_true": y_true,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-path", default="cross-encoder/ms-marco-MiniLM-L-6-v2")
    ap.add_argument("--val-jsonl", type=Path, required=True)
    ap.add_argument("--gold-jsonl", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--max-length", type=int, default=512)
    ap.add_argument("--bf16", action="store_true")
    ap.add_argument("--fp16", action="store_true")
    args = ap.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)

    val_rows = read_jsonl(args.val_jsonl)
    gold_rows = read_jsonl(args.gold_jsonl)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("\nLoading Signal 2 relevance model")
    print("=" * 72)
    print(f"Model:  {args.model_path}")
    print(f"Device: {device}")

    tokenizer = AutoTokenizer.from_pretrained(args.model_path, use_fast=True)
    model = AutoModelForSequenceClassification.from_pretrained(args.model_path)
    model.to(device)

    print("\nScoring validation")
    print("=" * 72)
    val_relevance = get_relevance_scores(
        val_rows,
        tokenizer,
        model,
        batch_size=args.batch_size,
        max_length=args.max_length,
        device=device,
        bf16=args.bf16,
        fp16=args.fp16,
    )

    print("\nScoring gold")
    print("=" * 72)
    gold_relevance = get_relevance_scores(
        gold_rows,
        tokenizer,
        model,
        batch_size=args.batch_size,
        max_length=args.max_length,
        device=device,
        bf16=args.bf16,
        fp16=args.fp16,
    )

    val_eval = evaluate_split(val_rows, val_relevance, threshold=None)
    threshold = val_eval["threshold_selection"]["selected_threshold"]
    gold_eval = evaluate_split(gold_rows, gold_relevance, threshold=threshold)

    # Rough min-max diagnostic from val range, not used for thresholded metrics.
    val_minmax = minmax_from_val(val_eval["unsupported_score"], val_eval["unsupported_score"])
    gold_minmax = minmax_from_val(val_eval["unsupported_score"], gold_eval["unsupported_score"])

    val_eval["overall"]["ece_10_minmax_diagnostic"] = ece_score(
        val_eval["y_true"], val_minmax, threshold=minmax_from_val(val_eval["unsupported_score"], np.array([threshold]))[0]
    )
    gold_eval["overall"]["ece_10_minmax_diagnostic"] = ece_score(
        gold_eval["y_true"], gold_minmax, threshold=minmax_from_val(val_eval["unsupported_score"], np.array([threshold]))[0]
    )

    val_pred_rows = make_prediction_rows(
        val_rows,
        val_relevance,
        val_eval["unsupported_score"],
        threshold,
        unsupported_score_minmax=val_minmax,
    )
    gold_pred_rows = make_prediction_rows(
        gold_rows,
        gold_relevance,
        gold_eval["unsupported_score"],
        threshold,
        unsupported_score_minmax=gold_minmax,
    )

    write_jsonl(args.out_dir / "val_predictions.jsonl", val_pred_rows)
    write_jsonl(args.out_dir / "gold_predictions.jsonl", gold_pred_rows)

    summary = {
        "model_path": args.model_path,
        "scoring": {
            "pair": "claim, evidence_text",
            "relevance_score": "raw model logit",
            "unsupported_score": "-relevance_score",
            "threshold_selection": "validation max F1 on unsupported_score",
        },
        "selected_threshold_from_val_raw_unsupported_score": threshold,
        "selected_threshold_from_val_raw_relevance_score_equivalent": -threshold,
        "val": {
            "overall": val_eval["overall"],
            "slices": val_eval["slices"],
        },
        "gold": {
            "overall": gold_eval["overall"],
            "slices": gold_eval["slices"],
        },
        "notes": [
            "Signal 2 is a relevance signal, not a factual entailment verifier.",
            "High performance means evidence relevance alone separates many labels.",
            "Low performance does not necessarily disprove usefulness as a feature in fusion.",
            "ECE here is only a min-max diagnostic because raw cross-encoder scores are not calibrated probabilities.",
        ],
    }

    save_json(args.out_dir / "metrics_summary.json", summary)

    print("\nFinished Signal 2 relevance evaluation")
    print("=" * 72)
    print(f"Selected threshold from val, unsupported_score=-relevance: {threshold}")
    print(f"Equivalent relevance threshold: {-threshold}")
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
