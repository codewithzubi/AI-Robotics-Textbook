"""
Content Grounding for AI Agent

This module ensures that agent responses are grounded in retrieved content only,
preventing hallucination and maintaining accuracy.
"""
from typing import List, Dict, Any, Tuple
from ..rag_validation.content_validator import ContentValidator
from .api_models import AgentResponse


class ContentGrounding:
    """
    Ensures agent responses are properly grounded in retrieved content.
    """

    def __init__(self, content_validator: ContentValidator = None):
        """
        Initialize the ContentGrounding module.

        Args:
            content_validator: ContentValidator instance. If None, creates default
        """
        self.content_validator = content_validator or ContentValidator()

    def validate_response_against_content(self, query: str, response: str, retrieved_content: List[str]) -> Tuple[bool, Dict[str, Any]]:
        """
        Validate that the agent's response is grounded in the retrieved content.

        Args:
            query: Original query text
            response: Agent's response text
            retrieved_content: List of content snippets retrieved from the knowledge base

        Returns:
            Tuple[bool, Dict[str, Any]]: (is_valid, validation_details)
        """
        # Combine all retrieved content into a single string for validation
        combined_content = " ".join(retrieved_content)

        # Validate the response against the retrieved content
        validation_result = self.content_validator.validate_retrieved_content(
            query=query,
            retrieved_content=response,
            original_content=combined_content
        )

        # Create validation details
        validation_details = {
            'semantic_similarity': validation_result.semantic_similarity,
            'content_accuracy': validation_result.content_accuracy,
            'validation_notes': validation_result.validation_notes,
            'is_valid': validation_result.is_valid,
            'confidence_score': validation_result.semantic_similarity  # Using semantic similarity as confidence proxy
        }

        return validation_result.is_valid, validation_details

    def detect_hallucination(self, response: str, retrieved_content: List[str]) -> Tuple[bool, List[str]]:
        """
        Detect potential hallucinations in the agent's response.

        Args:
            response: Agent's response text
            retrieved_content: List of content snippets retrieved from the knowledge base

        Returns:
            Tuple[bool, List[str]]: (has_hallucination, list_of_potential_hallucinations)
        """
        # Split response into sentences
        import re
        sentences = re.split(r'[.!?]+', response)
        sentences = [s.strip() for s in sentences if s.strip()]

        potential_hallucinations = []

        # Check each sentence against the retrieved content
        for sentence in sentences:
            if sentence:
                # Check if this sentence is supported by the retrieved content
                is_supported = self._sentence_is_supported(sentence, retrieved_content)
                if not is_supported:
                    potential_hallucinations.append(sentence.strip())

        has_hallucination = len(potential_hallucinations) > 0
        return has_hallucination, potential_hallucinations

    def _sentence_is_supported(self, sentence: str, retrieved_content: List[str]) -> bool:
        """
        Check if a sentence is supported by the retrieved content.

        Args:
            sentence: Sentence to check
            retrieved_content: List of content snippets

        Returns:
            bool: True if sentence is supported, False otherwise
        """
        if not sentence or not retrieved_content:
            return False

        # Simple keyword overlap check - in a real implementation, this would be more sophisticated
        sentence_lower = sentence.lower()
        content_combined = " ".join(retrieved_content).lower()

        # Check for significant overlap between sentence and content
        sentence_words = set(sentence_lower.split())
        content_words = set(content_combined.split())

        if not sentence_words:
            return True  # Empty sentence is considered supported

        # Calculate overlap ratio
        common_words = sentence_words.intersection(content_words)
        overlap_ratio = len(common_words) / len(sentence_words)

        # If more than 30% of the sentence words appear in the content, consider it supported
        return overlap_ratio > 0.3

    def add_source_attribution(self, response: str, retrieved_sources: List[str]) -> str:
        """
        Add source attribution to the agent's response.

        Args:
            response: Original agent response
            retrieved_sources: List of sources used in the response

        Returns:
            str: Response with source attribution added
        """
        if not retrieved_sources:
            return response

        # Add sources at the end of the response
        sources_text = "\n\nSources: " + ", ".join(retrieved_sources)
        return response + sources_text

    def calculate_content_confidence(self, query: str, response: str, retrieved_content: List[str]) -> float:
        """
        Calculate a confidence score based on how well the response aligns with retrieved content.

        Args:
            query: Original query
            response: Agent's response
            retrieved_content: Content snippets used

        Returns:
            float: Confidence score between 0.0 and 1.0
        """
        # First validate the response against the content
        is_valid, validation_details = self.validate_response_against_content(
            query, response, retrieved_content
        )

        if not is_valid:
            return validation_details.get('confidence_score', 0.0)

        # Check for hallucinations
        has_hallucination, _ = self.detect_hallucination(response, retrieved_content)

        if has_hallucination:
            # Reduce confidence if hallucinations detected
            base_confidence = validation_details.get('confidence_score', 0.5)
            return base_confidence * 0.5  # Halve the confidence if hallucinations detected

        # Return the semantic similarity as confidence score
        return validation_details.get('semantic_similarity', 0.5)

    def enforce_content_restriction(self, response: AgentResponse, retrieved_content: List[str]) -> AgentResponse:
        """
        Enforce that the response only contains information from the retrieved content.

        Args:
            response: Original agent response
            retrieved_content: Content snippets used to generate response

        Returns:
            AgentResponse: Potentially modified response that adheres to content restrictions
        """
        # Validate the response
        is_valid, validation_details = self.validate_response_against_content(
            response.query, response.answer, retrieved_content
        )

        # Check for hallucinations
        has_hallucination, hallucinations = self.detect_hallucination(
            response.answer, retrieved_content
        )

        # Update confidence score based on validation
        response.confidence_score = self.calculate_content_confidence(
            response.query, response.answer, retrieved_content
        )

        # If hallucinations detected, potentially modify the response
        if has_hallucination:
            # In a real implementation, you might want to regenerate the response
            # or add warnings about potential inaccuracies
            response.answer += "\n\nNote: Some parts of this response may not be fully supported by the textbook content."

        return response