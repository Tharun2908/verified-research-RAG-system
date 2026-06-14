"""
backend/app/services/search.py

Semantic search over the ingested corpus. Given a natural-language query:
  1. embed the query into a 384-dim vector (same model as ingestion)
  2. ask Qdrant for the nearest chunk vectors (cosine similarity)
  3. for each hit, use the Qdrant point id to look up the full Chunk + Paper in Postgres
     (the qdrant_id bridge), so we return real text and provenance, not just an id

Run as a script:  python -m app.services.search
"""

from __future__ import annotations

import asyncio

from sqlalchemy import select
from sentence_transformers import SentenceTransformer

from app.db.session import AsyncSessionLocal
from app.db import models
from app.db.qdrant_setup import get_qdrant_client, COLLECTION_NAME

# Same embedding model as ingestion — the query MUST be embedded the same way the
# chunks were, or the vectors live in different spaces and similarity is meaningless.
_model = SentenceTransformer("all-MiniLM-L6-v2")


async def search(query: str, top_k: int = 3) -> list[dict]:
    """Return the top_k most semantically similar chunks to the query."""
    qdrant = get_qdrant_client()

    # 1. embed the query
    query_vector = _model.encode(query).tolist()

    # 2. nearest-neighbor search in Qdrant
    hits = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
    ).points

    # 3. resolve each hit back to its Postgres chunk + paper via qdrant_id
    results = []
    async with AsyncSessionLocal() as session:
        for hit in hits:
            qdrant_id = hit.id          # the shared UUID
            score = hit.score           # cosine similarity (higher = more similar)

            # find the Chunk whose qdrant_id matches this point
            stmt = select(models.Chunk).where(models.Chunk.qdrant_id == str(qdrant_id))
            chunk = (await session.execute(stmt)).scalar_one_or_none()

            if chunk is None:
                # vector existed in Qdrant but no matching Postgres row (shouldn't happen
                # if ingestion was clean) — skip defensively.
                continue

            # get the parent paper for provenance
            paper = await session.get(models.Paper, chunk.paper_id)

            results.append({
                "score": round(score, 4),
                "title": paper.title if paper else "(unknown)",
                "text": chunk.text,
            })

    return results


async def main():
    queries = [
        "how do you detect when generated text is unfaithful to the source?",
        "efficient passage retrieval with dense embeddings",
    ]
    for q in queries:
        print(f"\nQUERY: {q}")
        results = await search(q, top_k=3)
        for i, r in enumerate(results, 1):
            print(f"  {i}. [{r['score']}] {r['title']}")


if __name__ == "__main__":
    asyncio.run(main())
