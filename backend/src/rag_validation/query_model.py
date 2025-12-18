"""
Query Data Model for RAG Retrieval Validation

This module defines the Query data model according to the specification.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List
from typing import Optional
import json


@dataclass
class Query:
    """
    Represents a natural language query that needs to be validated against stored embeddings.
    """
    query_id: str
    text: str
    embedding: List[float]
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> str:
        """
        Serialize the Query object to JSON string.

        Returns:
            str: JSON representation of the Query object
        """
        data = {
            "query_id": self.query_id,
            "text": self.text,
            "embedding": self.embedding,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }
        return json.dumps(data)

    @classmethod
    def from_json(cls, json_str: str) -> 'Query':
        """
        Create a Query object from JSON string.

        Args:
            json_str: JSON string representation of a Query

        Returns:
            Query: Query object created from JSON
        """
        data = json.loads(json_str)
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)

    def validate(self) -> bool:
        """
        Validate the Query object fields.

        Returns:
            bool: True if all fields are valid, False otherwise
        """
        if not self.query_id or not isinstance(self.query_id, str):
            return False
        if not self.text or not isinstance(self.text, str):
            return False
        if not self.embedding or not isinstance(self.embedding, list):
            return False
        if not all(isinstance(val, (int, float)) for val in self.embedding):
            return False
        if not isinstance(self.metadata, dict):
            return False
        return True