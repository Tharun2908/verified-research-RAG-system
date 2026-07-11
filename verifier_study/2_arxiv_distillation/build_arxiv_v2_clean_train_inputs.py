"""
backend/app/services/build_arxiv_v2_clean_train_inputs.py

Build Option-B clean train generation inputs by filtering protected gold-evidence papers
out of retrieval results before selecting the evidence used for generation.

Why this script exists:
  Strict validation showed that most safe-source train questions still retrieve protected
  gold papers in raw top-3. Instead of dropping those questions, we build TRAIN inputs
  with protected evidence removed.

Policy:
  - Retrieve top `search_k` candidates.
  - Resolve each hit to corpus_paper_id by title/id.
  - Remove any hit whose paper is in protected_gold_evidence_papers.json.
  - Keep the question only if its home safe paper appears in the remaining candidates.
  - Select `evidence_k` non-protected evidence chunks.
  - If the home paper is retrieved after filtering but not in the selected evidence, replace
    the last selected evidence with the home-paper hit. This keeps generation answerable while
    preserving gold-evidence disjointness.

Inputs:
  data/distill_arxiv_v2/train_questions.json
  data/distill_arxiv_v2/protected_gold_evidence_papers.json
  data/arxiv_papers.json

Outputs:
  data/distill_arxiv_v2/train_questions_validated_clean_evidence.json
  data/distill_arxiv_v2/train_questions_dropped_clean_evidence.json
  data/distill_arxiv_v2/train_eval_inputs.json
  data/distill_arxiv_v2/train_eval_input_build_report.json

Run from backend/:
  python -m app.services.build_arxiv_v2_clean_train_inputs --limit 10
  python -m app.services.build_arxiv_v2_clean_train_inputs --search-k 10 --evidence-k 3
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

OUT_VALIDATED = V2_DIR / "train_questions_validated_clean_evidence.json"
OUT_DROPPED = V2_DIR / "train_questions_dropped_clean_evidence.json"
OUT_INPUTS = V2_DIR / "train_eval_inputs.json"
OUT_REPORT = V2_DIR / "train_eval_input_build_report.json"


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

        pid = resolve_hit_pid(h, title_to_pid)
        hits.append({
            "raw_rank": rank,
            "title": result_title(h),
            "text": result_text(h),
            "chunk_id": result_chunk_id(h),
            "score": result_score(h),
            "resolved_corpus_paper_id": pid,
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


def select_evidence(
    filtered_hits: list[dict[str, Any]],
    home_id: int,
    evidence_k: int,
) -> tuple[list[dict[str, Any]], bool]:
    """
    Return selected evidence and whether we had to force the home hit into the selected set.
    """
    selected = list(filtered_hits[:evidence_k])
    forced_home = False

    selected_pids = {h.get("resolved_corpus_paper_id") for h in selected}
    if home_id in selected_pids:
        return selected, forced_home

    home_hit = None
    for h in filtered_hits:
        if h.get("resolved_corpus_paper_id") == home_id:
            home_hit = h
            break

    if home_hit is None:
        return selected, forced_home

    if len(selected) < evidence_k:
        selected.append(home_hit)
    elif selected:
        selected[-1] = home_hit
    else:
        selected = [home_hit]

    forced_home = True
    return selected, forced_home


def renumber_evidence(selected: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    seen = set()

    for h in selected:
        # Dedupe repeated chunks/papers conservatively by (pid, chunk_id, title).
        key = (h.get("resolved_corpus_paper_id"), h.get("chunk_id"), h.get("title"))
        if key in seen:
            continue
        seen.add(key)

        rec = dict(h)
        rec["number"] = len(out) + 1
        # Keep a clean rank field expected by generation scripts.
        rec["rank"] = rec["number"]
        out.append(rec)

    return out


async def run_build(args: argparse.Namespace) -> None:
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

    validated = []
    dropped = []
    eval_inputs = []

    status_counts: Counter[str] = Counter()
    home_forced_count = 0
    protected_removed_total = 0
    protected_removed_by_pid: Counter[str] = Counter()

    print("\nBuilding v2 clean train eval inputs")
    print("=" * 64)
    print(f"Questions:             {len(questions)}")
    print(f"Search-k:              {args.search_k}")
    print(f"Evidence-k:            {args.evidence_k}")
    print(f"Protected gold papers: {len(protected_ids)}")

    for i, q in enumerate(questions, start=1):
        question_text = str(q.get("question") or "").strip()
        home_id = get_home_id(q)

        rec = dict(q)
        rec["search_k"] = args.search_k
        rec["evidence_k"] = args.evidence_k

        if not question_text:
            rec["validation_status"] = "drop_missing_question"
            dropped.append(rec)
            status_counts[rec["validation_status"]] += 1
            continue

        if home_id is None:
            rec["validation_status"] = "drop_missing_home_paper_id"
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

        home_retrieved_after_filter = any(h.get("resolved_corpus_paper_id") == home_id for h in filtered_hits)

        rec["retrieved_hits_raw"] = all_hits
        rec["retrieved_hits_nonprotected"] = filtered_hits
        rec["retrieved_corpus_paper_ids_raw"] = [
            h.get("resolved_corpus_paper_id") for h in all_hits if h.get("resolved_corpus_paper_id") is not None
        ]
        rec["retrieved_corpus_paper_ids_nonprotected"] = [
            h.get("resolved_corpus_paper_id") for h in filtered_hits if h.get("resolved_corpus_paper_id") is not None
        ]
        rec["retrieved_protected_gold_paper_ids"] = sorted({
            h.get("resolved_corpus_paper_id") for h in protected_hits if h.get("resolved_corpus_paper_id") is not None
        })
        rec["home_paper_retrieved_after_protected_filter"] = home_retrieved_after_filter

        if not home_retrieved_after_filter:
            rec["validation_status"] = "drop_home_not_retrieved_after_protected_filter"
            dropped.append(rec)
            status_counts[rec["validation_status"]] += 1
            continue

        selected, forced_home = select_evidence(filtered_hits, home_id=home_id, evidence_k=args.evidence_k)
        evidence = renumber_evidence(selected)

        if len(evidence) < args.min_evidence:
            rec["validation_status"] = "drop_too_few_nonprotected_evidence_hits"
            rec["selected_evidence"] = evidence
            dropped.append(rec)
            status_counts[rec["validation_status"]] += 1
            continue

        # Sanity: selected evidence must not contain protected papers.
        selected_pids = [e.get("resolved_corpus_paper_id") for e in evidence]
        selected_protected = [pid for pid in selected_pids if pid in protected_ids]
        if selected_protected:
            rec["validation_status"] = "drop_internal_error_selected_protected"
            rec["selected_protected_pids"] = selected_protected
            dropped.append(rec)
            status_counts[rec["validation_status"]] += 1
            continue

        if forced_home:
            home_forced_count += 1

        rec["validation_status"] = "keep_train_clean_filtered_retrieval"
        rec["home_forced_into_selected_evidence"] = forced_home
        rec["selected_evidence"] = evidence
        validated.append(rec)
        status_counts[rec["validation_status"]] += 1

        eval_inputs.append({
            "id": q.get("id") or q.get("qid") or len(eval_inputs) + 1,
            "qid": q.get("qid") or q.get("id") or len(eval_inputs) + 1,
            "split": "distill_train_v2",
            "type": q.get("type", "grounded"),
            "question": question_text,
            "home_paper_id": home_id,
            "home_corpus_paper_id": home_id,
            "home_title": q.get("home_title"),
            "source": q.get("source", "distill_arxiv_v2_safe_train"),
            "search_k": args.search_k,
            "evidence_k": args.evidence_k,
            "home_forced_into_selected_evidence": forced_home,
            "evidence": evidence,
        })

        if i == 1 or i % 25 == 0 or i == len(questions):
            print(f"  checked {i}/{len(questions)} | kept={len(eval_inputs)} dropped={len(dropped)}")

    report = {
        "inputs": {
            "questions": str(args.questions),
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
            "questions_checked": len(questions),
            "kept_eval_inputs": len(eval_inputs),
            "dropped": len(dropped),
            "keep_rate": round(len(eval_inputs) / len(questions), 4) if questions else 0.0,
            "protected_gold_paper_count": len(protected_ids),
            "protected_hits_removed_total": protected_removed_total,
            "home_forced_into_selected_evidence_count": home_forced_count,
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
    print(f"Kept eval inputs:          {len(eval_inputs)}")
    print(f"Dropped questions:         {len(dropped)}")
    if questions:
        print(f"Keep rate:                 {100 * len(eval_inputs) / len(questions):.1f}%")
    print(f"Protected hits removed:    {protected_removed_total}")
    print(f"Home forced into evidence: {home_forced_count}")
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
    ap.add_argument("--questions", type=Path, default=V2_DIR / "train_questions.json")
    ap.add_argument("--corpus", type=Path, default=DATA / "arxiv_papers.json")
    ap.add_argument("--protected", type=Path, default=V2_DIR / "protected_gold_evidence_papers.json")
    ap.add_argument("--search-k", type=int, default=10)
    ap.add_argument("--evidence-k", type=int, default=3)
    ap.add_argument("--min-evidence", type=int, default=1)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    asyncio.run(run_build(args))


if __name__ == "__main__":
    main()
