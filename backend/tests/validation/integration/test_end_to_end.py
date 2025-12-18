"""
Integration Tests for RAG Retrieval Validation

This module contains integration tests that validate the complete pipeline.
"""
import pytest
import unittest.mock as mock
from src.rag_validation.query_processor import QueryProcessor
from src.rag_validation.vector_search import VectorSearch
from src.rag_validation.content_validator import ContentValidator
from src.rag_validation.metrics_calculator import MetricsCalculator
from src.rag_validation.main import ValidationPipeline


@mock.patch('cohere.Client')
@mock.patch('qdrant_client.QdrantClient')
def test_end_to_end_pipeline_basic_flow(mock_qdrant_client, mock_cohere_client):
    """Test the complete end-to-end pipeline flow."""
    # Mock the Cohere client
    mock_cohere_instance = mock.Mock()
    mock_cohere_response = mock.Mock()
    mock_cohere_response.embeddings = [[0.1, 0.2, 0.3]]
    mock_cohere_instance.embed.return_value = mock_cohere_response
    mock_cohere_client.return_value = mock_cohere_instance

    # Mock the Qdrant client
    mock_qdrant_instance = mock.Mock()
    mock_qdrant_result = mock.Mock()
    mock_qdrant_result.id = "vector-1"
    mock_qdrant_result.score = 0.85
    mock_qdrant_result.payload = {
        "content": "This is a test content about robotics",
        "source": "test_source.txt",
        "metadata": {"test": "value"}
    }
    mock_qdrant_instance.search.return_value = [mock_qdrant_result]
    mock_qdrant_instance.get_collection.return_value = mock.Mock()
    mock_qdrant_client.return_value = mock_qdrant_instance

    # Create the pipeline
    pipeline = ValidationPipeline()

    # Execute a validation
    result = pipeline.validate_single_query(
        query_text="What is robotics?",
        top_k=5,
        similarity_threshold=0.5
    )

    # Verify the result structure
    assert "query_id" in result
    assert "query_text" in result
    assert "retrieved_results" in result
    assert "final_metrics" in result
    assert "pipeline_time_ms" in result
    assert "status" in result

    # Verify the query text matches
    assert result["query_text"] == "What is robotics?"

    # Verify we got results
    assert len(result["retrieved_results"]) == 1
    assert result["retrieved_results"][0]["content"] == "This is a test content about robotics"
    assert result["retrieved_results"][0]["similarity_score"] == 0.85

    # Verify metrics are calculated
    assert result["final_metrics"]["retrieval_accuracy"] >= 0.0
    assert result["final_metrics"]["mean_similarity_score"] >= 0.0
    assert result["final_metrics"]["response_time_ms"] >= 0.0
    assert result["status"] == "success"


@mock.patch('cohere.Client')
@mock.patch('qdrant_client.QdrantClient')
def test_pipeline_with_multiple_results(mock_qdrant_client, mock_cohere_client):
    """Test the pipeline with multiple retrieved results."""
    # Mock the Cohere client
    mock_cohere_instance = mock.Mock()
    mock_cohere_response = mock.Mock()
    mock_cohere_response.embeddings = [[0.1, 0.2, 0.3]]
    mock_cohere_instance.embed.return_value = mock_cohere_response
    mock_cohere_client.return_value = mock_cohere_instance

    # Mock the Qdrant client with multiple results
    mock_qdrant_instance = mock.Mock()
    mock_qdrant_results = []
    for i in range(3):
        mock_result = mock.Mock()
        mock_result.id = f"vector-{i+1}"
        mock_result.score = 0.9 - (i * 0.1)  # 0.9, 0.8, 0.7
        mock_result.payload = {
            "content": f"This is test content {i+1} about robotics",
            "source": f"test_source_{i+1}.txt",
            "metadata": {"test": f"value_{i+1}"}
        }
        mock_qdrant_results.append(mock_result)

    mock_qdrant_instance.search.return_value = mock_qdrant_results
    mock_qdrant_instance.get_collection.return_value = mock.Mock()
    mock_qdrant_client.return_value = mock_qdrant_instance

    # Create the pipeline
    pipeline = ValidationPipeline()

    # Execute a validation
    result = pipeline.validate_single_query(
        query_text="Tell me about robotics?",
        top_k=5,
        similarity_threshold=0.5
    )

    # Verify we got multiple results
    assert len(result["retrieved_results"]) == 3

    # Check that results are ordered by similarity score (highest first, based on mock)
    scores = [r["similarity_score"] for r in result["retrieved_results"]]
    assert scores == sorted(scores, reverse=True)  # Should be in descending order


@mock.patch('cohere.Client')
@mock.patch('qdrant_client.QdrantClient')
def test_pipeline_error_handling(mock_qdrant_client, mock_cohere_client):
    """Test the pipeline error handling."""
    # Mock the Cohere client to raise an exception
    mock_cohere_instance = mock.Mock()
    mock_cohere_instance.embed.side_effect = Exception("API Error")
    mock_cohere_client.return_value = mock_cohere_instance

    # Create the pipeline
    pipeline = ValidationPipeline()

    # Execute a validation that should fail
    result = pipeline.validate_single_query(
        query_text="This will fail",
        top_k=5,
        similarity_threshold=0.5
    )

    # Verify error handling
    assert result["status"] == "error"
    assert "error_message" in result
    assert result["final_metrics"]["failure_count"] >= 1


