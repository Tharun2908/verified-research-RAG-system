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

The model is constructed LAZILY. Building it at import time meant that importing anything
downstream — a route, a test, even `init_db` — pulled in ~100MB of transformers. Imports
should be free; work happens when work is asked for. main.py warms it at startup, so no
user request pays the load cost.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:                       # for editors/mypy only; never imported at runtime
    from sentence_transformers import CrossEncoder

# Thesis S2 model. Outputs a relevance score per (query, doc) pair (higher = more relevant).
# Runs fine on CPU for small candidate sets.
RERANK_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

_model: CrossEncoder | None = None


def get_reranker() -> CrossEncoder:
    """Lazy: importing this module must not import or download anything heavy."""
    global _model
    if _model is None:
        from sentence_transformers import CrossEncoder   # deferred until first use
        _model = CrossEncoder(RERANK_MODEL_NAME)
    return _model


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
    scores = get_reranker().predict(pairs)      # one score per pair

    chunk_ids = [cid for (cid, _text) in candidates]
    ranked = sorted(
        zip(chunk_ids, scores),
        key=lambda pair: pair[1],
        reverse=True,
    )
    return [(cid, float(s)) for cid, s in ranked[:top_k]]