#!/usr/bin/env python3
"""
Evaluate an uncertainty-routed DeBERTa -> MiniCheck-7B cascade on grounded-hard.

This script DOES NOT run either model. It reuses the committed predictions:
  - deployed SciFact/HealthVer DeBERTa predictions/scores
  - Bespoke-MiniCheck-7B predictions

Routing rule:
  1. DeBERTa always runs first.
  2. Its frozen validation threshold is 0.06 for P(unsupported).
  3. Uncertainty = absolute distance from that threshold:
         margin = abs(P_unsupported - 0.06)
     Smaller margin = more uncertain.
  4. Escalate the lowest-margin X% of claims to MiniCheck.
  5. Use MiniCheck's binary decision for escalated claims; otherwise keep DeBERTa's decision.

Important:
- This is an EXPLORATORY post-hoc quality/cost curve on grounded-hard.
- Escalation percentages are NOT a validated deployment policy.
- No human labels are used to choose which individual claims are escalated.
- SUPPORTED/UNSUPPORTED only; abstentions remain excluded.
- Metrics use the original sampling weights.
- Binary F1 treats UNSUPPORTED as the positive class.
- Bootstrap resamples whole qid clusters and keeps the routing membership fixed.

Run from repository root:
    python verifier_study/3_gold_and_eval/eval_minicheck_cascade.py

Outputs:
    backend/data/grounded_hard_eval/minicheck_cascade_summary.json
    backend/data/grounded_hard_eval/minicheck_cascade_curve.csv
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

DATA = Path("backend/data/grounded_hard_eval")
INPUT = DATA / "minicheck_7b_predictions.jsonl"
OUT_JSON = DATA / "minicheck_cascade_summary.json"
OUT_CSV = DATA / "minicheck_cascade_curve.csv"

BASE_THRESHOLD = 0.06
DEFAULT_RATES = [0, 5, 10, 20, 30, 40, 50, 75, 100]
N_BOOT = 5000
SEED = 2908


def load_jsonl(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def as_binary(value) -> int | None:
    """Return 1=UNSUPPORTED, 0=SUPPORTED, None=excluded."""
    if value is None:
        return None
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return int(value)
    s = str(value).strip().upper()
    if s in {"UNSUPPORTED", "1", "TRUE"}:
        return 1
    if s in {"SUPPORTED", "0", "FALSE"}:
        return 0
    return None


def binary_metrics(y: np.ndarray, pred: np.ndarray, w: np.ndarray) -> dict:
    tp = float(w[(pred == 1) & (y == 1)].sum())
    fp = float(w[(pred == 1) & (y == 0)].sum())
    fn = float(w[(pred == 0) & (y == 1)].sum())
    tn = float(w[(pred == 0) & (y == 0)].sum())
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2.0 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "weighted_tp": tp,
        "weighted_fp": fp,
        "weighted_fn": fn,
        "weighted_tn": tn,
    }


def f1_only(y: np.ndarray, pred: np.ndarray, w: np.ndarray) -> float:
    return binary_metrics(y, pred, w)["f1"]


def parse_rates(text: str) -> list[int]:
    rates = []
    for part in text.split(","):
        value = int(part.strip())
        if value < 0 or value > 100:
            raise argparse.ArgumentTypeError("Escalation rates must be between 0 and 100.")
        rates.append(value)
    rates = sorted(set(rates))
    if 0 not in rates:
        rates.insert(0, 0)
    if 100 not in rates:
        rates.append(100)
    return rates


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--rates",
        default=",".join(str(x) for x in DEFAULT_RATES),
        help="Comma-separated escalation percentages. Default: 0,5,10,20,30,40,50,75,100",
    )
    ap.add_argument("--n-boot", type=int, default=N_BOOT)
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args()

    rates = parse_rates(args.rates)

    if not INPUT.exists():
        raise SystemExit(
            f"Missing {INPUT}\n"
            "Run eval_minicheck_grounded_hard.py first and copy/commit its predictions."
        )

    source = load_jsonl(INPUT)
    rows = []

    for r in source:
        y = as_binary(r.get("human_final_label"))
        base_pred = as_binary(r.get("base_scifact_healthver_pred"))
        mc_pred = as_binary(r.get("minicheck_7b_pred"))
        if y is None or base_pred is None or mc_pred is None:
            continue
        base_score = r.get("base_scifact_healthver_score")
        if base_score is None:
            continue
        rows.append({
            "claim_id": str(r["claim_id"]),
            "qid": str(r["qid"]),
            "y": y,
            "w": float(r.get("sampling_weight", 1.0)),
            "base_score": float(base_score),
            "base_pred": base_pred,
            "mc_pred": mc_pred,
        })

    if not rows:
        raise SystemExit("No eligible binary rows found.")

    n = len(rows)
    y = np.asarray([r["y"] for r in rows], dtype=int)
    w = np.asarray([r["w"] for r in rows], dtype=float)
    base_score = np.asarray([r["base_score"] for r in rows], dtype=float)
    base_pred = np.asarray([r["base_pred"] for r in rows], dtype=int)
    mc_pred = np.asarray([r["mc_pred"] for r in rows], dtype=int)
    qids = np.asarray([r["qid"] for r in rows], dtype=object)

    recomputed_base_pred = (base_score >= BASE_THRESHOLD).astype(int)
    mismatches = np.where(recomputed_base_pred != base_pred)[0]
    if len(mismatches):
        examples = [rows[int(i)]["claim_id"] for i in mismatches[:10]]
        raise SystemExit(
            f"{len(mismatches)} base predictions do not match threshold {BASE_THRESHOLD}. "
            f"Examples: {examples}. Refusing to route with an inconsistent threshold."
        )

    margins = np.abs(base_score - BASE_THRESHOLD)
    order = sorted(range(n), key=lambda i: (float(margins[i]), rows[i]["claim_id"]))

    base_metrics = binary_metrics(y, base_pred, w)
    mc_metrics = binary_metrics(y, mc_pred, w)

    routing = {}
    point_estimates = {}

    for rate in rates:
        k = int(round(n * rate / 100.0))
        k = min(max(k, 0), n)
        mask = np.zeros(n, dtype=bool)
        if k:
            mask[np.asarray(order[:k], dtype=int)] = True
        cascade_pred = base_pred.copy()
        cascade_pred[mask] = mc_pred[mask]
        metrics = binary_metrics(y, cascade_pred, w)
        metrics.update({
            "requested_escalation_pct": rate,
            "escalated_claims": int(mask.sum()),
            "actual_escalation_pct": float(mask.mean() * 100.0),
            "minicheck_calls_per_100_claims": float(mask.mean() * 100.0),
            "f1_gain_vs_base": float(metrics["f1"] - base_metrics["f1"]),
            "f1_gap_vs_minicheck": float(metrics["f1"] - mc_metrics["f1"]),
        })
        routing[rate] = {"mask": mask, "pred": cascade_pred}
        point_estimates[rate] = metrics

    by_q: dict[str, np.ndarray] = {}
    for qid in sorted(set(qids.tolist())):
        by_q[qid] = np.where(qids == qid)[0]
    q_list = sorted(by_q)

    rng = np.random.default_rng(args.seed)
    boot_f1 = {rate: [] for rate in rates}
    boot_gain_vs_base = {rate: [] for rate in rates}
    boot_gap_vs_mc = {rate: [] for rate in rates}

    valid = 0
    for _ in range(args.n_boot):
        picked = rng.choice(len(q_list), size=len(q_list), replace=True)
        idx = np.concatenate([by_q[q_list[int(j)]] for j in picked])
        yy = y[idx]
        ww = w[idx]
        if yy.sum() == 0:
            continue
        valid += 1
        base_f1 = f1_only(yy, base_pred[idx], ww)
        mc_f1 = f1_only(yy, mc_pred[idx], ww)
        for rate in rates:
            cascade_f1 = f1_only(yy, routing[rate]["pred"][idx], ww)
            boot_f1[rate].append(cascade_f1)
            boot_gain_vs_base[rate].append(cascade_f1 - base_f1)
            boot_gap_vs_mc[rate].append(cascade_f1 - mc_f1)

    results = []
    for rate in rates:
        f1_arr = np.asarray(boot_f1[rate], dtype=float)
        gain_arr = np.asarray(boot_gain_vs_base[rate], dtype=float)
        gap_arr = np.asarray(boot_gap_vs_mc[rate], dtype=float)
        f1_ci = np.percentile(f1_arr, [2.5, 97.5])
        gain_ci = np.percentile(gain_arr, [2.5, 97.5])
        gap_ci = np.percentile(gap_arr, [2.5, 97.5])
        row = {
            **point_estimates[rate],
            "f1_95_ci": [float(f1_ci[0]), float(f1_ci[1])],
            "gain_vs_base_95_ci": [float(gain_ci[0]), float(gain_ci[1])],
            "gap_vs_minicheck_95_ci": [float(gap_ci[0]), float(gap_ci[1])],
        }
        results.append(row)

    summary = {
        "protocol": {
            "evaluation_set": "grounded-hard human-reviewed binary claims",
            "binary_positive_class": "UNSUPPORTED",
            "routing": "escalate smallest abs(base_prob_unsupported - frozen_base_threshold)",
            "base_threshold": BASE_THRESHOLD,
            "routing_uses_human_labels": False,
            "design_sampling_weights_used": True,
            "bootstrap_unit": "qid",
            "paired_cluster_bootstrap": True,
            "n_boot": args.n_boot,
            "valid_bootstrap_replicates": valid,
            "seed": args.seed,
            "important_caveat": (
                "The escalation percentages define a post-hoc quality/cost curve on this "
                "stress test. They are not a validated deployment policy. A production "
                "routing margin should be selected on independent validation data."
            ),
        },
        "sample": {
            "binary_claims": int(n),
            "supported_claims": int((y == 0).sum()),
            "unsupported_claims": int((y == 1).sum()),
            "question_clusters": int(len(q_list)),
        },
        "endpoints": {
            "deberta_only": base_metrics,
            "minicheck_only": mc_metrics,
        },
        "curve": results,
    }

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    csv_fields = [
        "requested_escalation_pct", "escalated_claims", "actual_escalation_pct",
        "precision", "recall", "f1", "f1_gain_vs_base", "f1_gap_vs_minicheck",
        "f1_ci_low", "f1_ci_high", "gain_vs_base_ci_low", "gain_vs_base_ci_high",
        "gap_vs_minicheck_ci_low", "gap_vs_minicheck_ci_high",
    ]

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields)
        writer.writeheader()
        for r in results:
            writer.writerow({
                "requested_escalation_pct": r["requested_escalation_pct"],
                "escalated_claims": r["escalated_claims"],
                "actual_escalation_pct": r["actual_escalation_pct"],
                "precision": r["precision"],
                "recall": r["recall"],
                "f1": r["f1"],
                "f1_gain_vs_base": r["f1_gain_vs_base"],
                "f1_gap_vs_minicheck": r["f1_gap_vs_minicheck"],
                "f1_ci_low": r["f1_95_ci"][0],
                "f1_ci_high": r["f1_95_ci"][1],
                "gain_vs_base_ci_low": r["gain_vs_base_95_ci"][0],
                "gain_vs_base_ci_high": r["gain_vs_base_95_ci"][1],
                "gap_vs_minicheck_ci_low": r["gap_vs_minicheck_95_ci"][0],
                "gap_vs_minicheck_ci_high": r["gap_vs_minicheck_95_ci"][1],
            })

    print("\nGrounded-hard DeBERTa -> MiniCheck cascade")
    print("=" * 86)
    print(f"Binary claims: {n}  unsupported: {int(y.sum())}  qid clusters: {len(q_list)}")
    print(f"Frozen DeBERTa threshold: {BASE_THRESHOLD:.2f}")
    print("Routing: smallest absolute margin to threshold escalated first\n")
    print(f"{'Esc %':>6} {'N':>4} {'Precision':>10} {'Recall':>9} {'F1':>9} {'Δ vs base':>11} {'Δ vs MC':>10}")
    print("-" * 86)
    for r in results:
        print(
            f"{r['actual_escalation_pct']:6.1f} {r['escalated_claims']:4d} "
            f"{r['precision']:10.4f} {r['recall']:9.4f} {r['f1']:9.4f} "
            f"{r['f1_gain_vs_base']:+11.4f} {r['f1_gap_vs_minicheck']:+10.4f}"
        )

    print("\nEndpoints")
    print(f"DeBERTa-only: P={base_metrics['precision']:.4f} R={base_metrics['recall']:.4f} F1={base_metrics['f1']:.4f}")
    print(f"MiniCheck-only: P={mc_metrics['precision']:.4f} R={mc_metrics['recall']:.4f} F1={mc_metrics['f1']:.4f}")
    print(f"\nSaved: {OUT_JSON}")
    print(f"Saved: {OUT_CSV}")


if __name__ == "__main__":
    main()
