"""
Structured Logging Module for RAG Retrieval Validation

This module implements structured logging for retrieval analysis.
"""
import logging
import json
from datetime import datetime
from typing import Any, Dict, Optional
import sys


class ValidationLogger:
    """
    Structured logger for RAG retrieval validation analysis.
    """

    def __init__(self, name: str = "rag_validation", level: int = logging.INFO):
        """
        Initialize the ValidationLogger.

        Args:
            name: Name of the logger
            level: Logging level
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Prevent adding multiple handlers if logger already exists
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log_query(self, query_id: str, query_text: str, embedding_metadata: Dict[str, Any]):
        """
        Log query text and embedding metadata.

        Args:
            query_id: Unique identifier for the query
            query_text: Original query text
            embedding_metadata: Metadata about the embedding process
        """
        log_data = {
            "event": "query_processed",
            "query_id": query_id,
            "query_text": query_text,
            "embedding_metadata": embedding_metadata,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.logger.info(json.dumps(log_data))

    def log_retrieved_results(self, query_id: str, results: list):
        """
        Log retrieved results with similarity scores.

        Args:
            query_id: ID of the original query
            results: List of retrieved results
        """
        log_data = {
            "event": "results_retrieved",
            "query_id": query_id,
            "result_count": len(results),
            "results": results,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.logger.info(json.dumps(log_data))

    def log_validation_outcome(self, validation_result: Dict[str, Any]):
        """
        Log validation outcomes.

        Args:
            validation_result: Dictionary containing validation results
        """
        log_data = {
            "event": "validation_completed",
            "validation_result": validation_result,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.logger.info(json.dumps(log_data))

    def log_performance_metrics(self, metrics: Dict[str, Any]):
        """
        Log performance metrics.

        Args:
            metrics: Dictionary containing performance metrics
        """
        log_data = {
            "event": "metrics_calculated",
            "metrics": metrics,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.logger.info(json.dumps(log_data))

    def log_error(self, error_type: str, error_message: str, context: Optional[Dict[str, Any]] = None):
        """
        Log error conditions and failures.

        Args:
            error_type: Type of error that occurred
            error_message: Detailed error message
            context: Additional context about the error
        """
        log_data = {
            "event": "error_occurred",
            "error_type": error_type,
            "error_message": error_message,
            "context": context or {},
            "timestamp": datetime.utcnow().isoformat()
        }
        self.logger.error(json.dumps(log_data))

    def log_warning(self, warning_type: str, warning_message: str, context: Optional[Dict[str, Any]] = None):
        """
        Log warning conditions.

        Args:
            warning_type: Type of warning that occurred
            warning_message: Detailed warning message
            context: Additional context about the warning
        """
        log_data = {
            "event": "warning_occurred",
            "warning_type": warning_type,
            "warning_message": warning_message,
            "context": context or {},
            "timestamp": datetime.utcnow().isoformat()
        }
        self.logger.warning(json.dumps(log_data))


# Global logger instance
validation_logger = ValidationLogger()