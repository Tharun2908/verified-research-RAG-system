"""
backend/app/services/build_gold_candidates.py

STEP 1 of the verifier fine-tuning project (#3): build the INDEPENDENT GOLD EVAL SET.

This is the load-bearing credibility artifact. Both fine-tuned verifiers (Path A = SciFact/
HealthVer, Path B = arXiv judge-distillation) and the original RAGTruth-trained verifier will be
measured against THIS set. It must be independent of any training signal — so:
  - it is NOT used to train either path,
  - its labels come from a labeler independent of the Llama-3.3 distillation judge (drafted by a
    GPT/Claude-class model, then HAND-CORRECTED by a human),
  - the drafting model labels BLIND: it sees only claim + evidence, NOT the verifier or judge labels.

Selection is ENRICHED for recall measurement. The M8 claim pool is ~93% Supported, which makes a
random sample useless for measuring RECALL (too few true-Unsupported cases). So we deliberately
oversample the cases most likely to be Unsupported / informative:
  - all BAIT-arm claims (out-of-distribution questions, likely unsupported)
  - all claims where verifier and judge DISAGREED (boundary cases)
  - all claims the JUDGE called UNSUPPORTED (the positive class for recall)
  - a capped RANDOM sample of clean Supported claims (so both classes are represented)

Output: data/gold_candidates.json — records with claim_text + evidence_text + a blank gold_label,
ready for the model-draft -> human-correct pass. The verifier/judge labels are kept in a SEPARATE
'_meta' block (for our analysis of selection), NOT shown to the drafting model.

NOTE on bait detection: M8 marked bait questions in eval_questions.json. We read that to tag
bait claims. If the arm field already encodes it differently, adjust BAIT detection below.
"""

from __future__ import annotations

import json
import random
from pathlib import Path

random.seed(42)  # reproducible selection

DATA = Path("data")
TARGET_GOLD_SIZE = 180          # rough target; enriched buckets may push slightly over
MAX_CLEAN_SUPPORTED = 60        # cap on easy supported cases (the rest are hard/positive)


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


def key(r):
    return (r["qid"], r["arm"], r["claim_index"])


