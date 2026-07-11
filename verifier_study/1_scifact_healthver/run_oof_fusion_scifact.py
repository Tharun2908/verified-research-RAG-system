from __future__ import annotations

import argparse
import json
import random
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
import torch
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, average_precision_score, precision_recall_fscore_support, roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer

LABEL_NAMES = {0: "SUPPORTED", 1: "UNSUPPORTED"}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise SystemExit(f"Invalid JSONL {path}:{n}: {e}") from e
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, default=str)


def key(row: dict[str, Any]) -> str:
    for k in ("claim_id", "review_id"):
        if row.get(k) is not None:
            return str(row[k])
    return f"qid={row.get('qid')}::{row.get('claim') or row.get('claim_text')}"


def group(row: dict[str, Any]) -> str:
    return str(row.get("qid", row.get("group_id", key(row))))


def label(row: dict[str, Any]) -> int:
    if row.get("label") is not None:
        return int(row["label"])
    name = str(row.get("final_label") or row.get("label_name") or "").upper()
    if name == "SUPPORTED":
        return 0
    if name == "UNSUPPORTED":
        return 1
    raise ValueError(f"Non-binary row {key(row)}: {name}")


def standardize_binary(row: dict[str, Any]) -> dict[str, Any]:
    out = dict(row)
    y = label(row)
    out["label"] = y
    out["label_name"] = LABEL_NAMES[y]
    return out


def claim(row: dict[str, Any]) -> str:
    return str(row.get("claim") or row.get("claim_text") or "").strip()


def evidence(row: dict[str, Any]) -> str:
    return str(row.get("evidence_text") or row.get("evidence_text_for_verifier") or "").strip()


def softmax_np(x: np.ndarray) -> np.ndarray:
    x = x - x.max(axis=1, keepdims=True)
    e = np.exp(x)
    return e / e.sum(axis=1, keepdims=True)


def safe_auc(y, s, w=None):
    try:
        return float(roc_auc_score(y, s, sample_weight=w)) if len(np.unique(y)) == 2 else None
    except Exception:
        return None


def safe_auprc(y, s, w=None):
    try:
        return float(average_precision_score(y, s, sample_weight=w)) if len(np.unique(y)) == 2 else None
    except Exception:
        return None


def metrics(y, s, threshold, w=None):
    if w is None:
        w = np.ones(len(y), dtype=float)
    pred = (s >= threshold).astype(int)
    p, r, f1, _ = precision_recall_fscore_support(y, pred, average="binary", pos_label=1, zero_division=0, sample_weight=w)
    return {
        "threshold": float(threshold),
        "n_raw": int(len(y)),
        "n_weighted": float(w.sum()),
        "accuracy": float(accuracy_score(y, pred, sample_weight=w)),
        "precision": float(p),
        "recall": float(r),
        "f1": float(f1),
        "auroc": safe_auc(y, s, w),
        "auprc": safe_auprc(y, s, w),
        "confusion": {
            "tn": float(w[(y == 0) & (pred == 0)].sum()),
            "fp": float(w[(y == 0) & (pred == 1)].sum()),
            "fn": float(w[(y == 1) & (pred == 0)].sum()),
            "tp": float(w[(y == 1) & (pred == 1)].sum()),
        },
    }


def choose_threshold(y, s):
    best = None
    for t in np.round(np.arange(0.01, 0.991, 0.01), 2):
        m = metrics(y, s, float(t))
        rank = (m["f1"], m["recall"], m["precision"])
        if best is None or rank > best[0]:
            best = (rank, float(t), m)
    return {"selected_threshold": best[1], "selection": "max_val_f1_then_recall_then_precision", "val_metrics": best[2]}


class PairDataset(Dataset):
    def __init__(self, rows):
        self.rows = rows
    def __len__(self):
        return len(self.rows)
    def __getitem__(self, i):
        return claim(self.rows[i]), evidence(self.rows[i])


