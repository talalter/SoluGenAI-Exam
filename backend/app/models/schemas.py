"""API request and response models."""

from typing import List, Dict, Any
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Request model for query endpoint."""
    query: str = Field(..., min_length=1, description="Search query")


class RetrievalResult(BaseModel):
    """Single retrieval result."""
    chunk_id: str
    text: str
    similarity_score: float
    chunk_index: int
    document_id: str


class QueryResponse(BaseModel):
    """Response model for query endpoint."""
    query: str
    results: List[RetrievalResult]
    num_results: int


class IngestionResponse(BaseModel):
    """Response model for ingestion endpoint."""
    num_documents: int
    num_chunks: int
    cost: float
