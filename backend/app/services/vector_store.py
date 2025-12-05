"""Vector database operations using ChromaDB."""

from typing import List, Tuple
import chromadb
from chromadb.config import Settings as ChromaSettings

from app.models.domain import Chunk
from app.core.exceptions import VectorStoreError


class VectorStore:
    """ChromaDB vector store for similarity search."""

    def __init__(self, collection_name: str, persist_directory: str):
        self.client = chromadb.PersistentClient(
            path=persist_directory
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    async def add_chunks(self, chunks: List[Chunk]) -> None:
        """
        Store chunks with embeddings in vector database.

        Args:
            chunks: List of chunks with embeddings

        Raises:
            VectorStoreError: If storage fails
        """
        try:
            if not chunks:
                return

            # Prepare data for ChromaDB
            ids = [chunk.chunk_id for chunk in chunks]
            embeddings = [chunk.embedding for chunk in chunks]
            documents = [chunk.text for chunk in chunks]
            metadatas = [
                {
                    "document_id": chunk.document_id,
                    "chunk_index": chunk.chunk_index,
                    **chunk.metadata
                }
                for chunk in chunks
            ]

            # Add to collection
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )

        except Exception as e:
            raise VectorStoreError(f"Failed to add chunks: {str(e)}")

    async def search(
        self,
        query_embedding: List[float],
        top_k: int,
        threshold: float
    ) -> List[Tuple[Chunk, float]]:
        """
        Search for similar chunks.

        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            threshold: Minimum similarity score

        Returns:
            List of (Chunk, similarity_score) tuples

        Raises:
            VectorStoreError: If search fails
        """
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )

            # Convert results to Chunk objects
            chunks_with_scores = []

            if not results['ids'] or not results['ids'][0]:
                return []

            for idx in range(len(results['ids'][0])):
                # ChromaDB returns distances, convert to similarity (1 - distance for cosine)
                distance = results['distances'][0][idx]
                similarity = 1 - distance

                # Apply threshold
                if similarity < threshold:
                    continue

                chunk = Chunk(
                    chunk_id=results['ids'][0][idx],
                    text=results['documents'][0][idx],
                    document_id=results['metadatas'][0][idx]['document_id'],
                    chunk_index=results['metadatas'][0][idx]['chunk_index'],
                    metadata=results['metadatas'][0][idx]
                )

                chunks_with_scores.append((chunk, similarity))

            return chunks_with_scores

        except Exception as e:
            raise VectorStoreError(f"Search failed: {str(e)}")

    def count(self) -> int:
        """Get total number of chunks stored."""
        return self.collection.count()

    def reset(self) -> None:
        """Clear all data from collection."""
        try:
            self.client.delete_collection(self.collection.name)
            self.collection = self.client.create_collection(
                name=self.collection.name,
                metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            raise VectorStoreError(f"Failed to reset collection: {str(e)}")
