"""
draft_grounded_hard_opus.py

Draft labels for the grounded-hard tranche claim pool using an Opus-class judge
through OpenRouter.

This is ONLY a draft/screen for stratified human review. It is not the final label.

Input:
  grounded_hard_claims.json

Outputs:
  grounded_hard_opus_draft.json
  grounded_hard_opus_draft_raw.jsonl
  grounded_hard_opus_draft_summary.json

Run from /workspace/project3, if OPENROUTER_API_KEY is available:
  python -u draft_grounded_hard_opus.py \
    --in grounded_hard_claims.json \
    --out grounded_hard_opus_draft.json \
    --raw grounded_hard_opus_draft_raw.jsonl \
    --summary grounded_hard_opus_draft_summary.json \
    --model anthropic/claude-opus-4.1 \
    --sleep 0.4

If the cluster has no key, copy grounded_hard_claims.json local and run from local backend
with OPENROUTER_API_KEY in .env or environment.

Labels:
  SUPPORTED:
    Every substantive factual assertion in the claim is directly supported by, or clearly
    inferable from, the provided evidence.
  UNSUPPORTED:
    The claim adds details, overstates scope, gives wrong specifics, attributes information
    to the evidence that is not there, or is contradicted by the evidence.
  ABSTENTION:
    The claim is a refusal / insufficient-evidence / "sources do not mention X" / meta
    non-answer rather than a substantive factual claim about the paper/topic.

Important:
  ABSTENTION is not the same as SUPPORTED.
  A true statement like "the sources do not mention X" is still ABSTENTION under this protocol.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

try:
    from openai import OpenAI
except Exception as e:
    raise SystemExit(
        "Missing openai package. Install with: python -m pip install openai python-dotenv --break-system-packages"
    ) from e


OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

ALLOWED = {"SUPPORTED", "UNSUPPORTED", "ABSTENTION"}

SYSTEM_PROMPT = """You are a careful scientific fact-checking judge.

You classify whether a CLAIM is faithful to the provided EVIDENCE.

Use exactly one of these labels:

SUPPORTED:
- Every substantive factual assertion in the claim is directly supported by, or clearly inferable from, the evidence.
- Minor wording differences are okay if the meaning is preserved.

UNSUPPORTED:
- The claim states something not supported by the evidence.
- This includes added details, overstated scope, wrong numbers, wrong method/result names, wrong comparisons, or claims that sound plausible but are absent from the evidence.
- Judge only against the evidence, not world knowledge.

ABSTENTION:
- The claim is not a substantive factual answer about the paper/topic.
- It is a refusal, insufficient-evidence statement, or meta statement such as "the sources do not mention X", "there is not enough information", or "the provided evidence does not discuss Y".
- Label these ABSTENTION even if the absence statement is technically accurate.

You must judge only the CLAIM against the EVIDENCE.
"""

USER_TEMPLATE = """QUESTION:
{question}

EVIDENCE:
{evidence}

CLAIM:
{claim}

