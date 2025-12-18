"""
Unit Tests for Vector Search Components

This module contains comprehensive unit tests for vector search components.
"""
import pytest
import unittest.mock as mock
from src.rag_validation.retrieved_result_model import RetrievedResult
from src.rag_validation.vector_search import VectorSearch


def test_retrieved_result_model_creation():
    """Test RetrievedResult model creation with valid data."""
    result = RetrievedResult(
        result_id="result-1",
        query_id="query-1",
        content="test content",
        similarity_score=0.8,
        original_source="source.txt",
        vector_id="vector-1"
    )

    assert result.result_id == "result-1"
    assert result.query_id == "query-1"
    assert result.content == "test content"
    assert result.similarity_score == 0.8
    assert result.original_source == "source.txt"
    assert result.vector_id == "vector-1"
    assert result.metadata == {}

    # Test validation
    assert result.validate() is True


def test_retrieved_result_model_validation():
    """Test RetrievedResult model validation."""
    # Valid result
    valid_result = RetrievedResult(
        result_id="result-1",
        query_id="query-1",
        content="test content",
        similarity_score=0.8,
        original_source="source.txt",
        vector_id="vector-1"
    )
    assert valid_result.validate() is True

    # Invalid result - similarity score out of range
    try:
        invalid_result = RetrievedResult(
            result_id="result-1",
            query_id="query-1",
            content="test content",
            similarity_score=1.5,  # Invalid
            original_source="source.txt",
            vector_id="vector-1"
        )
        assert False, "Should have raised ValueError"
    except ValueError:
        pass  # Expected

    # Invalid result - empty result_id
    invalid_result2 = RetrievedResult(
        result_id="",
        query_id="query-1",
        content="test content",
        similarity_score=0.8,
        original_source="source.txt",
        vector_id="vector-1"
    )
    assert invalid_result2.validate() is False


def test_retrieved_result_serialization():
    """Test RetrievedResult model serialization/deserialization."""
    original_result = RetrievedResult(
        result_id="result-1",
        query_id="query-1",
        content="test content",
        similarity_score=0.8,
        original_source="source.txt",
        vector_id="vector-1",
        metadata={"test": "value"}
    )

    json_str = original_result.to_json()
    deserialized_result = RetrievedResult.from_json(json_str)

    assert deserialized_result.result_id == original_result.result_id
    assert deserialized_result.query_id == original_result.query_id
    assert deserialized_result.content == original_result.content
    assert deserialized_result.similarity_score == original_result.similarity_score
    assert deserialized_result.original_source == original_result.original_source
    assert deserialized_result.vector_id == original_result.vector_id
    assert deserialized_result.metadata == original_result.metadata
    assert deserialized_result.validate() is True


@mock.patch('qdrant_client.QdrantClient')
def test_vector_search_initialization(mock_qdrant_client):
    """Test VectorSearch initialization."""
    # Mock the Qdrant client
    mock_client_instance = mock.Mock()
    mock_qdrant_client.return_value = mock_client_instance

    search = VectorSearch(url="http://test.com", api_key="test-key", collection_name="test-collection")

    assert search.client is mock_client_instance
    assert search.collection_name == "test-collection"


@mock.patch('qdrant_client.QdrantClient')
def test_vector_search_connect(mock_qdrant_client):
    """Test VectorSearch connect method."""
    # Mock the Qdrant client
    mock_client_instance = mock.Mock()
    mock_client_instance.get_collection.return_value = mock.Mock()
    mock_qdrant_client.return_value = mock_client_instance

    search = VectorSearch(url="http://test.com", api_key="test-key", collection_name="test-collection")
    result = search.connect()

    assert result is True
    mock_client_instance.get_collection.assert_called_once_with("test-collection")


@mock.patch('qdrant_client.QdrantClient')
def test_vector_search_connect_failure(mock_qdrant_client):
    """Test VectorSearch connect method with failure."""
    # Mock the Qdrant client to raise an exception
    mock_client_instance = mock.Mock()
    mock_client_instance.get_collection.side_effect = Exception("Connection failed")
    mock_qdrant_client.return_value = mock_client_instance

    search = VectorSearch(url="http://test.com", api_key="test-key", collection_name="test-collection")
    result = search.connect()

    assert result is False


@mock.patch('qdrant_client.QdrantClient')
def test_vector_search_search(mock_qdrant_client):
    """Test VectorSearch search method."""
    # Mock the Qdrant client and search results
    mock_client_instance = mock.Mock()
    mock_search_result = mock.Mock()
    mock_search_result.id = "vector-1"
    mock_search_result.score = 0.85
    mock_search_result.payload = {
        "content": "test content",
        "source": "source.txt",
        "metadata": {"test": "value"}
    }

    mock_client_instance.search.return_value = [mock_search_result]
    mock_qdrant_client.return_value = mock_client_instance

    search = VectorSearch(url="http://test.com", api_key="test-key", collection_name="test-collection")
    results = search.search([0.1, 0.2, 0.3], top_k=5, similarity_threshold=0.5)

    assert len(results) == 1
    assert isinstance(results[0], RetrievedResult)
    assert results[0].content == "test content"
    assert results[0].similarity_score == 0.85
    assert results[0].vector_id == "vector-1"

    # Verify search was called with correct parameters
    mock_client_instance.search.assert_called_once_with(
        collection_name="test-collection",
        query_vector=[0.1, 0.2, 0.3],
        limit=5,
        score_threshold=0.5
    )


@mock.patch('qdrant_client.QdrantClient')
def test_vector_search_search_failure(mock_qdrant_client):
    """Test VectorSearch search method with failure."""
    # Mock the Qdrant client to raise an exception
    mock_client_instance = mock.Mock()
    mock_client_instance.search.side_effect = Exception("Search failed")
    mock_qdrant_client.return_value = mock_client_instance

    search = VectorSearch(url="http://test.com", api_key="test-key", collection_name="test-collection")

    with pytest.raises(Exception):
        search.search([0.1, 0.2, 0.3])


def test_vector_search_validate_collection_exists():
    """Test VectorSearch validate_collection_exists method."""
    with mock.patch('src.rag_validation.vector_search.VectorSearch.__init__', return_value=None):
        search = VectorSearch.__new__(VectorSearch)
        search.client = mock.Mock()
        search.collection_name = "test-collection"

        # Mock successful collection check
        search.client.get_collection.return_value = mock.Mock()
        assert search.validate_collection_exists() is True

        # Mock failed collection check
        search.client.get_collection.side_effect = Exception("Collection not found")
        assert search.validate_collection_exists() is False


if __name__ == "__main__":
    pytest.main([__file__])