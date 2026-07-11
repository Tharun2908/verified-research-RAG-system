"""
fit_eval_s2_s4_fusion.py

Fit and evaluate a cheap S2+S4 logistic fusion head.

Features:
  x1 = norm_S2_unsupported_score
       - raw Signal 2 score is unsupported_score = -relevance_score
       - min-max normalization fitted on validation only
  x2 = S4 prob_unsupported

Training:
  - LogisticRegression on binary_val.jsonl labels via aligned prediction files
  - Gold/tranche never used for fitting or threshold selection
  - Threshold selected on validation by max F1
  - Same threshold applied to gold

Default runs expected under /workspace/project3:
  Signal 2:
    eval_signal2_relevance/val_predictions.jsonl
    eval_signal2_relevance/gold_predictions.jsonl

  S4 runs:
    eval_base_scifact_healthver/
    eval_base_original_s4/
    arxiv_s4_from_scifact_healthver/
    arxiv_s4_from_original_s4/

Example:
  python -u fit_eval_s2_s4_fusion.py \
    --s2-val eval_signal2_relevance/val_predictions.jsonl \
    --s2-gold eval_signal2_relevance/gold_predictions.jsonl \
    --out-dir fusion_s2_s4_results

Optional custom S4 run:
  --s4-run name:path/to/val_predictions.jsonl:path/to/gold_predictions.jsonl

Outputs:
  fusion_s2_s4_results/metrics_summary.json
  fusion_s2_s4_results/<run_name>_val_predictions.jsonl
  fusion_s2_s4_results/<run_name>_gold_predictions.jsonl
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    precision_recall_fscore_support,
    roc_auc_score,
)


LABEL_NAMES = {0: "SUPPORTED", 1: "UNSUPPORTED"}

DEFAULT_S4_RUNS = [
    (
        "base_scifact_healthver",
        "eval_base_scifact_healthver/val_predictions.jsonl",
        "eval_base_scifact_healthver/gold_predictions.jsonl",
    ),
    (
        "base_original_s4",
        "eval_base_original_s4/val_predictions.jsonl",
        "eval_base_original_s4/gold_predictions.jsonl",
    ),
    (
        "ft_scifact_healthver",
        "arxiv_s4_from_scifact_healthver/val_predictions.jsonl",
        "arxiv_s4_from_scifact_healthver/gold_predictions.jsonl",
    ),
    (
        "ft_original_s4",
        "arxiv_s4_from_original_s4/val_predictions.jsonl",
        "arxiv_s4_from_original_s4/gold_predictions.jsonl",
    ),
]


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


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def row_key(r: dict[str, Any]) -> str:
    for k in ["claim_id", "review_id", "qid"]:
        v = r.get(k)
        if v is not None and str(v).strip():
            return str(v)
    raise ValueError(f"Could not derive key for row: {r.keys()}")


def to_map(rows: list[dict[str, Any]], name: str) -> dict[str, dict[str, Any]]:
    out = {}
    dups = []
    for r in rows:
        k = row_key(r)
        if k in out:
            dups.append(k)
        out[k] = r
    if dups:
        raise SystemExit(f"{name} has duplicate keys. First duplicates: {dups[:10]}")
    return out


def get_s2_raw(row: dict[str, Any]) -> float:
    for k in [
        "signal2_unsupported_score_raw",
        "signal2_unsupported_score",
        "unsupported_score",
        "score",
    ]:
        if k in row and row[k] is not None:
            return float(row[k])
    raise KeyError(f"Could not find S2 unsupported score in row keys: {list(row.keys())}")


def get_s4_prob(row: dict[str, Any]) -> float:
    for k in [
        "prob_unsupported",
        "s4_prob_unsupported",
        "unsupported_probability",
        "score",
    ]:
        if k in row and row[k] is not None:
            return float(row[k])
    raise KeyError(f"Could not find S4 prob_unsupported in row keys: {list(row.keys())}")


def minmax_fit(scores: np.ndarray) -> tuple[float, float]:
    lo = float(np.min(scores))
    hi = float(np.max(scores))
    return lo, hi


def minmax_apply(scores: np.ndarray, lo: float, hi: float) -> np.ndarray:
    if hi <= lo:
        return np.zeros_like(scores, dtype=float)
    return np.clip((scores - lo) / (hi - lo), 0.0, 1.0)


def align_rows(
    s2_rows: list[dict[str, Any]],
    s4_rows: list[dict[str, Any]],
    split_name: str,
) -> list[dict[str, Any]]:
    s2_map = to_map(s2_rows, f"S2 {split_name}")
    s4_map = to_map(s4_rows, f"S4 {split_name}")

    common = sorted(set(s2_map) & set(s4_map))
    missing_s2 = sorted(set(s4_map) - set(s2_map))
    missing_s4 = sorted(set(s2_map) - set(s4_map))

    if missing_s2 or missing_s4:
        raise SystemExit(
            f"Key mismatch for {split_name}: "
            f"missing_s2={len(missing_s2)}, missing_s4={len(missing_s4)}. "
            f"First missing_s2={missing_s2[:5]}, first missing_s4={missing_s4[:5]}"
        )

    aligned = []
    for k in common:
        a = s2_map[k]
        b = s4_map[k]
        la = int(a["label"])
        lb = int(b["label"])
        if la != lb:
            raise SystemExit(f"Label mismatch for key {k}: S2={la}, S4={lb}")
        r = dict(a)
        r["_s4_row"] = b
        aligned.append(r)

    return aligned


def build_features(
    aligned: list[dict[str, Any]],
    s2_lo: float | None = None,
    s2_hi: float | None = None,
) -> tuple[np.ndarray, np.ndarray, tuple[float, float], list[dict[str, Any]]]:
    s2_raw = np.array([get_s2_raw(r) for r in aligned], dtype=float)
    s4_raw = np.array([get_s4_prob(r["_s4_row"]) for r in aligned], dtype=float)
    y = np.array([int(r["label"]) for r in aligned], dtype=int)

    if s2_lo is None or s2_hi is None:
        s2_lo, s2_hi = minmax_fit(s2_raw)

    s2_norm = minmax_apply(s2_raw, s2_lo, s2_hi)
    x = np.column_stack([s2_norm, s4_raw])

    clean_rows = []
    for r, s2r, s2n, s4p in zip(aligned, s2_raw, s2_norm, s4_raw):
        rr = dict(r)
        rr.pop("_s4_row", None)
        rr["fusion_feature_s2_unsupported_raw"] = float(s2r)
        rr["fusion_feature_s2_unsupported_norm"] = float(s2n)
        rr["fusion_feature_s4_prob_unsupported"] = float(s4p)
        clean_rows.append(rr)

    return x, y, (float(s2_lo), float(s2_hi)), clean_rows


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


def ece_score(y_true: np.ndarray, probs_pos: np.ndarray, threshold: float, n_bins: int = 10) -> float:
    y_pred = (probs_pos >= threshold).astype(int)
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
        "ece_10": ece_score(y_true, probs_pos, threshold=threshold, n_bins=10),
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
    thresholds = np.round(np.arange(0.01, 0.991, 0.01), 2)
    best = None

    for t in thresholds:
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
        rr["fusion_prob_unsupported"] = float(p)
        rr["fusion_pred_label"] = pred
        rr["fusion_pred_label_name"] = LABEL_NAMES[pred]
        rr["fusion_threshold"] = float(threshold)
        out.append(rr)
    return out


def parse_s4_run(spec: str) -> tuple[str, str, str]:
    parts = spec.split(":", 2)
    if len(parts) != 3:
        raise argparse.ArgumentTypeError(
            "--s4-run must be name:val_predictions.jsonl:gold_predictions.jsonl"
        )
    return parts[0], parts[1], parts[2]


def evaluate_one_run(
    run_name: str,
    s2_val_rows: list[dict[str, Any]],
    s2_gold_rows: list[dict[str, Any]],
    s4_val_path: Path,
    s4_gold_path: Path,
    out_dir: Path,
    class_weight: str | None,
    c_value: float,
) -> dict[str, Any]:
    s4_val_rows = read_jsonl(s4_val_path)
    s4_gold_rows = read_jsonl(s4_gold_path)

    val_aligned = align_rows(s2_val_rows, s4_val_rows, f"{run_name} val")
    gold_aligned = align_rows(s2_gold_rows, s4_gold_rows, f"{run_name} gold")

    x_val, y_val, (s2_lo, s2_hi), val_clean_rows = build_features(val_aligned)
    x_gold, y_gold, _, gold_clean_rows = build_features(gold_aligned, s2_lo=s2_lo, s2_hi=s2_hi)

    clf = LogisticRegression(
        solver="liblinear",
        class_weight=class_weight,
        C=c_value,
        random_state=2908,
    )
    clf.fit(x_val, y_val)

    val_probs = clf.predict_proba(x_val)[:, 1]
    gold_probs = clf.predict_proba(x_gold)[:, 1]

    threshold_info = choose_best_threshold(y_val, val_probs)
    threshold = threshold_info["selected_threshold"]

    val_overall = metrics_at_threshold(y_val, val_probs, threshold)
    gold_overall = metrics_at_threshold(y_gold, gold_probs, threshold)

    val_slices = compute_slices(val_clean_rows, y_val, val_probs, threshold)
    gold_slices = compute_slices(gold_clean_rows, y_gold, gold_probs, threshold)

    val_pred_rows = make_prediction_rows(val_clean_rows, val_probs, threshold)
    gold_pred_rows = make_prediction_rows(gold_clean_rows, gold_probs, threshold)

    write_jsonl(out_dir / f"{run_name}_val_predictions.jsonl", val_pred_rows)
    write_jsonl(out_dir / f"{run_name}_gold_predictions.jsonl", gold_pred_rows)

    return {
        "run_name": run_name,
        "s4_val_path": str(s4_val_path),
        "s4_gold_path": str(s4_gold_path),
        "features": ["norm_s2_unsupported_score", "s4_prob_unsupported"],
        "s2_minmax_from_val": {"lo": s2_lo, "hi": s2_hi},
        "logistic_regression": {
            "class_weight": class_weight,
            "C": c_value,
            "intercept": clf.intercept_.tolist(),
            "coef": clf.coef_.tolist(),
            "feature_names": ["norm_s2_unsupported_score", "s4_prob_unsupported"],
        },
        "selected_threshold_from_val": threshold,
        "threshold_selection": threshold_info,
        "val": {
            "overall": val_overall,
            "slices": val_slices,
        },
        "gold": {
            "overall": gold_overall,
            "slices": gold_slices,
        },
        "output_files": {
            "val_predictions": str(out_dir / f"{run_name}_val_predictions.jsonl"),
            "gold_predictions": str(out_dir / f"{run_name}_gold_predictions.jsonl"),
        },
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--s2-val", type=Path, default=Path("eval_signal2_relevance/val_predictions.jsonl"))
    ap.add_argument("--s2-gold", type=Path, default=Path("eval_signal2_relevance/gold_predictions.jsonl"))
    ap.add_argument("--out-dir", type=Path, default=Path("fusion_s2_s4_results"))
    ap.add_argument(
        "--s4-run",
        action="append",
        default=[],
        help="Optional run as name:val_predictions.jsonl:gold_predictions.jsonl. If omitted, default four S4 runs are used.",
    )
    ap.add_argument("--class-weight", choices=["balanced", "none"], default="none")
    ap.add_argument("--C", type=float, default=1.0)
    args = ap.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)

    s2_val_rows = read_jsonl(args.s2_val)
    s2_gold_rows = read_jsonl(args.s2_gold)

    if args.s4_run:
        runs = [parse_s4_run(x) for x in args.s4_run]
    else:
        runs = DEFAULT_S4_RUNS

    class_weight = None if args.class_weight == "none" else args.class_weight

    summary = {
        "s2_val": str(args.s2_val),
        "s2_gold": str(args.s2_gold),
        "out_dir": str(args.out_dir),
        "fit_protocol": {
            "fit_split": "binary validation",
            "gold_usage": "evaluation only",
            "threshold_selection": "validation max F1",
            "features": ["norm_S2_unsupported_score", "S4_prob_unsupported"],
            "evaluated_models_do_not_control_sampling": True,
        },
        "runs": {},
        "ranking": [],
    }

    print("\nFitting S2+S4 fusion heads")
    print("=" * 72)

    for name, val_path, gold_path in runs:
        val_p = Path(val_path)
        gold_p = Path(gold_path)
        if not val_p.exists() or not gold_p.exists():
            print(f"Skipping {name}: missing files")
            print(f"  val:  {val_p} exists={val_p.exists()}")
            print(f"  gold: {gold_p} exists={gold_p.exists()}")
            continue

        print(f"\nRun: {name}")
        res = evaluate_one_run(
            run_name=name,
            s2_val_rows=s2_val_rows,
            s2_gold_rows=s2_gold_rows,
            s4_val_path=val_p,
            s4_gold_path=gold_p,
            out_dir=args.out_dir,
            class_weight=class_weight,
            c_value=args.C,
        )
        summary["runs"][name] = res
        summary["ranking"].append({
            "run_name": name,
            "val_f1": res["val"]["overall"]["f1"],
            "val_auroc": res["val"]["overall"]["auroc"],
            "gold_f1": res["gold"]["overall"]["f1"],
            "gold_auroc": res["gold"]["overall"]["auroc"],
            "gold_auprc": res["gold"]["overall"]["auprc"],
            "gold_ece_10": res["gold"]["overall"]["ece_10"],
        })

        print("  threshold:", res["selected_threshold_from_val"])
        print("  coef:", res["logistic_regression"]["coef"], "intercept:", res["logistic_regression"]["intercept"])
        print("  VAL:", json.dumps(res["val"]["overall"], ensure_ascii=False))
        print("  GOLD:", json.dumps(res["gold"]["overall"], ensure_ascii=False))
        print("  GOLD slices:", json.dumps(res["gold"]["slices"]["question_type"], ensure_ascii=False))

    summary["ranking"] = sorted(
        summary["ranking"],
        key=lambda x: (x["val_f1"], x["val_auroc"], x["gold_f1"]),
        reverse=True,
    )

    save_json(args.out_dir / "metrics_summary.json", summary)

    print("\nFusion ranking by validation F1/AUROC")
    print("=" * 72)
    for r in summary["ranking"]:
        print(
            f"{r['run_name']}: "
            f"val_f1={r['val_f1']:.4f}, val_auroc={r['val_auroc']:.4f}, "
            f"gold_f1={r['gold_f1']:.4f}, gold_auroc={r['gold_auroc']:.4f}, "
            f"gold_auprc={r['gold_auprc']:.4f}"
        )

    print("\nWrote:")
    print(f"  {args.out_dir / 'metrics_summary.json'}")
    for name in summary["runs"]:
        print(f"  {args.out_dir / f'{name}_val_predictions.jsonl'}")
        print(f"  {args.out_dir / f'{name}_gold_predictions.jsonl'}")


if __name__ == "__main__":
    main()
