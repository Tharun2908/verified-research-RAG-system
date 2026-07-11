"""
backend/app/services/label_arxiv_v2_train_claims_non_opus.py

Teacher-label clean arXiv v2 train claims using a strong NON-OPUS model through OpenRouter.

Default teacher:
  meta-llama/llama-3.3-70b-instruct

Why non-Opus:
  Opus is reserved for gold drafting only. Train teacher and gold drafter should be
  different model families to avoid "student trained on Opus, evaluated by Opus-shaped gold."

Input:
  data/distill_arxiv_v2/train_claims_no_protected_overlap.json

Output:
  data/distill_arxiv_v2/train_teacher_labeled_non_opus.json
  data/distill_arxiv_v2/train_teacher_label_raw_non_opus.jsonl
  data/distill_arxiv_v2/train_teacher_label_summary_non_opus.json

Labels:
  SUPPORTED    - the evidence entails the claim
  UNSUPPORTED  - the claim is contradicted or not supported by the evidence
  ABSTENTION   - refusal/insufficient-evidence statement/no substantive factual claim

Run from backend/:
  set OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct
  python -m app.services.label_arxiv_v2_train_claims_non_opus --limit 8 --batch-size 4
  python -m app.services.label_arxiv_v2_train_claims_non_opus --batch-size 4 --sleep 0.25
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from collections import Counter
from pathlib import Path
from typing import Any

import httpx

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


V2_DIR = Path("data") / "distill_arxiv_v2"

DEFAULT_IN = V2_DIR / "train_claims_no_protected_overlap.json"
DEFAULT_OUT = V2_DIR / "train_teacher_labeled_non_opus.json"
DEFAULT_RAW = V2_DIR / "train_teacher_label_raw_non_opus.jsonl"
DEFAULT_SUMMARY = V2_DIR / "train_teacher_label_summary_non_opus.json"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct")

VALID_LABELS = {"SUPPORTED", "UNSUPPORTED", "ABSTENTION"}


SYSTEM_PROMPT = """You are a strict claim-level faithfulness judge for scientific retrieval-augmented generation.

Your task is to label whether each CLAIM is supported by its EVIDENCE.

Allowed labels:
- SUPPORTED: The evidence directly supports or entails the claim.
- UNSUPPORTED: The claim is contradicted by the evidence, adds specific details not present in the evidence, gives unsupported numbers/results, or makes a factual claim that cannot be verified from the evidence.
- ABSTENTION: The claim is not a substantive factual answer claim, or it is a refusal/insufficient-evidence statement such as "the provided evidence does not contain enough information."

Rules:
- Use only the provided evidence.
- Do not use outside knowledge.
- Be strict with exact numbers, dataset sizes, benchmark names, method names, and comparisons.
- If a claim combines multiple facts and any important part is unsupported, label UNSUPPORTED.
- If the answer says the evidence is insufficient, label ABSTENTION unless it also adds unsupported factual details.
- Return valid JSON only.
"""

USER_TEMPLATE = """Label the following {n} claim(s).

Return exactly a JSON array. Each element must have:
- claim_id: string
- label: one of SUPPORTED, UNSUPPORTED, ABSTENTION
- confidence: number from 0 to 1
- rationale: one short sentence

