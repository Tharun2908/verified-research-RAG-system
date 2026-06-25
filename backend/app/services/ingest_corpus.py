"""
backend/app/services/ingest_corpus.py

Phase A (M8) Step 2: batch-embedding ingestion of a real corpus (arXiv abstracts) into
Postgres + Qdrant. Upgrades M2's one-at-a-time loop to:
  - BATCH embedding: model.encode([all_texts], batch_size=32) in one call (much faster
    than 250 separate calls).
  - BATCHED Qdrant upserts: ~100 points per upsert call (fewer network round-trips).
  - optional RESET: wipe existing papers/chunks (Postgres) + recreate the Qdrant
    collection, so the eval runs against a clean, known corpus.

Same dual-store design as M2: each chunk gets a UUID written to BOTH Qdrant (point id)
and Postgres (chunks.qdrant_id) — the bridge.
"""

from __future__ import annotations

import json
import uuid
import asyncio

from sqlalchemy import delete
from sentence_transformers import SentenceTransformer
from qdrant_client.models import PointStruct, Distance, VectorParams

from app.db.session import AsyncSessionLocal
from app.db import models
from app.db.qdrant_setup import get_qdrant_client, COLLECTION_NAME, VECTOR_SIZE, DISTANCE

_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_batch(texts: list[str]) -> list[list[float]]:
    """Embed many texts in one batched call. Returns a list of 384-dim vectors."""
    vectors = _model.encode(texts, batch_size=32, show_progress_bar=True)
    return [v.tolist() for v in vectors]


async def _reset_postgres(session) -> None:
    """Delete existing chunk/paper rows (and dependent rows) for a clean corpus.
    Order matters for FKs: evidence -> claims -> research_results -> research_jobs,
    then chunks -> papers. We clear the whole research history too so old jobs that
    referenced sample chunks don't dangle."""
    await session.execute(delete(models.Evidence))
    await session.execute(delete(models.Feedback))
    await session.execute(delete(models.Claim))
    await session.execute(delete(models.ResearchResult))
    await session.execute(delete(models.ResearchJob))
    await session.execute(delete(models.Chunk))
    await session.execute(delete(models.Paper))
    await session.commit()


def _reset_qdrant() -> None:
    """Recreate the Qdrant collection (drops all existing vectors)."""
    client = get_qdrant_client()
    client.delete_collection(collection_name=COLLECTION_NAME)
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=DISTANCE),
    )


async def ingest_corpus(json_path: str, reset: bool = True) -> int:
    with open(json_path, encoding="utf-8") as f:
        papers = json.load(f)

    qdrant = get_qdrant_client()

    async with AsyncSessionLocal() as session:
        if reset:
            print("Resetting Postgres + Qdrant...")
            await _reset_postgres(session)
            _reset_qdrant()

        # --- 1. create Paper rows, collect (chunk_text, paper_id) ---
        chunk_texts: list[str] = []
        paper_ids: list[int] = []
        for paper in papers:
            paper_row = models.Paper(
                title=paper["title"],
                authors=paper.get("authors"),
                year=paper.get("year"),
                source="arxiv",
            )
            session.add(paper_row)
            await session.flush()             # assigns paper_id
            chunk_texts.append(paper["abstract"])
            paper_ids.append(paper_row.paper_id)

        # --- 2. BATCH embed all abstracts at once ---
        print(f"Batch-embedding {len(chunk_texts)} abstracts...")
        vectors = embed_batch(chunk_texts)

        # --- 3. build chunk rows + Qdrant points (shared UUID) ---
        points = []
        for text, pid, vec in zip(chunk_texts, paper_ids, vectors):
            point_id = str(uuid.uuid4())
            session.add(models.Chunk(
                paper_id=pid,
                section="abstract",
                text=text,
                qdrant_id=point_id,
            ))
            points.append(PointStruct(
                id=point_id,
                vector=vec,
                payload={"text": text},
            ))

        await session.commit()

        # --- 4. BATCHED Qdrant upserts (~100 points per call) ---
        print(f"Upserting {len(points)} vectors to Qdrant...")
        BATCH = 100
        for i in range(0, len(points), BATCH):
            qdrant.upsert(collection_name=COLLECTION_NAME, points=points[i:i + BATCH])

    # --- 5. refresh the in-memory BM25 index so it reflects the new corpus ---
    # Matters when ingestion is triggered IN-PROCESS (e.g. a future /ingest endpoint):
    # the server's shared BM25 singleton is stale until rebuilt. When this module is
    # run as a standalone CLI script, this rebuilds in the script's own process (a
    # no-op for the server) — in that case, restart the app so startup rebuilds it.
    from app.services.bm25_retriever import rebuild_bm25
    await rebuild_bm25()

    return len(papers)


async def main():
    n = await ingest_corpus("data/arxiv_papers.json", reset=True)
    print(f"Ingested {n} papers (batch-embedded, dual-store).")


if __name__ == "__main__":
    asyncio.run(main())
