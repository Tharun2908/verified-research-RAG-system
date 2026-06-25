"""
backend/app/services/gemini_judge.py

M8 step 7 (laptop): independent LLM-as-judge validation of the verifier, via OpenRouter,
on the FULL claim set, with RESUME support.

Uses OpenRouter (OpenAI-compatible API) so the judge is a DIFFERENT provider/model family
than the Mistral generator -> clean independence for the kappa comparison.

Resume: results written to OUT_PATH after every claim; on restart, already-judged claims
(keyed by qid/arm/claim_index) are skipped. Nothing is lost on interruption.

Requires OPENROUTER_API_KEY in backend/.env (gitignored). Never commit the key.
    pip install openai python-dotenv scikit-learn
"""

from __future__ import annotations

import os
import json
import time

from dotenv import load_dotenv
from openai import OpenAI
from sklearn.metrics import cohen_kappa_score, confusion_matrix

load_dotenv()

SCORES_PATH = "data/scores.json"
CLAIMS_PATH = "data/claims_to_verify.json"
OUT_PATH = "data/judge_results.json"

MODEL = "meta-llama/llama-3.3-70b-instruct"   # different family from the Mistral generator
REQUEST_SPACING_S = 0.5
MAX_RETRIES = 5

JUDGE_PROMPT = """You are evaluating whether a claim is supported by the provided evidence.

Evidence:
{evidence}

Claim:
{claim}

Question: Is the claim directly supported by the evidence above?
Answer with exactly one word: SUPPORTED or UNSUPPORTED."""


def setup_client():
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise SystemExit("OPENROUTER_API_KEY not found in environment / .env")
    return OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)


def judge_one(client, claim_text, evidence_text):
    prompt = JUDGE_PROMPT.format(evidence=evidence_text[:4000], claim=claim_text)
    for attempt in range(MAX_RETRIES):
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10,
                temperature=0,
            )
            text = (resp.choices[0].message.content or "").strip().upper()
            if "UNSUPPORTED" in text:
                return "UNSUPPORTED"
            if "SUPPORTED" in text:
                return "SUPPORTED"
            return "UNSUPPORTED"
        except Exception as e:
            wait = 5.0 * (attempt + 1)
            print(f"    retry {attempt+1}/{MAX_RETRIES} ({type(e).__name__}); waiting {wait:.0f}s")
            time.sleep(wait)
    return None


def load_existing():
    if not os.path.exists(OUT_PATH):
        return {}
    with open(OUT_PATH, encoding="utf-8") as f:
        rows = json.load(f)
    return {(r["qid"], r["arm"], r["claim_index"]): r for r in rows}


def main():
    with open(SCORES_PATH, encoding="utf-8") as f:
        scores = json.load(f)
    with open(CLAIMS_PATH, encoding="utf-8") as f:
        claims = json.load(f)
    claim_lookup = {(c["qid"], c["arm"], c["claim_index"]): c for c in claims}

    print(f"Full set: {len(scores)} claims (judge = {MODEL})")
    done = load_existing()
    print(f"Resuming: {len(done)} already judged, {len(scores) - len(done)} remaining.")

    client = setup_client()
    results = dict(done)

    for i, s in enumerate(scores):
        key = (s["qid"], s["arm"], s["claim_index"])
        if key in results:
            continue
        c = claim_lookup.get(key)
        if c is None:
            continue

        verdict = judge_one(client, c["claim_text"], c["evidence_text"])
        if verdict is None:
            print("  hit a wall (all retries failed). Saving progress and stopping.")
            break

        verifier_binary = "UNSUPPORTED" if s["label"] == "Unsupported" else "SUPPORTED"
        results[key] = {
            "qid": s["qid"], "arm": s["arm"], "claim_index": s["claim_index"],
            "verifier_label": s["label"], "verifier_binary": verifier_binary,
            "judge_verdict": verdict,
        }

        with open(OUT_PATH, "w", encoding="utf-8") as f:
            json.dump(list(results.values()), f, ensure_ascii=False, indent=2)

        if (len(results)) % 25 == 0:
            print(f"  judged {len(results)}/{len(scores)}", flush=True)
        time.sleep(REQUEST_SPACING_S)

    rows = list(results.values())
    if not rows:
        print("No results to score yet.")
        return

    v = [r["verifier_binary"] for r in rows]
    j = [r["judge_verdict"] for r in rows]
    labels = ["SUPPORTED", "UNSUPPORTED"]
    kappa = cohen_kappa_score(v, j, labels=labels)
    agree = sum(1 for a, b in zip(v, j) if a == b) / len(v)
    cm = confusion_matrix(v, j, labels=labels)

    print("\n" + "=" * 56)
    print("VERIFIER vs LLM JUDGE - AGREEMENT (full set, OpenRouter)")
    print("=" * 56)
    print(f"Judge model:     {MODEL}")
    print(f"Claims judged:   {len(rows)}")
    print(f"Raw agreement:   {agree*100:.1f}%")
    print(f"Cohen's kappa:   {kappa:.4f}")
    print("\nConfusion matrix (rows=verifier, cols=judge):")
    print(f"                 judge:SUP   judge:UNSUP")
    print(f"  verifier:SUP     {cm[0][0]:>6}      {cm[0][1]:>6}")
    print(f"  verifier:UNSUP   {cm[1][0]:>6}      {cm[1][1]:>6}")
    print("=" * 56)
    print(f"Results saved to {OUT_PATH}")


if __name__ == "__main__":
    main()
