#!/usr/bin/env python3
"""
Simple test to verify the RAG validation pipeline works with mocked dependencies
"""
import sys
import os
import unittest.mock as mock

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from backend.src.rag_validation.query_processor import QueryProcessor
from backend.src.rag_validation.vector_search import VectorSearch
from backend.src.rag_validation.content_validator import ContentValidator
from backend.src.rag_validation.metrics_calculator import MetricsCalculator
from backend.src.rag_validation.main import ValidationPipeline


def test_pipeline_with_mocks():
    """Test the pipeline with mocked external dependencies"""
    print("Testing RAG validation pipeline with mocked dependencies...")

    # Mock the Cohere client
    with mock.patch('cohere.Client') as mock_cohere:
        mock_cohere_instance = mock.Mock()
        mock_cohere_response = mock.Mock()
        mock_cohere_response.embeddings = [[0.1, 0.2, 0.3]]
        mock_cohere_instance.embed.return_value = mock_cohere_response
        mock_cohere.return_value = mock_cohere_instance

        # Mock the Qdrant client
        with mock.patch('qdrant_client.QdrantClient') as mock_qdrant:
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
            mock_qdrant.return_value = mock_qdrant_instance

            # Create the pipeline with mocked dependencies
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
            assert result["status"] == "success"

            print("✅ Pipeline test passed!")
            print(f"Query: {result['query_text']}")
            print(f"Results: {len(result['retrieved_results'])}")
            print(f"Status: {result['status']}")
            print(f"Metrics: {result['final_metrics']}")


if __name__ == "__main__":
    test_pipeline_with_mocks()
    print("\n🎉 All tests passed! RAG validation pipeline is working correctly.")