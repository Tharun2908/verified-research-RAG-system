"""
backend/app/db/init_db.py

Create the Postgres schema and the Qdrant collection. Run ONCE before ingesting the corpus.

    python -m app.db.init_db

Idempotent: safe to re-run. Existing tables are left alone (create_all is a no-op for them);
the Qdrant collection is only created if it does not already exist.

This exists because the repo previously had no way to bootstrap a fresh database — the
quickstart assumed the schema was already there, which is only true if you happened to have
created it by hand. A clone-and-run had no path.
"""

from __future__ import annotations

import asyncio

from app.db.session import engine
from app.db import models
from app.db.qdrant_setup import get_qdrant_client, COLLECTION_NAME

# all-MiniLM-L6-v2 embedding size — must match the model used in hybrid_search.py
VECTOR_SIZE = 384


async def create_tables() -> None:
    """Create every table declared on the SQLAlchemy Base."""
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    tables = ", ".join(sorted(models.Base.metadata.tables))
    print(f"[init_db] Postgres tables ready: {tables}")


def create_collection() -> None:
    """Create the Qdrant collection if it does not exist."""
    from qdrant_client.models import Distance, VectorParams

    client = get_qdrant_client()
    existing = {c.name for c in client.get_collections().collections}

    if COLLECTION_NAME in existing:
        info = client.get_collection(COLLECTION_NAME)
        print(f"[init_db] Qdrant collection '{COLLECTION_NAME}' already exists "
              f"({info.points_count} points).")
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
    )
    print(f"[init_db] Qdrant collection '{COLLECTION_NAME}' created "
          f"(dim={VECTOR_SIZE}, cosine).")


async def main() -> None:
    await create_tables()
    create_collection()
    print("\n[init_db] Done. Next: python -m app.services.ingest_corpus")


if __name__ == "__main__":
    asyncio.run(main())