def main():
    claims = load("claims_to_verify.json")   # claim_text + evidence_text
    scores = load("scores.json")             # verifier label + sub-scores
    judge = load("judge_results.json")       # judge verdict

    scores_by = {key(r): r for r in scores}
    judge_by = {key(r): r for r in judge}

    # identify bait questions from eval_questions.json
    try:
        eqs = load("eval_questions.json")
        # eval_questions.json is a DICT with a "questions" list; each question has
        # "id" and "type" ("grounded" | "bait"). Handle both dict and list shapes.
        question_list = eqs["questions"] if isinstance(eqs, dict) and "questions" in eqs else eqs
        bait_qids = set()
        for q in question_list:
            qid = q.get("id", q.get("qid"))
            is_bait = (
                q.get("type") == "bait"
                or q.get("bait") is True
                or q.get("category") == "bait"
                or str(q.get("kind", "")).lower() == "bait"
            )
            if is_bait and qid is not None:
                bait_qids.add(str(qid))
        print(f"Bait qids detected: {sorted(bait_qids) if bait_qids else 'NONE (check eval_questions schema)'}")
    except Exception as e:
        bait_qids = set()
        print(f"Could not read bait flags ({e}); proceeding without bait tagging.")

    # join all three + tag selection reasons
    joined = []
    for c in claims:
        k = key(c)
        s = scores_by.get(k, {})
        j = judge_by.get(k, {})
        v_label = s.get("label", "")                       # Supported / Weak / Unsupported
        j_verdict = (j.get("judge_verdict") or "").upper() # SUPPORTED / UNSUPPORTED
        v_binary = (j.get("verifier_binary") or "").upper()
        # Robust fallback: in this project Supported AND Weak are RETAINED (->SUPPORTED),
        # only Unsupported is REMOVED (->UNSUPPORTED). Don't rely on verifier_binary existing.
        if not v_binary:
            if v_label == "Unsupported":
                v_binary = "UNSUPPORTED"
            elif v_label in {"Supported", "Weak"}:
                v_binary = "SUPPORTED"
        is_bait = str(c["qid"]) in bait_qids
        disagree = bool(v_binary) and bool(j_verdict) and (v_binary != j_verdict)
        judge_unsupported = (j_verdict == "UNSUPPORTED")
        joined.append({
            "k": k,
            "rec": c,
            "v_label": v_label,
            "j_verdict": j_verdict,
            "is_bait": is_bait,
            "disagree": disagree,
            "judge_unsupported": judge_unsupported,
        })

    # --- enriched selection ---
    selected = {}
    def add(item, reason):
        kk = item["k"]
        if kk not in selected:
            selected[kk] = {"item": item, "reasons": [reason]}
        elif reason not in selected[kk]["reasons"]:
            selected[kk]["reasons"].append(reason)

    # bucket 1: bait claims
    for it in joined:
        if it["is_bait"]:
            add(it, "bait")
    # bucket 2: verifier/judge disagreements
    for it in joined:
        if it["disagree"]:
            add(it, "disagreement")
    # bucket 3: judge-unsupported (positive class for recall)
    for it in joined:
        if it["judge_unsupported"]:
            add(it, "judge_unsupported")
    # bucket 4: capped random clean Supported (both verifier & judge supported, not bait)
    clean = [
        it for it in joined
        if it["v_label"] == "Supported"
        and it["j_verdict"] == "SUPPORTED"
        and not it["is_bait"]
        and it["k"] not in selected
    ]
    random.shuffle(clean)
    for it in clean[:MAX_CLEAN_SUPPORTED]:
        add(it, "clean_supported_sample")

    # if we're under target, top up with more random non-selected
    if len(selected) < TARGET_GOLD_SIZE:
        rest = [it for it in joined if it["k"] not in selected]
        random.shuffle(rest)
        for it in rest[: TARGET_GOLD_SIZE - len(selected)]:
            add(it, "topup_random")

    # --- emit ---
    out = []
    reason_counts = {}
    for obj in selected.values():
        item = obj["item"]
        reasons = obj["reasons"]
        c = item["rec"]
        for r in reasons:                # count overlaps honestly
            reason_counts[r] = reason_counts.get(r, 0) + 1
        out.append({
            "qid": c["qid"],
            "arm": c["arm"],
            "claim_index": c["claim_index"],
            "claim_text": c["claim_text"],
            "evidence_text": c["evidence_text"],
            "gold_label": None,          # to be filled: "SUPPORTED" / "UNSUPPORTED"
            "_meta": {                    # for OUR analysis only; NOT in the blind file
                "selection_reasons": reasons,
                "verifier_label": item["v_label"],
                "judge_verdict": item["j_verdict"],
            },
        })

    with open(DATA / "gold_candidates.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    # PATCH 4: separate BLIND file for the drafting model / human labeling.
    # Contains ONLY claim + evidence + blank label. No verifier label, no judge verdict,
    # no selection reason. This structurally guarantees the labeling is blind, protecting
    # the independence of the gold set (the whole point of Step 1).
    blind = [
        {
            "qid": o["qid"],
            "arm": o["arm"],
            "claim_index": o["claim_index"],
            "claim_text": o["claim_text"],
            "evidence_text": o["evidence_text"],
            "gold_label": o["gold_label"],   # None, to be filled
        }
        for o in out
    ]
    with open(DATA / "gold_candidates_blind.json", "w", encoding="utf-8") as f:
        json.dump(blind, f, ensure_ascii=False, indent=2)

    # Methodology note travels WITH the data so the bias is owned, not hidden.
    note = (
        "GOLD EVAL SET — methodology note\n"
        "This set is ENRICHED for informative unsupported/boundary cases (bait claims, "
        "verifier/judge disagreements, judge-unsupported claims, plus a capped sample of clean "
        "supported claims). It is NOT prevalence-representative of the production claim "
        "distribution (which is ~93% supported). Use it for: recall, removal precision, "
        "false-negative / false-positive analysis, model-vs-gold comparison, and threshold "
        "tuning. DO NOT use it to estimate the natural unsupported rate of the live system "
        "(use the unenriched M8 eval for prevalence).\n"
    )
    with open(DATA / "gold_eval_README.txt", "w", encoding="utf-8") as f:
        f.write(note)

    print(f"\nSelected {len(out)} gold candidates (target {TARGET_GOLD_SIZE}).")
    print("By selection reason:")
    for r, n in sorted(reason_counts.items(), key=lambda x: -x[1]):
        print(f"  {r:24s} {n}")
    # class balance preview (by judge verdict, as a rough proxy)
    pos = sum(1 for o in out if o["_meta"]["judge_verdict"] == "UNSUPPORTED")
    print(f"\nRough positive (Unsupported) proxy in set: {pos}/{len(out)} "
          f"({100*pos/len(out):.0f}%) — want this meaningfully above the ~7% base rate.")
    print("Wrote data/gold_candidates.json (with _meta for analysis)")
    print("Wrote data/gold_candidates_blind.json (claim+evidence only, for blind labeling)")
    print("Wrote data/gold_eval_README.txt (methodology note — enriched, not prevalence-representative)")


if __name__ == "__main__":
    main()
