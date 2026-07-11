"""
backend/app/services/label_distill_claims.py

STEP 6 of arXiv distillation:
Teacher-label extracted claims for verifier distillation and draft-label the gold set.

Inputs:
  data/distill_arxiv/distill_train_claims.json
  data/distill_arxiv/gold_eval_claims.json

Outputs:
  data/distill_arxiv/distill_train_teacher_labeled.json
  data/distill_arxiv/gold_eval_teacher_drafted.json
  data/distill_arxiv/teacher_label_summary.json

Labels:
  SUPPORTED
  UNSUPPORTED
  ABSTENTION

Design:
  - Distillation train labels are teacher labels only.
  - Gold labels are draft labels only; final_label stays None until human review.
  - Resumable: writes after every claim.
  - Retryable: API_ERROR/PARSE_ERROR records are retried on rerun.
  - Uses OpenRouter via httpx and OPENROUTER_API_KEY from .env.

Run from backend/:
  python -m app.services.label_distill_claims --which train --limit 5
  python -m app.services.label_distill_claims --which gold --limit 5
  python -m app.services.label_distill_claims --which all

Recommended model can be set:
  set OPENROUTER_MODEL=google/gemini-2.5-flash-lite
  python -m app.services.label_distill_claims --which all
"""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from typing import Any

import httpx

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


DATA = Path("data")
DISTILL_DIR = DATA / "distill_arxiv"

TRAIN_IN = DISTILL_DIR / "distill_train_claims.json"
GOLD_IN = DISTILL_DIR / "gold_eval_claims.json"

TRAIN_OUT = DISTILL_DIR / "distill_train_teacher_labeled.json"
GOLD_OUT = DISTILL_DIR / "gold_eval_teacher_drafted.json"
SUMMARY_OUT = DISTILL_DIR / "teacher_label_summary.json"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash-lite")

VALID_LABELS = {"SUPPORTED", "UNSUPPORTED", "ABSTENTION"}
RETRYABLE_LABELS = {"API_ERROR", "PARSE_ERROR"}


SYSTEM_PROMPT = (
    "You are a careful scientific fact-checker. You judge whether a CLAIM is faithful to "
    "the EVIDENCE passage it is supposed to be grounded in. There are THREE possible verdicts:\n\n"
    "SUPPORTED:\n"
    "- Every factual assertion in the claim is directly supported by, or clearly inferable from, "
    "the evidence.\n\n"
    "UNSUPPORTED:\n"
    "- The claim states something not supported by the evidence, including added details, "
    "overstated scope, wrong numbers, wrong comparisons, wrong method/result names, or fabricated "
    "details. Label it UNSUPPORTED even if the claim sounds plausible or may be true elsewhere.\n\n"
    "ABSTENTION:\n"
    "- The claim does not make a substantive factual assertion about the topic. Instead, it says "
    "the evidence/sources do not contain or do not discuss the requested information, or it refuses "
    "to answer due to lack of evidence. Label these ABSTENTION.\n\n"
    "Judge ONLY against the given evidence. Do not use outside knowledge."
)

USER_TEMPLATE = (
    "EVIDENCE:\n"
    "{evidence}\n\n"
    "CLAIM:\n"
    "{claim}\n\n"
    "Classify the CLAIM against the EVIDENCE as SUPPORTED, UNSUPPORTED, or ABSTENTION.\n"
    "Respond with ONLY a JSON object, no markdown, no prose:\n"
    '{{"label": "SUPPORTED" or "UNSUPPORTED" or "ABSTENTION", '
    '"rationale": "one short sentence explaining the decision"}}'
)


def load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def get_claim_id(r: dict[str, Any]) -> str:
    if r.get("claim_id"):
        return str(r["claim_id"])

    split = r.get("split", "unknown")
    qid = r.get("qid", "q")
    variant = r.get("answer_variant", "answer")
    idx = r.get("claim_index", 0)
    return f"{split}_q{qid}_{variant}_c{idx}"


def get_claim_text(r: dict[str, Any]) -> str:
    return str(r.get("claim") or r.get("claim_text") or "").strip()


def get_evidence_text(r: dict[str, Any]) -> str:
    # Preferred field created by build_distill_claims.py
    txt = str(r.get("evidence_text_for_verifier") or "").strip()
    if txt:
        return txt

    # Fallback: concatenate evidence list if present.
    ev = r.get("evidence")
    if isinstance(ev, list):
        parts = []
        for e in ev:
            if not isinstance(e, dict):
                continue
            number = e.get("number", "?")
            title = e.get("title", "")
            text = e.get("text", "")
            if text:
                parts.append(f"[{number}] {title}\n{text}".strip())
        return "\n\n".join(parts).strip()

    return str(r.get("evidence_text") or "").strip()


