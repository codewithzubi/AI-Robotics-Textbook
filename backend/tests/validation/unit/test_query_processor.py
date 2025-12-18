"""
Unit Tests for Query Processing Components

This module contains comprehensive unit tests for query processing components.
"""
import pytest
import unittest.mock as mock
from src.rag_validation.query_model import Query
from src.rag_validation.query_processor import QueryProcessor


def test_query_model_creation():
    """Test Query model creation with valid data."""
    query = Query(
        query_id="test-id",
        text="test query",
        embedding=[0.1, 0.2, 0.3]
    )

    assert query.query_id == "test-id"
    assert query.text == "test query"
    assert query.embedding == [0.1, 0.2, 0.3]
    assert query.metadata == {}

    # Test validation
    assert query.validate() is True


def test_query_model_validation():
    """Test Query model validation."""
    # Valid query
    valid_query = Query(
        query_id="test-id",
        text="test query",
        embedding=[0.1, 0.2, 0.3]
    )
    assert valid_query.validate() is True

    # Invalid query - empty text
    invalid_query = Query(
        query_id="test-id",
        text="",
        embedding=[0.1, 0.2, 0.3]
    )
    assert invalid_query.validate() is False

    # Invalid query - invalid embedding
    invalid_query2 = Query(
        query_id="test-id",
        text="test query",
        embedding="invalid"
    )
    assert invalid_query2.validate() is False


def test_query_serialization():
    """Test Query model serialization/deserialization."""
    original_query = Query(
        query_id="test-id",
        text="test query",
        embedding=[0.1, 0.2, 0.3],
        metadata={"test": "value"}
    )

    json_str = original_query.to_json()
    deserialized_query = Query.from_json(json_str)

    assert deserialized_query.query_id == original_query.query_id
    assert deserialized_query.text == original_query.text
    assert deserialized_query.embedding == original_query.embedding
    assert deserialized_query.metadata == original_query.metadata
    assert deserialized_query.validate() is True


@mock.patch('cohere.Client')
def test_query_processor_initialization(mock_cohere_client):
    """Test QueryProcessor initialization."""
    # Mock the Cohere client
    mock_client_instance = mock.Mock()
    mock_cohere_client.return_value = mock_client_instance

    processor = QueryProcessor(api_key="test-key")

    assert processor.client is mock_client_instance
    assert processor.model == "embed-english-v3.0"  # Default from settings


@mock.patch('cohere.Client')
def test_query_processor_process_query(mock_cohere_client):
    """Test QueryProcessor process_query method."""
    # Mock the Cohere client
    mock_client_instance = mock.Mock()
    mock_response = mock.Mock()
    mock_response.embeddings = [[0.1, 0.2, 0.3]]
    mock_client_instance.embed.return_value = mock_response
    mock_cohere_client.return_value = mock_client_instance

    processor = QueryProcessor(api_key="test-key")
    query = processor.process_query("test query")

    # Verify the query was processed correctly
    assert query.text == "test query"
    assert query.embedding == [0.1, 0.2, 0.3]
    assert query.validate() is True
    assert len(query.query_id) > 0  # Should have a generated ID

    # Verify that the embed method was called
    mock_client_instance.embed.assert_called_once()


def test_query_processor_validate_query():
    """Test QueryProcessor validate_query method."""
    # Test valid queries
    processor = QueryProcessor.__new__(QueryProcessor)  # Create without init for this test

    assert processor.validate_query("valid query") is True
    assert processor.validate_query("a" * 500) is True  # Within length limit

    # Test invalid queries
    assert processor.validate_query("") is False
    assert processor.validate_query(None) is False
    assert processor.validate_query(123) is False  # Wrong type
    assert processor.validate_query("ab") is False  # Too short
    assert processor.validate_query("a" * 1001) is False  # Too long


def test_query_processor_batch_process():
    """Test QueryProcessor batch_process_queries method."""
    with mock.patch('src.rag_validation.query_processor.QueryProcessor.process_query') as mock_process:
        # Mock successful processing
        mock_query = Query(query_id="test", text="test", embedding=[0.1])
        mock_process.return_value = mock_query

        processor = QueryProcessor.__new__(QueryProcessor)
        queries = processor.batch_process_queries(["query1", "query2"])

        assert len(queries) == 2
        assert all(isinstance(q, Query) for q in queries)


if __name__ == "__main__":
    pytest.main([__file__])