"""
backend/app/services/build_claims_to_verify.py

M8 step 4 (laptop): read answers.json, extract atomic claims from each answer, pair each
claim with the evidence text it should be verified against, and write a SELF-CONTAINED
claims_to_verify.json for the cluster verifier (which has no DB access).

Arm mapping:
  - arm 1 (basic)  -> claims from plain_answer  (no citations -> verify vs ALL evidence)
  - arm 2 (cited)  -> claims from cited_answer  (citations -> verify vs cited evidence)
  - arm 3 (verified) shares arm 2's claims+scores; it differs only at metric time
    (it filters out claims the verifier flags). So we extract two claim sets per question:
    'plain' (arm 1) and 'cited' (arms 2 & 3).

Reuses M5 claim_extractor + the M6 evidence-selection logic (citation -> evidence text,
fair-chance fallback to all evidence for uncited claims).

Output: backend/data/claims_to_verify.json
  [
    {"qid", "arm", "claim_index", "claim_text", "evidence_text"},
    ...
  ]
Each row is one claim to score. arm is "plain" or "cited".
"""

from __future__ import annotations

import json

from app.services.claim_extractor import extract_claims

ANSWERS_PATH = "data/answers.json"
OUT_PATH = "data/claims_to_verify.json"


def evidence_text_for_claim(citations, evidence):
    """Citation numbers -> concatenated evidence text. Uncited -> all evidence (fair chance)."""
    by_number = {e["number"]: e for e in evidence}
    if citations:
        chosen = [by_number[c]["text"] for c in citations if c in by_number]
    else:
        chosen = [e["text"] for e in evidence]
    return "\n".join(chosen)


def build():
    with open(ANSWERS_PATH, encoding="utf-8") as f:
        answers = json.load(f)

    rows = []
    for item in answers:
        qid = item["id"]
        evidence = item["evidence"]

        for arm, answer_key in (("plain", "plain_answer"), ("cited", "cited_answer")):
            claims = extract_claims(item[answer_key])
            for idx, c in enumerate(claims):
                rows.append({
                    "qid": qid,
                    "arm": arm,
                    "claim_index": idx,
                    "claim_text": c["claim_text"],
                    "evidence_text": evidence_text_for_claim(c["citations"], evidence),
                })

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    # quick summary
    n_plain = sum(1 for r in rows if r["arm"] == "plain")
    n_cited = sum(1 for r in rows if r["arm"] == "cited")
    print(f"Wrote {len(rows)} claims to {OUT_PATH}")
    print(f"  plain-arm claims: {n_plain}")
    print(f"  cited-arm claims: {n_cited}")


if __name__ == "__main__":
    build()
