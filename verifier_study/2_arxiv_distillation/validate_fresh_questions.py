"""
backend/app/services/validate_fresh_questions.py

STEP 2 of arXiv distillation:
Retrieval-validate the fresh questions generated in Step 1.

Input:
  data/distill_arxiv/fresh_questions.json

Output:
  data/distill_arxiv/fresh_questions_validated.json
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
from pathlib import Path
from typing import Any

from app.services.hybrid_search import hybrid_search


DATA = Path("data")
DISTILL_DIR = DATA / "distill_arxiv"

CORPUS_PATH = DATA / "arxiv_papers.json"
IN_PATH = DISTILL_DIR / "fresh_questions.json"
OUT_PATH = DISTILL_DIR / "fresh_questions_validated.json"

DEFAULT_TOP_K = 8


def load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def norm_text(s: str) -> str:
    s = str(s or "").lower()
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def norm_arxiv_id(s: str | None) -> str:
    if not s:
        return ""

    s = str(s).strip()
    s = s.replace("arXiv:", "").replace("arxiv:", "")
    s = s.rstrip("/")

    if "/abs/" in s:
        s = s.split("/abs/")[-1]

    if "/pdf/" in s:
        s = s.split("/pdf/")[-1]
        s = s.replace(".pdf", "")

    return s.strip()


def hit_to_plain_dict(hit: Any) -> dict[str, Any]:
    if isinstance(hit, dict):
        return dict(hit)

    if hasattr(hit, "model_dump"):
        try:
            return hit.model_dump()
        except Exception:
            pass

    if hasattr(hit, "dict"):
        try:
            return hit.dict()
        except Exception:
            pass

    out: dict[str, Any] = {}

    for k in dir(hit):
        if k.startswith("_"):
            continue

        try:
            v = getattr(hit, k)
        except Exception:
            continue

        if callable(v):
            continue

        if isinstance(v, (str, int, float, bool, type(None), list, dict)):
            out[k] = v

    return out


def deep_get_values(obj: Any, candidate_keys: set[str]) -> list[Any]:
    found: list[Any] = []

    if isinstance(obj, dict):
        for k, v in obj.items():
            if str(k).lower() in candidate_keys:
                found.append(v)
            found.extend(deep_get_values(v, candidate_keys))

    elif isinstance(obj, list):
        for x in obj:
            found.extend(deep_get_values(x, candidate_keys))

    return found


def first_string_value(obj: Any, keys: set[str]) -> str:
    vals = deep_get_values(obj, keys)

    for v in vals:
        if isinstance(v, str) and v.strip():
            return v.strip()

    return ""


def all_string_values(obj: Any, keys: set[str]) -> list[str]:
    vals = deep_get_values(obj, keys)
    out: list[str] = []

    for v in vals:
        if isinstance(v, str) and v.strip():
            out.append(v.strip())

    return out


def all_int_values(obj: Any, keys: set[str]) -> list[int]:
    vals = deep_get_values(obj, keys)
    out: list[int] = []

    for v in vals:
        try:
            out.append(int(v))
        except Exception:
            continue

    return out


def extract_hit_title(hit: dict[str, Any]) -> str:
    return first_string_value(
        hit,
        {"title", "paper_title", "source_title", "document_title"},
    )


def extract_hit_arxiv_ids(hit: dict[str, Any]) -> list[str]:
    vals = all_string_values(
        hit,
        {"arxiv_id", "arxivid", "arxiv", "paper_arxiv_id", "source_arxiv_id"},
    )

    return [norm_arxiv_id(v) for v in vals if norm_arxiv_id(v)]


def extract_hit_paper_ids(hit: dict[str, Any]) -> list[int]:
    return all_int_values(
        hit,
        {"paper_id", "paperid", "source_paper_id", "document_id", "doc_id", "id"},
    )


def extract_hit_chunk_id(hit: dict[str, Any]) -> Any:
    vals = deep_get_values(hit, {"chunk_id", "chunkid"})
    return vals[0] if vals else None


def extract_hit_score(hit: dict[str, Any]) -> Any:
    vals = deep_get_values(
        hit,
        {"score", "rerank_score", "hybrid_score", "dense_score", "bm25_score"},
    )
    return vals[0] if vals else None


def extract_hit_text(hit: dict[str, Any]) -> str:
    return first_string_value(
        hit,
        {"text", "chunk_text", "content", "abstract", "passage", "body"},
    )


def compact_hit(hit: Any, rank: int, title_to_corpus_id: dict[str, int]) -> dict[str, Any]:
    d = hit_to_plain_dict(hit)

    title = extract_hit_title(d)
    text = extract_hit_text(d)
    title_norm = norm_text(title)
    resolved_id = title_to_corpus_id.get(title_norm)

    return {
        "rank": rank,
        "chunk_id": extract_hit_chunk_id(d),
        "score": extract_hit_score(d),
        "paper_ids": extract_hit_paper_ids(d),
        "arxiv_ids": extract_hit_arxiv_ids(d),
        "title": title,
        "resolved_corpus_paper_id": resolved_id,
        "text_preview": text[:500] if text else "",
        "raw_keys": sorted(list(d.keys()))[:50],
    }


def build_title_to_corpus_id(corpus: list[dict[str, Any]]) -> dict[str, int]:
    title_to_id: dict[str, int] = {}

    for i, p in enumerate(corpus):
        if not isinstance(p, dict):
            continue

        title = norm_text(str(p.get("title", "")))
        if title:
            title_to_id[title] = i

    return title_to_id


def build_arxiv_to_corpus_id(corpus: list[dict[str, Any]]) -> dict[str, int]:
    arxiv_to_id: dict[str, int] = {}

    for i, p in enumerate(corpus):
        if not isinstance(p, dict):
            continue

        arxiv_id = norm_arxiv_id(p.get("arxiv_id", ""))
        if arxiv_id:
            arxiv_to_id[arxiv_id] = i

    return arxiv_to_id


def paper_match(
    home_paper: dict[str, Any],
    home_paper_id: int,
    retrieved_hits: list[dict[str, Any]],
) -> tuple[bool, str]:
    home_title = str(home_paper.get("title", "")).strip()
    home_title_norm = norm_text(home_title)

    home_arxiv = norm_arxiv_id(home_paper.get("arxiv_id", ""))

    for h in retrieved_hits:
        if h.get("resolved_corpus_paper_id") == home_paper_id:
            return True, "resolved_corpus_paper_id_match"

    for h in retrieved_hits:
        hit_arxiv_ids = set(h.get("arxiv_ids", []))
        if home_arxiv and home_arxiv in hit_arxiv_ids:
            return True, "arxiv_id_match"

    for h in retrieved_hits:
        hit_title = h.get("title", "")
        if home_title_norm and norm_text(hit_title) == home_title_norm:
            return True, "title_match"

    allowed_numeric_ids = {home_paper_id, home_paper_id + 1}
    for h in retrieved_hits:
        hit_ids = set(h.get("paper_ids", []))
        if hit_ids & allowed_numeric_ids:
            return True, "numeric_id_match"

    return False, "no_home_paper_in_topk"


async def validate_one(
    q: dict[str, Any],
    corpus: list[dict[str, Any]],
    title_to_corpus_id: dict[str, int],
    top_k: int,
) -> dict[str, Any]:
    question = q["question"]

    hits_raw = await hybrid_search(question, top_k=top_k)

    hits_compact = [
        compact_hit(h, rank=i + 1, title_to_corpus_id=title_to_corpus_id)
        for i, h in enumerate(hits_raw)
    ]

    retrieved_titles = [h["title"] for h in hits_compact if h.get("title")]

    retrieved_arxiv_ids = sorted(
        {
            aid
            for h in hits_compact
            for aid in h.get("arxiv_ids", [])
            if aid
        }
    )

    retrieved_corpus_paper_ids = sorted(
        {
            h["resolved_corpus_paper_id"]
            for h in hits_compact
            if isinstance(h.get("resolved_corpus_paper_id"), int)
        }
    )

    retrieved_raw_paper_ids = sorted(
        {
            pid
            for h in hits_compact
            for pid in h.get("paper_ids", [])
            if isinstance(pid, int)
        }
    )

    out = dict(q)
    out["retrieval_top_k"] = top_k
    out["retrieved_paper_ids"] = retrieved_corpus_paper_ids
    out["retrieved_corpus_paper_ids"] = retrieved_corpus_paper_ids
    out["retrieved_raw_paper_ids"] = retrieved_raw_paper_ids
    out["retrieved_arxiv_ids"] = retrieved_arxiv_ids
    out["retrieved_titles"] = retrieved_titles
    out["retrieved_hits"] = hits_compact

    q_type = q.get("type")

    if q_type == "grounded":
        home_paper_id = q.get("home_paper_id")

        if home_paper_id is None:
            out["validation_status"] = "drop_grounded_missing_home_paper_id"
            out["home_paper_retrieved_topk"] = False
            out["match_reason"] = "missing_home_paper_id"
            return out

        try:
            home_paper_id_int = int(home_paper_id)
        except Exception:
            out["validation_status"] = "drop_grounded_bad_home_paper_id"
            out["home_paper_retrieved_topk"] = False
            out["match_reason"] = "bad_home_paper_id"
            return out

        if home_paper_id_int < 0 or home_paper_id_int >= len(corpus):
            out["validation_status"] = "drop_grounded_home_paper_out_of_range"
            out["home_paper_retrieved_topk"] = False
            out["match_reason"] = "home_paper_out_of_range"
            return out

        home_paper = corpus[home_paper_id_int]
        matched, reason = paper_match(
            home_paper=home_paper,
            home_paper_id=home_paper_id_int,
            retrieved_hits=hits_compact,
        )

        out["home_arxiv_id"] = norm_arxiv_id(home_paper.get("arxiv_id", ""))
        out["home_title"] = home_paper.get("title", "")
        out["home_paper_retrieved_topk"] = bool(matched)
        out["match_reason"] = reason
        out["validation_status"] = "keep_grounded" if matched else "drop_grounded_home_not_retrieved"

    elif q_type == "bait":
        out["home_paper_retrieved_topk"] = None
        out["match_reason"] = "bait_no_home_paper"
        out["validation_status"] = "keep_bait"

    else:
        out["home_paper_retrieved_topk"] = None
        out["match_reason"] = "unknown_type"
        out["validation_status"] = "drop_unknown_type"

    return out


async def main_async() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    ap.add_argument("--limit", type=int, default=0, help="0=all questions; >0=first N for smoke test")
    ap.add_argument("--resume", action="store_true", help="resume from existing output")
    args = ap.parse_args()

    if not CORPUS_PATH.exists():
        raise SystemExit(f"Missing corpus: {CORPUS_PATH}")

    if not IN_PATH.exists():
        raise SystemExit(f"Missing fresh questions: {IN_PATH}")

    corpus = load_json(CORPUS_PATH)
    questions = load_json(IN_PATH)

    if not isinstance(corpus, list):
        raise SystemExit(f"{CORPUS_PATH} must be a list")

    if not isinstance(questions, list):
        raise SystemExit(f"{IN_PATH} must be a list")

    title_to_corpus_id = build_title_to_corpus_id(corpus)
    arxiv_to_corpus_id = build_arxiv_to_corpus_id(corpus)

    if args.limit > 0:
        questions = questions[: args.limit]

    existing_by_qid: dict[int, dict[str, Any]] = {}
    results: list[dict[str, Any]] = []

    if args.resume and OUT_PATH.exists():
        existing = load_json(OUT_PATH)

        if isinstance(existing, list):
            for r in existing:
                try:
                    existing_by_qid[int(r["qid"])] = r
                except Exception:
                    pass

            results = list(existing)

    print(f"Loaded corpus papers: {len(corpus)}")
    print(f"Loaded fresh questions: {len(questions)}")
    print(f"title_to_corpus_id entries: {len(title_to_corpus_id)}")
    print(f"arxiv_to_corpus_id entries: {len(arxiv_to_corpus_id)}")
    print(f"top_k={args.top_k}")
    print(f"resume={args.resume}, already validated={len(existing_by_qid)}")
    print(f"Output: {OUT_PATH}")

    processed = 0

    for idx, q in enumerate(questions, start=1):
        try:
            qid = int(q["qid"])
        except Exception:
            qid = idx

        if qid in existing_by_qid:
            continue

        try:
            validated = await validate_one(
                q=q,
                corpus=corpus,
                title_to_corpus_id=title_to_corpus_id,
                top_k=args.top_k,
            )

        except Exception as e:
            validated = dict(q)
            validated["validation_status"] = "error"
            validated["error"] = repr(e)

        results.append(validated)
        processed += 1

        if processed == 1:
            print("\nFirst validated example:")
            print(json.dumps(validated, ensure_ascii=False, indent=2)[:3500])

        if processed % 10 == 0:
            keep_grounded = sum(1 for r in results if r.get("validation_status") == "keep_grounded")
            drop_grounded = sum(1 for r in results if r.get("validation_status") == "drop_grounded_home_not_retrieved")
            keep_bait = sum(1 for r in results if r.get("validation_status") == "keep_bait")
            errors = sum(1 for r in results if r.get("validation_status") == "error")

            print(
                f"validated new={processed} total={len(results)} | "
                f"keep_grounded={keep_grounded} drop_grounded={drop_grounded} "
                f"keep_bait={keep_bait} errors={errors}"
            )

            save_json(OUT_PATH, results)

    save_json(OUT_PATH, results)

    counts: dict[str, int] = {}
    for r in results:
        status = r.get("validation_status", "missing")
        counts[status] = counts.get(status, 0) + 1

    print("\nDone.")
    print(json.dumps(counts, indent=2))
    print(f"Wrote: {OUT_PATH}")

    usable = [
        r for r in results
        if r.get("validation_status") in {"keep_grounded", "keep_bait"}
    ]

    print(f"Usable after retrieval validation: {len(usable)} / {len(results)}")


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