def infer(rows, model_path, mode, batch_size, max_length, bf16, fp16):
    tok = AutoTokenizer.from_pretrained(model_path, use_fast=True)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device).eval()
    ds = PairDataset(rows)
    def collate(batch):
        return tok([x[0] for x in batch], [x[1] for x in batch], padding=True, truncation=True, max_length=max_length, return_tensors="pt")
    loader = DataLoader(ds, batch_size=batch_size, shuffle=False, collate_fn=collate)
    dtype = torch.bfloat16 if bf16 else (torch.float16 if fp16 else None)
    scores = []
    with torch.no_grad():
        for batch in loader:
            batch = {k: v.to(device) for k, v in batch.items()}
            if dtype is not None and device.type == "cuda":
                with torch.autocast("cuda", dtype=dtype):
                    logits = model(**batch).logits
            else:
                logits = model(**batch).logits
            arr = logits.detach().float().cpu().numpy()
            if mode == "s2":
                rel = arr if arr.ndim == 1 else (arr[:, 0] if arr.shape[1] == 1 else arr[:, 1])
                scores.extend((-rel).tolist())
            else:
                scores.extend(softmax_np(arr)[:, 1].tolist())
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return np.asarray(scores, dtype=float)


def cache_scores(path, rows, field, fn):
    if path.exists():
        cached = read_jsonl(path)
        if len(cached) == len(rows) and [r["row_key"] for r in cached] == [key(r) for r in rows]:
            print(f"Using cache: {path}", flush=True)
            return np.asarray([float(r[field]) for r in cached], dtype=float)
    scores = fn()
    write_jsonl(path, [{"row_key": key(r), field: float(s)} for r, s in zip(rows, scores)])
    return scores


def build_outer_folds(rows, n_splits, seed):
    y = np.asarray([label(r) for r in rows])
    groups = np.asarray([group(r) for r in rows])
    x = np.zeros((len(rows), 1))
    splitter = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    return list(splitter.split(x, y, groups))


def build_inner_split(rows, seed):
    y = np.asarray([label(r) for r in rows])
    groups = np.asarray([group(r) for r in rows])
    x = np.zeros((len(rows), 1))
    n_splits = min(10, len(np.unique(groups)))
    splitter = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    tr, va = next(splitter.split(x, y, groups))
    if len(np.unique(y[tr])) < 2 or len(np.unique(y[va])) < 2:
        raise RuntimeError("Inner split lost one class")
    return tr, va


def run_fold(fold, train_rows, test_rows, args):
    fold_dir = args.out_dir / "folds" / f"fold_{fold}"
    pred_path = fold_dir / "gold_predictions.jsonl"
    if pred_path.exists():
        preds = read_jsonl(pred_path)
        if len(preds) == len(test_rows):
            pmap = {key(r): float(r["prob_unsupported"]) for r in preds}
            if set(pmap) == {key(r) for r in test_rows}:
                print(f"Fold {fold}: using cached OOF predictions", flush=True)
                return np.asarray([pmap[key(r)] for r in test_rows], dtype=float)

    inner_tr_idx, inner_va_idx = build_inner_split(train_rows, args.seed + fold)
    inner_train = [standardize_binary(train_rows[i]) for i in inner_tr_idx]
    inner_val = [standardize_binary(train_rows[i]) for i in inner_va_idx]
    outer_test = [standardize_binary(r) for r in test_rows]

    tq, vq, oq = ({group(r) for r in x} for x in (inner_train, inner_val, outer_test))
    if tq & vq or tq & oq or vq & oq:
        raise RuntimeError(f"Question leakage in fold {fold}")

    fold_dir.mkdir(parents=True, exist_ok=True)
    train_path = fold_dir / "inner_train.jsonl"
    val_path = fold_dir / "inner_val.jsonl"
    test_path = fold_dir / "outer_test.jsonl"
    write_jsonl(train_path, inner_train)
    write_jsonl(val_path, inner_val)
    write_jsonl(test_path, outer_test)
    save_json(fold_dir / "split_summary.json", {
        "fold": fold,
        "inner_train_rows": len(inner_train), "inner_val_rows": len(inner_val), "outer_test_rows": len(outer_test),
        "inner_train_questions": len(tq), "inner_val_questions": len(vq), "outer_test_questions": len(oq),
        "inner_train_labels": dict(Counter(label(r) for r in inner_train)),
        "inner_val_labels": dict(Counter(label(r) for r in inner_val)),
        "outer_test_labels": dict(Counter(label(r) for r in outer_test)),
        "question_overlap": {"train_val": len(tq & vq), "train_test": len(tq & oq), "val_test": len(vq & oq)},
    })

    cmd = [
        sys.executable, "-u", str(args.finetune_script),
        "--model-path", str(args.base_model),
        "--train-jsonl", str(train_path),
        "--val-jsonl", str(val_path),
        "--gold-jsonl", str(test_path),
        "--out-dir", str(fold_dir),
        "--epochs", str(args.epochs),
        "--batch-size", str(args.batch_size),
        "--eval-batch-size", str(args.eval_batch_size),
        "--grad-accum", str(args.grad_accum),
        "--lr", str(args.lr),
        "--weight-decay", str(args.weight_decay),
        "--warmup-ratio", str(args.warmup_ratio),
        "--max-length", str(args.max_length),
        "--seed", str(args.seed + fold),
        "--early-stopping-patience", str(args.early_stopping_patience),
        "--weighted-loss",
    ]
    if args.bf16:
        cmd.append("--bf16")
    if args.fp16:
        cmd.append("--fp16")
    print("\nRUN:", " ".join(cmd), flush=True)
    with (fold_dir / "train.log").open("w", encoding="utf-8") as log:
        subprocess.run(cmd, check=True, stdout=log, stderr=subprocess.STDOUT)

    preds = read_jsonl(pred_path)
    pmap = {key(r): float(r["prob_unsupported"]) for r in preds}
    scores = np.asarray([pmap[key(r)] for r in test_rows], dtype=float)

    if not args.keep_fold_models:
        for p in (fold_dir / "checkpoints", fold_dir / "final_model"):
            if p.exists():
                shutil.rmtree(p)
    return scores


