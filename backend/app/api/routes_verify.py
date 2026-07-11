from fastapi import APIRouter, Query, HTTPException
from app.services.verification_service import verify_question

router = APIRouter()


@router.get("/verify")
async def verify_endpoint(
    q: str = Query(..., description="The research question to answer and verify"),
    top_k: int = Query(5, ge=1, le=20, description="How many evidence chunks to retrieve"),
):
    result = await verify_question(q, top_k=top_k)
    if result["verification_status"] == "generation_failed":
        # A generation outage is an upstream failure, not a verified answer.
        raise HTTPException(status_code=503, detail=result["error"])
    return result