def load_existing(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}

    data = load_json(path)
    if not isinstance(data, list):
        return {}

    out: dict[str, dict[str, Any]] = {}
    for r in data:
        if not isinstance(r, dict):
            continue
        cid = str(r.get("claim_id") or r.get("key") or "")
        if cid:
            out[cid] = r

    return out


def parse_label(content: str) -> tuple[str, str]:
    """
    Extract (label, rationale) from model output.

    The model is asked for JSON, but this tolerates fences/prose.
    """
    txt = (content or "").strip()

    if txt.startswith("```"):
        txt = txt.strip("`").strip()
        if txt.lower().startswith("json"):
            txt = txt[4:].strip()

    start = txt.find("{")
    end = txt.rfind("}")

    if start != -1 and end != -1 and end > start:
        try:
            obj = json.loads(txt[start : end + 1])
            label = str(obj.get("label", "")).upper().strip()
            rationale = str(obj.get("rationale", "")).strip()

            if label not in VALID_LABELS:
                if "ABSTAIN" in label or "ABSTENTION" in label:
                    label = "ABSTENTION"
                elif "UNSUP" in label or "NOT SUPPORTED" in label:
                    label = "UNSUPPORTED"
                elif "SUP" in label:
                    label = "SUPPORTED"
                else:
                    label = "PARSE_ERROR"

            return label, rationale

        except json.JSONDecodeError:
            pass

    up = txt.upper()
    if "ABSTENTION" in up or "ABSTAIN" in up:
        return "ABSTENTION", txt[:200]
    if "UNSUPPORTED" in up or "NOT SUPPORTED" in up:
        return "UNSUPPORTED", txt[:200]
    if "SUPPORTED" in up:
        return "SUPPORTED", txt[:200]

    return "PARSE_ERROR", txt[:200]


def call_teacher(
    client: httpx.Client,
    api_key: str,
    model: str,
    claim: str,
    evidence: str,
    max_evidence_chars: int,
    max_retries: int,
) -> tuple[str, str, str]:
    evidence = evidence[:max_evidence_chars]

    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_TEMPLATE.format(evidence=evidence, claim=claim)},
        ],
        "temperature": 0.0,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Verified Research Agent",
    }

    delay = 2.0

    for attempt in range(max_retries):
        try:
            resp = client.post(OPENROUTER_URL, json=body, headers=headers, timeout=120)

            if resp.status_code == 429:
                print(f"    rate-limited; sleeping {delay:.0f}s")
                time.sleep(delay)
                delay *= 2
                continue

            if resp.status_code == 402:
                # Payment/quota wall. Raise immediately so it is visible.
                raise httpx.HTTPStatusError(
                    "402 Payment Required from OpenRouter",
                    request=resp.request,
                    response=resp,
                )

            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"].strip()
            label, rationale = parse_label(content)
            return label, rationale, content

        except Exception as e:
            if attempt == max_retries - 1:
                raise

            print(f"    {type(e).__name__}; retrying in {delay:.0f}s")
            time.sleep(delay)
            delay *= 2

    raise RuntimeError("exhausted retries")


def make_output_record(
    source_record: dict[str, Any],
    label: str,
    rationale: str,
    raw_response: str,
    model: str,
    mode: str,
) -> dict[str, Any]:
    claim_id = get_claim_id(source_record)
    claim = get_claim_text(source_record)
    evidence_text = get_evidence_text(source_record)

    rec = dict(source_record)
    rec["claim_id"] = claim_id
    rec["claim"] = claim
    rec["claim_text"] = claim
    rec["evidence_text_for_verifier"] = evidence_text

    rec["teacher_provider"] = "OpenRouter"
    rec["teacher_model"] = model
    rec["teacher_label"] = label
    rec["teacher_rationale"] = rationale
    rec["teacher_raw_response"] = raw_response[:1000]

    # For gold, this is only a draft. Human review fills final_label.
    if mode == "gold":
        rec["final_label"] = rec.get("final_label", None)
    else:
        rec["distill_label"] = label

    return rec


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    counts: dict[str, int] = {}
    by_variant: dict[str, dict[str, int]] = {}
    by_qtype: dict[str, dict[str, int]] = {}

    for r in rows:
        lab = str(r.get("teacher_label", "MISSING"))
        counts[lab] = counts.get(lab, 0) + 1

        variant = str(r.get("answer_variant", "unknown"))
        by_variant.setdefault(variant, {})
        by_variant[variant][lab] = by_variant[variant].get(lab, 0) + 1

        qtype = str(r.get("question_type") or r.get("type") or "unknown")
        by_qtype.setdefault(qtype, {})
        by_qtype[qtype][lab] = by_qtype[qtype].get(lab, 0) + 1

    return {
        "n": len(rows),
        "label_counts": counts,
        "by_answer_variant": by_variant,
        "by_question_type": by_qtype,
    }


