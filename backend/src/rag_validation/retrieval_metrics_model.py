"""
RetrievalMetrics Data Model for RAG Retrieval Validation

This module defines the RetrievalMetrics data model according to the specification.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any
import json


@dataclass
class RetrievalMetrics:
    """
    Aggregated metrics for a single query's retrieval performance.
    """
    metrics_id: str
    query_id: str
    total_results: int
    relevant_results: int
    retrieval_accuracy: float
    mean_similarity_score: float
    response_time_ms: float
    failure_count: int
    mrr_score: float
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """
        Validate the RetrievalMetrics object after initialization.
        """
        if self.total_results < 0:
            raise ValueError(f"Total results must be non-negative, got {self.total_results}")
        if self.relevant_results < 0:
            raise ValueError(f"Relevant results must be non-negative, got {self.relevant_results}")
        if self.relevant_results > self.total_results:
            raise ValueError(f"Relevant results ({self.relevant_results}) cannot exceed total results ({self.total_results})")
        if not 0.0 <= self.retrieval_accuracy <= 1.0:
            raise ValueError(f"Retrieval accuracy must be between 0.0 and 1.0, got {self.retrieval_accuracy}")
        if not 0.0 <= self.mean_similarity_score <= 1.0:
            raise ValueError(f"Mean similarity score must be between 0.0 and 1.0, got {self.mean_similarity_score}")
        if self.response_time_ms < 0:
            raise ValueError(f"Response time must be non-negative, got {self.response_time_ms}")
        if self.failure_count < 0:
            raise ValueError(f"Failure count must be non-negative, got {self.failure_count}")
        if not 0.0 <= self.mrr_score <= 1.0:
            raise ValueError(f"MRR score must be between 0.0 and 1.0, got {self.mrr_score}")

    def to_json(self) -> str:
        """
        Serialize the RetrievalMetrics object to JSON string.

        Returns:
            str: JSON representation of the RetrievalMetrics object
        """
        data = {
            "metrics_id": self.metrics_id,
            "query_id": self.query_id,
            "total_results": self.total_results,
            "relevant_results": self.relevant_results,
            "retrieval_accuracy": self.retrieval_accuracy,
            "mean_similarity_score": self.mean_similarity_score,
            "response_time_ms": self.response_time_ms,
            "failure_count": self.failure_count,
            "mrr_score": self.mrr_score,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }
        return json.dumps(data)

    @classmethod
    def from_json(cls, json_str: str) -> 'RetrievalMetrics':
        """
        Create a RetrievalMetrics object from JSON string.

        Args:
            json_str: JSON string representation of a RetrievalMetrics

        Returns:
            RetrievalMetrics: RetrievalMetrics object created from JSON
        """
        data = json.loads(json_str)
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)

    def validate(self) -> bool:
        """
        Validate the RetrievalMetrics object fields.

        Returns:
            bool: True if all fields are valid, False otherwise
        """
        if not self.metrics_id or not isinstance(self.metrics_id, str):
            return False
        if not self.query_id or not isinstance(self.query_id, str):
            return False
        if not isinstance(self.total_results, int) or self.total_results < 0:
            return False
        if not isinstance(self.relevant_results, int) or self.relevant_results < 0:
            return False
        if self.relevant_results > self.total_results:
            return False
        if not isinstance(self.retrieval_accuracy, (int, float)) or not 0.0 <= self.retrieval_accuracy <= 1.0:
            return False
        if not isinstance(self.mean_similarity_score, (int, float)) or not 0.0 <= self.mean_similarity_score <= 1.0:
            return False
        if not isinstance(self.response_time_ms, (int, float)) or self.response_time_ms < 0:
            return False
        if not isinstance(self.failure_count, int) or self.failure_count < 0:
            return False
        if not isinstance(self.mrr_score, (int, float)) or not 0.0 <= self.mrr_score <= 1.0:
            return False
        if not isinstance(self.metadata, dict):
            return False
        return True