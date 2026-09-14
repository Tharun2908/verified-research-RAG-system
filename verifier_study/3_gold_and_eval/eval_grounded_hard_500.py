#!/usr/bin/env python3
"""
Expanded grounded-hard evaluation: DeBERTa + MiniCheck-7B + cascades.

Runs both models ONCE on the finalized 500-row human review, then evaluates the
339 binary SUPPORTED/UNSUPPORTED claims using the new 500-sample design weights.

Input:
    backend/data/grounded_hard_eval/grounded_hard_random_review_500_labeled.jsonl

Outputs:
    backend/data/grounded_hard_eval/grounded_hard_500_model_predictions.jsonl
    backend/data/grounded_hard_eval/grounded_hard_500_eval_summary.json
    backend/data/grounded_hard_eval/grounded_hard_500_uncertainty_cascade_curve.csv

Protocol:
- Human labels: SUPPORTED / UNSUPPORTED only.
- ABSTENTION and INVALID_EXTRACTION are excluded from binary metrics.
- UNSUPPORTED is the positive class.
- Sampling weights come from the nested 500-claim stratified sample.
- DeBERTa checkpoint is the pinned deployed SciFact+HealthVer verifier.
- DeBERTa binary threshold is frozen at P(unsupported) >= 0.06.
- MiniCheck uses its official binary output.
- Confirmation cascade: DeBERTa SUPPORTED -> accept; DeBERTa UNSUPPORTED -> MiniCheck.
- Uncertainty cascade: escalate smallest abs(P_unsupported - 0.06) margins first.
- Bootstrap resamples whole qid clusters and is paired across systems.
- Cascade routing never uses human labels.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np
import torch
from sklearn.metrics import roc_auc_score
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from minicheck.minicheck import MiniCheck

DATA = Path("backend/data/grounded_hard_eval")
INPUT = DATA / "grounded_hard_random_review_500_labeled.jsonl"
OUT_PRED = DATA / "grounded_hard_500_model_predictions.jsonl"
OUT_SUMMARY = DATA / "grounded_hard_500_eval_summary.json"
OUT_CURVE = DATA / "grounded_hard_500_uncertainty_cascade_curve.csv"

HF_MODEL_ID = "Primeinvincible/scifact-healthver-verifier"
HF_REVISION = "902d07844e30e59d311f5cc500b9ec13d08d0002"
BASE_THRESHOLD = 0.06
MAX_LENGTH = 512
DEFAULT_RATES = [0, 5, 10, 20, 30, 40, 50, 75, 100]
N_BOOT = 5000
SEED = 2908


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def as_binary(value: Any) -> int | None:
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


def metrics(y: np.ndarray, pred: np.ndarray, w: np.ndarray) -> dict[str, float]:
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
    return metrics(y, pred, w)["f1"]


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


def score_deberta(claims, evidence, batch_size, device, local_model_path):
    if local_model_path:
        model_source = local_model_path
        kwargs = {}
        print(f"[DeBERTa] loading local checkpoint: {model_source}")
    else:
        model_source = HF_MODEL_ID
        kwargs = {"revision": HF_REVISION}
        print(f"[DeBERTa] loading {model_source}@{HF_REVISION[:8]}")

    tokenizer = AutoTokenizer.from_pretrained(model_source, **kwargs)
    model = AutoModelForSequenceClassification.from_pretrained(model_source, **kwargs)
    model.to(device)
    model.eval()

    scores = []
    print(f"[DeBERTa] scoring {len(claims)} claims on {device}...")
    for start in range(0, len(claims), batch_size):
        end = min(start + batch_size, len(claims))
        enc = tokenizer(
            claims[start:end], evidence[start:end], max_length=MAX_LENGTH,
            truncation=True, padding=True, return_tensors="pt"
        )
        enc = {k: v.to(device) for k, v in enc.items()}
        with torch.no_grad():
            logits = model(**enc).logits
            probs = torch.softmax(logits, dim=1)[:, 1]
        scores.extend(probs.detach().cpu().numpy().astype(float).tolist())
        print(f"\r[DeBERTa] {end}/{len(claims)}", end="", flush=True)
    print()

    del model
    del tokenizer
    if device.type == "cuda":
        torch.cuda.empty_cache()
    return np.asarray(scores, dtype=float)


def score_minicheck(claims, evidence, cache_dir):
    print("[MiniCheck] loading Bespoke-MiniCheck-7B...")
    scorer = MiniCheck(
        model_name="Bespoke-MiniCheck-7B",
        enable_prefix_caching=False,
        cache_dir=cache_dir,
    )
    print(f"[MiniCheck] scoring {len(claims)} claims...")
    pred_supported, support_prob, _, _ = scorer.score(docs=evidence, claims=claims)
    if len(pred_supported) != len(claims) or len(support_prob) != len(claims):
        raise RuntimeError("MiniCheck returned an unexpected number of predictions.")
    pred_unsupported = 1 - np.asarray(pred_supported, dtype=int)
    score_unsupported = 1.0 - np.asarray(support_prob, dtype=float)
    return pred_unsupported, score_unsupported


def clustered_bootstrap(y, w, qids, systems, n_boot, seed):
    by_q = {q: np.where(qids == q)[0] for q in sorted(set(qids.tolist()))}
    q_list = sorted(by_q)
    rng = np.random.default_rng(seed)
    boot_f1 = {name: [] for name in systems}
    valid = 0

    for _ in range(n_boot):
        picked = rng.choice(len(q_list), size=len(q_list), replace=True)
        idx = np.concatenate([by_q[q_list[int(j)]] for j in picked])
        yy, ww = y[idx], w[idx]
        if np.sum(ww[yy == 1]) <= 0:
            continue
        valid += 1
        for name, pred in systems.items():
            boot_f1[name].append(f1_only(yy, pred[idx], ww))

    out = {}
    for name, vals in boot_f1.items():
        arr = np.asarray(vals, dtype=float)
        ci = np.percentile(arr, [2.5, 97.5])
        out[name] = {"f1_95_ci": [float(ci[0]), float(ci[1])]}

    for a, b in [
        ("minicheck_only", "deberta_only"),
        ("confirmation_cascade", "deberta_only"),
        ("confirmation_cascade", "minicheck_only"),
    ]:
        diff = np.asarray(boot_f1[a]) - np.asarray(boot_f1[b])
        ci = np.percentile(diff, [2.5, 97.5])
        out[a][f"f1_difference_vs_{b}"] = {"95_ci": [float(ci[0]), float(ci[1])]}

    return out, valid


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, default=INPUT)
    ap.add_argument("--out-pred", type=Path, default=OUT_PRED)
    ap.add_argument("--out-summary", type=Path, default=OUT_SUMMARY)
    ap.add_argument("--out-curve", type=Path, default=OUT_CURVE)
    ap.add_argument("--deberta-batch-size", type=int, default=16)
    ap.add_argument("--minicheck-cache-dir", default="./ckpts")
    ap.add_argument("--deberta-local-path", default=os.getenv("VERIFIER_MODEL_PATH"))
    ap.add_argument("--rates", default=",".join(str(x) for x in DEFAULT_RATES))
    ap.add_argument("--n-boot", type=int, default=N_BOOT)
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args()

    rates = parse_rates(args.rates)
    if not args.input.exists():
        raise SystemExit(f"Missing input: {args.input}")

    source = load_jsonl(args.input)
    rows = []
    excluded = defaultdict(int)

    for r in source:
        label_raw = r.get("human_final_label") or r.get("final_label") or r.get("label")
        y = as_binary(label_raw)
        if y is None:
            excluded[str(label_raw or "MISSING").upper()] += 1
            continue
        claim = str(r.get("claim") or "").strip()
        evidence = str(r.get("evidence_text_for_verifier") or "").strip()
        if not claim or not evidence:
            raise SystemExit(f"Binary row {r.get('claim_id')} is missing claim/evidence text.")
        rows.append({
            "source": r,
            "claim_id": str(r["claim_id"]),
            "qid": str(r["qid"]),
            "claim": claim,
            "evidence": evidence,
            "y": y,
            "weight": float(r.get("sampling_weight", 1.0)),
        })

    n = len(rows)
    n_unsupported = sum(r["y"] for r in rows)
    n_supported = n - n_unsupported
    q_count = len({r["qid"] for r in rows})
    q_with_unsupported = len({r["qid"] for r in rows if r["y"] == 1})

    print("\nExpanded grounded-hard benchmark")
    print("=" * 80)
    print(f"Reviewed rows:        {len(source)}")
    print(f"Binary claims:        {n}")
    print(f"Supported:            {n_supported}")
    print(f"Unsupported:          {n_unsupported}")
    print(f"QID clusters:         {q_count}")
    print(f"Clusters w/ UNSUP:    {q_with_unsupported}")
    print(f"Excluded labels:      {dict(excluded)}")
    print()

    if len(source) != 500 or n != 339 or n_unsupported != 51:
        raise SystemExit(
            "Expanded-benchmark guardrail failed. Expected 500 reviewed rows, "
            f"339 binary claims, and 51 unsupported claims; observed {len(source)}, {n}, {n_unsupported}."
        )

    claims = [r["claim"] for r in rows]
    evidence = [r["evidence"] for r in rows]
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if device.type != "cuda":
        print("WARNING: CUDA is not available; MiniCheck-7B will likely be impractical on CPU.")

    base_score = score_deberta(
        claims, evidence, args.deberta_batch_size, device, args.deberta_local_path
    )
    base_pred = (base_score >= BASE_THRESHOLD).astype(int)
    mc_pred, mc_score = score_minicheck(claims, evidence, args.minicheck_cache_dir)

    y = np.asarray([r["y"] for r in rows], dtype=int)
    w = np.asarray([r["weight"] for r in rows], dtype=float)
    qids = np.asarray([r["qid"] for r in rows], dtype=object)

    confirmation_pred = base_pred.copy()
    confirmation_mask = base_pred == 1
    confirmation_pred[confirmation_mask] = mc_pred[confirmation_mask]

    margins = np.abs(base_score - BASE_THRESHOLD)
    order = sorted(range(n), key=lambda i: (float(margins[i]), rows[i]["claim_id"]))
    uncertainty_preds, uncertainty_masks = {}, {}
    for rate in rates:
        k = min(max(int(round(n * rate / 100.0)), 0), n)
        mask = np.zeros(n, dtype=bool)
        if k:
            mask[np.asarray(order[:k], dtype=int)] = True
        pred = base_pred.copy()
        pred[mask] = mc_pred[mask]
        uncertainty_masks[rate] = mask
        uncertainty_preds[rate] = pred

    base_m = metrics(y, base_pred, w)
    base_m["auroc"] = float(roc_auc_score(y, base_score, sample_weight=w))
    mc_m = metrics(y, mc_pred, w)
    mc_m["auroc"] = float(roc_auc_score(y, mc_score, sample_weight=w))
    confirmation_m = metrics(y, confirmation_pred, w)
    confirmation_m.update({
        "claims_sent_to_minicheck": int(confirmation_mask.sum()),
        "raw_escalation_fraction": float(confirmation_mask.mean()),
        "raw_escalation_percent": float(100.0 * confirmation_mask.mean()),
        "weighted_escalation_fraction": float(w[confirmation_mask].sum() / w.sum()),
        "weighted_escalation_percent": float(100.0 * w[confirmation_mask].sum() / w.sum()),
        "minicheck_confirmed_unsupported": int(np.sum(confirmation_mask & (mc_pred == 1))),
        "minicheck_overruled_to_supported": int(np.sum(confirmation_mask & (mc_pred == 0))),
    })

    systems = {
        "deberta_only": base_pred,
        "minicheck_only": mc_pred,
        "confirmation_cascade": confirmation_pred,
    }
    boot, valid_boot = clustered_bootstrap(y, w, qids, systems, args.n_boot, args.seed)
    boot["minicheck_only"]["f1_difference_vs_deberta_only"]["point_estimate"] = float(mc_m["f1"] - base_m["f1"])
    boot["confirmation_cascade"]["f1_difference_vs_deberta_only"]["point_estimate"] = float(confirmation_m["f1"] - base_m["f1"])
    boot["confirmation_cascade"]["f1_difference_vs_minicheck_only"]["point_estimate"] = float(confirmation_m["f1"] - mc_m["f1"])

    by_q = {q: np.where(qids == q)[0] for q in sorted(set(qids.tolist()))}
    q_list = sorted(by_q)
    rng = np.random.default_rng(args.seed)
    curve_boot = {rate: {"f1": [], "gain_vs_base": [], "gap_vs_mc": []} for rate in rates}
    valid_curve_boot = 0
    for _ in range(args.n_boot):
        picked = rng.choice(len(q_list), size=len(q_list), replace=True)
        idx = np.concatenate([by_q[q_list[int(j)]] for j in picked])
        yy, ww = y[idx], w[idx]
        if np.sum(ww[yy == 1]) <= 0:
            continue
        valid_curve_boot += 1
        base_f1 = f1_only(yy, base_pred[idx], ww)
        mc_f1 = f1_only(yy, mc_pred[idx], ww)
        for rate in rates:
            cf1 = f1_only(yy, uncertainty_preds[rate][idx], ww)
            curve_boot[rate]["f1"].append(cf1)
            curve_boot[rate]["gain_vs_base"].append(cf1 - base_f1)
            curve_boot[rate]["gap_vs_mc"].append(cf1 - mc_f1)

    curve = []
    for rate in rates:
        mask, pred = uncertainty_masks[rate], uncertainty_preds[rate]
        m = metrics(y, pred, w)
        f1_ci = np.percentile(curve_boot[rate]["f1"], [2.5, 97.5])
        gain_ci = np.percentile(curve_boot[rate]["gain_vs_base"], [2.5, 97.5])
        gap_ci = np.percentile(curve_boot[rate]["gap_vs_mc"], [2.5, 97.5])
        curve.append({
            "requested_escalation_pct": rate,
            "escalated_claims": int(mask.sum()),
            "actual_escalation_pct": float(mask.mean() * 100.0),
            **m,
            "f1_gain_vs_base": float(m["f1"] - base_m["f1"]),
            "f1_gap_vs_minicheck": float(m["f1"] - mc_m["f1"]),
            "f1_95_ci": [float(f1_ci[0]), float(f1_ci[1])],
            "gain_vs_base_95_ci": [float(gain_ci[0]), float(gain_ci[1])],
            "gap_vs_minicheck_95_ci": [float(gap_ci[0]), float(gap_ci[1])],
        })

    pred_rows = []
    for i, r in enumerate(rows):
        out = dict(r["source"])
        out.update({
            "deberta_p_unsupported": float(base_score[i]),
            "deberta_pred": int(base_pred[i]),
            "deberta_pred_label": "UNSUPPORTED" if base_pred[i] else "SUPPORTED",
            "deberta_frozen_threshold": BASE_THRESHOLD,
            "minicheck_7b_support_score": float(1.0 - mc_score[i]),
            "minicheck_7b_unsupported_score": float(mc_score[i]),
            "minicheck_7b_pred": int(mc_pred[i]),
            "minicheck_7b_pred_label": "UNSUPPORTED" if mc_pred[i] else "SUPPORTED",
            "confirmation_cascade_escalated": bool(confirmation_mask[i]),
            "confirmation_cascade_pred": int(confirmation_pred[i]),
            "confirmation_cascade_pred_label": "UNSUPPORTED" if confirmation_pred[i] else "SUPPORTED",
            "deberta_margin_to_frozen_threshold": float(margins[i]),
        })
        pred_rows.append(out)
    write_jsonl(args.out_pred, pred_rows)

    summary = {
        "models": {
            "deberta": {"model": HF_MODEL_ID, "revision": HF_REVISION, "binary_threshold_p_unsupported": BASE_THRESHOLD},
            "minicheck": {"model": "Bespoke-MiniCheck-7B", "prefix_caching": False},
        },
        "protocol": {
            "evaluation_set": "nested 500-claim grounded-hard human review",
            "reviewed_rows": int(len(source)),
            "binary_positive_class": "UNSUPPORTED",
            "excluded_labels": dict(excluded),
            "weight_field": "sampling_weight",
            "cluster_field": "qid",
            "paired_question_clustered_bootstrap": True,
            "n_boot": args.n_boot,
            "valid_bootstrap_replicates": valid_boot,
            "seed": args.seed,
            "routing_uses_human_labels": False,
        },
        "sample": {
            "binary_claims": int(n),
            "supported_claims": int(n_supported),
            "unsupported_claims": int(n_unsupported),
            "question_clusters": int(q_count),
            "question_clusters_with_unsupported": int(q_with_unsupported),
            "weighted_supported_mass": float(w[y == 0].sum()),
            "weighted_unsupported_mass": float(w[y == 1].sum()),
        },
        "deberta_only": {**base_m, **boot["deberta_only"]},
        "minicheck_only": {**mc_m, **boot["minicheck_only"]},
        "confirmation_cascade": {**confirmation_m, **boot["confirmation_cascade"]},
        "uncertainty_cascade": {
            "routing": "escalate smallest abs(P_unsupported - 0.06) margins first",
            "valid_bootstrap_replicates": valid_curve_boot,
            "curve": curve,
        },
    }
    args.out_summary.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out_summary, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    args.out_curve.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "requested_escalation_pct", "escalated_claims", "actual_escalation_pct",
        "precision", "recall", "f1", "f1_gain_vs_base", "f1_gap_vs_minicheck",
        "f1_ci_low", "f1_ci_high", "gain_vs_base_ci_low", "gain_vs_base_ci_high",
        "gap_vs_minicheck_ci_low", "gap_vs_minicheck_ci_high",
    ]
    with open(args.out_curve, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for r in curve:
            writer.writerow({
                "requested_escalation_pct": r["requested_escalation_pct"],
                "escalated_claims": r["escalated_claims"],
                "actual_escalation_pct": r["actual_escalation_pct"],
                "precision": r["precision"], "recall": r["recall"], "f1": r["f1"],
                "f1_gain_vs_base": r["f1_gain_vs_base"],
                "f1_gap_vs_minicheck": r["f1_gap_vs_minicheck"],
                "f1_ci_low": r["f1_95_ci"][0], "f1_ci_high": r["f1_95_ci"][1],
                "gain_vs_base_ci_low": r["gain_vs_base_95_ci"][0],
                "gain_vs_base_ci_high": r["gain_vs_base_95_ci"][1],
                "gap_vs_minicheck_ci_low": r["gap_vs_minicheck_95_ci"][0],
                "gap_vs_minicheck_ci_high": r["gap_vs_minicheck_95_ci"][1],
            })

    print("\nExpanded grounded-hard results")
    print("=" * 80)
    print(f"DeBERTa-only          P={base_m['precision']:.4f} R={base_m['recall']:.4f} F1={base_m['f1']:.4f} AUROC={base_m['auroc']:.4f}")
    print(f"MiniCheck-only        P={mc_m['precision']:.4f} R={mc_m['recall']:.4f} F1={mc_m['f1']:.4f} AUROC={mc_m['auroc']:.4f}")
    print(f"Confirmation cascade P={confirmation_m['precision']:.4f} R={confirmation_m['recall']:.4f} F1={confirmation_m['f1']:.4f}")
    print(f"MiniCheck escalation: {confirmation_m['claims_sent_to_minicheck']}/{n} ({confirmation_m['raw_escalation_percent']:.1f}% raw claims)")
    c_db = boot["confirmation_cascade"]["f1_difference_vs_deberta_only"]
    c_mc = boot["confirmation_cascade"]["f1_difference_vs_minicheck_only"]
    print(f"Confirmation ΔF1 vs DeBERTa: {confirmation_m['f1'] - base_m['f1']:+.4f} 95% CI [{c_db['95_ci'][0]:+.4f}, {c_db['95_ci'][1]:+.4f}]")
    print(f"Confirmation ΔF1 vs MiniCheck: {confirmation_m['f1'] - mc_m['f1']:+.4f} 95% CI [{c_mc['95_ci'][0]:+.4f}, {c_mc['95_ci'][1]:+.4f}]")

    print("\nUncertainty cascade")
    print("-" * 80)
    print(f"{'Esc %':>6} {'N':>5} {'Precision':>10} {'Recall':>9} {'F1':>9} {'Δbase':>9} {'ΔMC':>9}")
    for r in curve:
        print(f"{r['actual_escalation_pct']:6.1f} {r['escalated_claims']:5d} {r['precision']:10.4f} {r['recall']:9.4f} {r['f1']:9.4f} {r['f1_gain_vs_base']:+9.4f} {r['f1_gap_vs_minicheck']:+9.4f}")

    print("\nSaved:")
    print(f"  {args.out_pred}")
    print(f"  {args.out_summary}")
    print(f"  {args.out_curve}")


if __name__ == "__main__":
    main()
