"""
Content Validator Module for RAG Retrieval Validation

This module validates retrieved content against original sources.
"""
import uuid
from typing import Tuple
from .validation_result_model import ValidationResult
from ..config.settings import settings


class ContentValidator:
    """
    Validates retrieved content against original sources.
    """

    def __init__(self, similarity_threshold: float = 0.7):
        """
        Initialize the ContentValidator.

        Args:
            similarity_threshold: Minimum similarity threshold for validation
        """
        self.similarity_threshold = similarity_threshold

    def validate_retrieved_content(
        self,
        query: str,
        retrieved_content: str,
        original_content: str
    ) -> ValidationResult:
        """
        Validate retrieved content against original content.

        Args:
            query: Original query text
            retrieved_content: Content retrieved from Qdrant
            original_content: Original source content for comparison

        Returns:
            ValidationResult: ValidationResult object with validation outcome
        """
        validation_id = str(uuid.uuid4())

        # Calculate semantic similarity between query and retrieved content
        semantic_similarity = self.calculate_semantic_similarity(query, retrieved_content)

        # Calculate content accuracy against original content
        content_accuracy = self.calculate_content_accuracy(retrieved_content, original_content)

        # Determine if the result is valid based on thresholds
        is_valid = semantic_similarity >= self.similarity_threshold and content_accuracy >= self.similarity_threshold

        # Create validation notes
        validation_notes = f"Semantic similarity: {semantic_similarity:.3f}, Content accuracy: {content_accuracy:.3f}"

        validation_result = ValidationResult(
            validation_id=validation_id,
            result_id="unknown",  # This will be set by the caller
            query_id="unknown",   # This will be set by the caller
            semantic_similarity=semantic_similarity,
            content_accuracy=content_accuracy,
            validation_notes=validation_notes,
            is_valid=is_valid
        )

        # Validate the result object before returning
        if not validation_result.validate():
            raise ValueError("Generated validation result failed validation")

        return validation_result

    def calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity between two texts using a simple approach.
        In a real implementation, this would use more sophisticated methods like
        sentence transformers or other semantic similarity models.

        Args:
            text1: First text for comparison
            text2: Second text for comparison

        Returns:
            float: Similarity score between 0.0 and 1.0
        """
        # For now, we'll use a simple approach based on common words
        # In a production system, this would use sentence transformers or Cohere's rerank
        if not text1 and not text2:
            return 1.0
        if not text1 or not text2:
            return 0.0

        # Normalize and split into words
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0

        # Calculate Jaccard similarity
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        jaccard_similarity = len(intersection) / len(union)

        # This is a simplified approach; in a real system, we'd use proper semantic similarity models
        return min(1.0, max(0.0, jaccard_similarity))

    def calculate_content_accuracy(self, retrieved_content: str, original_content: str) -> float:
        """
        Calculate how accurate the retrieved content is compared to the original.

        Args:
            retrieved_content: Content retrieved from Qdrant
            original_content: Original source content

        Returns:
            float: Accuracy score between 0.0 and 1.0
        """
        if not retrieved_content and not original_content:
            return 1.0
        if not retrieved_content or not original_content:
            return 0.0

        # Calculate similarity using the same approach as above
        return self.calculate_semantic_similarity(retrieved_content, original_content)

    def validate_content_relevance(self, query: str, content: str) -> Tuple[bool, float]:
        """
        Validate if the content is relevant to the query.

        Args:
            query: Query text
            content: Content to validate

        Returns:
            Tuple[bool, float]: (is_relevant, relevance_score)
        """
        relevance_score = self.calculate_semantic_similarity(query, content)
        is_relevant = relevance_score >= self.similarity_threshold
        return is_relevant, relevance_score