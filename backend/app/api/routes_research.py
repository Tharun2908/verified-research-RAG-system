from fastapi import APIRouter, Query

from app.services.generator import generate_answer

router = APIRouter()


@router.get("/research")
async def research_endpoint(
    q: str = Query(..., description="The research question"),
    top_k: int = Query(5, ge=1, le=20, description="How many evidence chunks to retrieve"),
):
    result = await generate_answer(q, top_k=top_k)
    return result