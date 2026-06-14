"""
backend/app/services/ingestion.py

The M2 ingestion pipeline. For each paper:
  1. create one Paper row in Postgres (title/authors/year/source)
  2. treat the abstract as one chunk
  3. embed the chunk text -> 384-dim vector (all-MiniLM-L6-v2)
  4. generate a UUID; write the vector to Qdrant under that UUID
  5. write a Chunk row to Postgres with qdrant_id = that same UUID  <-- the bridge

The same UUID living in both Qdrant (as the point id) and Postgres (as chunks.qdrant_id)
is what lets a later semantic search translate "Qdrant says point X is closest" back into
"here is the actual chunk text and which paper it came from."

Run as a script:  python -m app.services.ingestion
"""

from __future__ import annotations

import json
import uuid
import asyncio

from sentence_transformers import SentenceTransformer
from qdrant_client.models import PointStruct

from app.db.session import AsyncSessionLocal
from app.db import models
from app.db.qdrant_setup import get_qdrant_client, COLLECTION_NAME

# Load the embedding model once at import. 384-dim, matches the Qdrant collection.
_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed(text: str) -> list[float]:
    """Embed a single string into a 384-dim vector (as a plain Python list)."""
    vector = _model.encode(text)
    # .encode returns a numpy array; Qdrant + JSON want a plain list of floats.
    return vector.tolist()


async def ingest_papers(json_path: str) -> int:
    """
    Read a JSON file of papers and ingest each one into Postgres + Qdrant.
    Returns the number of papers ingested.
    """
    with open(json_path, encoding="utf-8") as f:
        papers = json.load(f)

    qdrant = get_qdrant_client()

    ingested = 0
    # One Postgres session for the whole batch.
    async with AsyncSessionLocal() as session:
        for paper in papers:
            # --- 1. Paper row -------------------------------------------------
            paper_row = models.Paper(
                title=paper["title"],
                authors=paper.get("authors"),
                year=paper.get("year"),
                source="sample",
            )
            session.add(paper_row)
            # flush() sends the INSERT now (without committing) so the DB assigns
            # paper_row.paper_id, which we need for the chunk's foreign key.
            await session.flush()

            # --- 2. chunk text + embedding -----------------------------------
            chunk_text = paper["abstract"]
            point_id = str(uuid.uuid4())      # shared id for Qdrant <-> Postgres
            vector = embed(chunk_text)

            # --- 3. write vector to Qdrant -----------------------------------
            qdrant.upsert(
                collection_name=COLLECTION_NAME,
                points=[
                    PointStruct(
                        id=point_id,
                        vector=vector,
                        payload={
                            "title": paper["title"],
                            "text": chunk_text,
                        },
                    )
                ],
            )

            # --- 4. write chunk metadata to Postgres -------------------------
            chunk_row = models.Chunk(
                paper_id=paper_row.paper_id,
                section="abstract",
                text=chunk_text,
                qdrant_id=point_id,          # <-- the bridge
            )
            session.add(chunk_row)
            ingested += 1

        # commit Paper + Chunk rows together at the end.
        await session.commit()

    return ingested


async def main():
    count = await ingest_papers("data/sample_papers.json")
    print(f"Ingested {count} papers (Postgres rows + Qdrant vectors).")


if __name__ == "__main__":
    asyncio.run(main())