def minmax_apply(s, lo, hi):
    return np.zeros_like(s) if hi <= lo else np.clip((s - lo) / (hi - lo), 0.0, 1.0)


def fit_and_eval_fusion(name, y_train, s2_train, s4_train, split_data, split_rows, out_dir, seed):
    lo, hi = float(s2_train.min()), float(s2_train.max())
    x_train = np.column_stack([minmax_apply(s2_train, lo, hi), s4_train])
    clf = LogisticRegression(solver="liblinear", C=1.0, class_weight=None, random_state=seed, max_iter=2000)
    clf.fit(x_train, y_train)

    probs = {}
    for split, (y, s2, s4) in split_data.items():
        x = np.column_stack([minmax_apply(s2, lo, hi), s4])
        probs[split] = clf.predict_proba(x)[:, 1]
    threshold_info = choose_threshold(split_data["val"][0], probs["val"])
    threshold = threshold_info["selected_threshold"]

    results = {}
    for split, p in probs.items():
        y = split_data[split][0]
        rows = split_rows[split]
        w = np.asarray([float(r.get("sampling_weight") or 1.0) for r in rows]) if split == "hard" else np.ones(len(rows))
        results[split] = {"raw": metrics(y, p, threshold), "weighted": metrics(y, p, threshold, w)}
        write_jsonl(out_dir / f"{name}_{split}_predictions.jsonl", [
            {**r, "fusion_name": name, "fusion_prob_unsupported": float(v), "fusion_threshold": threshold,
             "fusion_pred_label": int(v >= threshold), "fusion_pred_label_name": LABEL_NAMES[int(v >= threshold)]}
            for r, v in zip(rows, p)
        ])

    return {
        "fit_split": "binary_train",
        "s2_minmax_from_train": {"lo": lo, "hi": hi},
        "logistic_regression": {"solver": "liblinear", "C": 1.0, "class_weight": None,
                                "intercept": clf.intercept_.tolist(), "coef": clf.coef_.tolist()},
        "selected_threshold_from_val": threshold,
        "threshold_selection": threshold_info,
        "results": results,
    }


