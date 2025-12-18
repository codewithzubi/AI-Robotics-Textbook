"""
ValidationResult Data Model for RAG Retrieval Validation

This module defines the ValidationResult data model according to the specification.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any
import json


@dataclass
class ValidationResult:
    """
    Represents the validation outcome for a single retrieved result.
    """
    validation_id: str
    result_id: str
    query_id: str
    semantic_similarity: float
    content_accuracy: float
    validation_notes: str
    is_valid: bool
    validation_timestamp: datetime = field(default_factory=datetime.utcnow)
    validator_metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """
        Validate the ValidationResult object after initialization.
        """
        if not 0.0 <= self.semantic_similarity <= 1.0:
            raise ValueError(f"Semantic similarity must be between 0.0 and 1.0, got {self.semantic_similarity}")
        if not 0.0 <= self.content_accuracy <= 1.0:
            raise ValueError(f"Content accuracy must be between 0.0 and 1.0, got {self.content_accuracy}")

    def to_json(self) -> str:
        """
        Serialize the ValidationResult object to JSON string.

        Returns:
            str: JSON representation of the ValidationResult object
        """
        data = {
            "validation_id": self.validation_id,
            "result_id": self.result_id,
            "query_id": self.query_id,
            "semantic_similarity": self.semantic_similarity,
            "content_accuracy": self.content_accuracy,
            "validation_notes": self.validation_notes,
            "is_valid": self.is_valid,
            "validation_timestamp": self.validation_timestamp.isoformat(),
            "validator_metadata": self.validator_metadata
        }
        return json.dumps(data)

    @classmethod
    def from_json(cls, json_str: str) -> 'ValidationResult':
        """
        Create a ValidationResult object from JSON string.

        Args:
            json_str: JSON string representation of a ValidationResult

        Returns:
            ValidationResult: ValidationResult object created from JSON
        """
        data = json.loads(json_str)
        data['validation_timestamp'] = datetime.fromisoformat(data['validation_timestamp'])
        return cls(**data)

    def validate(self) -> bool:
        """
        Validate the ValidationResult object fields.

        Returns:
            bool: True if all fields are valid, False otherwise
        """
        if not self.validation_id or not isinstance(self.validation_id, str):
            return False
        if not self.result_id or not isinstance(self.result_id, str):
            return False
        if not self.query_id or not isinstance(self.query_id, str):
            return False
        if not isinstance(self.semantic_similarity, (int, float)) or not 0.0 <= self.semantic_similarity <= 1.0:
            return False
        if not isinstance(self.content_accuracy, (int, float)) or not 0.0 <= self.content_accuracy <= 1.0:
            return False
        if not isinstance(self.validation_notes, str):
            return False
        if not isinstance(self.is_valid, bool):
            return False
        if not isinstance(self.validator_metadata, dict):
            return False
        return True