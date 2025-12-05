"""Main RAG retrieval service orchestrator."""

from typing import List, Dict, Any
import pandas as pd

from app.models.domain import Document, Chunk
from app.models.schemas import RetrievalResult
from app.services.embedding_service import EmbeddingService
from app.services.chunking_service import ChunkingService
from app.services.vector_store import VectorStore


class RetrievalService:
    """Main orchestrator for RAG retrieval pipeline."""

    def __init__(
        self,
        embedding_service: EmbeddingService,
        chunking_service: ChunkingService,
        vector_store: VectorStore,
        top_k: int = 5,
        similarity_threshold: float = 0.65
    ):
        self.embedding_service = embedding_service
        self.chunking_service = chunking_service
        self.vector_store = vector_store
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold

    async def ingest_dataset(self, file_path: str) -> Dict[str, Any]:
        """
        Ingest dataset: load → chunk → embed → store.

        Args:
            file_path: Path to dataset file (CSV)

        Returns:
            Ingestion statistics
        """
        # Load dataset
        df = pd.read_csv(file_path)

        # Convert to documents (assuming a 'text' column exists)
        documents = []
        for idx, row in df.iterrows():
            # Adjust this based on your dataset structure
            text_content = str(row.get('text', row.iloc[0]))
            doc = Document(
                content=text_content,
                metadata={"source_file": file_path, "row_index": idx}
            )
            documents.append(doc)

        # Chunk all documents
        all_chunks = []
        for doc in documents:
            chunks = self.chunking_service.process_document(doc)
            all_chunks.extend(chunks)

        # Generate embeddings
        chunk_texts = [chunk.text for chunk in all_chunks]
        embeddings = await self.embedding_service.embed_batch(chunk_texts)

        # Assign embeddings to chunks
        for chunk, embedding in zip(all_chunks, embeddings):
            chunk.embedding = embedding

        # Store in vector database
        await self.vector_store.add_chunks(all_chunks)

        return {
            "num_documents": len(documents),
            "num_chunks": len(all_chunks)
        }

    async def retrieve(self, query: str) -> List[RetrievalResult]:
        """
        Retrieve relevant chunks for a query.

        Args:
            query: Search query

        Returns:
            List of retrieval results
        """
        # Generate query embedding
        query_embedding = await self.embedding_service.embed_text(query)

        # Search vector store
        chunks_with_scores = await self.vector_store.search(
            query_embedding=query_embedding,
            top_k=self.top_k,
            threshold=self.similarity_threshold
        )

        # Convert to API response format
        results = [
            RetrievalResult(
                chunk_id=chunk.chunk_id,
                text=chunk.text,
                similarity_score=score,
                chunk_index=chunk.chunk_index,
                document_id=chunk.document_id
            )
            for chunk, score in chunks_with_scores
        ]

        return results
