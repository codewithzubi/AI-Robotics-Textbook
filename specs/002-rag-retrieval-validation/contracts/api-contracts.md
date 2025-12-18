# API Contracts: RAG Retrieval Validation

## Overview

This document defines the API contracts for the RAG retrieval validation system. These contracts specify the interfaces for query processing, vector search, content validation, and metrics calculation.

## Query Processing Service

### Process Query Endpoint
**Endpoint**: `/api/v1/validation/query/process`
**Method**: `POST`
**Description**: Process a natural language query and generate embeddings for validation

**Request**:
```json
{
  "query_text": "string",
  "parameters": {
    "top_k": "integer",
    "similarity_threshold": "float"
  }
}
```

**Response**:
```json
{
  "query_id": "string",
  "embedding": "array[float]",
  "status": "string",
  "timestamp": "datetime"
}
```

**Error Responses**:
- 400: Invalid query format
- 429: Rate limit exceeded
- 500: Internal processing error

### Validate Query Endpoint
**Endpoint**: `/api/v1/validation/query/validate`
**Method**: `POST`
**Description**: Validate query format and content

**Request**:
```json
{
  "query_text": "string"
}
```

**Response**:
```json
{
  "is_valid": "boolean",
  "validation_notes": "string",
  "timestamp": "datetime"
}
```

## Vector Search Service

### Search Endpoint
**Endpoint**: `/api/v1/validation/search`
**Method**: `POST`
**Description**: Perform vector search in Qdrant using query embeddings

**Request**:
```json
{
  "query_embedding": "array[float]",
  "collection_name": "string",
  "top_k": "integer",
  "similarity_threshold": "float"
}
```

**Response**:
```json
{
  "results": [
    {
      "vector_id": "string",
      "content": "string",
      "similarity_score": "float",
      "metadata": "object"
    }
  ],
  "search_time_ms": "float",
  "status": "string"
}
```

**Error Responses**:
- 400: Invalid embedding format
- 500: Qdrant connectivity error
- 503: Qdrant service unavailable

## Content Validation Service

### Validate Content Endpoint
**Endpoint**: `/api/v1/validation/content/validate`
**Method**: `POST`
**Description**: Validate retrieved content against original source

**Request**:
```json
{
  "query_text": "string",
  "retrieved_content": "string",
  "original_content": "string",
  "similarity_threshold": "float"
}
```

**Response**:
```json
{
  "validation_result": {
    "is_valid": "boolean",
    "semantic_similarity": "float",
    "content_accuracy": "float",
    "validation_notes": "string"
  },
  "validation_time_ms": "float",
  "status": "string"
}
```

### Batch Validation Endpoint
**Endpoint**: `/api/v1/validation/content/validate-batch`
**Method**: `POST`
**Description**: Validate multiple retrieved contents against original sources

**Request**:
```json
{
  "validation_requests": [
    {
      "query_text": "string",
      "retrieved_content": "string",
      "original_content": "string",
      "similarity_threshold": "float"
    }
  ]
}
```

**Response**:
```json
{
  "validation_results": [
    {
      "validation_result": {
        "is_valid": "boolean",
        "semantic_similarity": "float",
        "content_accuracy": "float",
        "validation_notes": "string"
      },
      "validation_time_ms": "float"
    }
  ],
  "batch_validation_time_ms": "float",
  "status": "string"
}
```

## Metrics Calculation Service

### Calculate Metrics Endpoint
**Endpoint**: `/api/v1/validation/metrics/calculate`
**Method**: `POST`
**Description**: Calculate retrieval quality metrics

**Request**:
```json
{
  "query_id": "string",
  "retrieved_results": "array[object]",
  "validation_results": "array[object]"
}
```

**Response**:
```json
{
  "metrics": {
    "retrieval_accuracy": "float",
    "mean_similarity_score": "float",
    "response_time_ms": "float",
    "failure_count": "integer",
    "mrr_score": "float"
  },
  "calculation_time_ms": "float",
  "status": "string"
}
```

### Aggregate Metrics Endpoint
**Endpoint**: `/api/v1/validation/metrics/aggregate`
**Method**: `POST`
**Description**: Calculate aggregated metrics across multiple queries

**Request**:
```json
{
  "query_session_id": "string",
  "metrics_list": "array[object]"
}
```

**Response**:
```json
{
  "aggregated_metrics": {
    "average_retrieval_accuracy": "float",
    "average_similarity_score": "float",
    "total_queries": "integer",
    "success_rate": "float"
  },
  "aggregation_time_ms": "float",
  "status": "string"
}
```

## Validation Pipeline Service

### Full Validation Endpoint
**Endpoint**: `/api/v1/validation/full`
**Method**: `POST`
**Description**: Execute complete validation pipeline: query → embedding → search → validation → metrics

**Request**:
```json
{
  "query_text": "string",
  "parameters": {
    "top_k": "integer",
    "similarity_threshold": "float",
    "collection_name": "string"
  }
}
```

**Response**:
```json
{
  "query_id": "string",
  "retrieved_results": [
    {
      "vector_id": "string",
      "content": "string",
      "similarity_score": "float",
      "validation_result": {
        "is_valid": "boolean",
        "semantic_similarity": "float",
        "content_accuracy": "float"
      }
    }
  ],
  "final_metrics": {
    "retrieval_accuracy": "float",
    "mean_similarity_score": "float",
    "response_time_ms": "float"
  },
  "pipeline_time_ms": "float",
  "status": "string"
}
```

## Error Handling Contracts

### Standard Error Response Format
```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": "object",
    "timestamp": "datetime"
  }
}
```

### Error Codes
- `INVALID_QUERY_FORMAT`: Query text is malformed
- `EMBEDDING_GENERATION_FAILED`: Failed to generate query embedding
- `VECTOR_SEARCH_FAILED`: Qdrant search operation failed
- `CONTENT_VALIDATION_FAILED`: Content validation operation failed
- `METRICS_CALCULATION_FAILED`: Metrics calculation failed
- `QDRANT_CONNECTIVITY_ERROR`: Unable to connect to Qdrant
- `COHERE_API_ERROR`: Cohere API operation failed
- `RATE_LIMIT_EXCEEDED`: API rate limit exceeded
- `RESOURCE_LIMIT_EXCEEDED`: Resource usage exceeded limits

## Performance Contracts

### Response Time SLAs
- Query processing: < 500ms
- Vector search: < 1000ms
- Content validation: < 500ms
- Metrics calculation: < 200ms
- Full pipeline: < 2000ms

### Throughput Requirements
- Support up to 10 concurrent validation requests
- Handle queries up to 1000 characters in length
- Process up to 100 validation requests per minute

### Resource Limits
- Memory usage: < 512MB per validation request
- Connection limits: Respect Qdrant and Cohere API connection limits

## Authentication and Authorization

### Required Headers
All API requests require the following headers:
```
Content-Type: application/json
Authorization: Bearer {API_TOKEN}
```

### API Token Management
- API tokens are valid for 24 hours
- Tokens must be rotated daily
- Invalid tokens return 401 Unauthorized

## Rate Limiting

### Rate Limits
- Query processing: 100 requests per minute per IP
- Vector search: 50 requests per minute per IP
- Content validation: 75 requests per minute per IP
- Full pipeline: 25 requests per minute per IP

### Rate Limit Headers
Rate-limited responses include:
```
X-RateLimit-Limit: {limit}
X-RateLimit-Remaining: {remaining}
X-RateLimit-Reset: {timestamp}
```