"""Tests for API routes."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock, patch
from app.models.schemas import RetrievalResult


@pytest.fixture
def mock_retrieval_service():
    """Mock retrieval service for testing."""
    service = Mock()
    service.retrieve = AsyncMock(return_value=[
        RetrievalResult(
            chunk_id="test123",
            text="Test result text",
            similarity_score=0.85,
            chunk_index=0,
            document_id="doc1"
        )
    ])
    return service


def test_root_endpoint():
    """Test root endpoint returns basic info."""
    from main import app
    client = TestClient(app)
    
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_query_endpoint_success(mock_retrieval_service):
    """Test query endpoint with valid input."""
    from main import app
    from app.api.dependencies import get_retrieval_service
    
    # Override dependency
    app.dependency_overrides[get_retrieval_service] = lambda: mock_retrieval_service
    
    client = TestClient(app)
    response = client.post("/query", json={"query": "test query"})
    
    assert response.status_code == 200
    data = response.json()
    assert "query" in data
    assert "results" in data
    assert "num_results" in data
    assert data["query"] == "test query"
    assert len(data["results"]) == 1
    assert data["results"][0]["similarity_score"] == 0.85
    
    # Cleanup
    app.dependency_overrides = {}


def test_query_endpoint_empty_query(mock_retrieval_service):
    """Test query endpoint with empty query."""
    from main import app
    
    client = TestClient(app)
    response = client.post("/query", json={"query": ""})
    
    # Should return 422 for validation error
    assert response.status_code == 422


def test_query_endpoint_missing_query():
    """Test query endpoint without query field."""
    from main import app
    
    client = TestClient(app)
    response = client.post("/query", json={})
    
    assert response.status_code == 422


def test_query_endpoint_returns_correct_structure(mock_retrieval_service):
    """Test query response has correct structure."""
    from main import app
    from app.api.dependencies import get_retrieval_service
    
    app.dependency_overrides[get_retrieval_service] = lambda: mock_retrieval_service
    
    client = TestClient(app)
    response = client.post("/query", json={"query": "test"})
    
    assert response.status_code == 200
    data = response.json()
    
    # Check structure
    assert isinstance(data["query"], str)
    assert isinstance(data["results"], list)
    assert isinstance(data["num_results"], int)
    
    # Check result structure
    result = data["results"][0]
    assert "chunk_id" in result
    assert "text" in result
    assert "similarity_score" in result
    assert "chunk_index" in result
    assert "document_id" in result
    
    app.dependency_overrides = {}
