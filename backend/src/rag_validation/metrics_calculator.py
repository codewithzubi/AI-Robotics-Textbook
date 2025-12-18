"""
Metrics Calculator Module for RAG Retrieval Validation

This module computes retrieval quality metrics.
"""
import uuid
from typing import List
from .retrieved_result_model import RetrievedResult
from .validation_result_model import ValidationResult
from .retrieval_metrics_model import RetrievalMetrics


class MetricsCalculator:
    """
    Calculates retrieval quality metrics for validation.
    """

    def __init__(self):
        """
        Initialize the MetricsCalculator.
        """
        pass

    def calculate_retrieval_metrics(
        self,
        query_id: str,
        results: List[RetrievedResult],
        validations: List[ValidationResult]
    ) -> RetrievalMetrics:
        """
        Calculate retrieval quality metrics.

        Args:
            query_id: ID of the original query
            results: List of retrieved results
            validations: List of validation results

        Returns:
            RetrievalMetrics: RetrievalMetrics object with calculated metrics
        """
        metrics_id = str(uuid.uuid4())

        total_results = len(results)
        relevant_results = sum(1 for v in validations if v.is_valid)

        retrieval_accuracy = relevant_results / total_results if total_results > 0 else 0.0

        mean_similarity_score = (
            sum(r.similarity_score for r in results) / total_results if total_results > 0 else 0.0
        )

        # For now, setting response time to 0 - this would be calculated based on actual processing time
        response_time_ms = 0.0

        failure_count = sum(1 for v in validations if not v.is_valid)

        # Calculate MRR (Mean Reciprocal Rank)
        mrr_score = self.calculate_mrr(results, validations)

        # Create metadata for the metrics
        metadata = {
            "calculation_timestamp": uuid.uuid4().hex[:8]  # Short unique identifier
        }

        metrics = RetrievalMetrics(
            metrics_id=metrics_id,
            query_id=query_id,
            total_results=total_results,
            relevant_results=relevant_results,
            retrieval_accuracy=retrieval_accuracy,
            mean_similarity_score=mean_similarity_score,
            response_time_ms=response_time_ms,
            failure_count=failure_count,
            mrr_score=mrr_score,
            metadata=metadata
        )

        # Validate the metrics object before returning
        if not metrics.validate():
            raise ValueError("Generated metrics object failed validation")

        return metrics

    def calculate_mrr(self, results: List[RetrievedResult], validations: List[ValidationResult]) -> float:
        """
        Calculate Mean Reciprocal Rank (MRR) for ranking quality.

        Args:
            results: List of retrieved results
            validations: List of validation results

        Returns:
            float: MRR score between 0.0 and 1.0
        """
        if not results or not validations:
            return 0.0

        # Ensure results and validations are aligned
        if len(results) != len(validations):
            raise ValueError("Number of results must match number of validations")

        # Find the rank of the first relevant result (1-indexed)
        reciprocal_ranks = []
        for i, validation in enumerate(validations):
            if validation.is_valid:
                # Rank is the 1-indexed position of the first valid result
                reciprocal_ranks.append(1.0 / (i + 1))
                break  # Only consider the first relevant result for MRR

        if not reciprocal_ranks:
            # No relevant results found
            return 0.0

        # MRR is the average of reciprocal ranks
        return sum(reciprocal_ranks) / len(results)

    def calculate_aggregated_metrics(
        self,
        metrics_list: List[RetrievalMetrics]
    ) -> RetrievalMetrics:
        """
        Calculate aggregated metrics across multiple queries.

        Args:
            metrics_list: List of individual RetrievalMetrics objects

        Returns:
            RetrievalMetrics: Aggregated metrics
        """
        if not metrics_list:
            return RetrievalMetrics(
                metrics_id="aggregated_" + str(uuid.uuid4()),
                query_id="aggregated",
                total_results=0,
                relevant_results=0,
                retrieval_accuracy=0.0,
                mean_similarity_score=0.0,
                response_time_ms=0.0,
                failure_count=0,
                mrr_score=0.0
            )

        # Calculate aggregated values
        total_queries = len(metrics_list)
        total_results = sum(m.total_results for m in metrics_list)
        total_relevant = sum(m.relevant_results for m in metrics_list)
        avg_accuracy = sum(m.retrieval_accuracy for m in metrics_list) / total_queries
        avg_similarity = sum(m.mean_similarity_score for m in metrics_list) / total_queries
        total_response_time = sum(m.response_time_ms for m in metrics_list)
        total_failures = sum(m.failure_count for m in metrics_list)
        avg_mrr = sum(m.mrr_score for m in metrics_list) / total_queries

        return RetrievalMetrics(
            metrics_id="aggregated_" + str(uuid.uuid4()),
            query_id="aggregated",
            total_results=total_results,
            relevant_results=total_relevant,
            retrieval_accuracy=avg_accuracy,
            mean_similarity_score=avg_similarity,
            response_time_ms=total_response_time,
            failure_count=total_failures,
            mrr_score=avg_mrr
        )

    def calculate_response_time_metrics(self, response_times: List[float]) -> dict:
        """
        Calculate metrics based on response times.

        Args:
            response_times: List of response times in milliseconds

        Returns:
            dict: Dictionary with response time metrics
        """
        if not response_times:
            return {
                "avg_response_time": 0.0,
                "min_response_time": 0.0,
                "max_response_time": 0.0,
                "p95_response_time": 0.0
            }

        sorted_times = sorted(response_times)
        n = len(sorted_times)

        return {
            "avg_response_time": sum(response_times) / n,
            "min_response_time": sorted_times[0],
            "max_response_time": sorted_times[-1],
            "p95_response_time": sorted_times[int(0.95 * n) - 1] if n > 0 else 0.0
        }