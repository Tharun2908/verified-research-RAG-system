"""
backend/app/services/draft_gold_labels.py

STEP 1.3: model-draft the gold eval labels (BLIND), to be hand-corrected by a human.

Reads data/gold_candidates_blind.json (claim + evidence only — no verifier/judge labels),
asks an INDEPENDENT frontier model (Claude Opus 4.8 via OpenRouter — independent from the
Llama-3.3-70B judge used in M8 and for Path-B distillation) to label each claim's faithfulness
to its evidence, and writes data/gold_drafted.json.

The model is the DRAFTER, not the oracle. The human review pass (next step) is what makes the
set "gold". This script just produces a high-quality first pass to make that review fast.

Design:
  - RESUMABLE: writes after every item; on restart, skips already-drafted keys. (Learned from
    the M8 judge run where quota walls killed long unsaved runs.)
  - STRICT output parsing: asks for a single JSON object; falls back gracefully if the model
    wraps it in prose.
  - Rate-limit aware: small sleep + retry with backoff on transient errors.

Env: OPENROUTER_API_KEY must be set (already in .env from the M8 judge run).

USAGE (from backend/):
    python -m app.services.draft_gold_labels
    # optional: --model anthropic/claude-opus-4.8  --limit 5 (smoke test)
"""

from __future__ import annotations

import os
import json
import time
import argparse
from pathlib import Path

import httpx

# Load .env so OPENROUTER_API_KEY is available without manually exporting it.
# Graceful if python-dotenv isn't installed (falls back to shell env).
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

DATA = Path("data")
BLIND_IN = DATA / "gold_candidates_blind.json"
DRAFT_OUT = DATA / "gold_drafted.json"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "anthropic/claude-opus-4.8"

SYSTEM_PROMPT = (
    "You are a careful scientific fact-checker. You judge whether a CLAIM is faithful to "
    "the EVIDENCE passage it is supposed to be grounded in. There are THREE possible verdicts:\n"
    "- SUPPORTED: every factual assertion in the claim is directly supported by, or clearly "
    "inferable from, the evidence.\n"
    "- UNSUPPORTED: the claim states something not supported by the evidence — added details, "
    "overstated scope, wrong specifics, or fabricated method/result names — even if it sounds "
    "plausible or is true in the world.\n"
    "- ABSTENTION: the claim does NOT make a substantive factual assertion about the topic; "
    "instead it states that the evidence/sources do NOT contain or do NOT discuss the requested "
    "information (e.g. 'the sources provided do not contain information about X', 'the evidence "
    "does not discuss Y'). These are the model correctly declining to answer, not factual claims "
    "to verify. Label them ABSTENTION regardless of whether the absence is technically accurate.\n"
    "Judge ONLY against the given evidence, not your own knowledge."
)

USER_TEMPLATE = (
    "EVIDENCE:\n{evidence}\n\n"
    "CLAIM:\n{claim}\n\n"
    "Classify the CLAIM against the EVIDENCE as SUPPORTED, UNSUPPORTED, or ABSTENTION "
    "(see the three definitions above).\n"
    "Respond with ONLY a JSON object, no other text:\n"
    '{{"label": "SUPPORTED" or "UNSUPPORTED" or "ABSTENTION", "rationale": "one short sentence"}}'
)


def key(r):
    return f'{r["qid"]}|{r["arm"]}|{r["claim_index"]}'


def load_existing():
    if DRAFT_OUT.exists():
        with open(DRAFT_OUT, encoding="utf-8") as f:
            data = json.load(f)
        return {key(r): r for r in data}
    return {}


def call_model(client, api_key, model, claim, evidence, max_retries=4):
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_TEMPLATE.format(evidence=evidence, claim=claim)},
        ],
        "temperature": 0.0,
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    delay = 2.0
    for attempt in range(max_retries):
        try:
            resp = client.post(OPENROUTER_URL, json=body, headers=headers, timeout=90)
            if resp.status_code == 429:
                print(f"    rate-limited, backing off {delay:.0f}s...")
                time.sleep(delay)
                delay *= 2
                continue
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"].strip()
            return parse_label(content)
        except httpx.HTTPStatusError as e:
            if attempt == max_retries - 1:
                raise
            print(f"    HTTP {e.response.status_code}, retry in {delay:.0f}s...")
            time.sleep(delay)
            delay *= 2
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"    error {type(e).__name__}, retry in {delay:.0f}s...")
            time.sleep(delay)
            delay *= 2
    raise RuntimeError("exhausted retries")