CLAIMS:
{items_json}
"""


def load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def append_jsonl(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def truncate_text(s: Any, max_chars: int) -> str:
    s = str(s or "").strip()
    if len(s) <= max_chars:
        return s
    return s[:max_chars].rstrip() + "\n...[TRUNCATED]"


def normalize_label(label: Any) -> str:
    s = str(label or "").strip().upper()
    s = re.sub(r"[^A-Z_]+", "", s)

    if s in VALID_LABELS:
        return s

    # Common aliases.
    if s in {"SUPPORT", "SUPPORTEDBYEVIDENCE", "ENTAILS", "ENTAILED"}:
        return "SUPPORTED"
    if s in {"NOTSUPPORTED", "INSUFFICIENT", "UNVERIFIED", "HALLUCINATED", "CONTRADICTED", "REFUTED"}:
        return "UNSUPPORTED"
    if s in {"REFUSAL", "NOCLAIM", "NOFACTUALCLAIM", "NOTACLAIM"}:
        return "ABSTENTION"

    return "UNSUPPORTED"


def parse_json_array(content: str) -> list[dict[str, Any]]:
    txt = (content or "").strip()

    if txt.startswith("```"):
        txt = txt.strip("`").strip()
        if txt.lower().startswith("json"):
            txt = txt[4:].strip()

    # First try full JSON.
    try:
        obj = json.loads(txt)
        if isinstance(obj, list):
            return [x for x in obj if isinstance(x, dict)]
        if isinstance(obj, dict):
            for key in ["labels", "results", "items", "outputs"]:
                if isinstance(obj.get(key), list):
                    return [x for x in obj[key] if isinstance(x, dict)]
    except Exception:
        pass

    # Then try first JSON array substring.
    start = txt.find("[")
    end = txt.rfind("]")
    if start != -1 and end != -1 and end > start:
        try:
            arr = json.loads(txt[start : end + 1])
            if isinstance(arr, list):
                return [x for x in arr if isinstance(x, dict)]
        except Exception:
            pass

    raise ValueError("Could not parse JSON array from model response.")


def compact_claim_for_prompt(c: dict[str, Any], max_evidence_chars: int) -> dict[str, Any]:
    return {
        "claim_id": c.get("claim_id"),
        "question": truncate_text(c.get("question"), 700),
        "answer_variant": c.get("answer_variant"),
        "train_source": c.get("train_source"),
        "claim": truncate_text(c.get("claim") or c.get("claim_text"), 1200),
        "evidence_scope": c.get("evidence_scope"),
        "evidence": truncate_text(c.get("evidence_text_for_verifier"), max_evidence_chars),
    }


def call_openrouter(
    client: httpx.Client,
    api_key: str,
    model: str,
    batch: list[dict[str, Any]],
    max_evidence_chars: int,
    max_retries: int,
) -> tuple[list[dict[str, Any]], str]:
    items = [compact_claim_for_prompt(c, max_evidence_chars=max_evidence_chars) for c in batch]

    user_prompt = USER_TEMPLATE.format(
        n=len(items),
        items_json=json.dumps(items, ensure_ascii=False, indent=2),
    )

    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0,
        "max_tokens": max(800, 300 * len(items)),
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Verified Research Agent",
    }

    delay = 2.0
    last_content = ""
    for attempt in range(max_retries):
        try:
            resp = client.post(OPENROUTER_URL, json=body, headers=headers, timeout=180)

            if resp.status_code == 429:
                print(f"    rate-limited; sleeping {delay:.0f}s")
                time.sleep(delay)
                delay *= 2
                continue

            resp.raise_for_status()
            last_content = resp.json()["choices"][0]["message"]["content"].strip()
            parsed = parse_json_array(last_content)
            return parsed, last_content

        except Exception as e:
            if attempt == max_retries - 1:
                raise RuntimeError(f"{type(e).__name__}: {e}; last_content={last_content[:500]}")
            print(f"    {type(e).__name__}; retry in {delay:.0f}s")
            time.sleep(delay)
            delay *= 2

    raise RuntimeError("OpenRouter labeling failed after retries.")


def load_existing_labels(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    data = load_json(path)
    if not isinstance(data, list):
        return []
    return data


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, default=DEFAULT_IN)
    ap.add_argument("--output", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--raw-output", type=Path, default=DEFAULT_RAW)
    ap.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--batch-size", type=int, default=4)
    ap.add_argument("--sleep", type=float, default=0.25)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--max-evidence-chars", type=int, default=6000)
    ap.add_argument("--max-retries", type=int, default=4)
    args = ap.parse_args()

    model_lower = args.model.lower()
    if "opus" in model_lower or "anthropic/claude" in model_lower:
        raise SystemExit(
            f"Refusing to use model={args.model!r} for train labels. "
            "Train teacher must be non-Opus/non-Claude. Use Llama/Gemini/GPT-class instead."
        )

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise SystemExit("OPENROUTER_API_KEY not set. Check backend/.env or shell environment.")

    claims = load_json(args.input)
    if not isinstance(claims, list):
        raise SystemExit(f"{args.input} must be a JSON list.")

    if args.limit > 0:
        claims = claims[: args.limit]

    existing = load_existing_labels(args.output)
    by_id = {str(x.get("claim_id")): x for x in existing if x.get("claim_id")}

    todo = [c for c in claims if str(c.get("claim_id")) not in by_id]

    print("\nLabeling arXiv v2 train claims with NON-OPUS teacher")
    print("=" * 72)
    print(f"Input claims:        {len(claims)}")
    print(f"Existing labels:     {len(by_id)}")
    print(f"Todo:                {len(todo)}")
    print(f"Model:               {args.model}")
    print(f"Batch size:          {args.batch_size}")

    with httpx.Client() as client:
        for start in range(0, len(todo), args.batch_size):
            batch = todo[start : start + args.batch_size]
            batch_ids = [str(c.get("claim_id")) for c in batch]

            try:
                parsed, raw_content = call_openrouter(
                    client=client,
                    api_key=api_key,
                    model=args.model,
                    batch=batch,
                    max_evidence_chars=args.max_evidence_chars,
                    max_retries=args.max_retries,
                )
            except Exception as e:
                # Save a failure record and stop so resume is safe.
                append_jsonl(args.raw_output, {
                    "status": "error",
                    "model": args.model,
                    "batch_ids": batch_ids,
                    "error": str(e),
                })
                raise

            parsed_by_id = {str(x.get("claim_id")): x for x in parsed if x.get("claim_id")}

            labeled_this_batch = []
            for c in batch:
                cid = str(c.get("claim_id"))
                pred = parsed_by_id.get(cid)

                if pred is None:
                    # Conservative fallback if the model omitted one item.
                    pred = {
                        "claim_id": cid,
                        "label": "UNSUPPORTED",
                        "confidence": 0.0,
                        "rationale": "Model response omitted this claim; marked unsupported for manual review.",
                    }

                label = normalize_label(pred.get("label"))
                try:
                    conf = float(pred.get("confidence", 0.0))
                except Exception:
                    conf = 0.0
                conf = max(0.0, min(1.0, conf))

                out = dict(c)
                out["teacher_model"] = args.model
                out["teacher_label"] = label
                out["teacher_confidence"] = conf
                out["teacher_rationale"] = str(pred.get("rationale") or "").strip()
                out["teacher_label_source"] = "non_opus_openrouter"
                out["needs_manual_review"] = pred is None or conf < 0.55

                by_id[cid] = out
                labeled_this_batch.append(out)

            append_jsonl(args.raw_output, {
                "status": "ok",
                "model": args.model,
                "batch_ids": batch_ids,
                "raw_content": raw_content,
                "parsed": parsed,
            })

            # Preserve original input order in output.
            ordered = [by_id[str(c.get("claim_id"))] for c in claims if str(c.get("claim_id")) in by_id]
            save_json(args.output, ordered)

            done = len(by_id)
            counts = Counter(x.get("teacher_label", "UNKNOWN") for x in ordered)
            print(f"  labeled {done}/{len(claims)} | batch={len(batch)} | counts={dict(counts)}", flush=True)

            time.sleep(args.sleep)

    ordered = [by_id[str(c.get("claim_id"))] for c in claims if str(c.get("claim_id")) in by_id]
    counts = Counter(x.get("teacher_label", "UNKNOWN") for x in ordered)
    by_source = {}
    for src in sorted(set(x.get("train_source", "unknown") for x in ordered)):
        by_source[src] = dict(Counter(x.get("teacher_label", "UNKNOWN") for x in ordered if x.get("train_source", "unknown") == src))

    by_variant = {}
    for var in sorted(set(x.get("answer_variant", "unknown") for x in ordered)):
        by_variant[var] = dict(Counter(x.get("teacher_label", "UNKNOWN") for x in ordered if x.get("answer_variant", "unknown") == var))

    summary = {
        "input": str(args.input),
        "output": str(args.output),
        "raw_output": str(args.raw_output),
        "model": args.model,
        "claims_seen": len(claims),
        "claims_labeled": len(ordered),
        "label_counts": dict(counts),
        "label_counts_by_train_source": by_source,
        "label_counts_by_answer_variant": by_variant,
        "binary_usable_supported_unsupported": counts.get("SUPPORTED", 0) + counts.get("UNSUPPORTED", 0),
        "unsupported_train_count": counts.get("UNSUPPORTED", 0),
        "abstention_count": counts.get("ABSTENTION", 0),
        "positive_gate_train_unsupported_target": 150,
        "positive_gate_pass": counts.get("UNSUPPORTED", 0) >= 150,
    }

    save_json(args.summary_output, summary)

    print("\nDone.")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
