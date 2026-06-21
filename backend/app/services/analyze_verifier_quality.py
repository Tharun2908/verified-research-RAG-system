"""
backend/app/services/analyze_verifier_quality.py

M8 follow-up: grade the VERIFIER against the independent judge, replacing the circular
"~0% unsupported after filtering" (which only reflects the verifier's own labels) with
real classifier-quality metrics.

Treats the judge (Llama 3.3 70B via OpenRouter) as the REFERENCE. Important caveat: the
judge is itself imperfect and was found to be systematically STRICTER than the verifier
(M8). So these are agreement-framed-as-correctness metrics, not ground truth. They answer
"how does the verifier compare to an independent strict judge", which is far more honest
than the self-referential 0%.

2x2 (judge = reference):
                         judge:UNSUP        judge:SUP
  verifier removed (Unsupported)   true removal       wrongly removed (FP)
  verifier kept (Supported/Weak)   missed (FN)        correctly kept

Metrics:
  removal precision   = true_removal / (true_removal + wrongly_removed)
  recall              = true_removal / (true_removal + missed)
  supported loss      = wrongly_removed / (wrongly_removed + correctly_kept)
  retained unsup rate = missed / (missed + correctly_kept)   [judge's view of kept claims]
  F1                  = harmonic mean of removal precision and recall

Reads:  data/judge_results.json  (has verifier_label, verifier_binary, judge_verdict per claim,
                                   plus qid/arm/claim_index)
Prints metrics for all-409 (verifier quality) and cited-arm-only (deployment effect).
Writes data/verifier_quality.json.
"""

from __future__ import annotations

import json

JUDGE_PATH = "data/judge_results.json"
OUT_PATH = "data/verifier_quality.json"


def safe_div(a, b):
    return (a / b) if b else None


def compute(rows):
    # 2x2 cells (judge = reference)
    true_removal = sum(1 for r in rows if r["verifier_binary"] == "UNSUPPORTED" and r["judge_verdict"] == "UNSUPPORTED")
    wrongly_removed = sum(1 for r in rows if r["verifier_binary"] == "UNSUPPORTED" and r["judge_verdict"] == "SUPPORTED")
    missed = sum(1 for r in rows if r["verifier_binary"] == "SUPPORTED" and r["judge_verdict"] == "UNSUPPORTED")
    correctly_kept = sum(1 for r in rows if r["verifier_binary"] == "SUPPORTED" and r["judge_verdict"] == "SUPPORTED")

    removed = true_removal + wrongly_removed
    kept = missed + correctly_kept
    judge_unsup_total = true_removal + missed

    precision = safe_div(true_removal, removed)
    recall = safe_div(true_removal, judge_unsup_total)
    supported_loss = safe_div(wrongly_removed, wrongly_removed + correctly_kept)
    retained_unsup = safe_div(missed, kept)
    f1 = None
    if precision is not None and recall is not None and (precision + recall) > 0:
        f1 = 2 * precision * recall / (precision + recall)

    return {
        "n": len(rows),
        "cells": {
            "true_removal": true_removal,
            "wrongly_removed_FP": wrongly_removed,
            "missed_FN": missed,
            "correctly_kept": correctly_kept,
        },
        "n_removed_by_verifier": removed,
        "n_kept_by_verifier": kept,
        "n_judge_unsupported": judge_unsup_total,
        "removal_precision": round(precision, 4) if precision is not None else None,
        "recall": round(recall, 4) if recall is not None else None,
        "supported_claim_loss": round(supported_loss, 4) if supported_loss is not None else None,
        "retained_unsupported_rate_by_judge": round(retained_unsup, 4) if retained_unsup is not None else None,
        "f1": round(f1, 4) if f1 is not None else None,
    }


def show(title, m):
    print("=" * 60)
    print(title)
    print("=" * 60)
    print(f"  claims: {m['n']}")
    c = m["cells"]
    print(f"  2x2 (rows=verifier, cols=judge):")
    print(f"                    judge:UNSUP   judge:SUP")
    print(f"    verifier removed   {c['true_removal']:>6}      {c['wrongly_removed_FP']:>6}")
    print(f"    verifier kept      {c['missed_FN']:>6}      {c['correctly_kept']:>6}")
    print(f"  --")
    def pct(x): return f"{x*100:.1f}%" if x is not None else "n/a"
    print(f"  removal precision (of removed, judge agrees bad):  {pct(m['removal_precision'])}  ({c['true_removal']}/{m['n_removed_by_verifier']})")
    print(f"  recall (of judge-unsupported, verifier caught):    {pct(m['recall'])}  ({c['true_removal']}/{m['n_judge_unsupported']})")
    print(f"  F1 (precision/recall harmonic mean):               {pct(m['f1'])}")
    print(f"  supported-claim loss (good claims wrongly removed):{pct(m['supported_claim_loss'])}  ({c['wrongly_removed_FP']}/{c['wrongly_removed_FP']+c['correctly_kept']})")
    print(f"  retained unsupported rate (judge's view):          {pct(m['retained_unsupported_rate_by_judge'])}  ({c['missed_FN']}/{m['n_kept_by_verifier']})")
    print()


def main():
    with open(JUDGE_PATH, encoding="utf-8") as f:
        rows = json.load(f)

    all_m = compute(rows)
    cited_m = compute([r for r in rows if r["arm"] == "cited"])
    plain_m = compute([r for r in rows if r["arm"] == "plain"])

    show("VERIFIER QUALITY vs JUDGE — ALL CLAIMS (verifier-as-classifier)", all_m)
    show("DEPLOYMENT EFFECT — CITED ARM ONLY (what the Verified system filters)", cited_m)

    report = {
        "note": ("Judge (Llama-3.3-70B via OpenRouter) treated as reference; judge is imperfect "
                 "and was systematically stricter than the verifier (M8). Metrics are "
                 "agreement-framed-as-correctness, not ground truth."),
        "judge_model": "meta-llama/llama-3.3-70b-instruct",
        "judge_provider": "OpenRouter",
        "judge_run_date": "2026-06-21",   # <-- set to the ACTUAL judge run date
        "judge_prompt": ("Binary supported/unsupported judgment of each claim against its "
                         "evidence; one-word answer. See gemini_judge.py JUDGE_PROMPT."),
        "all_claims": all_m,
        "cited_arm": cited_m,
        "plain_arm": plain_m,
    }
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"Saved to {OUT_PATH}")


if __name__ == "__main__":
    main()
