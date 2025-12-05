"""OpenAI embedding service."""

from typing import List
from openai import OpenAI

from app.core.constants import EMBEDDING_MODEL
from app.core.exceptions import EmbeddingError


class EmbeddingService:
    """Handles OpenAI embedding generation."""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = EMBEDDING_MODEL

    async def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for single text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector

        Raises:
            EmbeddingError: If embedding generation fails
        """
        try:
            # Generate embedding
            response = self.client.embeddings.create(
                model=self.model,
                input=text
            )

            return response.data[0].embedding

        except Exception as e:
            raise EmbeddingError(f"Failed to generate embedding: {str(e)}")

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors

        Raises:
            EmbeddingError: If embedding generation fails
        """
        try:
            # Generate embeddings
            response = self.client.embeddings.create(
                model=self.model,
                input=texts
            )

            return [item.embedding for item in response.data]

        except Exception as e:
            raise EmbeddingError(f"Failed to generate embeddings: {str(e)}")
