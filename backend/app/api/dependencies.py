"""Dependency injection for API routes."""

from functools import lru_cache

from app.core.config import get_settings, Settings
from app.services.embedding_service import EmbeddingService
from app.services.chunking_service import ChunkingService
from app.services.vector_store import VectorStore
from app.services.retrieval_service import RetrievalService


# Singletons
_vector_store: VectorStore | None = None


@lru_cache()
def get_app_settings() -> Settings:
    """Get settings singleton."""
    return get_settings()


def get_embedding_service() -> EmbeddingService:
    """Create embedding service instance."""
    settings = get_app_settings()
    return EmbeddingService(
        api_key=settings.openai_api_key
    )


def get_chunking_service() -> ChunkingService:
    """Create chunking service instance."""
    settings = get_app_settings()
    return ChunkingService(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap
    )


def get_vector_store() -> VectorStore:
    """Get or create vector store singleton."""
    global _vector_store
    if _vector_store is None:
        settings = get_app_settings()
        _vector_store = VectorStore(
            collection_name=settings.chroma_collection_name,
            persist_directory=settings.chroma_persist_directory
        )
    return _vector_store


def get_retrieval_service() -> RetrievalService:
    """Create retrieval service instance."""
    settings = get_app_settings()
    return RetrievalService(
        embedding_service=get_embedding_service(),
        chunking_service=get_chunking_service(),
        vector_store=get_vector_store(),
        top_k=settings.top_k,
        similarity_threshold=settings.similarity_threshold
    )
