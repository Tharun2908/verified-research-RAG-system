"""
backend/app/services/hybrid_search.py

The M3 retrieval pipeline — combines all four components into one funnel:

    query
      ├─ BM25 (sparse/keyword)  ─┐
      ├─ Dense (embeddings)     ─┤→ both produce ranked chunk_id lists
      │                          │
      ▼                          ▼
      RRF fusion  → fused candidate chunk_ids (cheap, broad: ~candidate_pool)
      ▼
      fetch candidate texts from Postgres
      ▼
      cross-encoder rerank (thesis S2)  → final top_k (expensive, narrow)
      ▼
      fetch full chunk+paper for final ids → results with text + provenance

Funnel rationale: cheap retrievers (BM25 + dense bi-encoder) run over the whole
corpus to narrow to a small candidate pool; the expensive cross-encoder only reranks
that pool. Accuracy of a cross-encoder at a fraction of its full-corpus cost.
"""

from __future__ import annotations

import asyncio

from sqlalchemy import select
from sentence_transformers import SentenceTransformer

from app.db.session import AsyncSessionLocal
from app.db import models
from app.db.qdrant_setup import get_qdrant_client, COLLECTION_NAME
from app.services.bm25_retriever import BM25Retriever
from app.services.fusion import reciprocal_rank_fusion
from app.services.reranker import rerank

# Shared embedding model for the dense leg (same model used at ingestion — required).
_embed_model = SentenceTransformer("all-MiniLM-L6-v2")


def _dense_search_ids(query: str, top_k: int) -> list[int]:
    """
    Dense leg: embed the query, Qdrant nearest-neighbor, return ranked chunk_ids only.
    We resolve the Qdrant point id (a UUID) -> chunk_id by reading it from the payload?
    No — the chunk_id lives in Postgres keyed by qdrant_id. But for fusion we need
    chunk_ids, so we return the qdrant_ids here and map them in the caller. To keep this
    simple and self-contained, we instead return qdrant_ids and let the caller map.
    """
    qdrant = get_qdrant_client()
    query_vector = _embed_model.encode(query).tolist()
    hits = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
    ).points
    return [hit.id for hit in hits]   # list of qdrant_ids (UUID strings), ranked


async def hybrid_search(
    query: str,
    candidate_pool: int = 50,   # how many to keep after fusion, before reranking
    top_k: int = 5,             # final results after reranking
) -> list[dict]:
    # --- 1. dense leg: ranked qdrant_ids -> map to chunk_ids -------------------
    dense_qdrant_ids = _dense_search_ids(query, top_k=candidate_pool)

    async with AsyncSessionLocal() as session:
        # map qdrant_ids -> chunk_ids, preserving dense rank order
        dense_chunk_ids: list[int] = []
        if dense_qdrant_ids:
            stmt = select(models.Chunk.chunk_id, models.Chunk.qdrant_id).where(
                models.Chunk.qdrant_id.in_([str(q) for q in dense_qdrant_ids])
            )
            rows = (await session.execute(stmt)).all()
            qid_to_cid = {row.qdrant_id: row.chunk_id for row in rows}
            dense_chunk_ids = [
                qid_to_cid[str(q)] for q in dense_qdrant_ids if str(q) in qid_to_cid
            ]

        # --- 2. sparse leg: BM25 ranked chunk_ids -----------------------------
        bm25 = BM25Retriever()
        await bm25.build()
        bm25_hits = bm25.search(query, top_k=candidate_pool)
        bm25_chunk_ids = [cid for (cid, _score) in bm25_hits]

        # --- 3. RRF fuse the two ranked id-lists ------------------------------
        fused = reciprocal_rank_fusion(
            [dense_chunk_ids, bm25_chunk_ids],
            top_k=candidate_pool,
        )
        fused_ids = [cid for (cid, _score) in fused]

        # --- 4. fetch candidate texts for reranking ---------------------------
        if not fused_ids:
            return []
        stmt = select(models.Chunk.chunk_id, models.Chunk.text).where(
            models.Chunk.chunk_id.in_(fused_ids)
        )
        text_rows = (await session.execute(stmt)).all()
        text_map = {row.chunk_id: row.text for row in text_rows}
        candidates = [(cid, text_map[cid]) for cid in fused_ids if cid in text_map]

        # --- 5. cross-encoder rerank to final top_k ---------------------------
        reranked = rerank(query, candidates, top_k=top_k)

        # --- 6. resolve final ids to text + paper provenance ------------------
        results = []
        for cid, score in reranked:
            chunk = await session.get(models.Chunk, cid)
            paper = await session.get(models.Paper, chunk.paper_id) if chunk else None
            results.append({
                "score": round(score, 4),
                "title": paper.title if paper else "(unknown)",
                "text": chunk.text if chunk else "",
            })

    return results


async def _demo():
    for q in [
        "how do you detect when generated text is unfaithful to the source?",
        "efficient passage retrieval with dense embeddings",
    ]:
        print(f"\nQUERY: {q}")
        for i, r in enumerate(await hybrid_search(q, top_k=3), 1):
            print(f"  {i}. [{r['score']}] {r['title']}")


if __name__ == "__main__":
    asyncio.run(_demo())
