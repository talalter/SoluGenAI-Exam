"""Custom exceptions."""


class RAGException(Exception):
    """Base exception for RAG system."""
    pass


class EmbeddingError(RAGException):
    """Error during embedding generation."""
    pass


class VectorStoreError(RAGException):
    """Error with vector database operations."""
    pass


class ChunkingError(RAGException):
    """Error during text chunking."""
    pass


class BudgetExceededError(RAGException):
    """Budget limit exceeded."""
    pass