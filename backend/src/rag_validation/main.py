"""
Main Pipeline Module for RAG Retrieval Validation

This module orchestrates the complete validation pipeline.
"""
import argparse
import sys
import time
import json
from typing import List, Optional, Dict, Any
from .query_processor import QueryProcessor
from .vector_search import VectorSearch
from .content_validator import ContentValidator
from .metrics_calculator import MetricsCalculator
from .logger import validation_logger
from ..config.settings import settings


class ValidationPipeline:
    """
    Orchestrates the complete RAG retrieval validation pipeline.
    """

    def __init__(
        self,
        query_processor: Optional[QueryProcessor] = None,
        vector_search: Optional[VectorSearch] = None,
        content_validator: Optional[ContentValidator] = None,
        metrics_calculator: Optional[MetricsCalculator] = None
    ):
        """
        Initialize the ValidationPipeline.

        Args:
            query_processor: QueryProcessor instance. If None, creates default
            vector_search: VectorSearch instance. If None, creates default
            content_validator: ContentValidator instance. If None, creates default
            metrics_calculator: MetricsCalculator instance. If None, creates default
        """
        self.query_processor = query_processor or QueryProcessor()
        self.vector_search = vector_search or VectorSearch()
        self.content_validator = content_validator or ContentValidator()
        self.metrics_calculator = metrics_calculator or MetricsCalculator()

    def validate_single_query(
        self,
        query_text: str,
        top_k: int = 10,
        similarity_threshold: float = 0.7,
        collection_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute the complete validation pipeline for a single query.

        Args:
            query_text: Natural language query text
            top_k: Number of results to retrieve
            similarity_threshold: Minimum similarity threshold
            collection_name: Qdrant collection name

        Returns:
            Dict[str, Any]: Complete validation results
        """
        start_time = time.time()

        try:
            # Step 1: Process the query
            query = self.query_processor.process_query(query_text)
            validation_logger.log_query(
                query_id=query.query_id,
                query_text=query.text,
                embedding_metadata=query.metadata
            )

            # Step 2: Perform vector search
            retrieved_results = self.vector_search.search(
                query_embedding=query.embedding,
                top_k=top_k,
                similarity_threshold=similarity_threshold
            )
            validation_logger.log_retrieved_results(
                query_id=query.query_id,
                results=[{
                    "vector_id": r.vector_id,
                    "content": r.content[:100] + "..." if len(r.content) > 100 else r.content,
                    "similarity_score": r.similarity_score
                } for r in retrieved_results]
            )

            # Step 3: Validate retrieved results
            validation_results = []
            for result in retrieved_results:
                # For validation, we'll use the result's original source as the original content
                # In a real implementation, we'd have access to the full original content
                validation_result = self.content_validator.validate_retrieved_content(
                    query=query_text,
                    retrieved_content=result.content,
                    original_content=result.original_source
                )
                validation_result.result_id = result.result_id
                validation_result.query_id = query.query_id
                validation_results.append(validation_result)

                validation_logger.log_validation_outcome({
                    "validation_id": validation_result.validation_id,
                    "result_id": result.result_id,
                    "is_valid": validation_result.is_valid,
                    "semantic_similarity": validation_result.semantic_similarity
                })

            # Step 4: Calculate metrics
            pipeline_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            metrics = self.metrics_calculator.calculate_retrieval_metrics(
                query_id=query.query_id,
                results=retrieved_results,
                validations=validation_results
            )
            # Update the response time with actual processing time
            metrics.response_time_ms = pipeline_time

            validation_logger.log_performance_metrics({
                "query_id": query.query_id,
                "pipeline_time_ms": pipeline_time,
                "total_results": len(retrieved_results),
                "retrieval_accuracy": metrics.retrieval_accuracy,
                "mean_similarity_score": metrics.mean_similarity_score
            })

            # Prepare the response
            response = {
                "query_id": query.query_id,
                "query_text": query.text,
                "retrieved_results": [
                    {
                        "vector_id": r.vector_id,
                        "content": r.content,
                        "similarity_score": r.similarity_score,
                        "validation_result": {
                            "is_valid": vr.is_valid,
                            "semantic_similarity": vr.semantic_similarity,
                            "content_accuracy": vr.content_accuracy
                        }
                    }
                    for r, vr in zip(retrieved_results, validation_results)
                ],
                "final_metrics": {
                    "retrieval_accuracy": metrics.retrieval_accuracy,
                    "mean_similarity_score": metrics.mean_similarity_score,
                    "response_time_ms": metrics.response_time_ms,
                    "failure_count": metrics.failure_count,
                    "mrr_score": metrics.mrr_score
                },
                "pipeline_time_ms": pipeline_time,
                "status": "success"
            }

            return response

        except Exception as e:
            error_time = (time.time() - start_time) * 1000
            validation_logger.log_error(
                error_type="pipeline_failed",
                error_message=str(e),
                context={"query_text": query_text}
            )

            return {
                "query_id": "unknown",
                "query_text": query_text,
                "retrieved_results": [],
                "final_metrics": {
                    "retrieval_accuracy": 0.0,
                    "mean_similarity_score": 0.0,
                    "response_time_ms": error_time,
                    "failure_count": 1,
                    "mrr_score": 0.0
                },
                "pipeline_time_ms": error_time,
                "status": "error",
                "error_message": str(e)
            }

    def validate_batch_queries(
        self,
        query_texts: List[str],
        top_k: int = 10,
        similarity_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Execute the validation pipeline for multiple queries.

        Args:
            query_texts: List of query texts to validate
            top_k: Number of results to retrieve per query
            similarity_threshold: Minimum similarity threshold

        Returns:
            List[Dict[str, Any]]: List of validation results for each query
        """
        results = []
        for query_text in query_texts:
            result = self.validate_single_query(
                query_text=query_text,
                top_k=top_k,
                similarity_threshold=similarity_threshold
            )
            results.append(result)
        return results

    def run_performance_test(
        self,
        query_text: str,
        iterations: int = 10
    ) -> Dict[str, Any]:
        """
        Run performance test for a query.

        Args:
            query_text: Query text to test
            iterations: Number of iterations to run

        Returns:
            Dict[str, Any]: Performance test results
        """
        response_times = []
        results = []

        for i in range(iterations):
            result = self.validate_single_query(query_text)
            response_times.append(result["pipeline_time_ms"])
            results.append(result)

        # Calculate performance metrics
        avg_time = sum(response_times) / len(response_times)
        min_time = min(response_times)
        max_time = max(response_times)

        return {
            "query_text": query_text,
            "iterations": iterations,
            "avg_response_time_ms": avg_time,
            "min_response_time_ms": min_time,
            "max_response_time_ms": max_time,
            "results": results,
            "status": "performance_test_completed"
        }


def main():
    """
    Main function to run the validation pipeline from command line.
    """
    parser = argparse.ArgumentParser(description="RAG Retrieval Validation Pipeline")
    parser.add_argument("--query", type=str, help="Query text to validate")
    parser.add_argument("--top-k", type=int, default=10, help="Number of results to retrieve (default: 10)")
    parser.add_argument("--similarity-threshold", type=float, default=0.7, help="Similarity threshold (default: 0.7)")
    parser.add_argument("--collection-name", type=str, help="Qdrant collection name")
    parser.add_argument("--batch-file", type=str, help="File with multiple queries (one per line)")
    parser.add_argument("--output", type=str, help="Output file for results")
    parser.add_argument("--performance-test", action="store_true", help="Run performance test")

    args = parser.parse_args()

    # Initialize the pipeline
    pipeline = ValidationPipeline()

    # Check if we're running a performance test
    if args.performance_test and args.query:
        result = pipeline.run_performance_test(args.query)
    elif args.batch_file:
        # Read queries from file
        with open(args.batch_file, 'r', encoding='utf-8') as f:
            queries = [line.strip() for line in f if line.strip()]
        result = pipeline.validate_batch_queries(queries, args.top_k, args.similarity_threshold)
    elif args.query:
        # Process single query
        result = pipeline.validate_single_query(
            args.query,
            args.top_k,
            args.similarity_threshold,
            args.collection_name
        )
    else:
        print("Error: Please provide a query using --query or batch file using --batch-file")
        sys.exit(1)

    # Output the result
    output_str = json.dumps(result, indent=2)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output_str)
        print(f"Results written to {args.output}")
    else:
        print(output_str)


if __name__ == "__main__":
    main()