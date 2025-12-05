"""Pytest configuration and shared fixtures."""

import pytest
import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))


@pytest.fixture
def sample_document():
    """Create a sample document for testing."""
    from app.models.domain import Document
    return Document(
        content="This is a test document. It has multiple sentences. For testing purposes.",
        metadata={"source": "test"}
    )


@pytest.fixture
def sample_chunks():
    """Create sample chunks for testing."""
    from app.models.domain import Chunk
    return [
        Chunk(
            text="First chunk of text.",
            document_id="doc1",
            chunk_index=0,
            metadata={"source": "test"}
        ),
        Chunk(
            text="Second chunk of text.",
            document_id="doc1",
            chunk_index=1,
            metadata={"source": "test"}
        )
    ]
