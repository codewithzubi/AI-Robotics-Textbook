"""
Unit Tests for API Models

This module contains comprehensive unit tests for the API models.
"""
import pytest
from datetime import datetime
from src.ai_agent.api_models import (
    QueryRequest,
    AgentResponse,
    RetrievalResult,
    AgentSession,
    APIResponse
)


def test_query_request_model_validation():
    """Test QueryRequest model validation."""
    # Test valid query request
    query_request = QueryRequest(
        query="What is inverse kinematics?",
        max_tokens=500,
        temperature=0.7
    )

    assert query_request.query == "What is inverse kinematics?"
    assert query_request.max_tokens == 500
    assert query_request.temperature == 0.7
    assert query_request.metadata == {}


def test_query_request_model_invalid_query():
    """Test QueryRequest model with invalid query."""
    with pytest.raises(ValueError):
        QueryRequest(
            query="",  # Empty query should fail validation
            max_tokens=500,
            temperature=0.7
        )


def test_query_request_model_invalid_max_tokens():
    """Test QueryRequest model with invalid max_tokens."""
    with pytest.raises(ValueError):
        QueryRequest(
            query="Test query",
            max_tokens=0,  # Invalid max_tokens
            temperature=0.7
        )

    with pytest.raises(ValueError):
        QueryRequest(
            query="Test query",
            max_tokens=3000,  # Too large max_tokens
            temperature=0.7
        )


def test_query_request_model_invalid_temperature():
    """Test QueryRequest model with invalid temperature."""
    with pytest.raises(ValueError):
        QueryRequest(
            query="Test query",
            max_tokens=500,
            temperature=-0.1  # Invalid temperature
        )

    with pytest.raises(ValueError):
        QueryRequest(
            query="Test query",
            max_tokens=500,
            temperature=1.5  # Invalid temperature
        )


def test_query_request_model_long_query():
    """Test QueryRequest model with long query."""
    long_query = "a" * 1001  # Too long query

    with pytest.raises(ValueError):
        QueryRequest(
            query=long_query,
            max_tokens=500,
            temperature=0.7
        )


def test_agent_response_model():
    """Test AgentResponse model validation."""
    timestamp = datetime.utcnow()
    agent_response = AgentResponse(
        response_id="test-id",
        query="Test query",
        answer="Test answer",
        sources=["source1", "source2"],
        confidence_score=0.85,
        processing_time_ms=125.5,
        retrieval_context=["context1", "context2"],
        timestamp=timestamp,
        metadata={"test": "value"}
    )

    assert agent_response.response_id == "test-id"
    assert agent_response.query == "Test query"
    assert agent_response.answer == "Test answer"
    assert agent_response.sources == ["source1", "source2"]
    assert agent_response.confidence_score == 0.85
    assert agent_response.processing_time_ms == 125.5
    assert agent_response.retrieval_context == ["context1", "context2"]
    assert agent_response.timestamp == timestamp
    assert agent_response.metadata == {"test": "value"}


def test_agent_response_model_invalid_confidence():
    """Test AgentResponse model with invalid confidence score."""
    with pytest.raises(ValueError):
        AgentResponse(
            response_id="test-id",
            query="Test query",
            answer="Test answer",
            sources=["source1"],
            confidence_score=1.5,  # Invalid confidence score
            processing_time_ms=125.5,
            retrieval_context=["context1"],
            timestamp=datetime.utcnow(),
            metadata={}
        )

    with pytest.raises(ValueError):
        AgentResponse(
            response_id="test-id",
            query="Test query",
            answer="Test answer",
            sources=["source1"],
            confidence_score=-0.1,  # Invalid confidence score
            processing_time_ms=125.5,
            retrieval_context=["context1"],
            timestamp=datetime.utcnow(),
            metadata={}
        )


def test_retrieval_result_model():
    """Test RetrievalResult model validation."""
    retrieval_result = RetrievalResult(
        result_id="test-result",
        query_embedding=[0.1, 0.2, 0.3],
        retrieved_chunks=[
            {"content": "content1", "source": "source1"},
            {"content": "content2", "source": "source2"}
        ],
        similarity_scores=[0.8, 0.7],
        collection_name="test-collection",
        retrieval_time_ms=50.0,
        metadata={"test": "value"}
    )

    assert retrieval_result.result_id == "test-result"
    assert retrieval_result.query_embedding == [0.1, 0.2, 0.3]
    assert len(retrieval_result.retrieved_chunks) == 2
    assert retrieval_result.similarity_scores == [0.8, 0.7]
    assert retrieval_result.collection_name == "test-collection"
    assert retrieval_result.retrieval_time_ms == 50.0
    assert retrieval_result.metadata == {"test": "value"}


