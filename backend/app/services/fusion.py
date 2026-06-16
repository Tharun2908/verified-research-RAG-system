# backend/app/services/fusion.py
"""Reciprocal Rank Fusion: merge multiple ranked id-lists into one ranking."""

def reciprocal_rank_fusion(
    ranked_lists: list[list[int]],
    k: int = 60,
    top_k: int = 10,
) -> list[tuple[int, float]]:
    """
    ranked_lists: each is a list of chunk_ids in ranked order (best first).
    Returns (chunk_id, rrf_score) pairs, highest first, length <= top_k.
    """
    scores: dict[int, float] = {}
    for ranked in ranked_lists:
        for rank, chunk_id in enumerate(ranked, start=1):   # rank is 1-based
            scores[chunk_id] = scores.get(chunk_id, 0.0) + 1.0 / (k + rank)

    fused = sorted(scores.items(), key=lambda pair: pair[1], reverse=True)
    return fused[:top_k]