"""
AI Agent Implementation with Retrieval Integration

This module implements the core AI agent functionality using OpenAI's API
and integrates with the retrieval pipeline for content-grounded responses.
"""
import os
import uuid
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
import openai
from .api_models import QueryRequest, AgentResponse, RetrievalResult
from ..config.settings import settings


class AIAgent:
    """
    AI Agent that processes queries and generates responses based on retrieved content.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AI Agent.

        Args:
            api_key: OpenAI API key. If not provided, will use from settings
        """
        api_key = api_key or settings.OPENAI_API_KEY
        if not api_key:
            raise ValueError("OpenAI API key is required")

        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=api_key)
        self.model = getattr(settings, 'AGENT_MODEL', 'gpt-4-turbo-preview')

        # Agent instructions
        self.instructions = getattr(
            settings,
            'AGENT_INSTRUCTIONS',
            "You are an AI assistant for the AI Robotics textbook. Answer questions based only on the provided context from the textbook. Do not hallucinate information."
        )

    def process_query(self, query_request: QueryRequest, retrieval_result: RetrievalResult) -> AgentResponse:
        """
        Process a query using the AI agent with provided retrieval context.

        Args:
            query_request: The query request with user question and parameters
            retrieval_result: Retrieved context to ground the response

        Returns:
            AgentResponse: Structured response from the AI agent
        """
        start_time = time.time()

        # Format the context from retrieval results
        context = self._format_context(retrieval_result)

        # Create the full prompt with context
        full_prompt = self._create_prompt(query_request.query, context)

        try:
            # Call OpenAI API to generate response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.instructions},
                    {"role": "user", "content": full_prompt}
                ],
                max_tokens=query_request.max_tokens,
                temperature=query_request.temperature
            )

            # Extract the response text
            answer = response.choices[0].message.content

            # Calculate processing time
            processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds

            # Create sources from retrieval result
            sources = self._extract_sources(retrieval_result)

            # Generate response ID
            response_id = str(uuid.uuid4())

            # Calculate confidence based on similarity scores
            confidence_score = self._calculate_confidence(retrieval_result)

            # Create the agent response
            agent_response = AgentResponse(
                response_id=response_id,
                query=query_request.query,
                answer=answer,
                sources=sources,
                confidence_score=confidence_score,
                processing_time_ms=processing_time,
                retrieval_context=[chunk.get('content', '') for chunk in retrieval_result.retrieved_chunks],
                timestamp=datetime.utcnow(),
                metadata=query_request.metadata
            )

            return agent_response

        except Exception as e:
            # Handle API errors
            processing_time = (time.time() - start_time) * 1000
            raise Exception(f"Error processing query with AI agent: {str(e)}")

    def _format_context(self, retrieval_result: RetrievalResult) -> str:
        """
        Format the retrieved context for inclusion in the prompt.

        Args:
            retrieval_result: The retrieval results to format

        Returns:
            str: Formatted context string
        """
        if not retrieval_result.retrieved_chunks:
            return "No relevant context found in the textbook. This information is not covered in the textbook."

        context_parts = ["Relevant textbook content:"]
        for i, chunk in enumerate(retrieval_result.retrieved_chunks):
            content = chunk.get('content', '')
            if content:
                context_parts.append(f"\n{i+1}. {content}")

        return "\n".join(context_parts)

    def _create_prompt(self, query: str, context: str) -> str:
        """
        Create the full prompt for the AI agent.

        Args:
            query: The user's query
            context: The retrieved context to ground the response

        Returns:
            str: Complete prompt for the AI agent
        """
        if "No relevant context found in the textbook" in context:
            prompt = f"""Context: {context}

Question: {query}

Since no relevant context from the textbook was found, please respond with: "This information is not covered in the textbook." Do not attempt to answer based on external knowledge."""
        else:
            prompt = f"""Context: {context}

Question: {query}

Please answer the question based only on the provided context from the AI Robotics textbook. Do not use any external knowledge or make up information. If the context doesn't contain enough information to answer the question, please say so."""

        return prompt

    def _extract_sources(self, retrieval_result: RetrievalResult) -> List[str]:
        """
        Extract source information from retrieval results.

        Args:
            retrieval_result: The retrieval results

        Returns:
            List[str]: List of source identifiers
        """
        sources = []
        for chunk in retrieval_result.retrieved_chunks:
            source = chunk.get('source', chunk.get('metadata', {}).get('source', 'Unknown'))
            if source and source not in sources:
                sources.append(source)
        return sources

    def _calculate_confidence(self, retrieval_result: RetrievalResult) -> float:
        """
        Calculate a confidence score based on retrieval results.

        Args:
            retrieval_result: The retrieval results

        Returns:
            float: Confidence score between 0.0 and 1.0
        """
        if not retrieval_result.similarity_scores:
            return 0.0

        # Use average similarity score as a proxy for confidence
        avg_similarity = sum(retrieval_result.similarity_scores) / len(retrieval_result.similarity_scores)

        # Normalize to 0-1 scale (assuming similarity scores are already 0-1)
        return min(1.0, max(0.0, avg_similarity))

    def validate_response(self, response: str, context: List[str]) -> bool:
        """
        Validate that the response is grounded in the provided context.

        Args:
            response: The agent's response
            context: The context provided to the agent

        Returns:
            bool: True if response is properly grounded, False otherwise
        """
        # This is a simplified validation - in practice, you might want more sophisticated checks
        response_lower = response.lower()

        # Check if the response contains content that's likely from the context
        context_keywords = []
        for ctx in context:
            # Extract some key terms from context (this is simplified)
            words = ctx.lower().split()[:20]  # Take first 20 words as potential indicators
            context_keywords.extend(words[:5])  # Take first 5 words from each context snippet

        # Count how many context keywords appear in the response
        keyword_matches = sum(1 for word in set(context_keywords) if word in response_lower)

        # If at least some keywords from context appear in response, consider it grounded
        return keyword_matches > 0