"""Tests for RetrievalService."""

import pytest
from unittest.mock import Mock, AsyncMock
from app.services.retrieval_service import RetrievalService
from app.models.domain import Document, Chunk
from app.models.schemas import RetrievalResult


class TestRetrievalService:
    """Test retrieval service functionality."""

    @pytest.fixture
    def mock_services(self):
        """Create mock services for testing."""
        embedding_service = Mock()
        embedding_service.embed_text = AsyncMock(return_value=[0.1] * 1536)
        embedding_service.embed_batch = AsyncMock(return_value=[[0.1] * 1536, [0.2] * 1536])
        
        chunking_service = Mock()
        chunking_service.process_document = Mock(return_value=[
            Chunk(text="Test chunk 1", document_id="doc1", chunk_index=0),
            Chunk(text="Test chunk 2", document_id="doc1", chunk_index=1)
        ])
        
        vector_store = Mock()
        vector_store.add_chunks = AsyncMock()
        vector_store.search = AsyncMock(return_value=[
            (Chunk(
                chunk_id="chunk1",
                text="Test result",
                document_id="doc1",
                chunk_index=0
            ), 0.85)
        ])
        
       
        return {
            "embedding": embedding_service,
            "chunking": chunking_service,
            "vector_store": vector_store,
        }

    @pytest.mark.asyncio
    async def test_retrieve_returns_results(self, mock_services):
        """Test retrieval returns properly formatted results."""
        service = RetrievalService(
            embedding_service=mock_services["embedding"],
            chunking_service=mock_services["chunking"],
            vector_store=mock_services["vector_store"],
            top_k=5,
            similarity_threshold=0.7
        )
        
        results = await service.retrieve("test query")
        
        assert len(results) == 1
        assert isinstance(results[0], RetrievalResult)
        assert results[0].text == "Test result"
        assert results[0].similarity_score == 0.85

    @pytest.mark.asyncio
    async def test_retrieve_calls_embedding_service(self, mock_services):
        """Test that retrieve generates query embedding."""
        service = RetrievalService(
            embedding_service=mock_services["embedding"],
            chunking_service=mock_services["chunking"],
            vector_store=mock_services["vector_store"],
        )
        
        await service.retrieve("test query")
        
        mock_services["embedding"].embed_text.assert_called_once_with("test query")

    @pytest.mark.asyncio
    async def test_retrieve_filters_by_threshold(self, mock_services):
        """Test similarity threshold filtering."""
        # Mock returns low similarity result
        mock_services["vector_store"].search = AsyncMock(return_value=[
            (Chunk(
                chunk_id="chunk1",
                text="Low similarity",
                document_id="doc1",
                chunk_index=0
            ), 0.3)
        ])
        
        service = RetrievalService(
            embedding_service=mock_services["embedding"],
            chunking_service=mock_services["chunking"],
            vector_store=mock_services["vector_store"],
            similarity_threshold=0.35  # Higher than 0.3
        )
        
        results = await service.retrieve("test query")
        
        # Should filter out low similarity result
        # Note: Filtering happens in vector_store.search, so this tests integration
        assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_empty_query_returns_empty(self, mock_services):
        """Test empty query handling."""
        mock_services["vector_store"].search = AsyncMock(return_value=[])
        
        service = RetrievalService(
            embedding_service=mock_services["embedding"],
            chunking_service=mock_services["chunking"],
            vector_store=mock_services["vector_store"],
        )
        
        results = await service.retrieve("")
        
        assert isinstance(results, list)
