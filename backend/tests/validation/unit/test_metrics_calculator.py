"""
Unit Tests for Metrics Calculation Components

This module contains comprehensive unit tests for metrics calculation components.
"""
import pytest
from src.rag_validation.retrieval_metrics_model import RetrievalMetrics
from src.rag_validation.metrics_calculator import MetricsCalculator
from src.rag_validation.retrieved_result_model import RetrievedResult
from src.rag_validation.validation_result_model import ValidationResult


def test_retrieval_metrics_model_creation():
    """Test RetrievalMetrics model creation with valid data."""
    metrics = RetrievalMetrics(
        metrics_id="metrics-1",
        query_id="query-1",
        total_results=10,
        relevant_results=8,
        retrieval_accuracy=0.8,
        mean_similarity_score=0.75,
        response_time_ms=100.0,
        failure_count=2,
        mrr_score=0.85
    )

    assert metrics.metrics_id == "metrics-1"
    assert metrics.query_id == "query-1"
    assert metrics.total_results == 10
    assert metrics.relevant_results == 8
    assert metrics.retrieval_accuracy == 0.8
    assert metrics.mean_similarity_score == 0.75
    assert metrics.response_time_ms == 100.0
    assert metrics.failure_count == 2
    assert metrics.mrr_score == 0.85
    assert metrics.metadata == {}

    # Test validation
    assert metrics.validate() is True


def test_retrieval_metrics_model_validation():
    """Test RetrievalMetrics model validation."""
    # Valid metrics
    valid_metrics = RetrievalMetrics(
        metrics_id="metrics-1",
        query_id="query-1",
        total_results=10,
        relevant_results=8,
        retrieval_accuracy=0.8,
        mean_similarity_score=0.75,
        response_time_ms=100.0,
        failure_count=2,
        mrr_score=0.85
    )
    assert valid_metrics.validate() is True

    # Invalid metrics - negative total results
    try:
        invalid_metrics = RetrievalMetrics(
            metrics_id="metrics-1",
            query_id="query-1",
            total_results=-1,  # Invalid
            relevant_results=8,
            retrieval_accuracy=0.8,
            mean_similarity_score=0.75,
            response_time_ms=100.0,
            failure_count=2,
            mrr_score=0.85
        )
        assert False, "Should have raised ValueError"
    except ValueError:
        pass  # Expected

    # Invalid metrics - relevant results > total results
    try:
        invalid_metrics2 = RetrievalMetrics(
            metrics_id="metrics-1",
            query_id="query-1",
            total_results=5,  # Less than relevant
            relevant_results=8,  # More than total
            retrieval_accuracy=0.8,
            mean_similarity_score=0.75,
            response_time_ms=100.0,
            failure_count=2,
            mrr_score=0.85
        )
        assert False, "Should have raised ValueError"
    except ValueError:
        pass  # Expected

    # Invalid metrics - retrieval accuracy out of range
    try:
        invalid_metrics3 = RetrievalMetrics(
            metrics_id="metrics-1",
            query_id="query-1",
            total_results=10,
            relevant_results=8,
            retrieval_accuracy=1.5,  # Invalid
            mean_similarity_score=0.75,
            response_time_ms=100.0,
            failure_count=2,
            mrr_score=0.85
        )
        assert False, "Should have raised ValueError"
    except ValueError:
        pass  # Expected


