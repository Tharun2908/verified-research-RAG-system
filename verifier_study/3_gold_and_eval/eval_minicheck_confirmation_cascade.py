#!/usr/bin/env python3
"""
Evaluate a confirmation cascade on the existing grounded-hard predictions.

Policy:
    1. Run DeBERTa first.
    2. If DeBERTa predicts SUPPORTED -> accept SUPPORTED.
    3. If DeBERTa predicts UNSUPPORTED -> escalate to MiniCheck-7B.
    4. Use MiniCheck's final binary decision for escalated claims.

This script does NOT run either model. It reuses:
    backend/data/grounded_hard_eval/minicheck_7b_predictions.jsonl

Run from repository root:
    python verifier_study/3_gold_and_eval/eval_minicheck_confirmation_cascade.py

Outputs:
    backend/data/grounded_hard_eval/minicheck_confirmation_cascade_summary.json

Metrics:
- human-reviewed SUPPORTED/UNSUPPORTED claims only
- UNSUPPORTED is the positive class
- original sampling weights retained
- paired question-clustered bootstrap over qid
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


DATA = Path("backend/data/grounded_hard_eval")
INPUT = DATA / "minicheck_7b_predictions.jsonl"
OUTPUT = DATA / "minicheck_confirmation_cascade_summary.json"

N_BOOT = 5000
SEED = 2908


def load_jsonl(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def as_binary(value) -> int | None:
    """1 = UNSUPPORTED, 0 = SUPPORTED."""
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


def metrics(y: np.ndarray, pred: np.ndarray, w: np.ndarray) -> dict:
    tp = float(w[(pred == 1) & (y == 1)].sum())
    fp = float(w[(pred == 1) & (y == 0)].sum())
    fn = float(w[(pred == 0) & (y == 1)].sum())
    tn = float(w[(pred == 0) & (y == 0)].sum())

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall
        else 0.0
    )

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
    return metrics(y, pred, w)["f1"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-boot", type=int, default=N_BOOT)
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args()

    if not INPUT.exists():
        raise SystemExit(
            f"Missing {INPUT}\n"
            "Run eval_minicheck_grounded_hard.py first."
        )

    source = load_jsonl(INPUT)

    rows = []
    for r in source:
        y = as_binary(r.get("human_final_label"))
        base = as_binary(r.get("base_scifact_healthver_pred"))
        mc = as_binary(r.get("minicheck_7b_pred"))

        if y is None or base is None or mc is None:
            continue

        rows.append(
            {
                "claim_id": str(r["claim_id"]),
                "qid": str(r["qid"]),
                "y": y,
                "w": float(r.get("sampling_weight", 1.0)),
                "base": base,
                "mc": mc,
            }
        )

    if not rows:
        raise SystemExit("No eligible binary claims found.")

    y = np.asarray([r["y"] for r in rows], dtype=int)
    w = np.asarray([r["w"] for r in rows], dtype=float)
    base = np.asarray([r["base"] for r in rows], dtype=int)
    mc = np.asarray([r["mc"] for r in rows], dtype=int)
    qids = np.asarray([r["qid"] for r in rows], dtype=object)

    # Confirmation cascade:
    # DeBERTa SUPPORTED (0) -> keep 0
    # DeBERTa UNSUPPORTED (1) -> replace with MiniCheck decision
    cascade = base.copy()
    escalated = base == 1
    cascade[escalated] = mc[escalated]

    base_m = metrics(y, base, w)
    mc_m = metrics(y, mc, w)
    cascade_m = metrics(y, cascade, w)

    # Raw and weighted escalation rates.
    raw_escalation = float(escalated.mean())
    weighted_escalation = float(w[escalated].sum() / w.sum())

    # How MiniCheck changed DeBERTa's rejected claims.
    n_escalated = int(escalated.sum())
    n_confirmed_unsupported = int(np.sum(escalated & (mc == 1)))
    n_overruled_to_supported = int(np.sum(escalated & (mc == 0)))

    # Cluster bootstrap.
    by_q: dict[str, np.ndarray] = {}
    for q in sorted(set(qids.tolist())):
        by_q[q] = np.where(qids == q)[0]
    q_list = sorted(by_q)

    rng = np.random.default_rng(args.seed)

    cascade_f1_boot = []
    diff_vs_base_boot = []
    diff_vs_mc_boot = []

    valid = 0

    for _ in range(args.n_boot):
        picked = rng.choice(len(q_list), size=len(q_list), replace=True)
        idx = np.concatenate([by_q[q_list[int(j)]] for j in picked])

        yy = y[idx]
        ww = w[idx]
        if yy.sum() == 0:
            continue

        valid += 1

        f_base = f1_only(yy, base[idx], ww)
        f_mc = f1_only(yy, mc[idx], ww)
        f_cascade = f1_only(yy, cascade[idx], ww)

        cascade_f1_boot.append(f_cascade)
        diff_vs_base_boot.append(f_cascade - f_base)
        diff_vs_mc_boot.append(f_cascade - f_mc)

    cascade_f1_boot = np.asarray(cascade_f1_boot)
    diff_vs_base_boot = np.asarray(diff_vs_base_boot)
    diff_vs_mc_boot = np.asarray(diff_vs_mc_boot)

    cascade_ci = np.percentile(cascade_f1_boot, [2.5, 97.5])
    base_diff_ci = np.percentile(diff_vs_base_boot, [2.5, 97.5])
    mc_diff_ci = np.percentile(diff_vs_mc_boot, [2.5, 97.5])

    summary = {
        "protocol": {
            "policy": (
                "DeBERTa SUPPORTED -> accept; "
                "DeBERTa UNSUPPORTED -> MiniCheck final decision"
            ),
            "binary_positive_class": "UNSUPPORTED",
            "weight_field": "sampling_weight",
            "cluster_field": "qid",
            "paired_cluster_bootstrap": True,
            "n_boot": args.n_boot,
            "valid_bootstrap_replicates": valid,
            "seed": args.seed,
        },
        "sample": {
            "binary_claims": int(len(rows)),
            "supported_claims": int((y == 0).sum()),
            "unsupported_claims": int((y == 1).sum()),
            "question_clusters": int(len(q_list)),
        },
        "escalation": {
            "claims_sent_to_minicheck": n_escalated,
            "raw_escalation_fraction": raw_escalation,
            "raw_escalation_percent": raw_escalation * 100.0,
            "weighted_escalation_fraction": weighted_escalation,
            "weighted_escalation_percent": weighted_escalation * 100.0,
            "minicheck_confirmed_unsupported": n_confirmed_unsupported,
            "minicheck_overruled_to_supported": n_overruled_to_supported,
        },
        "deberta_only": base_m,
        "minicheck_only": mc_m,
        "confirmation_cascade": {
            **cascade_m,
            "f1_95_ci": [
                float(cascade_ci[0]),
                float(cascade_ci[1]),
            ],
            "f1_difference_vs_deberta": float(cascade_m["f1"] - base_m["f1"]),
            "difference_vs_deberta_95_ci": [
                float(base_diff_ci[0]),
                float(base_diff_ci[1]),
            ],
            "f1_difference_vs_minicheck": float(cascade_m["f1"] - mc_m["f1"]),
            "difference_vs_minicheck_95_ci": [
                float(mc_diff_ci[0]),
                float(mc_diff_ci[1]),
            ],
        },
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("\nGrounded-hard confirmation cascade")
    print("=" * 76)
    print(f"Binary claims: {len(rows)}")
    print(f"Unsupported:   {int((y == 1).sum())}")
    print(f"QID clusters:  {len(q_list)}")
    print()
    print(
        f"MiniCheck escalation: {n_escalated}/{len(rows)} "
        f"({100*raw_escalation:.1f}% raw claims)"
    )
    print(
        f"Within escalated claims: MiniCheck kept "
        f"{n_confirmed_unsupported} unsupported and overruled "
        f"{n_overruled_to_supported} to supported."
    )
    print()
    print("Results")
    print("-" * 76)
    print(
        f"DeBERTa-only        P={base_m['precision']:.4f} "
        f"R={base_m['recall']:.4f} F1={base_m['f1']:.4f}"
    )
    print(
        f"MiniCheck-only      P={mc_m['precision']:.4f} "
        f"R={mc_m['recall']:.4f} F1={mc_m['f1']:.4f}"
    )
    print(
        f"Confirmation cascade P={cascade_m['precision']:.4f} "
        f"R={cascade_m['recall']:.4f} F1={cascade_m['f1']:.4f}"
    )
    print()
    print(
        f"ΔF1 vs DeBERTa: "
        f"{cascade_m['f1'] - base_m['f1']:+.4f} "
        f"95% CI [{base_diff_ci[0]:+.4f}, {base_diff_ci[1]:+.4f}]"
    )
    print(
        f"ΔF1 vs MiniCheck: "
        f"{cascade_m['f1'] - mc_m['f1']:+.4f} "
        f"95% CI [{mc_diff_ci[0]:+.4f}, {mc_diff_ci[1]:+.4f}]"
    )
    print()
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    main()