Return only a JSON object:
{{
  "label": "SUPPORTED" or "UNSUPPORTED" or "ABSTENTION",
  "confidence": number from 0.0 to 1.0,
  "rationale": "one short sentence"
}}
"""


def load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    tmp.replace(path)


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_jsonl_existing(path: Path) -> dict[str, dict[str, Any]]:
    out = {}
    if not path.exists():
        return out
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            cid = str(r.get("claim_id") or "")
            if cid:
                out[cid] = r
    return out


def extract_json_object(text: str) -> dict[str, Any] | None:
    text = (text or "").strip()
    try:
        obj = json.loads(text)
        if isinstance(obj, dict):
            return obj
    except Exception:
        pass

    m = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not m:
        return None
    try:
        obj = json.loads(m.group(0))
        if isinstance(obj, dict):
            return obj
    except Exception:
        return None
    return None


def normalize_label(x: Any) -> str:
    s = str(x or "").strip().upper()
    s = re.sub(r"[^A-Z_]", "", s)
    if "ABSTENTION" in s:
        return "ABSTENTION"
    if "UNSUPPORTED" in s:
        return "UNSUPPORTED"
    if s == "SUPPORTED" or ("SUPPORTED" in s and "UNSUPPORTED" not in s):
        return "SUPPORTED"
    return ""


def clamp_conf(x: Any) -> float:
    try:
        v = float(x)
    except Exception:
        return 0.5
    return max(0.0, min(1.0, v))


def call_judge(
    client: OpenAI,
    model: str,
    claim: str,
    evidence: str,
    question: str,
    max_retries: int,
    timeout: float,
) -> dict[str, Any]:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": USER_TEMPLATE.format(
                question=question[:1200],
                evidence=evidence[:9000],
                claim=claim[:1800],
            ),
        },
    ]

    delay = 2.0
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0,
                max_tokens=250,
                timeout=timeout,
            )
            content = (resp.choices[0].message.content or "").strip()
            obj = extract_json_object(content)
            if not obj:
                raise ValueError(f"Could not parse JSON from response: {content[:500]}")

            label = normalize_label(obj.get("label"))
            if label not in ALLOWED:
                raise ValueError(f"Invalid label: {obj.get('label')} raw={content[:500]}")

            return {
                "label": label,
                "confidence": clamp_conf(obj.get("confidence")),
                "rationale": str(obj.get("rationale") or "").strip()[:1000],
                "raw_content": content,
            }

        except Exception as e:
            last_error = repr(e)
            print(f"  retry {attempt}/{max_retries}: {type(e).__name__}: {e}; sleeping {delay:.1f}s", flush=True)
            time.sleep(delay)
            delay = min(delay * 2, 60)

    return {
        "label": "UNSUPPORTED",
        "confidence": 0.0,
        "rationale": f"Judge failed after retries; defaulted to UNSUPPORTED for manual review. Last error: {last_error}",
        "raw_content": "",
        "error": last_error,
    }


def make_output_row(row: dict[str, Any], draft: dict[str, Any], model: str) -> dict[str, Any]:
    rr = dict(row)
    rr["opus_model"] = model
    rr["opus_label"] = draft["label"]
    rr["opus_confidence"] = draft["confidence"]
    rr["opus_rationale"] = draft["rationale"]
    rr["opus_raw_content"] = draft.get("raw_content", "")
    if draft.get("error"):
        rr["opus_error"] = draft["error"]
    return rr


def summarize(rows: list[dict[str, Any]], input_path: Path, out_path: Path, raw_path: Path, model: str) -> dict[str, Any]:
    by_label = Counter(r.get("opus_label") for r in rows)
    by_policy = defaultdict(Counter)
    by_template = defaultdict(Counter)
    by_variant = defaultdict(Counter)
    by_scope = defaultdict(Counter)

    for r in rows:
        lab = r.get("opus_label")
        by_policy[str(r.get("hard_policy") or "unknown")][lab] += 1
        by_template[str(r.get("question_template") or "unknown")][lab] += 1
        by_variant[str(r.get("answer_variant") or "unknown")][lab] += 1
        by_scope[str(r.get("evidence_scope") or "unknown")][lab] += 1

    return {
        "input": str(input_path),
        "output": str(out_path),
        "raw": str(raw_path),
        "model": model,
        "claims_total": len(rows),
        "label_counts": dict(by_label),
        "by_hard_policy": {k: dict(v) for k, v in sorted(by_policy.items())},
        "by_question_template": {k: dict(v) for k, v in sorted(by_template.items())},
        "by_answer_variant": {k: dict(v) for k, v in sorted(by_variant.items())},
        "by_evidence_scope": {k: dict(v) for k, v in sorted(by_scope.items())},
        "screening_protocol": {
            "opus_is_not_evaluated_model": True,
            "human_review_plan": "Review all Opus-flagged UNSUPPORTED plus a random sample of Opus-unflagged SUPPORTED/ABSTENTION rows; compute weighted metrics by stratum.",
            "evaluated_models_not_used_for_sampling": True,
        },
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="in_path", type=Path, default=Path("grounded_hard_claims.json"))
    ap.add_argument("--out", type=Path, default=Path("grounded_hard_opus_draft.json"))
    ap.add_argument("--raw", type=Path, default=Path("grounded_hard_opus_draft_raw.jsonl"))
    ap.add_argument("--summary", type=Path, default=Path("grounded_hard_opus_draft_summary.json"))
    ap.add_argument("--model", default=os.environ.get("OPUS_MODEL", "anthropic/claude-opus-4.1"))
    ap.add_argument("--sleep", type=float, default=0.4)
    ap.add_argument("--max-retries", type=int, default=5)
    ap.add_argument("--timeout", type=float, default=120)
    ap.add_argument("--limit", type=int, default=None, help="Debug limit; omit for full run.")
    args = ap.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise SystemExit(
            "OPENROUTER_API_KEY not found. Set it in the environment or .env. "
            "Do not commit the key."
        )

    claims = load_json(args.in_path)
    if not isinstance(claims, list):
        raise SystemExit(f"{args.in_path} must be a JSON list.")

    if args.limit is not None:
        claims = claims[: args.limit]

    existing = read_jsonl_existing(args.raw)
    print("\nDrafting grounded-hard Opus labels")
    print("=" * 72)
    print(f"Input claims: {len(claims)}")
    print(f"Existing raw: {len(existing)}")
    print(f"Model:        {args.model}")

    client = OpenAI(base_url=OPENROUTER_BASE_URL, api_key=api_key)

    drafted_map: dict[str, dict[str, Any]] = dict(existing)
    completed = 0

    for i, row in enumerate(claims, start=1):
        cid = str(row.get("claim_id"))
        if cid in drafted_map:
            continue

        claim = str(row.get("claim") or "")
        evidence = str(row.get("evidence_text_for_verifier") or "")
        question = str(row.get("question") or "")

        print(f"[{i}/{len(claims)}] {cid}", flush=True)
        draft = call_judge(
            client=client,
            model=args.model,
            claim=claim,
            evidence=evidence,
            question=question,
            max_retries=args.max_retries,
            timeout=args.timeout,
        )

        out_row = make_output_row(row, draft, args.model)
        append_jsonl(args.raw, out_row)
        drafted_map[cid] = out_row
        completed += 1

        if completed % 25 == 0:
            ordered = [drafted_map[str(r.get("claim_id"))] for r in claims if str(r.get("claim_id")) in drafted_map]
            save_json(args.out, ordered)
            save_json(args.summary, summarize(ordered, args.in_path, args.out, args.raw, args.model))
            print(f"  checkpoint saved at completed={completed}, total_drafted={len(ordered)}", flush=True)

        time.sleep(args.sleep)

    ordered = [drafted_map[str(r.get("claim_id"))] for r in claims if str(r.get("claim_id")) in drafted_map]
    save_json(args.out, ordered)
    save_json(args.summary, summarize(ordered, args.in_path, args.out, args.raw, args.model))

    summary = summarize(ordered, args.in_path, args.out, args.raw, args.model)
    print("\nFinished Opus drafting")
    print("=" * 72)
    print(f"Drafted rows: {len(ordered)}")
    print(f"Label counts: {summary['label_counts']}")
    print(f"By policy:    {summary['by_hard_policy']}")
    print("\nWrote:")
    print(f"  {args.out}")
    print(f"  {args.raw}")
    print(f"  {args.summary}")


if __name__ == "__main__":
    main()
