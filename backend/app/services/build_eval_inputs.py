"""
backend/app/services/build_eval_inputs.py

M8 step 2: for each eval question, run hybrid retrieval and capture the top evidence
chunks, then write a SELF-CONTAINED eval_inputs.json that the cluster generation script
can consume without any database access.

Self-contained is the key requirement: the cluster has no Postgres/Qdrant, so every piece
of evidence text must be physically in this file. Each question entry carries its numbered
evidence (number = citation handle, chunk_id = provenance, title + text = what the model reads).

Output: backend/data/eval_inputs.json
  [
    {"id", "type", "question",
     "evidence": [{"number", "chunk_id", "title", "text"}, ...]},
    ...
  ]
"""

from __future__ import annotations

import json
import asyncio

from app.services.hybrid_search import hybrid_search

QUESTIONS_PATH = "data/eval_questions.json"
OUT_PATH = "data/eval_inputs.json"
TOP_K = 5


async def build_inputs() -> int:
    with open(QUESTIONS_PATH, encoding="utf-8") as f:
        spec = json.load(f)
    questions = spec["questions"]

    inputs = []
    for q in questions:
        hits = await hybrid_search(q["question"], top_k=TOP_K)
        evidence = [
            {
                "number": i,
                "chunk_id": h["chunk_id"],
                "title": h["title"],
                "text": h["text"],
            }
            for i, h in enumerate(hits, start=1)
        ]
        inputs.append({
            "id": q["id"],
            "type": q["type"],
            "question": q["question"],
            "evidence": evidence,
        })
        print(f"  Q{q['id']:>2} ({q['type']:<8}) -> {len(evidence)} evidence chunks")

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(inputs, f, ensure_ascii=False, indent=2)

    print(f"\nWrote {len(inputs)} question inputs to {OUT_PATH}")
    return len(inputs)


if __name__ == "__main__":
    asyncio.run(build_inputs())