def test_retrieval_metrics_serialization():
    """Test RetrievalMetrics model serialization/deserialization."""
    original_metrics = RetrievalMetrics(
        metrics_id="metrics-1",
        query_id="query-1",
        total_results=10,
        relevant_results=8,
        retrieval_accuracy=0.8,
        mean_similarity_score=0.75,
        response_time_ms=100.0,
        failure_count=2,
        mrr_score=0.85,
        metadata={"test": "value"}
    )

    json_str = original_metrics.to_json()
    deserialized_metrics = RetrievalMetrics.from_json(json_str)

    assert deserialized_metrics.metrics_id == original_metrics.metrics_id
    assert deserialized_metrics.query_id == original_metrics.query_id
    assert deserialized_metrics.total_results == original_metrics.total_results
    assert deserialized_metrics.relevant_results == original_metrics.relevant_results
    assert deserialized_metrics.retrieval_accuracy == original_metrics.retrieval_accuracy
    assert deserialized_metrics.mean_similarity_score == original_metrics.mean_similarity_score
    assert deserialized_metrics.response_time_ms == original_metrics.response_time_ms
    assert deserialized_metrics.failure_count == original_metrics.failure_count
    assert deserialized_metrics.mrr_score == original_metrics.mrr_score
    assert deserialized_metrics.metadata == original_metrics.metadata
    assert deserialized_metrics.validate() is True


def test_metrics_calculator_initialization():
    """Test MetricsCalculator initialization."""
    calculator = MetricsCalculator()
    assert calculator is not None


def test_metrics_calculator_calculate_retrieval_metrics():
    """Test MetricsCalculator calculate_retrieval_metrics method."""
    calculator = MetricsCalculator()

    # Create test results
    results = [
        RetrievedResult(
            result_id=f"result-{i}",
            query_id="query-1",
            content=f"content {i}",
            similarity_score=0.8 - (i * 0.1),
            original_source="source.txt",
            vector_id=f"vector-{i}"
        )
        for i in range(5)
    ]

    # Create test validations
    validations = [
        ValidationResult(
            validation_id=f"validation-{i}",
            result_id=f"result-{i}",
            query_id="query-1",
            semantic_similarity=0.8 - (i * 0.1),
            content_accuracy=0.75 - (i * 0.1),
            validation_notes=f"Validation for result {i}",
            is_valid=True if i < 4 else False  # Last one is invalid
        )
        for i in range(5)
    ]

    # Calculate metrics
    metrics = calculator.calculate_retrieval_metrics(
        query_id="query-1",
        results=results,
        validations=validations
    )

    assert isinstance(metrics, RetrievalMetrics)
    assert metrics.total_results == 5
    assert metrics.relevant_results == 4  # 4 valid out of 5
    assert metrics.retrieval_accuracy == 0.8  # 4/5
    assert metrics.mean_similarity_score == 0.6  # Average of [0.8, 0.7, 0.6, 0.5, 0.4]
    assert metrics.failure_count == 1  # 1 invalid out of 5
    assert 0.0 <= metrics.mrr_score <= 1.0
    assert metrics.query_id == "query-1"
    assert metrics.validate() is True


def test_metrics_calculator_calculate_mrr():
    """Test MetricsCalculator calculate_mrr method."""
    calculator = MetricsCalculator()

    # Create test results and validations
    results = [
        RetrievedResult(
            result_id="result-1",
            query_id="query-1",
            content="content 1",
            similarity_score=0.9,
            original_source="source.txt",
            vector_id="vector-1"
        ),
        RetrievedResult(
            result_id="result-2",
            query_id="query-1",
            content="content 2",
            similarity_score=0.8,
            original_source="source.txt",
            vector_id="vector-2"
        ),
        RetrievedResult(
            result_id="result-3",
            query_id="query-1",
            content="content 3",
            similarity_score=0.7,
            original_source="source.txt",
            vector_id="vector-3"
        )
    ]

    validations = [
        ValidationResult(
            validation_id="validation-1",
            result_id="result-1",
            query_id="query-1",
            semantic_similarity=0.9,
            content_accuracy=0.85,
            validation_notes="Valid",
            is_valid=False  # First is invalid
        ),
        ValidationResult(
            validation_id="validation-2",
            result_id="result-2",
            query_id="query-1",
            semantic_similarity=0.8,
            content_accuracy=0.75,
            validation_notes="Valid",
            is_valid=True  # Second is valid - rank 2
        ),
        ValidationResult(
            validation_id="validation-3",
            result_id="result-3",
            query_id="query-1",
            semantic_similarity=0.7,
            content_accuracy=0.65,
            validation_notes="Valid",
            is_valid=False  # Third is invalid
        )
    ]

    mrr = calculator.calculate_mrr(results, validations)
    # First valid result is at position 2 (0-indexed), so reciprocal rank is 1/2 = 0.5
    assert mrr == 0.5


