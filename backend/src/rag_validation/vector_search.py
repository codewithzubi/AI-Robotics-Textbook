"""
Vector Search Module for RAG Retrieval Validation

This module handles vector search operations in Qdrant.
"""
from typing import List, Optional, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
from .retrieved_result_model import RetrievedResult
from ..config.settings import settings


class VectorSearch:
    """
    Handles vector search operations in Qdrant for retrieval validation.
    """

    def __init__(self, url: Optional[str] = None, api_key: Optional[str] = None, collection_name: Optional[str] = None):
        """
        Initialize the VectorSearch.

        Args:
            url: Qdrant URL. If not provided, will use from settings
            api_key: Qdrant API key. If not provided, will use from settings
            collection_name: Qdrant collection name. If not provided, will use from settings
        """
        url = url or settings.QDRANT_URL
        api_key = api_key or settings.QDRANT_API_KEY
        collection_name = collection_name or settings.QDRANT_COLLECTION_NAME

        if not url:
            raise ValueError("Qdrant URL is required")

        self.client = QdrantClient(
            url=url,
            api_key=api_key,
            timeout=settings.REQUEST_TIMEOUT
        )
        self.collection_name = collection_name

    def connect(self) -> bool:
        """
        Establish connection to Qdrant.

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Test the connection by getting collection info
            self.client.get_collection(self.collection_name)
            return True
        except Exception as e:
            from .logger import validation_logger
            validation_logger.log_error(
                error_type="qdrant_connection_failed",
                error_message=str(e),
                context={"collection_name": self.collection_name}
            )
            return False

    def search(self, query_embedding: List[float], top_k: int = 10, similarity_threshold: float = 0.0) -> List[RetrievedResult]:
        """
        Search Qdrant for similar vectors.

        Args:
            query_embedding: Query vector to search for
            top_k: Number of results to return
            similarity_threshold: Minimum similarity score threshold

        Returns:
            List[RetrievedResult]: List of RetrievedResult objects
        """
        try:
            # Perform the search in Qdrant
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                score_threshold=similarity_threshold
            )

            # Convert Qdrant results to RetrievedResult objects
            retrieved_results = []
            for i, result in enumerate(search_results):
                result_id = f"result_{i}_{result.id}"
                retrieved_result = RetrievedResult(
                    result_id=result_id,
                    query_id="unknown",  # This will be set by the caller
                    content=result.payload.get("content", ""),
                    similarity_score=result.score,
                    original_source=result.payload.get("source", ""),
                    vector_id=result.id,
                    metadata=result.payload.get("metadata", {})
                )
                retrieved_results.append(retrieved_result)

            return retrieved_results

        except Exception as e:
            from .logger import validation_logger
            validation_logger.log_error(
                error_type="vector_search_failed",
                error_message=str(e),
                context={
                    "collection_name": self.collection_name,
                    "top_k": top_k,
                    "similarity_threshold": similarity_threshold
                }
            )
            raise

    def close(self) -> None:
        """
        Close connection to Qdrant.
        """
        try:
            if hasattr(self.client, '_client'):
                self.client.close()
        except Exception as e:
            from .logger import validation_logger
            validation_logger.log_warning(
                warning_type="connection_close_failed",
                warning_message=str(e)
            )

    def validate_collection_exists(self) -> bool:
        """
        Validate that the specified collection exists in Qdrant.

        Returns:
            bool: True if collection exists, False otherwise
        """
        try:
            self.client.get_collection(self.collection_name)
            return True
        except Exception:
            return False

    def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the collection.

        Returns:
            Dict[str, Any]: Collection information
        """
        try:
            collection_info = self.client.get_collection(self.collection_name)
            return {
                "name": collection_info.config.params.vectors_count,
                "vectors_count": collection_info.config.params.vectors_count,
                "indexed_vectors_count": collection_info.indexed_vectors_count
            }
        except Exception as e:
            from .logger import validation_logger
            validation_logger.log_error(
                error_type="collection_info_failed",
                error_message=str(e),
                context={"collection_name": self.collection_name}
            )
            return {}