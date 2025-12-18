# API Contracts: AI Agent with Retrieval

## Overview

This document defines the API contracts for the AI agent with retrieval functionality. These contracts specify the interfaces for agent interaction, query processing, and response delivery.

## Agent Query Endpoint

### Submit Query
**Endpoint**: `/api/v1/agent/query`
**Method**: `POST`
**Description**: Submit a natural language query to the AI agent

**Request**:
```json
{
  "query": "string",
  "max_tokens": "integer",
  "temperature": "float",
  "metadata": "object"
}
```

**Response**:
```json
{
  "status": "string",
  "data": {
    "response_id": "string",
    "query": "string",
    "answer": "string",
    "sources": ["string"],
    "confidence_score": "float",
    "processing_time_ms": "float",
    "retrieval_context": ["string"],
    "timestamp": "datetime",
    "metadata": "object"
  },
  "error": "object",
  "request_id": "string",
  "timestamp": "datetime"
}
```

**Example Request**:
```json
{
  "query": "What is inverse kinematics in robotics?",
  "max_tokens": 500,
  "temperature": 0.7
}
```

**Example Response**:
```json
{
  "status": "success",
  "data": {
    "response_id": "resp_abc123",
    "query": "What is inverse kinematics in robotics?",
    "answer": "Inverse kinematics is the mathematical process of determining the joint angles required to achieve a desired end-effector position and orientation...",
    "sources": ["Chapter 3: Kinematics", "Section 3.2: Inverse Kinematics"],
    "confidence_score": 0.92,
    "processing_time_ms": 1250,
    "retrieval_context": ["Forward kinematics solves the problem of finding the end-effector position given joint angles..."],
    "timestamp": "2025-12-15T10:30:00Z",
    "metadata": {}
  },
  "error": null,
  "request_id": "req_def456",
  "timestamp": "2025-12-15T10:30:00Z"
}
```

**Error Responses**:
- 400: Invalid query format
- 429: Rate limit exceeded
- 500: Internal processing error
- 503: OpenAI API unavailable

## Health Check Endpoint

### Health Status
**Endpoint**: `/health`
**Method**: `GET`
**Description**: Check the health status of the AI agent service

**Response**:
```json
{
  "status": "string",
  "timestamp": "datetime",
  "services": {
    "openai": "boolean",
    "qdrant": "boolean",
    "cohere": "boolean"
  }
}
```

**Example Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-15T10:30:00Z",
  "services": {
    "openai": true,
    "qdrant": true,
    "cohere": true
  }
}
```

## Configuration Endpoint

### Get Configuration
**Endpoint**: `/api/v1/agent/config`
**Method**: `GET`
**Description**: Get the current configuration of the AI agent

**Response**:
```json
{
  "status": "string",
  "data": {
    "model": "string",
    "max_tokens": "integer",
    "temperature_range": {
      "min": "float",
      "max": "float"
    },
    "retrieval_settings": {
      "top_k": "integer",
      "similarity_threshold": "float"
    },
    "rate_limits": {
      "requests_per_minute": "integer"
    }
  },
  "timestamp": "datetime"
}
```

## Interface Specifications

### Agent Interface
```python
class AgentInterface:
    def create_agent(self, instructions: str) -> str:
        """
        Create a new AI agent with specific instructions
        Returns agent ID
        """

    def process_query(self, query: str, context: List[str] = None) -> AgentResponse:
        """
        Process a query with the AI agent using optional context
        Returns structured agent response
        """

    def validate_response(self, response: str, context: List[str]) -> bool:
        """
        Validate that the response is grounded in the provided context
        Returns True if valid, False otherwise
        """
```

### Retrieval Interface
```python
class RetrievalInterface:
    def retrieve_context(self, query: str, top_k: int = 5) -> RetrievalResult:
        """
        Retrieve relevant context from the knowledge base
        Returns retrieval results with context snippets
        """

    def validate_content_access(self, content_id: str) -> bool:
        """
        Validate that the agent can access specific content
        Returns True if accessible, False otherwise
        """
```

### API Interface
```python
class APIInterface:
    def handle_query_request(self, request: QueryRequest) -> APIResponse:
        """
        Handle incoming query requests
        Returns standardized API response
        """

    def validate_input(self, request: QueryRequest) -> List[str]:
        """
        Validate input request parameters
        Returns list of validation errors
        """
```

## Integration Contracts

### OpenAI API Integration
- **Rate Limit**: Respect OpenAI's API rate limits (typically 3000 requests per minute for GPT-4)
- **Timeout**: Set request timeout to 30 seconds
- **Retry Logic**: Implement exponential backoff for rate limit errors
- **Error Handling**: Handle API errors gracefully with fallback strategies

### Qdrant Integration
- **Connection Pooling**: Use connection pooling for efficient resource usage
- **Query Parameters**: Support configurable search parameters (top_k, similarity threshold)
- **Collection Schema**: Validate collection schema matches expected data model

### Cohere Integration
- **Embedding Consistency**: Use the same embedding model as the existing RAG pipeline
- **Batch Processing**: Support batch embedding requests for efficiency
- **Rate Limiting**: Handle API rate limits appropriately

### Environment Configuration
Required environment variables:
```bash
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
COHERE_API_KEY=your_cohere_api_key
EMBEDDING_MODEL=embed-multilingual-v3.0  # Or other Cohere model used
COLLECTION_NAME=robotics_textbook_chunks
AGENT_INSTRUCTIONS="You are an AI assistant for the AI Robotics textbook. Answer questions based only on the provided context from the textbook. Do not hallucinate information."
```

## Error Handling Contracts

### Error Categories
1. **Client Errors (4xx)**: Invalid requests, malformed queries, rate limits
2. **Server Errors (5xx)**: API failures, database connectivity issues
3. **Content Errors**: No relevant content found, retrieval failures
4. **Agent Errors**: OpenAI API failures, response validation failures

### Error Response Format
```json
{
  "status": "error",
  "data": null,
  "error": {
    "type": "string",
    "message": "string",
    "details": "object",
    "timestamp": "datetime"
  },
  "request_id": "string",
  "timestamp": "datetime"
}
```

## Performance Contracts

### Response Time SLAs
- Query processing: < 5000ms (5 seconds)
- Retrieval operation: < 2000ms (2 seconds)
- Agent response generation: < 3000ms (3 seconds)

### Throughput Requirements
- Support up to 10 concurrent agent requests
- Handle queries up to 500 characters in length
- Process up to 1000 validation requests per hour

### Resource Limits
- Memory usage: < 1GB per service instance
- Connection limits: Respect OpenAI and Qdrant API connection limits
- Response size: Limit to 10KB per response to prevent oversized payloads