def load_threshold(path, *keys):
    obj = json.load(open(path, encoding="utf-8"))
    for dotted in keys:
        cur = obj
        ok = True
        for part in dotted.split("."):
            if isinstance(cur, dict) and part in cur:
                cur = cur[part]
            else:
                ok = False
                break
        if ok:
            return float(cur)
    raise KeyError(f"No threshold found in {path}: {keys}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", type=Path, default=Path("data/distill_arxiv_v2/binary_train.jsonl"))
    ap.add_argument("--val", type=Path, default=Path("data/distill_arxiv_v2/binary_val.jsonl"))
    ap.add_argument("--gold", type=Path, default=Path("data/distill_arxiv/gold_binary_eval.jsonl"))
    ap.add_argument("--hard", type=Path, default=Path("grounded_hard_random_review_labeled.jsonl"))
    ap.add_argument("--base-model", default="signal4_model_scifact_healthver")
    ap.add_argument("--final-ft-model", default="arxiv_s4_from_scifact_healthver/final_model")
    ap.add_argument("--s2-model", default="cross-encoder/ms-marco-MiniLM-L-6-v2")
    ap.add_argument("--finetune-script", type=Path, default=Path("finetune_s4_arxiv_binary.py"))
    ap.add_argument("--out-dir", type=Path, default=Path("oof_fusion_scifact_healthver"))
    ap.add_argument("--n-folds", type=int, default=5)
    ap.add_argument("--epochs", type=float, default=5)
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--eval-batch-size", type=int, default=16)
    ap.add_argument("--grad-accum", type=int, default=2)
    ap.add_argument("--lr", type=float, default=2e-5)
    ap.add_argument("--weight-decay", type=float, default=0.01)
    ap.add_argument("--warmup-ratio", type=float, default=0.06)
    ap.add_argument("--max-length", type=int, default=512)
    ap.add_argument("--seed", type=int, default=2908)
    ap.add_argument("--early-stopping-patience", type=int, default=2)
    ap.add_argument("--bf16", action="store_true")
    ap.add_argument("--fp16", action="store_true")
    ap.add_argument("--keep-fold-models", action="store_true")
    args = ap.parse_args()

    random.seed(args.seed); np.random.seed(args.seed); torch.manual_seed(args.seed)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    cache = args.out_dir / "score_cache"; cache.mkdir(exist_ok=True)

    train = [standardize_binary(r) for r in read_jsonl(args.train)]
    val = [standardize_binary(r) for r in read_jsonl(args.val)]
    gold = [standardize_binary(r) for r in read_jsonl(args.gold)]
    hard_all = read_jsonl(args.hard)
    hard = [standardize_binary(r) for r in hard_all if str(r.get("final_label") or "").upper() in {"SUPPORTED", "UNSUPPORTED"}]

    if {group(r) for r in train} & {group(r) for r in val}:
        raise SystemExit("Train/val qid overlap detected")

    y = {name: np.asarray([label(r) for r in rows]) for name, rows in {"train": train, "val": val, "gold": gold, "hard": hard}.items()}
    rows = {"train": train, "val": val, "gold": gold, "hard": hard}
    print(f"train={len(train)} val={len(val)} gold={len(gold)} hard_binary={len(hard)} hard_total={len(hard_all)}", flush=True)

    folds = build_outer_folds(train, args.n_folds, args.seed)
    oof = np.full(len(train), np.nan)
    assignments = []
    for fold, (tr_idx, te_idx) in enumerate(folds):
        tr_rows = [train[i] for i in tr_idx]
        te_rows = [train[i] for i in te_idx]
        if {group(r) for r in tr_rows} & {group(r) for r in te_rows}:
            raise RuntimeError(f"Outer qid leakage fold {fold}")
        scores = run_fold(fold, tr_rows, te_rows, args)
        oof[te_idx] = scores
        assignments.extend({"row_index": int(i), "row_key": key(train[i]), "claim_id": train[i].get("claim_id"),
                            "qid": train[i].get("qid"), "label": label(train[i]), "outer_fold": fold} for i in te_idx)
    if np.isnan(oof).any():
        raise RuntimeError("Incomplete OOF coverage")
    write_jsonl(args.out_dir / "fold_assignments.jsonl", sorted(assignments, key=lambda r: r["row_index"]))
    write_jsonl(args.out_dir / "oof_s4_train_predictions.jsonl", [
        {"row_key": key(r), "claim_id": r.get("claim_id"), "qid": r.get("qid"), "label": label(r), "oof_s4_prob_unsupported": float(s)}
        for r, s in zip(train, oof)
    ])

    s2, base, ft = {}, {}, {"train": oof}
    for split, rr in rows.items():
        s2[split] = cache_scores(cache / f"s2_{split}.jsonl", rr, "score", lambda rr=rr: infer(rr, args.s2_model, "s2", args.eval_batch_size, args.max_length, args.bf16, args.fp16))
        base[split] = cache_scores(cache / f"base_{split}.jsonl", rr, "score", lambda rr=rr: infer(rr, args.base_model, "s4", args.eval_batch_size, args.max_length, args.bf16, args.fp16))
        if split != "train":
            ft[split] = cache_scores(cache / f"ft_{split}.jsonl", rr, "score", lambda rr=rr: infer(rr, args.final_ft_model, "s4", args.eval_batch_size, args.max_length, args.bf16, args.fp16))

    split_rows = {k: rows[k] for k in ("val", "gold", "hard")}
    base_split = {k: (y[k], s2[k], base[k]) for k in split_rows}
    ft_split = {k: (y[k], s2[k], ft[k]) for k in split_rows}

    fusion_base = fit_and_eval_fusion("fusion_base_scifact_trainfit", y["train"], s2["train"], base["train"], base_split, split_rows, args.out_dir, args.seed)
    fusion_oof = fit_and_eval_fusion("fusion_ft_scifact_oof", y["train"], s2["train"], oof, ft_split, split_rows, args.out_dir, args.seed)

    s2_t = load_threshold("eval_signal2_relevance/metrics_summary.json", "selected_threshold_from_val_raw_unsupported_score", "selected_threshold_from_val")
    base_t = load_threshold("eval_base_scifact_healthver/metrics_summary.json", "selected_threshold_from_val")
    ft_t = load_threshold("arxiv_s4_from_scifact_healthver/metrics_summary.json", "selected_threshold_from_val")

    standalone = {}
    for split in ("val", "gold", "hard"):
        w = np.asarray([float(r.get("sampling_weight") or 1.0) for r in rows[split]]) if split == "hard" else np.ones(len(rows[split]))
        standalone[split] = {
            "signal2": {"raw": metrics(y[split], s2[split], s2_t), "weighted": metrics(y[split], s2[split], s2_t, w)},
            "base_scifact_healthver": {"raw": metrics(y[split], base[split], base_t), "weighted": metrics(y[split], base[split], base_t, w)},
            "ft_scifact_healthver": {"raw": metrics(y[split], ft[split], ft_t), "weighted": metrics(y[split], ft[split], ft_t, w)},
        }

    summary = {
        "protocol": {
            "outer_folds": args.n_folds,
            "outer_group_key": "qid",
            "inner_validation": "group-disjoint inner split; outer fold never used for early stopping",
            "fusion_fit": "binary_train with OOF S4 predictions",
            "s2_minmax_fit": "binary_train",
            "threshold_selection": "binary_val only",
            "gold_usage": "evaluation only",
            "grounded_hard_usage": "evaluation only",
            "grounded_hard_excluded_labels": ["ABSTENTION", "INVALID_EXTRACTION"],
        },
        "data": {
            "train_rows": len(train), "train_questions": len({group(r) for r in train}),
            "val_rows": len(val), "val_questions": len({group(r) for r in val}),
            "gold_rows": len(gold), "hard_total": len(hard_all), "hard_binary": len(hard),
            "hard_nonbinary": dict(Counter(str(r.get("final_label") or "UNKNOWN").upper() for r in hard_all if str(r.get("final_label") or "").upper() not in {"SUPPORTED", "UNSUPPORTED"})),
        },
        "training": {"epochs": args.epochs, "batch_size": args.batch_size, "grad_accum": args.grad_accum, "lr": args.lr,
                     "weight_decay": args.weight_decay, "warmup_ratio": args.warmup_ratio, "max_length": args.max_length,
                     "weighted_loss": True, "seed": args.seed, "bf16": args.bf16, "fp16": args.fp16},
        "standalone": standalone,
        "fusion_base_scifact_trainfit": fusion_base,
        "fusion_ft_scifact_oof": fusion_oof,
    }

    ranking = []
    for name, result in standalone["hard"].items():
        ranking.append({"model": name, **{k: result["weighted"][k] for k in ("precision", "recall", "f1", "auroc", "auprc")}})
    for name, result in (("fusion_base_scifact_trainfit", fusion_base), ("fusion_ft_scifact_oof", fusion_oof)):
        m = result["results"]["hard"]["weighted"]
        ranking.append({"model": name, **{k: m[k] for k in ("precision", "recall", "f1", "auroc", "auprc")}})
    ranking.sort(key=lambda r: (r["f1"], r["auroc"] if r["auroc"] is not None else -1), reverse=True)
    summary["hard_ranking_by_weighted_f1"] = ranking
    save_json(args.out_dir / "metrics_summary.json", summary)

    print("\nGrounded-hard ranking", flush=True)
    for r in ranking:
        print(f"{r['model']:<36} wF1={r['f1']:.4f} wP={r['precision']:.4f} wR={r['recall']:.4f} wAUROC={r['auroc']:.4f} wAUPRC={r['auprc']:.4f}", flush=True)
    print(f"\nWrote {args.out_dir / 'metrics_summary.json'}", flush=True)


if __name__ == "__main__":
    main()
