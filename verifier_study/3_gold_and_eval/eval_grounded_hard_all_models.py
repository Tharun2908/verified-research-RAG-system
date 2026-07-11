
from __future__ import annotations

import argparse
import json
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

LABEL_TO_ID = {"SUPPORTED": 0, "UNSUPPORTED": 1}
ID_TO_LABEL = {0: "SUPPORTED", 1: "UNSUPPORTED"}

S4_RUNS = {
    "base_scifact_healthver": {
        "model_path": "signal4_model_scifact_healthver",
        "metrics_path": "eval_base_scifact_healthver/metrics_summary.json",
    },
    "base_original_s4": {
        "model_path": "/workspace/signal4_model",
        "metrics_path": "eval_base_original_s4/metrics_summary.json",
    },
    "ft_scifact_healthver": {
        "model_path": "arxiv_s4_from_scifact_healthver/final_model",
        "metrics_path": "arxiv_s4_from_scifact_healthver/metrics_summary.json",
    },
    "ft_original_s4": {
        "model_path": "arxiv_s4_from_original_s4/final_model",
        "metrics_path": "arxiv_s4_from_original_s4/metrics_summary.json",
    },
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with open(path, encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise SystemExit(f"Invalid JSONL at {path}:{line_no}: {e}") from e
    return rows


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


def softmax_np(logits: np.ndarray) -> np.ndarray:
    x = logits - np.max(logits, axis=1, keepdims=True)
    e = np.exp(x)
    return e / np.sum(e, axis=1, keepdims=True)


def safe_auc(y, s, w):
    try:
        if len(np.unique(y)) < 2:
            return None
        return float(roc_auc_score(y, s, sample_weight=w))
    except Exception:
        return None


def safe_auprc(y, s, w):
    try:
        if len(np.unique(y)) < 2:
            return None
        return float(average_precision_score(y, s, sample_weight=w))
    except Exception:
        return None


def weighted_ece(y_true, probs_pos, threshold, weights, n_bins=10):
    y_pred = (probs_pos >= threshold).astype(int)
    conf = np.where(y_pred == 1, probs_pos, 1.0 - probs_pos)
    correct = (y_pred == y_true).astype(float)
    total_weight = float(weights.sum())
    if total_weight <= 0:
        return 0.0
    bins = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    for i in range(n_bins):
        lo, hi = bins[i], bins[i + 1]
        mask = (conf >= lo) & (conf <= hi) if i == n_bins - 1 else (conf >= lo) & (conf < hi)
        if not mask.any():
            continue
        wb = weights[mask]
        bw = float(wb.sum())
        if bw <= 0:
            continue
        acc = float(np.average(correct[mask], weights=wb))
        avg_conf = float(np.average(conf[mask], weights=wb))
        ece += (bw / total_weight) * abs(acc - avg_conf)
    return float(ece)


def metrics_at_threshold(y_true, score, threshold, weights=None):
    if weights is None:
        weights = np.ones(len(y_true), dtype=float)
    y_pred = (score >= threshold).astype(int)
    p, r, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average="binary", pos_label=1,
        zero_division=0, sample_weight=weights
    )
    tn = float(weights[(y_true == 0) & (y_pred == 0)].sum())
    fp = float(weights[(y_true == 0) & (y_pred == 1)].sum())
    fn = float(weights[(y_true == 1) & (y_pred == 0)].sum())
    tp = float(weights[(y_true == 1) & (y_pred == 1)].sum())
    return {
        "threshold": float(threshold),
        "n_raw": int(len(y_true)),
        "n_weighted": float(weights.sum()),
        "accuracy": float(accuracy_score(y_true, y_pred, sample_weight=weights)),
        "precision": float(p),
        "recall": float(r),
        "f1": float(f1),
        "auroc": safe_auc(y_true, score, weights),
        "auprc": safe_auprc(y_true, score, weights),
        "ece_10": weighted_ece(y_true, score, threshold, weights),
        "confusion": {"tn": tn, "fp": fp, "fn": fn, "tp": tp},
    }


class PairDataset(Dataset):
    def __init__(self, rows):
        self.rows = rows

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, idx):
        r = self.rows[idx]
        return {
            "claim": str(r.get("claim") or r.get("claim_text") or "").strip(),
            "evidence": str(r.get("evidence_text") or r.get("evidence_text_for_verifier") or "").strip(),
        }