def test_metrics_calculator_calculate_mrr_no_valid():
    """Test MetricsCalculator calculate_mrr method with no valid results."""
    calculator = MetricsCalculator()

    results = [
        RetrievedResult(
            result_id="result-1",
            query_id="query-1",
            content="content 1",
            similarity_score=0.9,
            original_source="source.txt",
            vector_id="vector-1"
        )
    ]

    validations = [
        ValidationResult(
            validation_id="validation-1",
            result_id="result-1",
            query_id="query-1",
            semantic_similarity=0.9,
            content_accuracy=0.85,
            validation_notes="Invalid",
            is_valid=False  # All invalid
        )
    ]

    mrr = calculator.calculate_mrr(results, validations)
    assert mrr == 0.0  # No valid results


def test_metrics_calculator_calculate_aggregated_metrics():
    """Test MetricsCalculator calculate_aggregated_metrics method."""
    calculator = MetricsCalculator()

    # Create test metrics
    metrics_list = [
        RetrievalMetrics(
            metrics_id=f"metrics-{i}",
            query_id=f"query-{i}",
            total_results=10,
            relevant_results=8,
            retrieval_accuracy=0.8,
            mean_similarity_score=0.75,
            response_time_ms=100.0,
            failure_count=2,
            mrr_score=0.85
        )
        for i in range(3)
    ]

    aggregated = calculator.calculate_aggregated_metrics(metrics_list)

    assert aggregated.total_results == 30  # 10*3
    assert aggregated.relevant_results == 24  # 8*3
    assert aggregated.retrieval_accuracy == 0.8  # Average of 0.8, 0.8, 0.8
    assert aggregated.mean_similarity_score == 0.75  # Average of 0.75, 0.75, 0.75
    assert aggregated.response_time_ms == 300.0  # Sum of 100.0, 100.0, 100.0
    assert aggregated.failure_count == 6  # 2*3
    assert aggregated.mrr_score == 0.85  # Average of 0.85, 0.85, 0.85


def test_metrics_calculator_calculate_aggregated_metrics_empty():
    """Test MetricsCalculator calculate_aggregated_metrics method with empty list."""
    calculator = MetricsCalculator()

    aggregated = calculator.calculate_aggregated_metrics([])

    assert aggregated.total_results == 0
    assert aggregated.relevant_results == 0
    assert aggregated.retrieval_accuracy == 0.0
    assert aggregated.mean_similarity_score == 0.0
    assert aggregated.response_time_ms == 0.0
    assert aggregated.failure_count == 0
    assert aggregated.mrr_score == 0.0


def test_metrics_calculator_calculate_response_time_metrics():
    """Test MetricsCalculator calculate_response_time_metrics method."""
    calculator = MetricsCalculator()

    response_times = [50.0, 100.0, 150.0, 200.0, 250.0]

    time_metrics = calculator.calculate_response_time_metrics(response_times)

    assert time_metrics["avg_response_time"] == 150.0
    assert time_metrics["min_response_time"] == 50.0
    assert time_metrics["max_response_time"] == 250.0
    assert time_metrics["p95_response_time"] == 250.0  # 95th percentile of 5 items is the max


def test_metrics_calculator_calculate_response_time_metrics_empty():
    """Test MetricsCalculator calculate_response_time_metrics method with empty list."""
    calculator = MetricsCalculator()

    time_metrics = calculator.calculate_response_time_metrics([])

    assert time_metrics["avg_response_time"] == 0.0
    assert time_metrics["min_response_time"] == 0.0
    assert time_metrics["max_response_time"] == 0.0
    assert time_metrics["p95_response_time"] == 0.0


if __name__ == "__main__":
    pytest.main([__file__])