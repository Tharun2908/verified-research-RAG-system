"""
backend/app/services/build_arxiv_v2_bait_inputs.py

Build clean v2 bait generation inputs.

Policy:
  - Bait has no home paper requirement.
  - Retrieve top search-k candidates.
  - Remove protected gold-evidence papers.
  - Select top evidence-k non-protected evidence chunks.
  - Drop bait question only if too few non-protected evidence chunks remain.

Inputs:
  data/distill_arxiv_v2/bait_questions.json
  data/distill_arxiv_v2/protected_gold_evidence_papers.json
  data/arxiv_papers.json

Outputs:
  data/distill_arxiv_v2/bait_eval_inputs.json
  data/distill_arxiv_v2/bait_questions_validated_clean_evidence.json
  data/distill_arxiv_v2/bait_questions_dropped_clean_evidence.json
  data/distill_arxiv_v2/bait_eval_input_build_report.json

Run from backend/:
  python -m app.services.build_arxiv_v2_bait_inputs --limit 10
  python -m app.services.build_arxiv_v2_bait_inputs --search-k 10 --evidence-k 3
"""

from __future__ import annotations

import argparse
import asyncio
import inspect
import json
from collections import Counter
from pathlib import Path
from typing import Any

from app.services.hybrid_search import hybrid_search


DATA = Path("data")
V2_DIR = DATA / "distill_arxiv_v2"

DEFAULT_BAIT = V2_DIR / "bait_questions.json"
DEFAULT_CORPUS = DATA / "arxiv_papers.json"
DEFAULT_PROTECTED = V2_DIR / "protected_gold_evidence_papers.json"

OUT_VALIDATED = V2_DIR / "bait_questions_validated_clean_evidence.json"
OUT_DROPPED = V2_DIR / "bait_questions_dropped_clean_evidence.json"
OUT_INPUTS = V2_DIR / "bait_eval_inputs.json"
OUT_REPORT = V2_DIR / "bait_eval_input_build_report.json"


def load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def norm_title(x: Any) -> str:
    return " ".join(str(x or "").lower().strip().split())


def paper_title(p: dict[str, Any]) -> str:
    return str(p.get("_v2_title") or p.get("title") or p.get("paper_title") or p.get("name") or "").strip()


def corpus_id_from_paper(p: dict[str, Any], fallback: int | None = None) -> int | None:
    for k in ["corpus_paper_id", "resolved_corpus_paper_id", "paper_id"]:
        if p.get(k) is not None and str(p.get(k)).strip() != "":
            try:
                return int(p[k])
            except Exception:
                pass
    return fallback


def protected_ids_from_rows(rows: list[dict[str, Any]]) -> set[int]:
    out: set[int] = set()
    for p in rows:
        if not isinstance(p, dict):
            continue
        pid = corpus_id_from_paper(p, fallback=None)
        if pid is not None:
            out.add(pid)
    return out


