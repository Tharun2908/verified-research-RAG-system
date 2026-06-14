from fastapi import APIRouter, Query

from app.services.search import search

router = APIRouter()


@router.get("/search")
async def search_endpoint(
    q: str = Query(..., description="The search query text"),
    top_k: int = Query(3, ge=1, le=20, description="How many results to return"),
):
    results = await search(q, top_k=top_k)
    return {"query": q, "count": len(results), "results": results}