def score_model(rows, model_path, batch_size, max_length, device, bf16, fp16, mode):
    tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=True)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    model.to(device)
    model.eval()

    ds = PairDataset(rows)

    def collate(batch):
        return tokenizer(
            [x["claim"] for x in batch],
            [x["evidence"] for x in batch],
            padding=True,
            truncation=True,
            max_length=max_length,
            return_tensors="pt",
        )

    dl = DataLoader(ds, batch_size=batch_size, shuffle=False, collate_fn=collate)
    scores = []
    dtype = torch.bfloat16 if bf16 else (torch.float16 if fp16 else None)

    with torch.no_grad():
        for batch in dl:
            batch = {k: v.to(device) for k, v in batch.items()}
            if dtype is not None and device.type == "cuda":
                with torch.autocast("cuda", dtype=dtype):
                    out = model(**batch)
            else:
                out = model(**batch)
            logits = out.logits.detach().float().cpu().numpy()
            if mode == "s2":
                relevance = logits if logits.ndim == 1 else (logits[:, 0] if logits.shape[1] == 1 else logits[:, 1])
                scores.extend((-relevance).tolist())
            else:
                if logits.shape[1] != 2:
                    raise RuntimeError(f"Expected [B,2] logits from {model_path}, got {logits.shape}")
                scores.extend(softmax_np(logits)[:, 1].tolist())

    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return np.asarray(scores, dtype=float)