def label_file(
    in_path: Path,
    out_path: Path,
    model: str,
    mode: str,
    limit: int,
    sleep_s: float,
    max_evidence_chars: int,
    max_retries: int,
) -> list[dict[str, Any]]:
    if not in_path.exists():
        raise SystemExit(f"Missing input file: {in_path}")

    claims = load_json(in_path)
    if not isinstance(claims, list):
        raise SystemExit(f"{in_path} must be a JSON list")

    if limit > 0:
        claims = claims[:limit]

    existing = load_existing(out_path)

    retryable = {
        cid
        for cid, r in existing.items()
        if r.get("teacher_label") in RETRYABLE_LABELS
    }

    results_by_id: dict[str, dict[str, Any]] = {
        cid: r
        for cid, r in existing.items()
        if cid not in retryable
    }

    done_ids = set(results_by_id.keys())

    print(f"\nLabeling {mode}: {in_path}")
    print(f"Output: {out_path}")
    print(f"Model: {model}")
    print(f"Claims requested: {len(claims)}")
    print(f"Existing records: {len(existing)} ({len(retryable)} retryable errors)")

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise SystemExit("OPENROUTER_API_KEY not set. Check .env or environment variables.")

    with httpx.Client() as client:
        for i, c in enumerate(claims, start=1):
            claim_id = get_claim_id(c)

            if claim_id in done_ids:
                continue

            claim = get_claim_text(c)
            evidence = get_evidence_text(c)

            if not claim:
                label = "PARSE_ERROR"
                rationale = "Missing claim text."
                raw = ""
            elif not evidence:
                label = "UNSUPPORTED"
                rationale = "No evidence text was provided."
                raw = ""
            else:
                try:
                    label, rationale, raw = call_teacher(
                        client=client,
                        api_key=api_key,
                        model=model,
                        claim=claim,
                        evidence=evidence,
                        max_evidence_chars=max_evidence_chars,
                        max_retries=max_retries,
                    )

                except Exception as e:
                    label = "API_ERROR"
                    rationale = str(e)[:500]
                    raw = ""

            rec = make_output_record(
                source_record=c,
                label=label,
                rationale=rationale,
                raw_response=raw,
                model=model,
                mode=mode,
            )
            results_by_id[claim_id] = rec
            done_ids.add(claim_id)

            # Resumable write after every claim.
            save_json(out_path, list(results_by_id.values()))

            suffix = ""
            if label in RETRYABLE_LABELS:
                suffix = "  <-- retry/review"
            print(f"  [{i}/{len(claims)}] {claim_id}: {label}{suffix}")

            time.sleep(sleep_s)

    rows = list(results_by_id.values())
    save_json(out_path, rows)

    summary = summarize(rows)
    print("\nSummary:")
    print(json.dumps(summary, indent=2))
    print(f"Wrote {len(rows)} rows to {out_path}")

    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--which", choices=["train", "gold", "all"], default="all")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--limit", type=int, default=0, help="0=all; >0=smoke test on first N per selected file")
    ap.add_argument("--sleep", type=float, default=0.3)
    ap.add_argument("--max-evidence-chars", type=int, default=6000)
    ap.add_argument("--max-retries", type=int, default=4)
    args = ap.parse_args()

    all_summary: dict[str, Any] = {
        "model": args.model,
        "max_evidence_chars": args.max_evidence_chars,
        "outputs": {},
    }

    if args.which in {"train", "all"}:
        train_rows = label_file(
            in_path=TRAIN_IN,
            out_path=TRAIN_OUT,
            model=args.model,
            mode="train",
            limit=args.limit,
            sleep_s=args.sleep,
            max_evidence_chars=args.max_evidence_chars,
            max_retries=args.max_retries,
        )
        all_summary["outputs"]["train"] = summarize(train_rows)

    if args.which in {"gold", "all"}:
        gold_rows = label_file(
            in_path=GOLD_IN,
            out_path=GOLD_OUT,
            model=args.model,
            mode="gold",
            limit=args.limit,
            sleep_s=args.sleep,
            max_evidence_chars=args.max_evidence_chars,
            max_retries=args.max_retries,
        )
        all_summary["outputs"]["gold"] = summarize(gold_rows)

    save_json(SUMMARY_OUT, all_summary)

    print(f"\nWrote summary: {SUMMARY_OUT}")
    print("Next:")
    print("  - Train output is used for distillation.")
    print("  - Gold output is only a draft; human review must fill/confirm final_label.")


if __name__ == "__main__":
    main()
