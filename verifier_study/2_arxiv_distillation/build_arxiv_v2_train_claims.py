"""
backend/app/services/build_arxiv_v2_train_claims.py

Extract claims from merged v2 train answers.

Inputs:
  data/distill_arxiv_v2/train_answers_merged.json

Outputs:
  data/distill_arxiv_v2/train_claims.json
  data/distill_arxiv_v2/train_claims_summary.json

Uses:
  app.services.claim_extractor.extract_claims

Evidence policy:
  - cited claims: use cited evidence only when citations exist and match evidence numbers
  - uncited claims: use all retrieved evidence
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from app.services.claim_extractor import extract_claims


V2_DIR = Path("data") / "distill_arxiv_v2"

ANSWERS_IN = V2_DIR / "train_answers_merged.json"
CLAIMS_OUT = V2_DIR / "train_claims.json"
SUMMARY_OUT = V2_DIR / "train_claims_summary.json"


ANSWER_VARIANTS = ["plain_answer", "cited_answer"]


def load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def evidence_number_map(evidence: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    out = {}
    for i, ev in enumerate(evidence, start=1):
        if not isinstance(ev, dict):
            continue
        n = ev.get("number", ev.get("rank", i))
        try:
            n = int(n)
        except Exception:
            n = i
        out[n] = ev
    return out


def format_evidence_text(evidence: list[dict[str, Any]]) -> str:
    parts = []
    for i, ev in enumerate(evidence, start=1):
        if not isinstance(ev, dict):
            continue
        n = ev.get("number", ev.get("rank", i))
        title = str(ev.get("title") or "").strip()
        text = str(ev.get("text") or "").strip()
        if title or text:
            parts.append(f"[{n}] {title}\n{text}".strip())
    return "\n\n".join(parts)


def selected_evidence_for_claim(all_evidence: list[dict[str, Any]], citations: list[int]) -> tuple[list[dict[str, Any]], str]:
    if not citations:
        return all_evidence, "all_retrieved_evidence_uncited_claim"

    by_num = evidence_number_map(all_evidence)
    selected = []
    for c in citations:
        if c in by_num:
            selected.append(by_num[c])

    if selected:
        return selected, "cited_evidence"

    # If the model cites numbers that are not available, fall back to all evidence but mark it.
    return all_evidence, "all_retrieved_evidence_bad_citation_fallback"


def clean_variant_name(answer_variant: str) -> str:
    if answer_variant == "plain_answer":
        return "plain"
    if answer_variant == "cited_answer":
        return "cited"
    return answer_variant.replace("_answer", "")


def main() -> None:
    answers = load_json(ANSWERS_IN)
    if not isinstance(answers, list):
        raise SystemExit(f"{ANSWERS_IN} must be a JSON list.")

    claims = []
    per_row_counts = []

    for row in answers:
        train_row_id = row.get("train_row_id", row.get("qid", row.get("id")))
        qid = row.get("qid", train_row_id)
        qtype = row.get("type", "unknown")
        train_source = row.get("train_source", qtype)
        question = row.get("question", "")
        evidence = row.get("evidence", [])

        if not isinstance(evidence, list):
            evidence = []

        row_count = {
            "train_row_id": train_row_id,
            "qid": qid,
            "type": qtype,
            "train_source": train_source,
        }

        for answer_variant in ANSWER_VARIANTS:
            answer = str(row.get(answer_variant) or "").strip()
            extracted = extract_claims(answer)
            row_count[f"{clean_variant_name(answer_variant)}_claims"] = len(extracted)

            for idx, c in enumerate(extracted, start=1):
                claim_text = str(c.get("claim_text") or "").strip()
                citations = c.get("citations", [])
                if not isinstance(citations, list):
                    citations = []

                selected_evidence, evidence_scope = selected_evidence_for_claim(evidence, citations)
                evidence_text_for_verifier = format_evidence_text(selected_evidence)

                claim_id = f"v2_train_r{train_row_id}_{clean_variant_name(answer_variant)}_c{idx:03d}"

                claims.append({
                    "claim_id": claim_id,
                    "split": "distill_train_v2",
                    "train_row_id": train_row_id,
                    "qid": qid,
                    "original_qid": row.get("original_qid"),
                    "question": question,
                    "question_type": qtype,
                    "train_source": train_source,
                    "answer_variant": answer_variant,
                    "answer": answer,
                    "claim_index": idx,
                    "claim": claim_text,
                    "claim_text": claim_text,
                    "citations": sorted(set(int(x) for x in citations if str(x).isdigit())),
                    "evidence_scope": evidence_scope,
                    "evidence": selected_evidence,
                    "evidence_text_for_verifier": evidence_text_for_verifier,
                    "all_evidence": evidence,
                    "home_paper_id": row.get("home_paper_id"),
                    "home_corpus_paper_id": row.get("home_corpus_paper_id"),
                    "home_title": row.get("home_title"),
                })

        per_row_counts.append(row_count)

    label_counts = Counter()
    by_source = defaultdict(Counter)
    by_variant = defaultdict(Counter)
    by_scope = Counter()

    for c in claims:
        by_source[c["train_source"]]["claims"] += 1
        by_variant[c["answer_variant"]]["claims"] += 1
        by_scope[c["evidence_scope"]] += 1

    summary = {
        "input": str(ANSWERS_IN),
        "output": str(CLAIMS_OUT),
        "answer_rows": len(answers),
        "claims_total": len(claims),
        "claims_by_train_source": {k: dict(v) for k, v in by_source.items()},
        "claims_by_answer_variant": {k: dict(v) for k, v in by_variant.items()},
        "claims_by_evidence_scope": dict(by_scope),
        "per_answer_counts_preview": per_row_counts[:20],
    }

    save_json(CLAIMS_OUT, claims)
    save_json(SUMMARY_OUT, summary)

    print("\nExtracted v2 train claims")
    print("=" * 56)
    print(f"Answer rows:    {len(answers)}")
    print(f"Claims total:   {len(claims)}")
    print(f"By source:      {summary['claims_by_train_source']}")
    print(f"By variant:     {summary['claims_by_answer_variant']}")
    print(f"By scope:       {summary['claims_by_evidence_scope']}")
    print(f"Wrote:          {CLAIMS_OUT}")
    print(f"Wrote summary:  {SUMMARY_OUT}")

    if claims:
        print("\nFirst claim preview:")
        print(json.dumps(claims[0], ensure_ascii=False, indent=2)[:2500])


if __name__ == "__main__":
    main()
