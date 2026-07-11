"""
build_grounded_hard_claims.py

Extract claim-level rows from grounded_hard_answers.json.

Input:
  grounded_hard_answers.json
  grounded_hard_eval_inputs.json

Outputs:
  grounded_hard_claims.json
  grounded_hard_claims_summary.json

Run:
  python -u build_grounded_hard_claims.py \
    --answers grounded_hard_answers.json \
    --inputs grounded_hard_eval_inputs.json \
    --out grounded_hard_claims.json \
    --summary grounded_hard_claims_summary.json
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


SENT_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])")
CITE_RE = re.compile(r"\[(\d+(?:\s*,\s*\d+)*)\]")


def load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def normalize_space(s: Any) -> str:
    s = str(s or "")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def answer_text(row: dict[str, Any], variant: str) -> str:
    """
    Robustly retrieve plain/cited answer text from several possible generate_batch schemas.
    """
    variant_keys = {
        "plain_answer": [
            "plain_answer",
            "answer_plain",
            "plain",
            "answer",
            "response",
            "model_answer",
        ],
        "cited_answer": [
            "cited_answer",
            "answer_cited",
            "cited",
            "answer_with_citations",
            "response_cited",
            "model_answer_cited",
        ],
    }

    # Direct keys first.
    for k in variant_keys[variant]:
        if row.get(k):
            return normalize_space(row[k])

    # Nested possibilities.
    for parent in ["answers", "outputs", "generations", "responses"]:
        obj = row.get(parent)
        if isinstance(obj, dict):
            for k in variant_keys[variant]:
                if obj.get(k):
                    return normalize_space(obj[k])

    return ""


def map_inputs(inputs: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out = {}
    for r in inputs:
        for k in [r.get("qid"), r.get("id")]:
            if k is not None:
                out[str(k)] = r
    return out


def merge_answer_with_input(ans: dict[str, Any], input_map: dict[str, dict[str, Any]]) -> dict[str, Any]:
    for k in [ans.get("qid"), ans.get("id")]:
        if k is not None and str(k) in input_map:
            merged = dict(input_map[str(k)])
            merged.update(ans)
            # Keep input evidence if answer row lacks it.
            if not ans.get("evidence") and input_map[str(k)].get("evidence"):
                merged["evidence"] = input_map[str(k)]["evidence"]
            return merged
    return ans


def split_claims(text: str) -> list[str]:
    text = normalize_space(text)
    if not text:
        return []

    # Remove common preambles but keep substantive sentences.
    text = re.sub(r"^(Based on the provided sources?|According to the provided sources?|From the provided sources?),?\s*", "", text, flags=re.I)

    # Split bullets/newlines first, then sentences.
    rough_parts = []
    for part in re.split(r"(?:\n+|(?:^|\s)[\-*•]\s+|\s+\d+\.\s+)", text):
        part = normalize_space(part)
        if part:
            rough_parts.append(part)

    claims = []
    for part in rough_parts:
        for sent in SENT_SPLIT_RE.split(part):
            sent = normalize_space(sent)
            if not sent:
                continue

            # Strip leading connective fragments.
            sent = re.sub(r"^(and|also|however|therefore|thus|moreover|in addition),?\s+", "", sent, flags=re.I).strip()

            # Filter non-claims / too-short fragments.
            word_count = len(re.findall(r"\w+", sent))
            if word_count < 5:
                continue
            if sent.lower() in {"yes.", "no.", "not mentioned.", "not specified."}:
                continue

            claims.append(sent)

    # Deduplicate within answer while preserving order.
    seen = set()
    deduped = []
    for c in claims:
        key = re.sub(r"\W+", "", c.lower())
        if key in seen:
            continue
        seen.add(key)
        deduped.append(c)

    return deduped


def cited_numbers(claim: str) -> list[int]:
    nums = []
    for m in CITE_RE.finditer(claim):
        raw = m.group(1)
        for x in raw.split(","):
            try:
                nums.append(int(x.strip()))
            except ValueError:
                pass
    return sorted(set(nums))


def strip_citations(claim: str) -> str:
    return normalize_space(CITE_RE.sub("", claim))


def evidence_for_claim(row: dict[str, Any], variant: str, claim: str) -> tuple[list[dict[str, Any]], str]:
    evidence = list(row.get("evidence", []) or [])
    if variant == "cited_answer":
        nums = cited_numbers(claim)
        if nums:
            selected = []
            for e in evidence:
                n = e.get("number") or e.get("rank")
                try:
                    n = int(n)
                except Exception:
                    n = None
                if n in nums:
                    selected.append(e)
            if selected:
                return selected, "cited_evidence"

    return evidence, "all_retrieved_evidence_uncited_claim"


def evidence_text(evidence: list[dict[str, Any]]) -> str:
    chunks = []
    for i, e in enumerate(evidence, start=1):
        num = e.get("number") or e.get("rank") or i
        title = normalize_space(e.get("title"))
        text = normalize_space(e.get("text"))
        chunks.append(f"[{num}] {title}\n{text}".strip())
    return "\n\n".join(chunks)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--answers", type=Path, default=Path("grounded_hard_answers.json"))
    ap.add_argument("--inputs", type=Path, default=Path("grounded_hard_eval_inputs.json"))
    ap.add_argument("--out", type=Path, default=Path("grounded_hard_claims.json"))
    ap.add_argument("--summary", type=Path, default=Path("grounded_hard_claims_summary.json"))
    args = ap.parse_args()

    answers = load_json(args.answers)
    inputs = load_json(args.inputs)
    if not isinstance(answers, list):
        raise SystemExit(f"{args.answers} must be a JSON list.")
    if not isinstance(inputs, list):
        raise SystemExit(f"{args.inputs} must be a JSON list.")

    input_map = map_inputs(inputs)

    claims = []
    answer_rows_with_no_claims = []

    for ans in answers:
        row = merge_answer_with_input(ans, input_map)

        for variant in ["plain_answer", "cited_answer"]:
            text = answer_text(row, variant)
            extracted = split_claims(text)

            if not extracted:
                answer_rows_with_no_claims.append({
                    "qid": row.get("qid") or row.get("id"),
                    "variant": variant,
                    "text_preview": text[:300],
                })

            for local_idx, claim_raw in enumerate(extracted, start=1):
                ev, scope = evidence_for_claim(row, variant, claim_raw)
                claim_clean = strip_citations(claim_raw)

                claim_id = f"gh_{row.get('qid') or row.get('id')}_{variant}_{local_idx}"

                claims.append({
                    "claim_id": claim_id,
                    "qid": row.get("qid") or row.get("id"),
                    "source_answer_id": row.get("id"),
                    "split": "grounded_hard_tranche_pool",
                    "question_type": "grounded_hard",
                    "answer_variant": variant,
                    "evidence_scope": scope,
                    "hard_policy": row.get("hard_policy"),
                    "question_template": row.get("question_template"),
                    "question": row.get("question"),
                    "home_paper_id": row.get("home_paper_id"),
                    "home_corpus_paper_id": row.get("home_corpus_paper_id"),
                    "home_title": row.get("home_title"),
                    "claim": claim_clean,
                    "claim_with_citations": claim_raw,
                    "answer_text": text,
                    "evidence": ev,
                    "evidence_text_for_verifier": evidence_text(ev),
                    "construction_notes": row.get("construction_notes"),
                    "policy_meta": row.get("policy_meta"),
                })

    summary = {
        "input_answers": len(answers),
        "input_eval_inputs": len(inputs),
        "claims_total": len(claims),
        "claims_by_answer_variant": dict(Counter(c["answer_variant"] for c in claims)),
        "claims_by_hard_policy": dict(Counter(c.get("hard_policy") for c in claims)),
        "claims_by_template": dict(Counter(c.get("question_template") for c in claims)),
        "claims_by_evidence_scope": dict(Counter(c.get("evidence_scope") for c in claims)),
        "answer_rows_with_no_claims_count": len(answer_rows_with_no_claims),
        "answer_rows_with_no_claims_sample": answer_rows_with_no_claims[:20],
        "no_evaluated_model_used_for_sampling": True,
        "notes": [
            "These are unlabeled claim candidates for Opus-assisted stratified human review.",
            "ABSTENTION/refusal/meta statements should later be labeled separately and excluded from binary metrics.",
        ],
    }

    save_json(args.out, claims)
    save_json(args.summary, summary)

    print("\nBuilt grounded-hard claims")
    print("=" * 72)
    print(f"Input answers:       {len(answers)}")
    print(f"Claims total:        {len(claims)}")
    print(f"By variant:          {summary['claims_by_answer_variant']}")
    print(f"By policy:           {summary['claims_by_hard_policy']}")
    print(f"By evidence scope:   {summary['claims_by_evidence_scope']}")
    print(f"No-claim answers:    {len(answer_rows_with_no_claims)}")
    print("\nExample claim:")
    if claims:
        ex = claims[0]
        print(json.dumps({
            "claim_id": ex["claim_id"],
            "question": ex["question"],
            "hard_policy": ex["hard_policy"],
            "answer_variant": ex["answer_variant"],
            "claim": ex["claim"],
            "evidence_titles": [e.get("title") for e in ex["evidence"]],
        }, ensure_ascii=False, indent=2))
    print("\nWrote:")
    print(f"  {args.out}")
    print(f"  {args.summary}")


if __name__ == "__main__":
    main()