@mock.patch('cohere.Client')
@mock.patch('qdrant_client.QdrantClient')
def test_pipeline_batch_processing(mock_qdrant_client, mock_cohere_client):
    """Test the pipeline batch processing functionality."""
    # Mock the Cohere client
    mock_cohere_instance = mock.Mock()
    mock_cohere_response = mock.Mock()
    mock_cohere_response.embeddings = [[0.1, 0.2, 0.3]]
    mock_cohere_instance.embed.return_value = mock_cohere_response
    mock_cohere_client.return_value = mock_cohere_instance

    # Mock the Qdrant client
    mock_qdrant_instance = mock.Mock()
    mock_qdrant_result = mock.Mock()
    mock_qdrant_result.id = "vector-1"
    mock_qdrant_result.score = 0.85
    mock_qdrant_result.payload = {
        "content": "This is test content",
        "source": "test_source.txt",
        "metadata": {"test": "value"}
    }
    mock_qdrant_instance.search.return_value = [mock_qdrant_result]
    mock_qdrant_instance.get_collection.return_value = mock.Mock()
    mock_qdrant_client.return_value = mock_qdrant_instance

    # Create the pipeline
    pipeline = ValidationPipeline()

    # Execute batch validation
    results = pipeline.validate_batch_queries(
        query_texts=["Query 1", "Query 2", "Query 3"],
        top_k=3,
        similarity_threshold=0.5
    )

    # Verify we got results for all queries
    assert len(results) == 3
    for result in results:
        assert result["status"] == "success"
        assert "query_text" in result
        assert result["query_text"] in ["Query 1", "Query 2", "Query 3"]


def test_individual_component_integration():
    """Test integration between individual components."""
    # Create components
    query_processor = QueryProcessor.__new__(QueryProcessor)
    content_validator = ContentValidator(similarity_threshold=0.3)
    metrics_calculator = MetricsCalculator()

    # Create a mock query (bypassing API call)
    from src.rag_validation.query_model import Query
    mock_query = Query(
        query_id="test-query",
        text="Test query about robotics",
        embedding=[0.1, 0.2, 0.3]
    )

    # Create mock results
    from src.rag_validation.retrieved_result_model import RetrievedResult
    mock_results = [
        RetrievedResult(
            result_id="result-1",
            query_id=mock_query.query_id,
            content="This is content about robotics",
            similarity_score=0.85,
            original_source="source.txt",
            vector_id="vector-1"
        )
    ]

    # Validate the results
    mock_validations = [
        content_validator.validate_retrieved_content(
            query=mock_query.text,
            retrieved_content=mock_results[0].content,
            original_content=mock_results[0].original_source
        )
    ]

    # Calculate metrics
    metrics = metrics_calculator.calculate_retrieval_metrics(
        query_id=mock_query.query_id,
        results=mock_results,
        validations=mock_validations
    )

    # Verify integration worked
    assert metrics.total_results == 1
    assert metrics.relevant_results >= 0
    assert 0.0 <= metrics.retrieval_accuracy <= 1.0
    assert 0.0 <= metrics.mrr_score <= 1.0


@mock.patch('cohere.Client')
@mock.patch('qdrant_client.QdrantClient')
def test_pipeline_data_flow_validation(mock_qdrant_client, mock_cohere_client):
    """Test that data flows correctly between pipeline components."""
    # Mock the Cohere client
    mock_cohere_instance = mock.Mock()
    mock_cohere_response = mock.Mock()
    mock_cohere_response.embeddings = [[0.1, 0.2, 0.3]]
    mock_cohere_instance.embed.return_value = mock_cohere_response
    mock_cohere_client.return_value = mock_cohere_instance

    # Mock the Qdrant client
    mock_qdrant_instance = mock.Mock()
    mock_qdrant_result = mock.Mock()
    mock_qdrant_result.id = "vector-1"
    mock_qdrant_result.score = 0.85
    mock_qdrant_result.payload = {
        "content": "Robotics is the field of engineering focused on creating robots",
        "source": "robotics_introduction.txt",
        "metadata": {"section": "introduction", "page": 1}
    }
    mock_qdrant_instance.search.return_value = [mock_qdrant_result]
    mock_qdrant_instance.get_collection.return_value = mock.Mock()
    mock_qdrant_client.return_value = mock_qdrant_instance

    # Create the pipeline
    pipeline = ValidationPipeline()

    # Execute validation
    result = pipeline.validate_single_query(
        query_text="What is robotics?",
        top_k=1,
        similarity_threshold=0.5
    )

    # Verify data flow
    assert result["query_text"] == "What is robotics?"
    assert len(result["retrieved_results"]) == 1
    retrieved = result["retrieved_results"][0]

    # Check that the content is preserved through the pipeline
    assert "robotics" in retrieved["content"].lower()
    assert retrieved["similarity_score"] == 0.85

    # Check that validation was performed
    assert "validation_result" in retrieved
    validation = retrieved["validation_result"]
    assert "is_valid" in validation
    assert "semantic_similarity" in validation
    assert "content_accuracy" in validation

    # Check that final metrics were calculated
    assert "final_metrics" in result
    final_metrics = result["final_metrics"]
    assert "retrieval_accuracy" in final_metrics
    assert "mean_similarity_score" in final_metrics
    assert "mrr_score" in final_metrics


if __name__ == "__main__":
    pytest.main([__file__])