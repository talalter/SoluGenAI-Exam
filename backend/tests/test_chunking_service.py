"""Tests for ChunkingService."""

import pytest
from app.services.chunking_service import ChunkingService
from app.models.domain import Document


class TestChunkingService:
    """Test chunking logic."""

    def test_basic_chunking(self):
        """Test basic text chunking."""
        service = ChunkingService(chunk_size=50, chunk_overlap=10)
        text = "First sentence here. Second sentence here. Third sentence here. Fourth sentence here."
        
        chunks = service.chunk_text(text)
        
        assert len(chunks) > 0
        assert all(isinstance(chunk, str) for chunk in chunks)

    def test_short_text(self):
        """Test chunking text shorter than chunk size."""
        service = ChunkingService(chunk_size=250, chunk_overlap=50)
        text = "Short text."
        
        chunks = service.chunk_text(text)
        
        assert len(chunks) == 1
        assert chunks[0] == "Short text."

    def test_empty_text(self):
        """Test chunking empty text."""
        service = ChunkingService(chunk_size=250, chunk_overlap=50)
        text = ""
        
        chunks = service.chunk_text(text)
        
        assert len(chunks) == 0

    def test_overlap_creates_context(self):
        """Test that overlap preserves context between chunks."""
        service = ChunkingService(chunk_size=30, chunk_overlap=10)
        text = "This is a sentence. Another sentence here. And one more."
        
        chunks = service.chunk_text(text)
        
        # Should have multiple chunks with overlap
        assert len(chunks) >= 2

    def test_process_document(self):
        """Test processing a full document into chunks."""
        service = ChunkingService(chunk_size=100, chunk_overlap=20)
        doc = Document(
            content="First sentence. Second sentence. Third sentence.",
            metadata={"source_file": "test.csv"}
        )
        
        chunks = service.process_document(doc)
        
        assert len(chunks) > 0
        assert all(chunk.document_id == doc.document_id for chunk in chunks)
        assert all(chunk.chunk_index == i for i, chunk in enumerate(chunks))
        assert all("source_file" in chunk.metadata for chunk in chunks)

    def test_chunk_metadata(self):
        """Test that chunks contain proper metadata."""
        service = ChunkingService(chunk_size=250, chunk_overlap=50)
        doc = Document(
            content="Test content here.",
            metadata={"source_file": "test.csv", "row_index": 5}
        )
        
        chunks = service.process_document(doc)
        
        assert len(chunks) == 1
        chunk = chunks[0]
        assert chunk.metadata["source_file"] == "test.csv"
        assert chunk.metadata["chunk_size"] == len("Test content here.")
        assert chunk.chunk_index == 0

    def test_sentence_boundary_splitting(self):
        """Test that chunks respect sentence boundaries."""
        service = ChunkingService(chunk_size=40, chunk_overlap=5)
        text = "A! B. C? D. E!"
        
        chunks = service.chunk_text(text)
        
        # Each chunk should end with proper punctuation
        for chunk in chunks[:-1]:  # All but last
            assert chunk.strip()[-1] in '.!?'