def build_title_to_pid(corpus: list[dict[str, Any]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for i, p in enumerate(corpus):
        if not isinstance(p, dict):
            continue
        title = norm_title(paper_title(p))
        if title:
            out[title] = i
    return out


def result_title(r: Any) -> str:
    if isinstance(r, dict):
        return str(r.get("title") or r.get("paper_title") or r.get("source_title") or "").strip()
    return ""


def result_text(r: Any) -> str:
    if isinstance(r, dict):
        return str(r.get("text") or r.get("chunk") or r.get("content") or r.get("abstract") or "").strip()
    return ""


def result_score(r: Any) -> Any:
    if isinstance(r, dict):
        return r.get("score") if r.get("score") is not None else r.get("similarity")
    return None


def result_chunk_id(r: Any) -> Any:
    if isinstance(r, dict):
        return r.get("chunk_id") if r.get("chunk_id") is not None else r.get("id")
    return None


def resolve_hit_pid(hit: dict[str, Any], title_to_pid: dict[str, int]) -> int | None:
    for k in ["resolved_corpus_paper_id", "corpus_paper_id", "paper_id"]:
        if hit.get(k) is not None and str(hit.get(k)).strip() != "":
            try:
                return int(hit[k])
            except Exception:
                pass

    title = norm_title(result_title(hit))
    if title and title in title_to_pid:
        return title_to_pid[title]

    return None


def normalize_hits(raw_hits: Any, title_to_pid: dict[str, int]) -> list[dict[str, Any]]:
    if isinstance(raw_hits, dict):
        if isinstance(raw_hits.get("results"), list):
            raw_hits = raw_hits["results"]
        elif isinstance(raw_hits.get("hits"), list):
            raw_hits = raw_hits["hits"]
        else:
            raw_hits = []

    if raw_hits is None:
        raw_hits = []

    hits = []
    for rank, h in enumerate(raw_hits, start=1):
        if not isinstance(h, dict):
            continue
        hits.append({
            "raw_rank": rank,
            "title": result_title(h),
            "text": result_text(h),
            "chunk_id": result_chunk_id(h),
            "score": result_score(h),
            "resolved_corpus_paper_id": resolve_hit_pid(h, title_to_pid),
        })
    return hits


async def call_hybrid_search(question_text: str, top_k: int) -> Any:
    try:
        result = hybrid_search(question_text, top_k=top_k)
    except TypeError:
        result = hybrid_search(question_text, k=top_k)

    if inspect.isawaitable(result):
        result = await result

    return result


def renumber_evidence(selected: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    seen = set()

    for h in selected:
        key = (h.get("resolved_corpus_paper_id"), h.get("chunk_id"), h.get("title"))
        if key in seen:
            continue
        seen.add(key)
        rec = dict(h)
        rec["number"] = len(out) + 1
        rec["rank"] = rec["number"]
        out.append(rec)

    return out


async def run_build(args: argparse.Namespace) -> None:
    bait_questions = load_json(args.bait_questions)
    corpus = load_json(args.corpus)
    protected_rows = load_json(args.protected)

    if isinstance(corpus, dict) and "papers" in corpus:
        corpus = corpus["papers"]

    if not isinstance(bait_questions, list):
        raise SystemExit(f"{args.bait_questions} must be a JSON list.")
    if not isinstance(corpus, list):
        raise SystemExit(f"{args.corpus} must be a JSON list or dict with papers.")
    if not isinstance(protected_rows, list):
        raise SystemExit(f"{args.protected} must be a JSON list.")

    if args.limit > 0:
        bait_questions = bait_questions[: args.limit]

    title_to_pid = build_title_to_pid(corpus)
    protected_ids = protected_ids_from_rows(protected_rows)

    validated = []
    dropped = []
    eval_inputs = []

    status_counts: Counter[str] = Counter()
    protected_removed_total = 0
    protected_removed_by_pid: Counter[str] = Counter()

    print("\nBuilding v2 bait eval inputs")
    print("=" * 64)
    print(f"Bait questions:        {len(bait_questions)}")
    print(f"Search-k:              {args.search_k}")
    print(f"Evidence-k:            {args.evidence_k}")
    print(f"Protected gold papers: {len(protected_ids)}")

    for i, q in enumerate(bait_questions, start=1):
        question_text = str(q.get("question") or "").strip()

        rec = dict(q)
        rec["search_k"] = args.search_k
        rec["evidence_k"] = args.evidence_k

        if not question_text:
            rec["validation_status"] = "drop_missing_question"
            dropped.append(rec)
            status_counts[rec["validation_status"]] += 1
            continue

        raw_hits = await call_hybrid_search(question_text, args.search_k)
        all_hits = normalize_hits(raw_hits, title_to_pid)

        protected_hits = [h for h in all_hits if h.get("resolved_corpus_paper_id") in protected_ids]
        for h in protected_hits:
            pid = h.get("resolved_corpus_paper_id")
            protected_removed_by_pid[str(pid)] += 1
        protected_removed_total += len(protected_hits)

        filtered_hits = [
            h for h in all_hits
            if h.get("resolved_corpus_paper_id") is not None
            and h.get("resolved_corpus_paper_id") not in protected_ids
        ]

        selected = renumber_evidence(filtered_hits[: args.evidence_k])

        rec["retrieved_hits_raw"] = all_hits
        rec["retrieved_hits_nonprotected"] = filtered_hits
        rec["retrieved_protected_gold_paper_ids"] = sorted({
            h.get("resolved_corpus_paper_id") for h in protected_hits if h.get("resolved_corpus_paper_id") is not None
        })
        rec["selected_evidence"] = selected

        if len(selected) < args.min_evidence:
            rec["validation_status"] = "drop_too_few_nonprotected_evidence_hits"
            dropped.append(rec)
            status_counts[rec["validation_status"]] += 1
            continue

        selected_pids = [e.get("resolved_corpus_paper_id") for e in selected]
        selected_protected = [pid for pid in selected_pids if pid in protected_ids]
        if selected_protected:
            rec["validation_status"] = "drop_internal_error_selected_protected"
            rec["selected_protected_pids"] = selected_protected
            dropped.append(rec)
            status_counts[rec["validation_status"]] += 1
            continue

        rec["validation_status"] = "keep_bait_clean_filtered_retrieval"
        validated.append(rec)
        status_counts[rec["validation_status"]] += 1

        eval_inputs.append({
            "id": q.get("id") or q.get("qid") or len(eval_inputs) + 1,
            "qid": q.get("qid") or q.get("id") or len(eval_inputs) + 1,
            "split": "distill_train_v2_bait",
            "type": "bait",
            "question": question_text,
            "home_paper_id": None,
            "home_corpus_paper_id": None,
            "home_title": None,
            "source": q.get("source", "distill_arxiv_v2_bait_train"),
            "search_k": args.search_k,
            "evidence_k": args.evidence_k,
            "evidence": selected,
        })

        if i == 1 or i % 25 == 0 or i == len(bait_questions):
            print(f"  checked {i}/{len(bait_questions)} | kept={len(eval_inputs)} dropped={len(dropped)}")

    report = {
        "inputs": {
            "bait_questions": str(args.bait_questions),
            "corpus": str(args.corpus),
            "protected": str(args.protected),
        },
        "outputs": {
            "validated_questions": str(OUT_VALIDATED),
            "dropped_questions": str(OUT_DROPPED),
            "eval_inputs": str(OUT_INPUTS),
            "report": str(OUT_REPORT),
        },
        "search_k": args.search_k,
        "evidence_k": args.evidence_k,
        "min_evidence": args.min_evidence,
        "summary": {
            "bait_questions_checked": len(bait_questions),
            "kept_eval_inputs": len(eval_inputs),
            "dropped": len(dropped),
            "keep_rate": round(len(eval_inputs) / len(bait_questions), 4) if bait_questions else 0.0,
            "protected_gold_paper_count": len(protected_ids),
            "protected_hits_removed_total": protected_removed_total,
            "selected_evidence_protected_overlap": 0,
        },
        "status_counts": dict(status_counts),
        "protected_removed_by_pid_top30": dict(protected_removed_by_pid.most_common(30)),
    }

    save_json(OUT_VALIDATED, validated)
    save_json(OUT_DROPPED, dropped)
    save_json(OUT_INPUTS, eval_inputs)
    save_json(OUT_REPORT, report)

    print("\nDone.")
    print(f"Kept bait eval inputs:    {len(eval_inputs)}")
    print(f"Dropped bait questions:   {len(dropped)}")
    if bait_questions:
        print(f"Keep rate:                {100 * len(eval_inputs) / len(bait_questions):.1f}%")
    print(f"Protected hits removed:   {protected_removed_total}")
    print("Status counts:")
    for k, v in status_counts.most_common():
        print(f"  {k:48s} {v}")
    print("\nWrote:")
    print(f"  {OUT_VALIDATED}")
    print(f"  {OUT_DROPPED}")
    print(f"  {OUT_INPUTS}")
    print(f"  {OUT_REPORT}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bait-questions", type=Path, default=DEFAULT_BAIT)
    ap.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    ap.add_argument("--protected", type=Path, default=DEFAULT_PROTECTED)
    ap.add_argument("--search-k", type=int, default=10)
    ap.add_argument("--evidence-k", type=int, default=3)
    ap.add_argument("--min-evidence", type=int, default=1)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    asyncio.run(run_build(args))


if __name__ == "__main__":
    main()
