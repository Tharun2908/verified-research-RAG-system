"""
backend/app/services/bm25_retriever.py

Sparse (keyword) retrieval using BM25 over the ingested chunks.

Unlike dense retrieval (whose index lives persistently in Qdrant), BM25 via the
rank-bm25 library is an IN-MEMORY index built at runtime from the chunk texts.
So this retriever:
  1. loads all chunk texts + ids from Postgres,
  2. tokenizes them with a SHARED tokenizer (must match how the query is tokenized),
  3. builds a BM25Okapi index,
  4. scores a query and returns the top-k (chunk_id, score) pairs.

For this corpus size (thousands of chunks) an in-memory rebuild is fine. At large
scale you'd back this with Elasticsearch/OpenSearch instead.
"""

from __future__ import annotations

import re

from rank_bm25 import BM25Okapi
from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.db import models


def tokenize(text: str) -> list[str]:
    """
    Lowercase + split on non-word characters. The SAME function must tokenize both
    documents and queries, or exact-token matching silently fails (e.g. 'BRCA1'
    vs 'brca1'). Simple and good enough; a production system might add stemming.
    """
    return re.findall(r"\w+", text.lower())


class BM25Retriever:
    """Builds an in-memory BM25 index from the current Postgres chunks."""

    def __init__(self) -> None:
        self.chunk_ids: list[int] = []      # parallel to the corpus: index i -> chunk_id
        self.bm25: BM25Okapi | None = None

    async def build(self) -> int:
        """Load all chunks from Postgres and build the BM25 index. Returns chunk count."""
        async with AsyncSessionLocal() as session:
            stmt = select(models.Chunk.chunk_id, models.Chunk.text)
            rows = (await session.execute(stmt)).all()

        self.chunk_ids = [row.chunk_id for row in rows]
        tokenized_corpus = [tokenize(row.text) for row in rows]
        self.bm25 = BM25Okapi(tokenized_corpus)
        return len(self.chunk_ids)

    def search(self, query: str, top_k: int = 10) -> list[tuple[int, float]]:
        """
        Return up to top_k (chunk_id, bm25_score) pairs, highest score first.
        Must call build() first.
        """
        if self.bm25 is None:
            raise RuntimeError("BM25 index not built — call await build() first.")

        scores = self.bm25.get_scores(tokenize(query))

        # pair each chunk_id with its score, sort by score desc, take top_k
        ranked = sorted(
            zip(self.chunk_ids, scores),
            key=lambda pair: pair[1],
            reverse=True,
        )
        return [(cid, float(s)) for cid, s in ranked if s>0][:top_k]
    
# --- module-level singleton: build the index ONCE, reuse across requests -----
# Rebuilding BM25 per request reads + tokenizes + indexes the whole corpus
# synchronously, blocking the event loop. We build once at startup instead.
_shared_retriever: BM25Retriever | None = None


async def get_bm25_retriever() -> BM25Retriever:
    """Return the process-wide BM25 index, building it once on first use."""
    global _shared_retriever
    if _shared_retriever is None:
        r = BM25Retriever()
        await r.build()
        _shared_retriever = r
    return _shared_retriever


async def warm_bm25() -> int:
    """Build the shared index eagerly (called at app startup). Returns chunk count."""
    r = await get_bm25_retriever()
    return len(r.chunk_ids)

async def rebuild_bm25() -> int:
    """
    Invalidate and rebuild the shared BM25 index.

    The index is built once at startup (see get_bm25_retriever / warm_bm25) to avoid a
    per-request full-corpus rebuild that blocked the event loop. The cost of that choice
    is staleness: the in-memory index does NOT see newly ingested chunks until rebuilt.
    Call this after any ingestion/reset so the sparse retriever reflects the current
    Postgres corpus without an app restart. Returns the new chunk count.
    """
    global _shared_retriever
    _shared_retriever = None          # drop the stale index
    r = await get_bm25_retriever()    # rebuild from the current corpus
    return len(r.chunk_ids)


# --- quick manual test -----------------------------------------------------
async def _demo():
    r = BM25Retriever()
    n = await r.build()
    print(f"Built BM25 index over {n} chunks.")
    for q in ["faithfulness summarization", "dense passage retrieval"]:
        hits = r.search(q, top_k=3)
        print(f"\nQUERY: {q}")
        for cid, score in hits:
            print(f"  chunk_id={cid}  score={score:.3f}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(_demo())
