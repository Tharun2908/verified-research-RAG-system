"""
Creates (if missing) the Qdrant collection that stores chunk embeddings.
Run this once after Qdrant is up. Safe to run repeatedly — it checks first.
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.config import settings

COLLECTION_NAME = "research_papers"
VECTOR_SIZE = 384          # all-MiniLM-L6-v2 output dimension
DISTANCE = Distance.COSINE # standard for sentence-transformer embeddings


def get_qdrant_client() -> QdrantClient:
    return QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)


def ensure_collection():
    client = get_qdrant_client()

    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME in existing:
        print(f"Collection '{COLLECTION_NAME}' already exists.")
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=DISTANCE),
    )
    print(f"Created collection '{COLLECTION_NAME}' (size={VECTOR_SIZE}, distance={DISTANCE}).")


if __name__ == "__main__":
    ensure_collection()