"""
Query Processor Module for RAG Retrieval Validation

This module processes natural language queries and generates embeddings for validation.
"""
import uuid
import time
from typing import Optional, Dict, Any
import cohere
from .query_model import Query
from ..config.settings import settings


class QueryProcessor:
    """
    Process natural language queries and generate embeddings for validation.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the QueryProcessor.

        Args:
            api_key: Cohere API key. If not provided, will use from settings
        """
        api_key = api_key or settings.COHERE_API_KEY
        if not api_key:
            raise ValueError("Cohere API key is required")

        self.client = cohere.Client(api_key)
        self.model = settings.EMBEDDING_MODEL

    def process_query(self, query_text: str) -> Query:
        """
        Process natural language query and generate embedding.

        Args:
            query_text: Natural language query text

        Returns:
            Query: Query object with embedding and metadata
        """
        if not self.validate_query(query_text):
            raise ValueError(f"Invalid query: {query_text}")

        query_id = str(uuid.uuid4())

        # Generate embedding using Cohere
        response = None
        try:
            # For Cohere v3 models, input_type is required and must be provided
            # Different versions of the library may require different approaches
            try:
                response = self.client.embed(
                    texts=[query_text],
                    model=self.model,
                    input_type="search_query"  # Required for query embeddings in v3 models
                )
            except TypeError:
                # If input_type parameter is not accepted as a direct parameter, try without it
                response = self.client.embed(
                    texts=[query_text],
                    model=self.model
                )
            except Exception as e:
                # If it's a different error (like the API requiring input_type), we need to handle it differently
                if "input_type must be provided" in str(e):
                    # For this specific error, we need to ensure input_type is passed correctly
                    response = self.client.embed(
                        texts=[query_text],
                        model=self.model,
                        input_type="search_query"
                    )
                else:
                    raise e
        except Exception as e:
            # Handle any other exceptions that may occur during embedding generation
            raise e

        if response is None:
            raise ValueError("Failed to generate embedding for query")

        embedding = response.embeddings[0]  # Extract the embedding from the response

        # Create metadata for the query
        metadata = {
            "embedding_model": self.model,
            "processing_timestamp": time.time()
        }

        query = Query(
            query_id=query_id,
            text=query_text,
            embedding=embedding,
            metadata=metadata
        )

        # Validate the query object before returning
        if not query.validate():
            raise ValueError("Generated query object failed validation")

        return query

    def validate_query(self, query_text: str) -> bool:
        """
        Validate query format and content.

        Args:
            query_text: Query text to validate

        Returns:
            bool: True if valid, False otherwise
        """
        if not query_text or not isinstance(query_text, str):
            return False

        # Check minimum length
        if len(query_text.strip()) < 3:
            return False

        # Check maximum length to prevent overly large queries
        if len(query_text) > 1000:
            return False

        return True

    def batch_process_queries(self, query_texts: list) -> list:
        """
        Process multiple queries in batch.

        Args:
            query_texts: List of query texts to process

        Returns:
            list: List of Query objects
        """
        queries = []
        for text in query_texts:
            try:
                query = self.process_query(text)
                queries.append(query)
            except Exception as e:
                # Log the error and continue processing other queries
                from .logger import validation_logger
                validation_logger.log_error(
                    error_type="query_processing_failed",
                    error_message=str(e),
                    context={"query_text": text}
                )
                continue
        return queries