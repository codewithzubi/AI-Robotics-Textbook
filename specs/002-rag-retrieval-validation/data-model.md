# Data Model: RAG Retrieval Validation

**Feature**: 002-rag-retrieval-validation
**Date**: 2025-12-15
**Version**: 1.0

## Overview

This document defines the data models required for validating the RAG retrieval pipeline using stored embeddings in Qdrant. The models support query processing, vector search, content validation, and metrics calculation.

## Core Entities

### Query
Represents a natural language query that needs to be validated against stored embeddings.

```python
class Query:
    query_id: str              # Unique identifier for the query
    text: str                  # Original query text
    embedding: List[float]     # Vector representation of the query
    timestamp: datetime        # When the query was processed
    metadata: Dict[str, Any]   # Additional query metadata
```

**Purpose**: Captures the user's information need and its vector representation for similarity search.

### RetrievedResult
Represents a single result from the vector search in Qdrant.

```python
class RetrievedResult:
    result_id: str                    # Unique identifier for this result
    query_id: str                    # Reference to the original query
    content: str                     # Retrieved text content
    similarity_score: float          # Semantic similarity score (0.0-1.0)
    original_source: str             # Reference to original content location
    vector_id: str                   # ID of the vector in Qdrant
    metadata: Dict[str, Any]         # Additional result metadata
```

**Purpose**: Stores individual retrieval results with similarity scores for validation.

### ValidationResult
Represents the validation outcome for a single retrieved result.

```python
class ValidationResult:
    validation_id: str                    # Unique identifier for validation
    result_id: str                       # Reference to the retrieved result
    query_id: str                        # Reference to the original query
    semantic_similarity: float           # Semantic similarity between query and content
    content_accuracy: float              # Accuracy of content match to original
    validation_notes: str                # Human-readable validation details
    is_valid: bool                      # Whether the result is considered valid
    validation_timestamp: datetime       # When validation was performed
    validator_metadata: Dict[str, Any]   # Additional validation metadata
```

**Purpose**: Captures the validation assessment of retrieval quality and accuracy.

### RetrievalMetrics
Aggregated metrics for a single query's retrieval performance.

```python
class RetrievalMetrics:
    metrics_id: str                    # Unique identifier for metrics set
    query_id: str                      # Reference to the original query
    total_results: int                 # Total number of results retrieved
    relevant_results: int              # Number of relevant results (is_valid=True)
    retrieval_accuracy: float          # Percentage of relevant results
    mean_similarity_score: float       # Average similarity score across results
    response_time_ms: float            # Time taken for retrieval operation
    failure_count: int                 # Number of failed retrieval attempts
    mrr_score: float                   # Mean Reciprocal Rank
    timestamp: datetime                # When metrics were calculated
    metadata: Dict[str, Any]           # Additional metrics metadata
```

**Purpose**: Provides quantitative measures of retrieval quality and performance.

### QuerySession
Represents a session of multiple related queries for analysis.

```python
class QuerySession:
    session_id: str                    # Unique identifier for the session
    queries: List[str]                 # List of query IDs in this session
    session_start: datetime            # When the session started
    session_end: datetime              # When the session ended
    average_metrics: RetrievalMetrics  # Average metrics across all queries
    total_queries: int                 # Total number of queries in session
    success_rate: float               # Percentage of successful retrievals
    metadata: Dict[str, Any]          # Additional session metadata
```

**Purpose**: Tracks and analyzes retrieval performance across multiple queries.

## Relationships

```
Query --(1 to many)--> RetrievedResult
RetrievedResult --(1 to 1)--> ValidationResult
RetrievedResult --(many to 1)--> RetrievalMetrics
Query --(1 to 1)--> RetrievalMetrics
Query --(many to 1)--> QuerySession
```

## Data Flow

1. **Query Processing**: Natural language queries are converted to Query objects with embeddings
2. **Vector Search**: Query embeddings are used to search Qdrant, producing RetrievedResult objects
3. **Content Validation**: Retrieved results are validated against original content, creating ValidationResult objects
4. **Metrics Calculation**: Validation results are aggregated into RetrievalMetrics
5. **Session Analysis**: Multiple queries are grouped into QuerySession for comprehensive analysis

## Validation Rules

- Query.embedding must be a valid vector from Cohere API
- RetrievedResult.similarity_score must be between 0.0 and 1.0
- ValidationResult.semantic_similarity must be between 0.0 and 1.0
- ValidationResult.content_accuracy must be between 0.0 and 1.0
- RetrievalMetrics.retrieval_accuracy must be between 0.0 and 1.0
- All timestamp fields must be in UTC

## Serialization Format

All entities will be serializable to JSON format for logging, analysis, and potential API exposure:

```json
{
  "entity_type": "Query|RetrievedResult|ValidationResult|RetrievalMetrics|QuerySession",
  "data": { /* entity-specific fields */ },
  "version": "1.0"
}
```

## Performance Considerations

- Query and RetrievedResult objects should be lightweight for high-volume processing
- ValidationResults may be stored separately for analysis but linked via IDs
- Metrics aggregation should be efficient to avoid performance bottlenecks
- Caching strategies should be considered for repeated queries