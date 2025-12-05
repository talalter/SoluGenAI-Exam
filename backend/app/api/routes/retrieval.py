"""Retrieval endpoint."""

from fastapi import APIRouter, Depends

from app.models.schemas import QueryRequest, QueryResponse
from app.services.retrieval_service import RetrievalService
from app.api.dependencies import get_retrieval_service

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query(
    request: QueryRequest,
    service: RetrievalService = Depends(get_retrieval_service)
) -> QueryResponse:
    """
    Search for relevant text chunks.

    Returns the top-k most similar chunks with similarity scores.
    """
    results = await service.retrieve(request.query)

    return QueryResponse(
        query=request.query,
        results=results,
        num_results=len(results)
    )
