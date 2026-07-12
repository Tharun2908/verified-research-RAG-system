"""
verifier_study/3_gold_and_eval/reproduce_bootstrap.py

Recompute the headline grounded-hard result from COMMITTED artifacts only.

The original `bootstrap_grounded_hard_clustered.py` runs on the cluster and expects a
`score_cache/` directory and a differently-named metrics file — neither of which is in this
repository. The reported numbers were therefore *documented* but not independently *runnable*.

This script closes that gap. It reads only what is committed under
`backend/data/grounded_hard_eval/` and recomputes:

    base verifier weighted F1
    OOF fusion weighted F1
    their paired difference
    a question-clustered bootstrap CI on that difference

Expected (matching backend/data/grounded_hard_eval/bootstrap_summary.json):

    base verifier F1        0.402926
    OOF fusion F1           0.329228
    difference             -0.073698
    95% clustered CI       [-0.131, -0.018]

THE METRIC is BINARY F1 on the UNSUPPORTED class (sklearn average="binary"), NOT a
support-weighted average over both classes. That distinction matters enormously here: with 86
supported and only 15 unsupported claims, a both-class weighted F1 would sit around 0.73 —
inflated by the easy majority class — and would say almost nothing about the thing the
verifier exists to do, which is CATCH UNSUPPORTED CLAIMS.

DESIGN WEIGHTS. The human review sampled claims under a stratified protocol, so every claim
carries a `sampling_weight`. Metrics are computed WITH those weights, so they estimate
performance on the population the sample was drawn from rather than on the sample itself.

WHY A CLUSTERED BOOTSTRAP. Claims from the same question share evidence and one generator
pass, so they are correlated. Resampling individual claims would treat them as independent
and give a CI that is too narrow. We resample whole QUESTIONS (qid) — 62 of them.

WHY PAIRED. Both models score the same claims, so the DIFFERENCE has far less variance than
either absolute figure. The paired comparison is the trustworthy quantity, and it is what the
reported conclusion rests on.

Usage (from the repository root):

    python verifier_study/3_gold_and_eval/reproduce_bootstrap.py
    python verifier_study/3_gold_and_eval/reproduce_bootstrap.py --n-boot 2000 --seed 42
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

DATA = Path("backend/data/grounded_hard_eval")
BASE_FILE = DATA / "binary_predictions.jsonl"                        # all model columns
OOF_FILE = DATA / "fusion_ft_scifact_oof_hard_predictions.jsonl"     # the OOF fusion

# Column names in the committed artifacts.
JOIN_KEY = "claim_id"
CLUSTER = "qid"
HUMAN_LABEL = "human_final_label"

BASE_PRED = "base_scifact_healthver_pred"       # the deployed (unadapted) verifier
OOF_PRED = "fusion_pred_label"                  # the OOF fusion
WEIGHT = "sampling_weight"                      # stratified-review design weight

# Matches bootstrap_summary.json -> protocol
N_BOOT = 5000
SEED = 2908


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        raise SystemExit(
            f"Missing artifact: {path}\n"
            "Run this from the repository ROOT (not from backend/)."
        )
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def as_binary(value) -> int | None:
    """Normalise a label/prediction to 1 (unsupported) or 0 (supported)."""
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
    return None            # ABSTENTION and anything else -> excluded from the binary set


def binary_f1(y: np.ndarray, pred: np.ndarray, w: np.ndarray) -> float:
    """
    Weighted BINARY F1 on the positive (UNSUPPORTED) class — sklearn average="binary" with
    sample_weight. This is the metric the reported figures use.

    Deliberately NOT a both-class weighted average: 85% of the claims are supported, so such
    an average would be dominated by the easy class and would obscure the only thing that
    matters here — whether the verifier catches unsupported claims.
    """
    tp = float(w[(pred == 1) & (y == 1)].sum())
    fp = float(w[(pred == 1) & (y == 0)].sum())
    fn = float(w[(pred == 0) & (y == 1)].sum())
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec = tp / (tp + fn) if (tp + fn) else 0.0
    return 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-boot", type=int, default=N_BOOT)
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)

    base_rows = {r[JOIN_KEY]: r for r in load_jsonl(BASE_FILE)}
    oof_rows = {r[JOIN_KEY]: r for r in load_jsonl(OOF_FILE)}

    # Keep claims that are (a) human-labeled SUPPORTED/UNSUPPORTED and (b) predicted by BOTH.
    # Abstentions are excluded from the binary comparison by construction — they assert the
    # absence of information rather than a checkable fact.
    rows = []
    for cid, b in base_rows.items():
        o = oof_rows.get(cid)
        if o is None:
            continue
        y = as_binary(b.get(HUMAN_LABEL))
        pb = as_binary(b.get(BASE_PRED))
        po = as_binary(o.get(OOF_PRED))
        if y is None or pb is None or po is None:
            continue
        rows.append({
            "qid": b[CLUSTER],
            "y": y,
            "base": pb,
            "oof": po,
            "w": float(b.get(WEIGHT, 1.0)),
        })

    if not rows:
        raise SystemExit(
            "No claims matched. Check that the committed artifacts still carry "
            f"'{HUMAN_LABEL}', '{BASE_PRED}', and '{OOF_PRED}'."
        )

    y = np.array([r["y"] for r in rows])
    pb = np.array([r["base"] for r in rows])
    po = np.array([r["oof"] for r in rows])
    w = np.array([r["w"] for r in rows])
    qids = [r["qid"] for r in rows]

    print(f"Binary claims: {len(rows)}   unsupported: {int(y.sum())}   "
          f"question clusters (qid): {len(set(qids))}")
    print(f"Design-weighted mass — supported: {w[y == 0].sum():.1f}   "
          f"unsupported: {w[y == 1].sum():.1f}")
    print("Metric: weighted binary F1 on the UNSUPPORTED class\n")

    f1_base = binary_f1(y, pb, w)
    f1_oof = binary_f1(y, po, w)
    diff = f1_oof - f1_base

    print(f"base verifier  F1  {f1_base:.6f}")
    print(f"OOF fusion     F1  {f1_oof:.6f}")
    print(f"difference         {diff:+.6f}")

    # --- question-clustered paired bootstrap ---
    by_q: dict[object, list[int]] = defaultdict(list)
    for i, q in enumerate(qids):
        by_q[q].append(i)
    q_list = list(by_q)

    diffs = []
    for _ in range(args.n_boot):
        picked = rng.choice(len(q_list), size=len(q_list), replace=True)
        idx = [i for j in picked for i in by_q[q_list[j]]]
        yy, ww = y[idx], w[idx]
        if yy.sum() == 0:
            continue        # a replicate with no unsupported claims has no defined F1
        diffs.append(binary_f1(yy, po[idx], ww) - binary_f1(yy, pb[idx], ww))

    diffs = np.array(diffs)
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    print(f"\n95% question-clustered paired bootstrap CI "
          f"({len(diffs)}/{args.n_boot} valid reps, seed {args.seed}):")
    print(f"  [{lo:+.4f}, {hi:+.4f}]")

    if hi < 0:
        verdict = "reliably WORSE than the base verifier (CI excludes zero)"
    elif lo > 0:
        verdict = "reliably BETTER than the base verifier (CI excludes zero)"
    else:
        verdict = "not distinguishable from the base verifier"
    print(f"  -> OOF fusion is {verdict}")


if __name__ == "__main__":
    main()
