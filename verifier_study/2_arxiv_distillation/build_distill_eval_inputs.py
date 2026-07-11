"""
backend/app/services/build_distill_eval_inputs.py

Build self-contained cluster generation inputs for the arXiv distillation pipeline.

Inputs:
  data/distill_arxiv/distill_train_questions.json
  data/distill_arxiv/gold_eval_questions.json

Outputs:
  data/distill_arxiv/distill_train_eval_inputs.json
  data/distill_arxiv/gold_eval_inputs.json

Why:
  The cluster does not need Postgres/Qdrant/project imports. It should receive a simple JSON:
    [
      {
        "id": 1,
        "qid": 1,
        "split": "distill_train",
        "type": "grounded",
        "question": "...",
        "evidence": [
          {"number": 1, "title": "...", "text": "...", "chunk_id": ..., "score": ...}
        ]
      }
    ]

Run from backend/:
  python -m app.services.build_distill_eval_inputs --limit 5
  python -m app.services.build_distill_eval_inputs
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

TRAIN_Q_PATH = DISTILL_DIR / "distill_train_questions.json"
GOLD_Q_PATH = DISTILL_DIR / "gold_eval_questions.json"

TRAIN_OUT = DISTILL_DIR / "distill_train_eval_inputs.json"
GOLD_OUT = DISTILL_DIR / "gold_eval_inputs.json"

CORPUS_PATH = DATA / "arxiv_papers.json"

DEFAULT_TOP_K = 3


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


def first_string_value(obj: Any, keys: set[str]) -> str:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if str(k).lower() in keys and isinstance(v, str) and v.strip():
                return v.strip()
            if isinstance(v, (dict, list)):
                found = first_string_value(v, keys)
                if found:
                    return found

    elif isinstance(obj, list):
        for x in obj:
            found = first_string_value(x, keys)
            if found:
                return found

    return ""


def first_value(obj: Any, keys: set[str]) -> Any:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if str(k).lower() in keys:
                return v
            if isinstance(v, (dict, list)):
                found = first_value(v, keys)
                if found is not None:
                    return found

    elif isinstance(obj, list):
        for x in obj:
            found = first_value(x, keys)
            if found is not None:
                return found

    return None


def build_title_to_corpus_id(corpus: list[dict[str, Any]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for i, p in enumerate(corpus):
        if isinstance(p, dict):
            title = norm_text(p.get("title", ""))
            if title:
                out[title] = i
    return out


def compact_evidence_hit(hit: Any, number: int, title_to_corpus_id: dict[str, int]) -> dict[str, Any]:
    d = hit_to_plain_dict(hit)

    title = first_string_value(
        d,
        {"title", "paper_title", "source_title", "document_title"},
    )
    text = first_string_value(
        d,
        {"text", "chunk_text", "content", "abstract", "passage", "body"},
    )
    chunk_id = first_value(d, {"chunk_id", "chunkid"})
    score = first_value(d, {"score", "rerank_score", "hybrid_score", "dense_score", "bm25_score"})

    resolved_paper_id = title_to_corpus_id.get(norm_text(title))

    return {
        "number": number,
        "title": title,
        "text": text,
        "chunk_id": chunk_id,
        "score": score,
        "resolved_corpus_paper_id": resolved_paper_id,
    }


async def build_one_split(
    questions: list[dict[str, Any]],
    split_name: str,
    out_path: Path,
    top_k: int,
    title_to_corpus_id: dict[str, int],
    limit: int = 0,
) -> None:
    if limit > 0:
        questions = questions[:limit]

    rows: list[dict[str, Any]] = []

    print(f"\nBuilding {split_name}: {len(questions)} questions, top_k={top_k}")

    for i, q in enumerate(questions, start=1):
        question = q["question"]
        hits = await hybrid_search(question, top_k=top_k)

        evidence = [
            compact_evidence_hit(hit, number=j + 1, title_to_corpus_id=title_to_corpus_id)
            for j, hit in enumerate(hits)
        ]

        # Drop empty evidence texts defensively.
        evidence = [e for e in evidence if e.get("text")]

        rows.append(
            {
                "id": int(q["qid"]),
                "qid": int(q["qid"]),
                "split": split_name,
                "type": q.get("type"),
                "validation_status": q.get("validation_status"),
                "question": question,
                "home_paper_id": q.get("home_paper_id"),
                "home_title": q.get("home_title") or q.get("source_title"),
                "retrieved_corpus_paper_ids_validation": q.get("retrieved_corpus_paper_ids", []),
                "evidence": evidence,
            }
        )

        if i == 1:
            print("First row preview:")
            print(json.dumps(rows[-1], ensure_ascii=False, indent=2)[:2500])

        if i % 25 == 0:
            print(f"  {i}/{len(questions)} done")

    save_json(out_path, rows)
    print(f"Wrote {len(rows)} rows to {out_path}")


async def main_async() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    ap.add_argument("--limit", type=int, default=0, help="smoke-test first N per split; 0=all")
    ap.add_argument("--split", choices=["all", "train", "gold"], default="all")
    args = ap.parse_args()

    if not TRAIN_Q_PATH.exists():
        raise SystemExit(f"Missing {TRAIN_Q_PATH}")
    if not GOLD_Q_PATH.exists():
        raise SystemExit(f"Missing {GOLD_Q_PATH}")
    if not CORPUS_PATH.exists():
        raise SystemExit(f"Missing {CORPUS_PATH}")

    train_q = load_json(TRAIN_Q_PATH)
    gold_q = load_json(GOLD_Q_PATH)
    corpus = load_json(CORPUS_PATH)

    if not isinstance(train_q, list):
        raise SystemExit(f"{TRAIN_Q_PATH} must be a list")
    if not isinstance(gold_q, list):
        raise SystemExit(f"{GOLD_Q_PATH} must be a list")
    if not isinstance(corpus, list):
        raise SystemExit(f"{CORPUS_PATH} must be a list")

    title_to_corpus_id = build_title_to_corpus_id(corpus)

    print(f"Loaded train questions: {len(train_q)}")
    print(f"Loaded gold questions:  {len(gold_q)}")
    print(f"Loaded corpus papers:   {len(corpus)}")
    print(f"title_to_corpus_id:     {len(title_to_corpus_id)}")

    if args.split in {"all", "train"}:
        await build_one_split(
            questions=train_q,
            split_name="distill_train",
            out_path=TRAIN_OUT,
            top_k=args.top_k,
            title_to_corpus_id=title_to_corpus_id,
            limit=args.limit,
        )

    if args.split in {"all", "gold"}:
        await build_one_split(
            questions=gold_q,
            split_name="gold_eval",
            out_path=GOLD_OUT,
            top_k=args.top_k,
            title_to_corpus_id=title_to_corpus_id,
            limit=args.limit,
        )

    print("\nDone.")


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()