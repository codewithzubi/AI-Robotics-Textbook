"""
RetrievedResult Data Model for RAG Retrieval Validation

This module defines the RetrievedResult data model according to the specification.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List
import json


@dataclass
class RetrievedResult:
    """
    Represents a single result from the vector search in Qdrant.
    """
    result_id: str
    query_id: str
    content: str
    similarity_score: float
    original_source: str
    vector_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """
        Validate the RetrievedResult object after initialization.
        """
        if not 0.0 <= self.similarity_score <= 1.0:
            raise ValueError(f"Similarity score must be between 0.0 and 1.0, got {self.similarity_score}")

    def to_json(self) -> str:
        """
        Serialize the RetrievedResult object to JSON string.

        Returns:
            str: JSON representation of the RetrievedResult object
        """
        data = {
            "result_id": self.result_id,
            "query_id": self.query_id,
            "content": self.content,
            "similarity_score": self.similarity_score,
            "original_source": self.original_source,
            "vector_id": self.vector_id,
            "metadata": self.metadata
        }
        return json.dumps(data)

    @classmethod
    def from_json(cls, json_str: str) -> 'RetrievedResult':
        """
        Create a RetrievedResult object from JSON string.

        Args:
            json_str: JSON string representation of a RetrievedResult

        Returns:
            RetrievedResult: RetrievedResult object created from JSON
        """
        data = json.loads(json_str)
        return cls(**data)

    def validate(self) -> bool:
        """
        Validate the RetrievedResult object fields.

        Returns:
            bool: True if all fields are valid, False otherwise
        """
        if not self.result_id or not isinstance(self.result_id, str):
            return False
        if not self.query_id or not isinstance(self.query_id, str):
            return False
        if not self.content or not isinstance(self.content, str):
            return False
        if not isinstance(self.similarity_score, (int, float)) or not 0.0 <= self.similarity_score <= 1.0:
            return False
        if not self.original_source or not isinstance(self.original_source, str):
            return False
        if not self.vector_id or not isinstance(self.vector_id, str):
            return False
        if not isinstance(self.metadata, dict):
            return False
        return True