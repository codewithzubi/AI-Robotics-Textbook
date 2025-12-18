"""
Unit Tests for Content Validation Components

This module contains comprehensive unit tests for content validation components.
"""
import pytest
from src.rag_validation.validation_result_model import ValidationResult
from src.rag_validation.content_validator import ContentValidator


def test_validation_result_model_creation():
    """Test ValidationResult model creation with valid data."""
    result = ValidationResult(
        validation_id="validation-1",
        result_id="result-1",
        query_id="query-1",
        semantic_similarity=0.8,
        content_accuracy=0.75,
        validation_notes="Test validation",
        is_valid=True
    )

    assert result.validation_id == "validation-1"
    assert result.result_id == "result-1"
    assert result.query_id == "query-1"
    assert result.semantic_similarity == 0.8
    assert result.content_accuracy == 0.75
    assert result.validation_notes == "Test validation"
    assert result.is_valid is True
    assert result.validator_metadata == {}

    # Test validation
    assert result.validate() is True


def test_validation_result_model_validation():
    """Test ValidationResult model validation."""
    # Valid result
    valid_result = ValidationResult(
        validation_id="validation-1",
        result_id="result-1",
        query_id="query-1",
        semantic_similarity=0.8,
        content_accuracy=0.75,
        validation_notes="Test validation",
        is_valid=True
    )
    assert valid_result.validate() is True

    # Invalid result - semantic similarity out of range
    try:
        invalid_result = ValidationResult(
            validation_id="validation-1",
            result_id="result-1",
            query_id="query-1",
            semantic_similarity=1.5,  # Invalid
            content_accuracy=0.75,
            validation_notes="Test validation",
            is_valid=True
        )
        assert False, "Should have raised ValueError"
    except ValueError:
        pass  # Expected

    # Invalid result - content accuracy out of range
    try:
        invalid_result2 = ValidationResult(
            validation_id="validation-1",
            result_id="result-1",
            query_id="query-1",
            semantic_similarity=0.8,
            content_accuracy=-0.5,  # Invalid
            validation_notes="Test validation",
            is_valid=True
        )
        assert False, "Should have raised ValueError"
    except ValueError:
        pass  # Expected


def test_validation_result_serialization():
    """Test ValidationResult model serialization/deserialization."""
    original_result = ValidationResult(
        validation_id="validation-1",
        result_id="result-1",
        query_id="query-1",
        semantic_similarity=0.8,
        content_accuracy=0.75,
        validation_notes="Test validation",
        is_valid=True,
        validator_metadata={"test": "value"}
    )

    json_str = original_result.to_json()
    deserialized_result = ValidationResult.from_json(json_str)

    assert deserialized_result.validation_id == original_result.validation_id
    assert deserialized_result.result_id == original_result.result_id
    assert deserialized_result.query_id == original_result.query_id
    assert deserialized_result.semantic_similarity == original_result.semantic_similarity
    assert deserialized_result.content_accuracy == original_result.content_accuracy
    assert deserialized_result.validation_notes == original_result.validation_notes
    assert deserialized_result.is_valid == original_result.is_valid
    assert deserialized_result.validator_metadata == original_result.validator_metadata
    assert deserialized_result.validate() is True


def test_content_validator_initialization():
    """Test ContentValidator initialization."""
    validator = ContentValidator(similarity_threshold=0.7)

    assert validator.similarity_threshold == 0.7

    # Test default threshold
    validator_default = ContentValidator()
    assert validator_default.similarity_threshold == 0.7  # Default from constructor


def test_content_validator_validate_retrieved_content():
    """Test ContentValidator validate_retrieved_content method."""
    validator = ContentValidator(similarity_threshold=0.3)  # Lower threshold for test

    # Test with similar content
    result = validator.validate_retrieved_content(
        query="robotics",
        retrieved_content="robotics and artificial intelligence",
        original_content="robotics and artificial intelligence"
    )

    assert isinstance(result, ValidationResult)
    assert result.semantic_similarity >= 0.0  # Should have some similarity
    assert result.content_accuracy >= 0.0
    assert result.validation_notes is not None
    assert result.validate() is True


def test_content_validator_calculate_semantic_similarity():
    """Test ContentValidator calculate_semantic_similarity method."""
    validator = ContentValidator()

    # Test with identical content
    similarity = validator.calculate_semantic_similarity("test content", "test content")
    assert similarity == 1.0

    # Test with completely different content
    similarity = validator.calculate_semantic_similarity("test", "completely different")
    assert similarity == 0.0

    # Test with partially similar content
    similarity = validator.calculate_semantic_similarity("robotics and AI", "robotics and artificial intelligence")
    assert 0.0 <= similarity <= 1.0

    # Test with empty content
    similarity = validator.calculate_semantic_similarity("", "")
    assert similarity == 1.0

    similarity = validator.calculate_semantic_similarity("test", "")
    assert similarity == 0.0

    similarity = validator.calculate_semantic_similarity("", "test")
    assert similarity == 0.0


def test_content_validator_calculate_content_accuracy():
    """Test ContentValidator calculate_content_accuracy method."""
    validator = ContentValidator()

    # Test with identical content
    accuracy = validator.calculate_content_accuracy("test content", "test content")
    assert accuracy == 1.0

    # Test with different content
    accuracy = validator.calculate_content_accuracy("test", "different")
    assert 0.0 <= accuracy <= 1.0


def test_content_validator_validate_content_relevance():
    """Test ContentValidator validate_content_relevance method."""
    validator = ContentValidator(similarity_threshold=0.3)

    # Test with relevant content
    is_relevant, score = validator.validate_content_relevance("robotics", "robotics and AI")
    assert isinstance(is_relevant, bool)
    assert 0.0 <= score <= 1.0

    # Test with irrelevant content
    is_relevant, score = validator.validate_content_relevance("robotics", "completely different topic")
    assert isinstance(is_relevant, bool)
    assert 0.0 <= score <= 1.0


def test_content_validator_edge_cases():
    """Test ContentValidator with edge cases."""
    validator = ContentValidator()

    # Test with very short content
    result = validator.validate_retrieved_content(
        query="a",
        retrieved_content="a",
        original_content="a"
    )
    assert result.semantic_similarity >= 0.0
    assert result.content_accuracy >= 0.0

    # Test with long content
    long_content = "This is a very long content " * 100
    result = validator.validate_retrieved_content(
        query=long_content,
        retrieved_content=long_content,
        original_content=long_content
    )
    assert result.validate() is True


if __name__ == "__main__":
    pytest.main([__file__])