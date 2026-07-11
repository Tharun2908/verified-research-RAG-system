"""
backend/app/services/validate_arxiv_v2_train_questions.py

Validate Option-B train questions with strict protected-gold evidence filtering.

This version supports both sync and async versions of app.services.hybrid_search.hybrid_search.

Keep a v2 train question only if:
  1. the question's home/safe paper appears in retrieved top-k
  2. NONE of the retrieved top-k evidence papers are protected gold-evidence papers

Inputs:
  data/distill_arxiv_v2/train_questions.json
  data/distill_arxiv_v2/protected_gold_evidence_papers.json
  data/arxiv_papers.json

Outputs:
  data/distill_arxiv_v2/train_questions_validated.json
  data/distill_arxiv_v2/train_questions_dropped.json
  data/distill_arxiv_v2/train_retrieval_validation_report.json

Run from backend/:
  python -m app.services.validate_arxiv_v2_train_questions --limit 10 --top-k 3
  python -m app.services.validate_arxiv_v2_train_questions --top-k 3
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

DEFAULT_QUESTIONS = V2_DIR / "train_questions.json"
DEFAULT_CORPUS = DATA / "arxiv_papers.json"
DEFAULT_PROTECTED = V2_DIR / "protected_gold_evidence_papers.json"

OUT_VALIDATED = V2_DIR / "train_questions_validated.json"
OUT_DROPPED = V2_DIR / "train_questions_dropped.json"
OUT_REPORT = V2_DIR / "train_retrieval_validation_report.json"


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


def get_home_id(q: dict[str, Any]) -> int | None:
    for k in ["home_corpus_paper_id", "home_paper_id", "corpus_paper_id", "paper_id"]:
        if q.get(k) is not None and str(q.get(k)).strip() != "":
            try:
                return int(q[k])
            except Exception:
                pass
    return None


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


def build_title_to_pid(corpus: list[dict[str, Any]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for i, p in enumerate(corpus):
        if not isinstance(p, dict):
            continue
        title = norm_title(paper_title(p))
        if title:
            out[title] = i
    return out


def protected_ids_from_rows(rows: list[dict[str, Any]]) -> set[int]:
    out: set[int] = set()
    for p in rows:
        if not isinstance(p, dict):
            continue
        pid = corpus_id_from_paper(p, fallback=None)
        if pid is not None:
            out.add(pid)
    return out


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
    """
    Normalize possible retrieval result shapes.

    Supported shapes:
      - list[dict]
      - {"results": list[dict]}
      - {"hits": list[dict]}
    """
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

        title = result_title(h)
        text = result_text(h)
        pid = resolve_hit_pid(h, title_to_pid)

        hits.append({
            "rank": rank,
            "title": title,
            "text": text,
            "chunk_id": result_chunk_id(h),
            "score": result_score(h),
            "resolved_corpus_paper_id": pid,
        })

    return hits


async def call_hybrid_search(question_text: str, top_k: int) -> Any:
    """
    Call hybrid_search whether repo implementation is sync or async.
    Also tolerates older parameter name `k`.
    """
    try:
        result = hybrid_search(question_text, top_k=top_k)
    except TypeError:
        result = hybrid_search(question_text, k=top_k)

    if inspect.isawaitable(result):
        result = await result

    return result


async def run_validation(args: argparse.Namespace) -> None:
    questions = load_json(args.questions)
    corpus = load_json(args.corpus)
    protected_rows = load_json(args.protected)

    if isinstance(corpus, dict) and "papers" in corpus:
        corpus = corpus["papers"]

    if not isinstance(questions, list):
        raise SystemExit(f"{args.questions} must be a JSON list.")
    if not isinstance(corpus, list):
        raise SystemExit(f"{args.corpus} must be a JSON list or dict with papers.")
    if not isinstance(protected_rows, list):
        raise SystemExit(f"{args.protected} must be a JSON list.")

    if args.limit > 0:
        questions = questions[: args.limit]

    title_to_pid = build_title_to_pid(corpus)
    protected_ids = protected_ids_from_rows(protected_rows)

    kept = []
    dropped = []
    status_counts: Counter[str] = Counter()
    protected_hit_counter: Counter[str] = Counter()

    print("\nValidating v2 train questions")
    print("=" * 64)
    print(f"Questions:                 {len(questions)}")
    print(f"Top-k:                     {args.top_k}")
    print(f"Protected gold papers:     {len(protected_ids)}")

    for i, q in enumerate(questions, start=1):
        question_text = str(q.get("question") or "").strip()
        home_id = get_home_id(q)

        if not question_text:
            rec = dict(q)
            rec["validation_status"] = "drop_missing_question"
            dropped.append(rec)
            status_counts[rec["validation_status"]] += 1
            continue

        if home_id is None:
            rec = dict(q)
            rec["validation_status"] = "drop_missing_home_paper_id"
            dropped.append(rec)
            status_counts[rec["validation_status"]] += 1
            continue

        raw_hits = await call_hybrid_search(question_text, args.top_k)
        hits = normalize_hits(raw_hits, title_to_pid)
        retrieved_ids = [h["resolved_corpus_paper_id"] for h in hits if h["resolved_corpus_paper_id"] is not None]

        protected_hits = sorted(set(pid for pid in retrieved_ids if pid in protected_ids))
        home_retrieved = home_id in set(retrieved_ids)

        rec = dict(q)
        rec["retrieval_top_k"] = args.top_k
        rec["retrieved_hits"] = hits
        rec["retrieved_corpus_paper_ids"] = retrieved_ids
        rec["retrieved_protected_gold_paper_ids"] = protected_hits
        rec["home_paper_retrieved"] = home_retrieved

        if protected_hits:
            rec["validation_status"] = "drop_retrieved_protected_gold_evidence"
            for pid in protected_hits:
                protected_hit_counter[str(pid)] += 1
            dropped.append(rec)
        elif not home_retrieved:
            rec["validation_status"] = "drop_home_not_retrieved"
            dropped.append(rec)
        else:
            rec["validation_status"] = "keep_train_clean"
            kept.append(rec)

        status_counts[rec["validation_status"]] += 1

        if i == 1 or i % 25 == 0 or i == len(questions):
            print(f"  checked {i}/{len(questions)} | kept={len(kept)} dropped={len(dropped)}")

    report = {
        "inputs": {
            "questions": str(args.questions),
            "corpus": str(args.corpus),
            "protected": str(args.protected),
        },
        "outputs": {
            "validated": str(OUT_VALIDATED),
            "dropped": str(OUT_DROPPED),
            "report": str(OUT_REPORT),
        },
        "top_k": args.top_k,
        "summary": {
            "questions_checked": len(questions),
            "kept": len(kept),
            "dropped": len(dropped),
            "keep_rate": round(len(kept) / len(questions), 4) if questions else 0.0,
            "protected_gold_paper_count": len(protected_ids),
        },
        "status_counts": dict(status_counts),
        "protected_hit_counts": dict(protected_hit_counter.most_common(30)),
    }

    save_json(OUT_VALIDATED, kept)
    save_json(OUT_DROPPED, dropped)
    save_json(OUT_REPORT, report)

    print("\nDone.")
    print(f"Kept:       {len(kept)}")
    print(f"Dropped:    {len(dropped)}")
    if questions:
        print(f"Keep rate:  {100 * len(kept) / len(questions):.1f}%")
    print("Status counts:")
    for k, v in status_counts.most_common():
        print(f"  {k:40s} {v}")
    print("\nWrote:")
    print(f"  {OUT_VALIDATED}")
    print(f"  {OUT_DROPPED}")
    print(f"  {OUT_REPORT}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--questions", type=Path, default=DEFAULT_QUESTIONS)
    ap.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    ap.add_argument("--protected", type=Path, default=DEFAULT_PROTECTED)
    ap.add_argument("--top-k", type=int, default=3)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    asyncio.run(run_validation(args))


if __name__ == "__main__":
    main()
