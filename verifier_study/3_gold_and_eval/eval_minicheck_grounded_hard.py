#!/usr/bin/env python3
"""
Evaluate Bespoke-MiniCheck-7B on the existing human-reviewed grounded-hard set.

Run from the repository root.

Install in a CUDA/Linux environment:
    pip install "minicheck[llm] @ git+https://github.com/Liyan06/MiniCheck.git@main"
    pip install scikit-learn

Example:
    CUDA_VISIBLE_DEVICES=0 python verifier_study/3_gold_and_eval/eval_minicheck_grounded_hard.py

Inputs:
    backend/data/grounded_hard_eval/binary_predictions.jsonl

Outputs:
    backend/data/grounded_hard_eval/minicheck_7b_predictions.jsonl
    backend/data/grounded_hard_eval/minicheck_7b_summary.json

Protocol:
- Same human-reviewed binary claims as the existing grounded-hard comparison.
- SUPPORTED/UNSUPPORTED only; abstentions are excluded.
- Same sampling weights.
- Binary F1 treats UNSUPPORTED as the positive class.
- AUROC uses P(unsupported) = 1 - MiniCheck support probability.
- Paired question-clustered bootstrap compares MiniCheck against the deployed
  SciFact/HealthVer DeBERTa on exactly the same claims.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_auc_score

from minicheck.minicheck import MiniCheck


DATA = Path("backend/data/grounded_hard_eval")
INPUT = DATA / "binary_predictions.jsonl"
OUT_PRED = DATA / "minicheck_7b_predictions.jsonl"
OUT_SUMMARY = DATA / "minicheck_7b_summary.json"

N_BOOT = 5000
SEED = 2908


def load_jsonl(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def as_binary(value) -> int | None:
    """Return 1=UNSUPPORTED, 0=SUPPORTED, None=excluded."""
    if value is None:
        return None
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
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall)
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
    return binary_metrics(y, pred, w)["f1"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-boot", type=int, default=N_BOOT)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--cache-dir", default="./ckpts")
    args = ap.parse_args()

    if not INPUT.exists():
        raise SystemExit(f"Missing {INPUT}. Run this script from the repository root.")

    source_rows = load_jsonl(INPUT)

    rows = []
    for r in source_rows:
        y = as_binary(r.get("human_final_label"))
        base_pred = as_binary(r.get("base_scifact_healthver_pred"))
        claim = r.get("claim")
        evidence = r.get("evidence_text_for_verifier")

        if y is None or base_pred is None or not claim or not evidence:
            continue

        rows.append(
            {
                "source": r,
                "claim_id": r["claim_id"],
                "qid": str(r["qid"]),
                "claim": claim,
                "evidence": evidence,
                "y": y,
                "weight": float(r.get("sampling_weight", 1.0)),
                "base_pred": base_pred,
                "base_score": float(r.get("base_scifact_healthver_score", 0.0)),
            }
        )

    if not rows:
        raise SystemExit("No eligible human-reviewed binary claims found.")

    print(
        f"Evaluating {len(rows)} claims "
        f"({sum(r['y'] for r in rows)} unsupported) with Bespoke-MiniCheck-7B..."
    )

    # Official MiniCheck convention:
    # pred_label: 1=SUPPORTED, 0=UNSUPPORTED
    # raw_prob: probability/support score for SUPPORTED.
    scorer = MiniCheck(
        model_name="Bespoke-MiniCheck-7B",
        enable_prefix_caching=False,
        cache_dir=args.cache_dir,
    )

    docs = [r["evidence"] for r in rows]
    claims = [r["claim"] for r in rows]

    pred_supported, support_prob, _, _ = scorer.score(
        docs=docs,
        claims=claims,
    )

    if len(pred_supported) != len(rows) or len(support_prob) != len(rows):
        raise RuntimeError("MiniCheck returned an unexpected number of predictions.")

    out_rows = []
    for r, p_sup, p_support in zip(rows, pred_supported, support_prob):
        unsupported_pred = 1 - int(p_sup)
        unsupported_score = 1.0 - float(p_support)

        out = dict(r["source"])
        out["minicheck_7b_support_score"] = float(p_support)
        out["minicheck_7b_unsupported_score"] = unsupported_score
        out["minicheck_7b_pred"] = unsupported_pred
        out["minicheck_7b_pred_label"] = (
            "UNSUPPORTED" if unsupported_pred == 1 else "SUPPORTED"
        )
        out_rows.append(out)

    with open(OUT_PRED, "w", encoding="utf-8") as f:
        for r in out_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    y = np.array([r["y"] for r in rows], dtype=int)
    w = np.array([r["weight"] for r in rows], dtype=float)
    base_pred = np.array([r["base_pred"] for r in rows], dtype=int)
    mc_pred = np.array([r["minicheck_7b_pred"] for r in out_rows], dtype=int)
    mc_score = np.array(
        [r["minicheck_7b_unsupported_score"] for r in out_rows], dtype=float
    )
    qids = [r["qid"] for r in rows]

    base = binary_metrics(y, base_pred, w)
    minicheck = binary_metrics(y, mc_pred, w)
    minicheck["auroc"] = float(roc_auc_score(y, mc_score, sample_weight=w))

    diff = minicheck["f1"] - base["f1"]

    # Paired question-clustered bootstrap.
    by_q: dict[str, list[int]] = defaultdict(list)
    for i, qid in enumerate(qids):
        by_q[qid].append(i)
    q_list = sorted(by_q)

    rng = np.random.default_rng(args.seed)
    f1_diffs = []
    mc_f1_boot = []

    for _ in range(args.n_boot):
        picked = rng.choice(len(q_list), size=len(q_list), replace=True)
        idx = [i for j in picked for i in by_q[q_list[j]]]

        yy = y[idx]
        ww = w[idx]
        if yy.sum() == 0:
            continue

        base_f1 = f1_only(yy, base_pred[idx], ww)
        mc_f1 = f1_only(yy, mc_pred[idx], ww)

        mc_f1_boot.append(mc_f1)
        f1_diffs.append(mc_f1 - base_f1)

    f1_diffs = np.asarray(f1_diffs, dtype=float)
    mc_f1_boot = np.asarray(mc_f1_boot, dtype=float)

    diff_ci = np.percentile(f1_diffs, [2.5, 97.5])
    mc_ci = np.percentile(mc_f1_boot, [2.5, 97.5])

    summary = {
        "model": "Bespoke-MiniCheck-7B",
        "protocol": {
            "binary_positive_class": "UNSUPPORTED",
            "human_label_field": "human_final_label",
            "weight_field": "sampling_weight",
            "cluster_field": "qid",
            "n_boot": args.n_boot,
            "seed": args.seed,
            "prefix_caching": False,
        },
        "sample": {
            "binary_claims": int(len(rows)),
            "unsupported_claims": int(y.sum()),
            "supported_claims": int((y == 0).sum()),
            "question_clusters": int(len(set(qids))),
            "question_clusters_with_unsupported": int(
                len({q for q, yy in zip(qids, y) if yy == 1})
            ),
        },
        "deployed_base": base,
        "minicheck_7b": minicheck,
        "bootstrap": {
            "valid_replicates": int(len(f1_diffs)),
            "minicheck_f1_95_ci": [float(mc_ci[0]), float(mc_ci[1])],
            "f1_difference_minicheck_minus_base": float(diff),
            "difference_95_ci": [float(diff_ci[0]), float(diff_ci[1])],
        },
    }

    with open(OUT_SUMMARY, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("\nGrounded-hard results (design-weighted; UNSUPPORTED positive class)")
    print(
        f"Deployed base : P={base['precision']:.4f} "
        f"R={base['recall']:.4f} F1={base['f1']:.4f}"
    )
    print(
        f"MiniCheck-7B  : P={minicheck['precision']:.4f} "
        f"R={minicheck['recall']:.4f} F1={minicheck['f1']:.4f} "
        f"AUROC={minicheck['auroc']:.4f}"
    )
    print(f"F1 difference: {diff:+.4f}")
    print(
        "Paired question-clustered 95% CI: "
        f"[{diff_ci[0]:+.4f}, {diff_ci[1]:+.4f}]"
    )
    print(f"\nSaved predictions: {OUT_PRED}")
    print(f"Saved summary    : {OUT_SUMMARY}")


if __name__ == "__main__":
    main()
