"""Ingestion endpoint."""

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import os
import tempfile

from app.models.schemas import IngestionResponse
from app.services.retrieval_service import RetrievalService
from app.api.dependencies import get_retrieval_service

router = APIRouter()


@router.post("/ingest", response_model=IngestionResponse)
async def ingest_dataset(
    file: UploadFile = File(...),
    service: RetrievalService = Depends(get_retrieval_service)
) -> IngestionResponse:
    """
    Ingest and process a dataset.

    Accepts CSV files with text data.
    """
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        # Process the dataset
        result = await service.ingest_dataset(tmp_path)
        return IngestionResponse(**result)

    finally:
        # Clean up temp file
        os.unlink(tmp_path)
