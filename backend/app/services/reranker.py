"""
backend/app/services/reranker.py

Cross-encoder reranking — the precision stage of retrieval, and a direct reuse of
the thesis S2 model (cross-encoder/ms-marco-MiniLM-L-6-v2).

Bi-encoder (dense retrieval): encodes query and doc SEPARATELY into vectors that can
be precomputed/stored. Fast, scalable, but misses fine-grained query-doc interaction.

Cross-encoder (this): feeds (query, doc) TOGETHER into the model and outputs one
relevance score. More accurate because the two texts attend to each other, but nothing
can be precomputed — every (query, candidate) pair is a fresh forward pass. So it only
runs over the small candidate set the cheap retrievers already narrowed down.
"""

from __future__ import annotations

from sentence_transformers import CrossEncoder

# Thesis S2 model. Loaded once at import. Outputs a relevance score per (query, doc) pair
# (higher = more relevant). Runs fine on CPU for small candidate sets.
_reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank(
    query: str,
    candidates: list[tuple[int, str]],
    top_k: int = 5,
) -> list[tuple[int, float]]:
    """
    candidates: list of (chunk_id, chunk_text) to score against the query.
    Returns (chunk_id, rerank_score) pairs, highest relevance first, length <= top_k.
    """
    if not candidates:
        return []

    # Build the (query, doc) pairs the cross-encoder scores jointly.
    pairs = [(query, text) for (_cid, text) in candidates]
    scores = _reranker.predict(pairs)   # one score per pair

    chunk_ids = [cid for (cid, _text) in candidates]
    ranked = sorted(
        zip(chunk_ids, scores),
        key=lambda pair: pair[1],
        reverse=True,
    )
    return [(cid, float(s)) for cid, s in ranked[:top_k]]