def test_retrieval_result_model_empty_values():
    """Test RetrievalResult model with empty values."""
    retrieval_result = RetrievalResult(
        result_id="test-result",
        query_embedding=[],
        retrieved_chunks=[],
        similarity_scores=[],
        collection_name="test-collection",
        retrieval_time_ms=0.0,
        metadata={}
    )

    assert retrieval_result.result_id == "test-result"
    assert retrieval_result.query_embedding == []
    assert retrieval_result.retrieved_chunks == []
    assert retrieval_result.similarity_scores == []
    assert retrieval_result.collection_name == "test-collection"
    assert retrieval_result.retrieval_time_ms == 0.0
    assert retrieval_result.metadata == {}


def test_agent_session_model():
    """Test AgentSession model validation."""
    created_at = datetime.utcnow()
    last_interaction = datetime.utcnow()

    agent_session = AgentSession(
        session_id="test-session",
        created_at=created_at,
        last_interaction=last_interaction,
        interaction_count=5,
        user_id="user123",
        context_history=[
            {"query": "q1", "response": "r1"},
            {"query": "q2", "response": "r2"}
        ],
        metadata={"test": "value"}
    )

    assert agent_session.session_id == "test-session"
    assert agent_session.created_at == created_at
    assert agent_session.last_interaction == last_interaction
    assert agent_session.interaction_count == 5
    assert agent_session.user_id == "user123"
    assert len(agent_session.context_history) == 2
    assert agent_session.metadata == {"test": "value"}


def test_agent_session_model_defaults():
    """Test AgentSession model with default values."""
    created_at = datetime.utcnow()
    last_interaction = datetime.utcnow()

    agent_session = AgentSession(
        session_id="test-session",
        created_at=created_at,
        last_interaction=last_interaction
    )

    assert agent_session.session_id == "test-session"
    assert agent_session.created_at == created_at
    assert agent_session.last_interaction == last_interaction
    assert agent_session.interaction_count == 0  # Default value
    assert agent_session.user_id is None  # Default value
    assert agent_session.context_history == []  # Default value
    assert agent_session.metadata == {}  # Default value


def test_api_response_model_success():
    """Test APIResponse model for success case."""
    timestamp = datetime.utcnow()
    api_response = APIResponse(
        status="success",
        data={"result": "test"},
        error=None,
        request_id="req-test",
        timestamp=timestamp
    )

    assert api_response.status == "success"
    assert api_response.data == {"result": "test"}
    assert api_response.error is None
    assert api_response.request_id == "req-test"
    assert api_response.timestamp == timestamp


def test_api_response_model_error():
    """Test APIResponse model for error case."""
    timestamp = datetime.utcnow()
    api_response = APIResponse(
        status="error",
        data=None,
        error={"type": "ValidationError", "message": "Invalid input"},
        request_id="req-test",
        timestamp=timestamp
    )

    assert api_response.status == "error"
    assert api_response.data is None
    assert api_response.error == {"type": "ValidationError", "message": "Invalid input"}
    assert api_response.request_id == "req-test"
    assert api_response.timestamp == timestamp


def test_api_response_model_serialization():
    """Test APIResponse model serialization."""
    timestamp = datetime.utcnow()
    api_response = APIResponse(
        status="success",
        data={"result": "test"},
        error=None,
        request_id="req-test",
        timestamp=timestamp
    )

    # Test that the model can be serialized to dict
    response_dict = api_response.dict()
    assert response_dict["status"] == "success"
    assert response_dict["data"] == {"result": "test"}
    assert response_dict["error"] is None
    assert response_dict["request_id"] == "req-test"
    assert response_dict["timestamp"] == timestamp


def test_query_request_model_optional_fields():
    """Test QueryRequest model with optional fields."""
    query_request = QueryRequest(
        query="Test query"
        # max_tokens and temperature use defaults
    )

    assert query_request.query == "Test query"
    assert query_request.max_tokens == 500  # Default value
    assert query_request.temperature == 0.7  # Default value
    assert query_request.metadata == {}  # Default value


def test_agent_response_model_required_fields():
    """Test AgentResponse model with required fields only."""
    timestamp = datetime.utcnow()
    agent_response = AgentResponse(
        response_id="test-id",
        query="Test query",
        answer="Test answer",
        sources=[],
        confidence_score=0.5,
        processing_time_ms=100.0,
        retrieval_context=[],
        timestamp=timestamp
        # metadata uses default
    )

    assert agent_response.response_id == "test-id"
    assert agent_response.query == "Test query"
    assert agent_response.answer == "Test answer"
    assert agent_response.sources == []
    assert agent_response.confidence_score == 0.5
    assert agent_response.processing_time_ms == 100.0
    assert agent_response.retrieval_context == []
    assert agent_response.timestamp == timestamp
    assert agent_response.metadata == {}  # Default value


if __name__ == "__main__":
    pytest.main([__file__])