def apply_fusion(s2_score, s4_score, run):
    mm = run["s2_minmax_from_val"]
    lo, hi = float(mm["lo"]), float(mm["hi"])
    s2_norm = np.zeros_like(s2_score) if hi <= lo else np.clip((s2_score - lo) / (hi - lo), 0.0, 1.0)
    coef = np.asarray(run["logistic_regression"]["coef"], dtype=float).reshape(-1)
    intercept = float(np.asarray(run["logistic_regression"]["intercept"]).reshape(-1)[0])
    logit = intercept + coef[0] * s2_norm + coef[1] * s4_score
    prob = 1.0 / (1.0 + np.exp(-logit))
    return prob, float(run["selected_threshold_from_val"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tranche", type=Path, default=Path("grounded_hard_random_review_labeled.jsonl"))
    ap.add_argument("--out-dir", type=Path, default=Path("grounded_hard_all_model_eval"))
    ap.add_argument("--s2-model", default="cross-encoder/ms-marco-MiniLM-L-6-v2")
    ap.add_argument("--s2-metrics", type=Path, default=Path("eval_signal2_relevance/metrics_summary.json"))
    ap.add_argument("--fusion-summary", type=Path, default=Path("fusion_s2_s4_results/metrics_summary.json"))
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--max-length", type=int, default=512)
    ap.add_argument("--bf16", action="store_true")
    ap.add_argument("--fp16", action="store_true")
    args = ap.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    reviewed = read_jsonl(args.tranche)
    binary_rows = [r for r in reviewed if str(r.get("final_label") or "").upper() in LABEL_TO_ID]
    abstention_rows = [r for r in reviewed if str(r.get("final_label") or "").upper() == "ABSTENTION"]
    for r in binary_rows:
        r["final_label"] = str(r["final_label"]).upper()

    y = np.asarray([LABEL_TO_ID[r["final_label"]] for r in binary_rows], dtype=int)
    w_raw = np.ones(len(binary_rows), dtype=float)
    w_design = np.asarray([float(r.get("sampling_weight") or 1.0) for r in binary_rows], dtype=float)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Reviewed={len(reviewed)} binary={len(binary_rows)} abstention={len(abstention_rows)} device={device}")

    results = {
        "protocol": {
            "thresholds_fixed_from_validation": True,
            "fusion_fixed_from_validation": True,
            "grounded_hard_used_for_fitting": False,
            "abstention_excluded_from_binary_metrics": True,
        },
        "label_counts_raw": {
            "SUPPORTED": int((y == 0).sum()),
            "UNSUPPORTED": int((y == 1).sum()),
            "ABSTENTION": len(abstention_rows),
        },
        "models": {},
    }
    pred_rows = [dict(r) for r in binary_rows]

    print("Scoring Signal 2")
    s2 = score_model(binary_rows, args.s2_model, args.batch_size, args.max_length, device, args.bf16, args.fp16, "s2")
    s2_meta = load_json(args.s2_metrics)
    s2_t = float(s2_meta["selected_threshold_from_val_raw_unsupported_score"])
    results["models"]["signal2"] = {
        "threshold": s2_t,
        "raw": metrics_at_threshold(y, s2, s2_t, w_raw),
        "weighted": metrics_at_threshold(y, s2, s2_t, w_design),
    }
    for r, s in zip(pred_rows, s2):
        r["signal2_score"] = float(s)
        r["signal2_pred"] = int(s >= s2_t)

    s4_scores = {}
    for name, cfg in S4_RUNS.items():
        print(f"Scoring {name}")
        score = score_model(binary_rows, cfg["model_path"], args.batch_size, args.max_length, device, args.bf16, args.fp16, "s4")
        t = float(load_json(Path(cfg["metrics_path"]))["selected_threshold_from_val"])
        s4_scores[name] = score
        results["models"][name] = {
            "threshold": t,
            "raw": metrics_at_threshold(y, score, t, w_raw),
            "weighted": metrics_at_threshold(y, score, t, w_design),
        }
        for r, s in zip(pred_rows, score):
            r[f"{name}_score"] = float(s)
            r[f"{name}_pred"] = int(s >= t)

    fusion_meta = load_json(args.fusion_summary)
    for name, run in fusion_meta.get("runs", {}).items():
        if name not in s4_scores:
            continue
        print(f"Applying fusion {name}")
        score, t = apply_fusion(s2, s4_scores[name], run)
        out_name = f"fusion_{name}"
        results["models"][out_name] = {
            "threshold": t,
            "raw": metrics_at_threshold(y, score, t, w_raw),
            "weighted": metrics_at_threshold(y, score, t, w_design),
            "fixed_parameters": run["logistic_regression"],
        }
        for r, s in zip(pred_rows, score):
            r[f"{out_name}_score"] = float(s)
            r[f"{out_name}_pred"] = int(s >= t)

    ranking = []
    for name, m in results["models"].items():
        ranking.append({
            "model": name,
            "weighted_f1": m["weighted"]["f1"],
            "weighted_precision": m["weighted"]["precision"],
            "weighted_recall": m["weighted"]["recall"],
            "weighted_auroc": m["weighted"]["auroc"],
            "weighted_auprc": m["weighted"]["auprc"],
            "raw_f1": m["raw"]["f1"],
        })
    ranking.sort(key=lambda x: (x["weighted_f1"], x["weighted_auroc"] or -1), reverse=True)
    results["ranking_by_weighted_f1"] = ranking

    save_json(args.out_dir / "metrics_summary.json", results)
    write_jsonl(args.out_dir / "binary_predictions.jsonl", pred_rows)
    write_jsonl(args.out_dir / "abstention_rows.jsonl", abstention_rows)

    print("\nRanking")
    for r in ranking:
        print(
            f"{r['model']:<34} "
            f"wF1={r['weighted_f1']:.4f} "
            f"wP={r['weighted_precision']:.4f} "
            f"wR={r['weighted_recall']:.4f} "
            f"wAUROC={r['weighted_auroc']:.4f} "
            f"wAUPRC={r['weighted_auprc']:.4f}"
        )
    print(f"\nWrote {args.out_dir / 'metrics_summary.json'}")


if __name__ == "__main__":
    main()
