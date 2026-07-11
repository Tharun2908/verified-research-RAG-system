"""
bootstrap_grounded_hard_clustered.py

Question-clustered paired bootstrap confidence intervals for the frozen
grounded-hard binary evaluation.

The script uses existing saved predictions only. It does not retrain, refit,
or retune any model.

Models:
  - Signal 2
  - base SciFact/HealthVer S4
  - arXiv-ft SciFact/HealthVer S4
  - train-fitted S2 + base-S4 fusion
  - OOF-trained S2 + ft-S4 fusion

Bootstrap unit:
  qid (all sampled claims from one generated question move together)

Outputs:
  bootstrap_summary.json
  bootstrap_model_replicates.jsonl
  bootstrap_pairwise_replicates.jsonl

Example:
  python -u bootstrap_grounded_hard_clustered.py \
    --run-dir oof_fusion_scifact_healthver \
    --n-bootstrap 5000 \
    --seed 2908
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    precision_recall_fscore_support,
    roc_auc_score,
)


MODEL_ORDER = [
    "base_scifact_healthver",
    "fusion_base_scifact_trainfit",
    "ft_scifact_healthver",
    "fusion_ft_scifact_oof",
    "signal2",
]

PAIRWISE = [
    ("fusion_ft_scifact_oof", "base_scifact_healthver"),
    ("fusion_ft_scifact_oof", "ft_scifact_healthver"),
    ("fusion_base_scifact_trainfit", "base_scifact_healthver"),
    ("ft_scifact_healthver", "base_scifact_healthver"),
]

METRICS = ["accuracy", "precision", "recall", "f1", "auroc", "auprc"]


def read_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


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


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def row_key(row: dict[str, Any]) -> str:
    for key in ("row_key", "claim_id", "review_id"):
        value = row.get(key)
        if value is not None and str(value).strip():
            return str(value)
    raise KeyError(f"Could not identify row: keys={sorted(row.keys())}")


def binary_label(row: dict[str, Any]) -> int:
    name = str(row.get("final_label") or row.get("label_name") or "").upper()
    if name == "SUPPORTED":
        return 0
    if name == "UNSUPPORTED":
        return 1
    if row.get("label") is not None:
        return int(row["label"])
    raise ValueError(f"Non-binary row: {row_key(row)} label={name!r}")


def safe_auroc(y: np.ndarray, score: np.ndarray, weight: np.ndarray) -> float:
    if len(np.unique(y)) < 2:
        return float("nan")
    try:
        return float(roc_auc_score(y, score, sample_weight=weight))
    except Exception:
        return float("nan")


def safe_auprc(y: np.ndarray, score: np.ndarray, weight: np.ndarray) -> float:
    if len(np.unique(y)) < 2:
        return float("nan")
    try:
        return float(average_precision_score(y, score, sample_weight=weight))
    except Exception:
        return float("nan")


def compute_metrics(
    y: np.ndarray,
    score: np.ndarray,
    threshold: float,
    weight: np.ndarray,
) -> dict[str, float]:
    pred = (score >= threshold).astype(int)

    precision, recall, f1, _ = precision_recall_fscore_support(
        y,
        pred,
        average="binary",
        pos_label=1,
        zero_division=0,
        sample_weight=weight,
    )

    return {
        "accuracy": float(accuracy_score(y, pred, sample_weight=weight)),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "auroc": safe_auroc(y, score, weight),
        "auprc": safe_auprc(y, score, weight),
    }


def percentile_ci(values: list[float], level: float = 0.95) -> dict[str, Any]:
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    alpha = (1.0 - level) / 2.0

    if len(arr) == 0:
        return {
            "lower": None,
            "upper": None,
            "median": None,
            "mean": None,
            "valid_replicates": 0,
        }

    return {
        "lower": float(np.quantile(arr, alpha)),
        "upper": float(np.quantile(arr, 1.0 - alpha)),
        "median": float(np.median(arr)),
        "mean": float(np.mean(arr)),
        "valid_replicates": int(len(arr)),
    }


def cache_map(path: Path, score_field: str) -> dict[str, float]:
    result = {}
    for row in read_jsonl(path):
        result[row_key(row)] = float(row[score_field])
    return result


def fusion_map(path: Path) -> tuple[list[dict[str, Any]], dict[str, float]]:
    rows = read_jsonl(path)
    return rows, {
        row_key(row): float(row["fusion_prob_unsupported"])
        for row in rows
    }


def threshold_from_summary(summary: dict[str, Any], model: str) -> float:
    if model in {"signal2", "base_scifact_healthver", "ft_scifact_healthver"}:
        return float(
            summary["standalone"]["hard"][model]["weighted"]["threshold"]
        )

    if model == "fusion_base_scifact_trainfit":
        return float(
            summary["fusion_base_scifact_trainfit"]["selected_threshold_from_val"]
        )

    if model == "fusion_ft_scifact_oof":
        return float(
            summary["fusion_ft_scifact_oof"]["selected_threshold_from_val"]
        )

    raise KeyError(model)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--run-dir",
        type=Path,
        default=Path("oof_fusion_scifact_healthver"),
    )
    ap.add_argument("--n-bootstrap", type=int, default=5000)
    ap.add_argument("--seed", type=int, default=2908)
    ap.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Default: <run-dir>/bootstrap_grounded_hard",
    )
    args = ap.parse_args()

    run_dir = args.run_dir
    out_dir = args.out_dir or (run_dir / "bootstrap_grounded_hard")
    out_dir.mkdir(parents=True, exist_ok=True)

    summary = read_json(run_dir / "metrics_summary.json")

    master_rows, fusion_ft_scores = fusion_map(
        run_dir / "fusion_ft_scifact_oof_hard_predictions.jsonl"
    )
    _, fusion_base_scores = fusion_map(
        run_dir / "fusion_base_scifact_trainfit_hard_predictions.jsonl"
    )

    base_scores = cache_map(
        run_dir / "score_cache" / "base_s4_hard.jsonl",
        "base_s4_prob_unsupported",
    )
    ft_scores = cache_map(
        run_dir / "score_cache" / "ft_s4_hard.jsonl",
        "ft_s4_prob_unsupported",
    )
    s2_scores = cache_map(
        run_dir / "score_cache" / "s2_hard.jsonl",
        "s2_unsupported_score",
    )

    score_maps = {
        "signal2": s2_scores,
        "base_scifact_healthver": base_scores,
        "ft_scifact_healthver": ft_scores,
        "fusion_base_scifact_trainfit": fusion_base_scores,
        "fusion_ft_scifact_oof": fusion_ft_scores,
    }

    keys = [row_key(row) for row in master_rows]
    missing = {
        model: [key for key in keys if key not in score_map]
        for model, score_map in score_maps.items()
    }
    missing = {model: vals for model, vals in missing.items() if vals}
    if missing:
        raise SystemExit(
            "Missing prediction rows: "
            + json.dumps(
                {model: vals[:10] for model, vals in missing.items()},
                indent=2,
            )
        )

    y = np.asarray([binary_label(row) for row in master_rows], dtype=int)
    weights = np.asarray(
        [float(row.get("sampling_weight") or 1.0) for row in master_rows],
        dtype=float,
    )
    qids = np.asarray(
        [str(row.get("qid") or row.get("group_id") or row_key(row)) for row in master_rows]
    )

    scores = {
        model: np.asarray([score_map[key] for key in keys], dtype=float)
        for model, score_map in score_maps.items()
    }
    thresholds = {
        model: threshold_from_summary(summary, model)
        for model in MODEL_ORDER
    }

    unique_qids = np.asarray(sorted(set(qids.tolist())))
    qid_to_indices: dict[str, np.ndarray] = {
        qid: np.where(qids == qid)[0]
        for qid in unique_qids
    }

    qids_with_unsupported = sorted(
        {
            qid
            for qid, idx in qid_to_indices.items()
            if np.any(y[idx] == 1)
        }
    )

    print("\nQuestion-clustered grounded-hard bootstrap")
    print("=" * 76)
    print(f"Binary claims:             {len(master_rows)}")
    print(f"Unique qids:               {len(unique_qids)}")
    print(f"Qids with unsupported:     {len(qids_with_unsupported)}")
    print(f"Raw unsupported claims:    {int((y == 1).sum())}")
    print(f"Weighted unsupported mass: {float(weights[y == 1].sum()):.4f}")
    print(f"Bootstrap replicates:      {args.n_bootstrap}")

    point_estimates = {
        model: compute_metrics(
            y,
            scores[model],
            thresholds[model],
            weights,
        )
        for model in MODEL_ORDER
    }

    rng = np.random.default_rng(args.seed)
    model_replicates: list[dict[str, Any]] = []
    pairwise_replicates: list[dict[str, Any]] = []

    collected: dict[str, dict[str, list[float]]] = {
        model: {metric: [] for metric in METRICS}
        for model in MODEL_ORDER
    }
    differences: dict[str, dict[str, list[float]]] = {
        f"{left}_minus_{right}": {metric: [] for metric in METRICS}
        for left, right in PAIRWISE
    }

    for replicate in range(args.n_bootstrap):
        sampled_qids = rng.choice(
            unique_qids,
            size=len(unique_qids),
            replace=True,
        )
        sampled_indices = np.concatenate(
            [qid_to_indices[str(qid)] for qid in sampled_qids]
        )

        y_b = y[sampled_indices]
        w_b = weights[sampled_indices]

        replicate_metrics: dict[str, dict[str, float]] = {}

        for model in MODEL_ORDER:
            values = compute_metrics(
                y_b,
                scores[model][sampled_indices],
                thresholds[model],
                w_b,
            )
            replicate_metrics[model] = values

            record = {
                "replicate": replicate,
                "model": model,
                **values,
            }
            model_replicates.append(record)

            for metric in METRICS:
                collected[model][metric].append(values[metric])

        for left, right in PAIRWISE:
            pair_name = f"{left}_minus_{right}"
            diff_row = {
                "replicate": replicate,
                "comparison": pair_name,
            }
            for metric in METRICS:
                value = (
                    replicate_metrics[left][metric]
                    - replicate_metrics[right][metric]
                )
                diff_row[metric] = value
                differences[pair_name][metric].append(value)
            pairwise_replicates.append(diff_row)

        if (replicate + 1) % 500 == 0:
            print(f"Completed {replicate + 1}/{args.n_bootstrap}", flush=True)

    model_intervals = {}
    for model in MODEL_ORDER:
        model_intervals[model] = {
            "point_estimate": point_estimates[model],
            "bootstrap_95_percentile_ci": {
                metric: percentile_ci(collected[model][metric])
                for metric in METRICS
            },
            "threshold_fixed_from_val": thresholds[model],
        }

    pairwise_intervals = {}
    for left, right in PAIRWISE:
        name = f"{left}_minus_{right}"
        pairwise_intervals[name] = {}

        for metric in METRICS:
            vals = np.asarray(differences[name][metric], dtype=float)
            finite = vals[np.isfinite(vals)]
            ci = percentile_ci(finite.tolist())

            pairwise_intervals[name][metric] = {
                **ci,
                "point_difference": float(
                    point_estimates[left][metric]
                    - point_estimates[right][metric]
                ),
                "probability_difference_gt_zero": (
                    float(np.mean(finite > 0))
                    if len(finite)
                    else None
                ),
                "probability_difference_lt_zero": (
                    float(np.mean(finite < 0))
                    if len(finite)
                    else None
                ),
            }

    output = {
        "protocol": {
            "evaluation_set": "grounded-hard binary rows only",
            "excluded_labels": ["ABSTENTION", "INVALID_EXTRACTION"],
            "bootstrap_unit": "qid",
            "paired_bootstrap": True,
            "design_sampling_weights_used": True,
            "thresholds_refit_in_bootstrap": False,
            "model_parameters_refit_in_bootstrap": False,
            "n_bootstrap": args.n_bootstrap,
            "seed": args.seed,
            "ci": "95% percentile cluster bootstrap",
            "caveat": (
                "Approximate uncertainty interval: the human review used a "
                "stratified claim sample, while the bootstrap resamples question "
                "clusters and retains the original design weights."
            ),
        },
        "data": {
            "binary_claims": len(master_rows),
            "unique_qids": len(unique_qids),
            "qids_with_at_least_one_unsupported_claim": len(qids_with_unsupported),
            "raw_supported_claims": int((y == 0).sum()),
            "raw_unsupported_claims": int((y == 1).sum()),
            "weighted_supported_mass": float(weights[y == 0].sum()),
            "weighted_unsupported_mass": float(weights[y == 1].sum()),
        },
        "models": model_intervals,
        "pairwise_differences": pairwise_intervals,
    }

    write_json(out_dir / "bootstrap_summary.json", output)
    write_jsonl(
        out_dir / "bootstrap_model_replicates.jsonl",
        model_replicates,
    )
    write_jsonl(
        out_dir / "bootstrap_pairwise_replicates.jsonl",
        pairwise_replicates,
    )

    print("\nModel confidence intervals")
    print("=" * 76)
    for model in MODEL_ORDER:
        point = point_estimates[model]
        f1_ci = model_intervals[model]["bootstrap_95_percentile_ci"]["f1"]
        auc_ci = model_intervals[model]["bootstrap_95_percentile_ci"]["auroc"]
        print(
            f"{model:<36} "
            f"F1={point['f1']:.4f} "
            f"[{f1_ci['lower']:.4f}, {f1_ci['upper']:.4f}]  "
            f"AUROC={point['auroc']:.4f} "
            f"[{auc_ci['lower']:.4f}, {auc_ci['upper']:.4f}]"
        )

    print("\nPaired F1 differences")
    print("=" * 76)
    for left, right in PAIRWISE:
        name = f"{left}_minus_{right}"
        result = pairwise_intervals[name]["f1"]
        print(
            f"{name:<70} "
            f"diff={result['point_difference']:.4f} "
            f"[{result['lower']:.4f}, {result['upper']:.4f}] "
            f"P(diff>0)={result['probability_difference_gt_zero']:.3f}"
        )

    print("\nWrote:")
    print(f"  {out_dir / 'bootstrap_summary.json'}")
    print(f"  {out_dir / 'bootstrap_model_replicates.jsonl'}")
    print(f"  {out_dir / 'bootstrap_pairwise_replicates.jsonl'}")


if __name__ == "__main__":
    main()
