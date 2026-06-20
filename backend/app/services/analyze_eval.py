"""
backend/app/services/analyze_eval.py

M8 step 6 (laptop): join the verifier scores back to the three eval arms and compute the
headline comparison — per-arm unsupported-claim rates.

Arms (all use the same 409 scored claims, differ in which claims and how rate is computed):
  Arm 1 Basic RAG        : plain-answer claims, unsupported / total
  Arm 2 RAG + citations  : cited-answer claims, unsupported / total
  Arm 3 Verified system  : cited-answer claims AFTER removing verifier-flagged Unsupported
                           -> reports how many claims verification removed, and the
                              before/after grounding.

Also breaks results down by question type (grounded vs bait) to show the verifier catches
more on out-of-distribution (bait) questions.

Reads:  data/scores.json          (per-claim: qid, arm, label, support_score, ...)
        data/eval_questions.json   (qid -> type: grounded/bait)
Prints a report; writes data/eval_report.json.
"""

from __future__ import annotations

import json
from collections import defaultdict

SCORES_PATH = "data/scores.json"
QUESTIONS_PATH = "data/eval_questions.json"
OUT_PATH = "data/eval_report.json"


def rate(unsupported, total):
    return (unsupported / total) if total else 0.0


def main():
    with open(SCORES_PATH, encoding="utf-8") as f:
        scores = json.load(f)
    with open(QUESTIONS_PATH, encoding="utf-8") as f:
        qtype = {q["id"]: q["type"] for q in json.load(f)["questions"]}

    # split claims by arm
    plain = [s for s in scores if s["arm"] == "plain"]   # arm 1
    cited = [s for s in scores if s["arm"] == "cited"]    # arms 2 & 3

    def arm_stats(claims):
        n = len(claims)
        unsup = sum(1 for c in claims if c["label"] == "Unsupported")
        weak = sum(1 for c in claims if c["label"] == "Weak")
        supp = sum(1 for c in claims if c["label"] == "Supported")
        return {"n": n, "supported": supp, "weak": weak, "unsupported": unsup,
                "unsupported_rate": round(rate(unsup, n), 4)}

    arm1 = arm_stats(plain)
    arm2 = arm_stats(cited)

    # Arm 3: verified system removes Unsupported claims from the cited set.
    # delivered = supported + weak; removed = unsupported.
    cited_unsup = arm2["unsupported"]
    cited_total = arm2["n"]
    delivered = cited_total - cited_unsup
    arm3 = {
        "n_before": cited_total,
        "removed_unsupported": cited_unsup,
        "n_delivered": delivered,
        "unsupported_rate_before": arm2["unsupported_rate"],
        "unsupported_rate_after": 0.0,   # by construction, flagged claims removed
        "supported_claim_retention": round(rate(delivered, cited_total), 4),
    }

    # breakdown by question type (grounded vs bait), on the cited arm
    by_type = defaultdict(lambda: {"n": 0, "unsupported": 0})
    for c in cited:
        t = qtype.get(c["qid"], "unknown")
        by_type[t]["n"] += 1
        if c["label"] == "Unsupported":
            by_type[t]["unsupported"] += 1
    type_rates = {
        t: {"n": v["n"], "unsupported": v["unsupported"],
            "unsupported_rate": round(rate(v["unsupported"], v["n"]), 4)}
        for t, v in by_type.items()
    }

    report = {
        "arm1_basic_rag": arm1,
        "arm2_rag_citations": arm2,
        "arm3_verified": arm3,
        "cited_arm_by_question_type": type_rates,
    }

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    # ---- printed report ----
    print("=" * 64)
    print("M8 EVAL — THREE-ARM COMPARISON (real S2+S4 verifier)")
    print("=" * 64)
    print(f"\nArm 1  Basic RAG (plain answers)")
    print(f"   claims={arm1['n']}  supported={arm1['supported']}  weak={arm1['weak']}  unsupported={arm1['unsupported']}")
    print(f"   unsupported rate = {arm1['unsupported_rate']*100:.1f}%")
    print(f"\nArm 2  RAG + citations (cited answers)")
    print(f"   claims={arm2['n']}  supported={arm2['supported']}  weak={arm2['weak']}  unsupported={arm2['unsupported']}")
    print(f"   unsupported rate = {arm2['unsupported_rate']*100:.1f}%")
    print(f"\nArm 3  Verified system (cited answers, unsupported claims removed)")
    print(f"   before: {arm3['n_before']} claims, {arm3['unsupported_rate_before']*100:.1f}% unsupported")
    print(f"   verification removed {arm3['removed_unsupported']} unsupported claims")
    print(f"   delivered: {arm3['n_delivered']} claims, ~0% unsupported")
    print(f"   supported-claim retention = {arm3['supported_claim_retention']*100:.1f}%")
    print(f"\nCited-arm unsupported rate by question type:")
    for t, v in sorted(type_rates.items()):
        print(f"   {t:<9}: {v['unsupported']}/{v['n']} = {v['unsupported_rate']*100:.1f}% unsupported")
    print("\n" + "=" * 64)
    print(f"Saved report to {OUT_PATH}")


if __name__ == "__main__":
    main()
