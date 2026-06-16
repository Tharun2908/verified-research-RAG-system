from fastapi import APIRouter, Query

from app.services.hybrid_search import hybrid_search

router = APIRouter()


@router.get("/retrieve")
async def retrieve_endpoint(
    q: str = Query(..., description="The search query text"),
    top_k: int = Query(5, ge=1, le=20, description="Final results after reranking"),
    candidate_pool: int = Query(50, ge=10, le=200, description="Candidates kept after fusion, before reranking"),
):
    results = await hybrid_search(q, candidate_pool=candidate_pool, top_k=top_k)
    return {"query": q, "count": len(results), "results": results}