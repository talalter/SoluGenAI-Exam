"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.constants import API_TITLE, API_VERSION
from app.api.routes import ingestion, retrieval

# Initialize settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description="RAG Retrieval System"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ingestion.router, tags=["ingestion"])
app.include_router(retrieval.router, tags=["retrieval"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "RAG Retrieval System API",
        "version": API_VERSION,
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
