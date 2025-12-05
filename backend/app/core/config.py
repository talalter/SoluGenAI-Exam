"""
Application configuration using Pydantic Settings.

This module provides centralized configuration management with environment
variable support and validation.
"""

from typing import List
from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    All settings can be overridden via .env file or environment variables.
    """

    # OpenAI Configuration
    openai_api_key: str = Field(
        ...,
        description="OpenAI API key for embedding generation"
    )

    # Vector Database Configuration
    vector_db_type: str = Field(
        default="chroma",
        description="Type of vector database to use (chroma, pinecone, etc.)"
    )
    chroma_persist_directory: str = Field(
        default="./chroma_db",
        description="Directory for ChromaDB persistence"
    )
    chroma_collection_name: str = Field(
        default="rag_documents",
        description="ChromaDB collection name"
    )

    # RAG Configuration
    chunk_size: int = Field(
        default=250,
        ge=50,
        le=1000,
        description="Maximum size of text chunks in characters"
    )
    chunk_overlap: int = Field(
        default=50,
        ge=0,
        le=500,
        description="Number of overlapping characters between chunks"
    )
    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of top results to return from retrieval"
    )
    similarity_threshold: float = Field(
        default=0.65,
        ge=0.0,
        le=1.0,
        description="Minimum cosine similarity score to accept results"
    )

    # Cost Management
    budget_limit: float = Field(
        default=1.0,
        ge=0.0,
        description="Maximum allowed cost in USD"
    )

    # API Configuration
    api_host: str = Field(
        default="0.0.0.0",
        description="API host address"
    )
    api_port: int = Field(
        default=8000,
        ge=1000,
        le=65535,
        description="API port number"
    )
    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:5173",
        description="Allowed CORS origins (comma-separated)"
    )

    # OpenAI Model Configuration
    embedding_model: str = Field(
        default="text-embedding-3-small",
        description="OpenAI embedding model to use"
    )
    embedding_dimensions: int = Field(
        default=1536,
        description="Dimensions of the embedding vectors"
    )

    @validator("chunk_overlap")
    def validate_chunk_overlap(cls, v, values):
        """Ensure chunk overlap is less than chunk size."""
        if "chunk_size" in values and v >= values["chunk_size"]:
            raise ValueError("chunk_overlap must be less than chunk_size")
        return v

    def get_cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Singleton instance
_settings: Settings | None = None


def get_settings() -> Settings:
    """
    Get or create the settings singleton instance.

    Returns:
        Settings: Application settings instance
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
