# Data Model: AI Agent with Retrieval

**Feature**: 003-ai-agent-retrieval
**Date**: 2025-12-15
**Version**: 1.0

## Overview

This document defines the data models for the AI agent with retrieval functionality. The models support query processing, agent interaction, retrieval integration, and API communication.

## Core Entities

### QueryRequest
Represents a natural language query submitted by the user to the AI agent.

```python
class QueryRequest:
    query: str              # The natural language question from the user
    max_tokens: int         # Maximum number of tokens for the response (default: 500)
    temperature: float      # Temperature setting for response creativity (default: 0.7)
    metadata: Dict[str, Any] # Additional metadata for the query (optional)
```

**Purpose**: Captures user input and configuration parameters for the AI agent query.

### AgentResponse
Represents the AI-generated response to a user query, including metadata about the response.

```python
class AgentResponse:
    response_id: str                    # Unique identifier for this response
    query: str                         # The original query that generated this response
    answer: str                        # The AI-generated answer
    sources: List[str]                 # List of sources/references used in the answer
    confidence_score: float            # Confidence score for the response (0.0-1.0)
    processing_time_ms: float          # Time taken to process the query
    retrieval_context: List[str]       # Context snippets used from the knowledge base
    timestamp: datetime                # When the response was generated
    metadata: Dict[str, Any]           # Additional metadata
```

**Purpose**: Contains the complete response from the AI agent with provenance information.

### RetrievalResult
Represents the results from the retrieval pipeline that inform the agent's response.

```python
class RetrievalResult:
    result_id: str              # Unique identifier for this result
    query_embedding: List[float] # Embedding of the original query
    retrieved_chunks: List[Dict[str, Any]] # List of retrieved content chunks
    similarity_scores: List[float] # Similarity scores for each chunk
    collection_name: str        # Name of the vector collection used
    retrieval_time_ms: float    # Time taken for retrieval operation
    metadata: Dict[str, Any]    # Additional retrieval metadata
```

**Purpose**: Contains the retrieved context that will be provided to the AI agent.

### AgentSession
Represents a session of interactions with the AI agent (for potential conversation support).

```python
class AgentSession:
    session_id: str                    # Unique identifier for the session
    created_at: datetime               # When the session was created
    last_interaction: datetime         # When the last interaction occurred
    interaction_count: int             # Number of interactions in this session
    user_id: Optional[str]             # Optional user identifier
    context_history: List[Dict[str, str]] # History of query-response pairs
    metadata: Dict[str, Any]           # Additional session metadata
```

**Purpose**: Maintains state for multi-turn conversations (future enhancement).

### APIResponse
Standardized response format for the FastAPI endpoints.

```python
class APIResponse:
    status: str                       # Status of the response (success/error)
    data: Optional[Union[AgentResponse, Dict[str, Any]]] # Response data
    error: Optional[Dict[str, str]]   # Error information if status is error
    request_id: str                   # Unique identifier for the request
    timestamp: datetime               # When the response was generated
```

**Purpose**: Standardized format for all API responses.

## Relationships

```
QueryRequest --(1 to 1)--> RetrievalResult
RetrievalResult --(1 to 1)--> AgentResponse
QueryRequest --(1 to 1)--> AgentResponse
AgentResponse --(many to 1)--> AgentSession
APIResponse --(1 to 1)--> AgentResponse
```

## Data Flow

1. **Query Processing**: QueryRequest is received via FastAPI endpoint
2. **Retrieval**: Query is processed through the RAG pipeline to generate RetrievalResult
3. **Agent Processing**: RetrievalResult is used as context to generate AgentResponse
4. **API Response**: AgentResponse is wrapped in APIResponse for return to client
5. **Session Tracking**: Interactions may be tracked in AgentSession for conversation support

## Validation Rules

- QueryRequest.query must be non-empty and less than 1000 characters
- AgentResponse.answer must be non-empty and properly grounded in retrieval context
- Confidence scores must be between 0.0 and 1.0
- Processing times must be positive values
- All timestamp fields must be in UTC
- Metadata fields must be valid JSON-serializable dictionaries

## Serialization Format

All entities will be serializable to JSON format for API communication:

```json
{
  "entity_type": "QueryRequest|AgentResponse|RetrievalResult|AgentSession|APIResponse",
  "data": { /* entity-specific fields */ },
  "version": "1.0"
}
```

## Performance Considerations

- QueryRequest and APIResponse objects should be lightweight for fast API communication
- AgentResponse should include only necessary context to minimize payload size
- RetrievalResult may be large but is internal to the service
- Caching strategies should consider the size of retrieval context
- Consider pagination for large retrieval results