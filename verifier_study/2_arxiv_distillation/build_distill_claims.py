"""
backend/app/services/build_distill_claims.py

STEP 4 of arXiv distillation:
Extract sentence-level claims from generated Mistral answers.

Inputs:
  data/distill_arxiv/distill_train_answers.json
  data/distill_arxiv/gold_eval_answers.json

Outputs:
  data/distill_arxiv/distill_train_claims.json
  data/distill_arxiv/gold_eval_claims.json
  data/distill_arxiv/distill_claims_summary.json

For each answer record, this extracts claims from BOTH:
  - plain_answer
  - cited_answer

Each claim keeps:
  - claim text
  - citation numbers found in that sentence
  - cited evidence if citations exist
  - all retrieved evidence as fallback/context
  - evidence_text_for_verifier:
      cited evidence text if citations exist, otherwise all retrieved evidence text

Run from backend/:
  python -m app.services.build_distill_claims --limit 3
  python -m app.services.build_distill_claims
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from app.services.claim_extractor import extract_claims


DATA = Path("data")
DISTILL_DIR = DATA / "distill_arxiv"

TRAIN_ANSWERS = DISTILL_DIR / "distill_train_answers.json"
GOLD_ANSWERS = DISTILL_DIR / "gold_eval_answers.json"

TRAIN_OUT = DISTILL_DIR / "distill_train_claims.json"
GOLD_OUT = DISTILL_DIR / "gold_eval_claims.json"
SUMMARY_OUT = DISTILL_DIR / "distill_claims_summary.json"

ANSWER_VARIANTS = ["plain_answer", "cited_answer"]


def load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def evidence_number_map(evidence: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    out: dict[int, dict[str, Any]] = {}
    for ev in evidence:
        try:
            number = int(ev.get("number"))
        except Exception:
            continue
        out[number] = ev
    return out


def compact_evidence(ev: dict[str, Any]) -> dict[str, Any]:
    """Keep the evidence fields needed downstream without changing the schema too much."""
    return {
        "number": ev.get("number"),
        "title": ev.get("title"),
        "text": ev.get("text"),
        "chunk_id": ev.get("chunk_id"),
        "score": ev.get("score"),
        "resolved_corpus_paper_id": ev.get("resolved_corpus_paper_id"),
    }


def join_evidence_text(evidence: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for ev in evidence:
        number = ev.get("number")
        title = ev.get("title") or "Untitled source"
        text = ev.get("text") or ""
        if not text.strip():
            continue
        parts.append(f"[{number}] {title}\n{text}")
    return "\n\n".join(parts).strip()


def source_ids_from_evidence(evidence: list[dict[str, Any]]) -> list[int]:
    ids = set()
    for ev in evidence:
        pid = ev.get("resolved_corpus_paper_id")
        if isinstance(pid, int):
            ids.add(pid)
    return sorted(ids)


def claim_record(
    *,
    split: str,
    answer_row: dict[str, Any],
    answer_variant: str,
    claim_idx: int,
    extracted: dict[str, Any],
) -> dict[str, Any]:
    qid = int(answer_row["id"])
    evidence = answer_row.get("evidence", []) or []
    ev_by_num = evidence_number_map(evidence)

    citations = [int(x) for x in extracted.get("citations", [])]
    cited_evidence = [ev_by_num[n] for n in citations if n in ev_by_num]
    all_evidence = [compact_evidence(ev) for ev in evidence]
    cited_evidence_compact = [compact_evidence(ev) for ev in cited_evidence]

    if cited_evidence_compact:
        verifier_evidence = cited_evidence_compact
        evidence_scope = "cited_evidence"
    else:
        verifier_evidence = all_evidence
        evidence_scope = "all_retrieved_evidence_uncited_claim"

    answer_text = answer_row.get(answer_variant, "") or ""
    claim_text = extracted.get("claim_text", "") or ""

    claim_id = f"{split}_q{qid}_{answer_variant.replace('_answer', '')}_c{claim_idx:03d}"

    return {
        "claim_id": claim_id,
        "split": split,
        "qid": qid,
        "question": answer_row.get("question", ""),
        "question_type": answer_row.get("type"),
        "answer_variant": answer_variant,
        "answer": answer_text,
        "claim_index": claim_idx,
        "claim": claim_text,
        "claim_text": claim_text,
        "citations": citations,
        "evidence_scope": evidence_scope,
        "evidence": verifier_evidence,
        "evidence_text_for_verifier": join_evidence_text(verifier_evidence),
        "all_retrieved_evidence": all_evidence,
        "cited_evidence": cited_evidence_compact,
        "all_retrieved_corpus_paper_ids": source_ids_from_evidence(all_evidence),
        "verifier_evidence_corpus_paper_ids": source_ids_from_evidence(verifier_evidence),
    }


def extract_split(
    *,
    in_path: Path,
    out_path: Path,
    split: str,
    limit: int = 0,
) -> dict[str, Any]:
    answers = load_json(in_path)
    if not isinstance(answers, list):
        raise SystemExit(f"{in_path} must contain a JSON list")

    if limit > 0:
        answers = answers[:limit]

    records: list[dict[str, Any]] = []
    per_answer_counts: list[dict[str, Any]] = []

    print(f"\nExtracting claims for {split}: {len(answers)} answer rows")

    for row_idx, row in enumerate(answers, start=1):
        qid = int(row["id"])

        row_summary = {
            "qid": qid,
            "type": row.get("type"),
            "plain_claims": 0,
            "cited_claims": 0,
        }

        for variant in ANSWER_VARIANTS:
            answer_text = row.get(variant, "") or ""
            extracted_claims = extract_claims(answer_text)

            if variant == "plain_answer":
                row_summary["plain_claims"] = len(extracted_claims)
            elif variant == "cited_answer":
                row_summary["cited_claims"] = len(extracted_claims)

            for claim_idx, extracted in enumerate(extracted_claims, start=1):
                rec = claim_record(
                    split=split,
                    answer_row=row,
                    answer_variant=variant,
                    claim_idx=claim_idx,
                    extracted=extracted,
                )
                records.append(rec)

        per_answer_counts.append(row_summary)

        if row_idx == 1:
            print("First answer claim-count summary:")
            print(json.dumps(row_summary, ensure_ascii=False, indent=2))
            if records:
                print("First claim preview:")
                print(json.dumps(records[0], ensure_ascii=False, indent=2)[:2500])

        if row_idx % 25 == 0:
            print(f"  {row_idx}/{len(answers)} answer rows processed; claims so far={len(records)}")

    save_json(out_path, records)

    n_plain = sum(1 for r in records if r["answer_variant"] == "plain_answer")
    n_cited = sum(1 for r in records if r["answer_variant"] == "cited_answer")
    n_with_citations = sum(1 for r in records if r.get("citations"))
    n_uncited = len(records) - n_with_citations

    summary = {
        "split": split,
        "input_path": str(in_path),
        "output_path": str(out_path),
        "answer_rows": len(answers),
        "claims_total": len(records),
        "claims_plain_answer": n_plain,
        "claims_cited_answer": n_cited,
        "claims_with_citations": n_with_citations,
        "claims_without_citations": n_uncited,
        "avg_claims_per_answer_row_both_variants": round(len(records) / max(1, len(answers)), 3),
        "per_answer_counts_preview": per_answer_counts[:10],
    }

    print(f"Wrote {len(records)} claims to {out_path}")
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    return summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="smoke-test first N answer rows per split; 0=all")
    ap.add_argument("--split", choices=["all", "train", "gold"], default="all")
    args = ap.parse_args()

    summaries: list[dict[str, Any]] = []

    if args.split in {"all", "train"}:
        if not TRAIN_ANSWERS.exists():
            raise SystemExit(f"Missing {TRAIN_ANSWERS}")
        summaries.append(
            extract_split(
                in_path=TRAIN_ANSWERS,
                out_path=TRAIN_OUT,
                split="distill_train",
                limit=args.limit,
            )
        )

    if args.split in {"all", "gold"}:
        if not GOLD_ANSWERS.exists():
            raise SystemExit(f"Missing {GOLD_ANSWERS}")
        summaries.append(
            extract_split(
                in_path=GOLD_ANSWERS,
                out_path=GOLD_OUT,
                split="gold_eval",
                limit=args.limit,
            )
        )

    save_json(SUMMARY_OUT, {"summaries": summaries})
    print(f"\nWrote summary to {SUMMARY_OUT}")


if __name__ == "__main__":
    main()