def parse_label(content):
    """Extract {label, rationale} from the model output, tolerating prose/markdown wrapping."""
    txt = content.strip()
    # strip code fences
    if txt.startswith("```"):
        txt = txt.strip("`")
        if txt.lower().startswith("json"):
            txt = txt[4:]
    # find first {...}
    start = txt.find("{")
    end = txt.rfind("}")
    if start != -1 and end != -1:
        try:
            obj = json.loads(txt[start:end + 1])
            label = str(obj.get("label", "")).upper().strip()
            if label not in {"SUPPORTED", "UNSUPPORTED", "ABSTENTION"}:
                # normalize common variants
                if "ABSTAIN" in label or "ABSTENTION" in label:
                    label = "ABSTENTION"
                elif "UNSUP" in label:
                    label = "UNSUPPORTED"
                elif "SUP" in label:
                    label = "SUPPORTED"
                else:
                    label = "PARSE_ERROR"
            return label, str(obj.get("rationale", "")).strip()
        except json.JSONDecodeError:
            pass
    # last-ditch keyword scan (check ABSTENTION first — it's the most specific)
    up = txt.upper()
    if "ABSTENTION" in up or "ABSTAIN" in up:
        return "ABSTENTION", txt[:120]
    if "UNSUPPORTED" in up:
        return "UNSUPPORTED", txt[:120]
    if "SUPPORTED" in up:
        return "SUPPORTED", txt[:120]
    return "PARSE_ERROR", txt[:120]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--limit", type=int, default=0, help="0 = all; >0 = smoke test on first N")
    ap.add_argument("--sleep", type=float, default=0.3, help="pause between calls (politeness)")
    args = ap.parse_args()

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise SystemExit("OPENROUTER_API_KEY not set (check .env / set it in this shell).")

    with open(BLIND_IN, encoding="utf-8") as f:
        candidates = json.load(f)
    if args.limit > 0:
        candidates = candidates[: args.limit]

    existing = load_existing()
    # Treat API_ERROR / PARSE_ERROR records as NOT done, so a re-run retries them.
    retryable = {k for k, r in existing.items()
                 if r.get("draft_label") in {"API_ERROR", "PARSE_ERROR"}}
    print(f"Drafting labels with {args.model}")
    print(f"{len(candidates)} candidates, {len(existing)} recorded "
          f"({len(retryable)} of those are errors to retry).\n")

    # keep only successful existing records; errors will be re-attempted and overwritten
    results = [r for k, r in existing.items() if k not in retryable]
    done_keys = {k for k in existing.keys() if k not in retryable}

    with httpx.Client() as client:
        for i, c in enumerate(candidates, 1):
            k = key(c)
            if k in done_keys:
                continue
            try:
                label, rationale = call_model(
                    client, api_key, args.model, c["claim_text"], c["evidence_text"]
                )
            except Exception as e:
                # Write a failure record (don't silently drop it) so failed items remain
                # visible and reviewable — a missing record in a gold set is a silent gap.
                rec = {
                    "key": k,
                    "qid": c["qid"],
                    "arm": c["arm"],
                    "claim_index": c["claim_index"],
                    "claim_text": c["claim_text"],
                    "evidence_text": c["evidence_text"],
                    "draft_provider": "OpenRouter",
                    "draft_model": args.model,
                    "draft_label": "API_ERROR",
                    "draft_rationale": str(e)[:300],
                    "final_label": None,
                }
                results.append(rec)
                done_keys.add(k)
                with open(DRAFT_OUT, "w", encoding="utf-8") as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
                print(f"  [{i}/{len(candidates)}] {k} API_ERROR: {e}")
                continue

            rec = {
                "key": k,
                "qid": c["qid"],
                "arm": c["arm"],
                "claim_index": c["claim_index"],
                "claim_text": c["claim_text"],
                "evidence_text": c["evidence_text"],
                "draft_provider": "OpenRouter",
                "draft_model": args.model,
                "draft_label": label,         # model's blind draft (NOT the gold label)
                "draft_rationale": rationale,
                "final_label": None,          # <-- HUMAN fills/confirms this in review = the gold label
            }
            results.append(rec)
            done_keys.add(k)

            # resumable: write after every item
            with open(DRAFT_OUT, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

            flag = "" if label != "PARSE_ERROR" else "  <-- PARSE_ERROR, check manually"
            print(f"  [{i}/{len(candidates)}] {k}: {label}{flag}")
            time.sleep(args.sleep)

    # summary
    counts = {}
    for r in results:
        counts[r["draft_label"]] = counts.get(r["draft_label"], 0) + 1
    print(f"\nDone. {len(results)} drafted.")
    print("Draft label distribution:")
    for lab, n in sorted(counts.items()):
        print(f"  {lab:14s} {n}")
    perr = counts.get("PARSE_ERROR", 0)
    if perr:
        print(f"\n{perr} parse errors — review those manually in gold_drafted.json.")
    print(f"\nWrote {DRAFT_OUT}. Next: human review — set final_label for each record.")


if __name__ == "__main__":
    main()
