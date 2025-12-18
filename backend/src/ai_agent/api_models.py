"""
API Models for AI Agent with Retrieval

This module defines the Pydantic models for API request/response validation
according to the data model specification.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class QueryRequest(BaseModel):
    """
    Represents a natural language query submitted by the user to the AI agent.
    """
    query: str = Field(..., description="The natural language question from the user", min_length=1, max_length=1000)
    max_tokens: int = Field(default=500, description="Maximum number of tokens for the response", ge=1, le=2000)
    temperature: float = Field(default=0.7, description="Temperature setting for response creativity", ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata for the query")


class AgentResponse(BaseModel):
    """
    Represents the AI-generated response to a user query, including metadata about the response.
    """
    response_id: str = Field(..., description="Unique identifier for this response")
    query: str = Field(..., description="The original query that generated this response")
    answer: str = Field(..., description="The AI-generated answer")
    sources: List[str] = Field(default_factory=list, description="List of sources/references used in the answer")
    confidence_score: float = Field(..., description="Confidence score for the response", ge=0.0, le=1.0)
    processing_time_ms: float = Field(..., description="Time taken to process the query", ge=0.0)
    retrieval_context: List[str] = Field(default_factory=list, description="Context snippets used from the knowledge base")
    timestamp: datetime = Field(..., description="When the response was generated")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class RetrievalResult(BaseModel):
    """
    Represents the results from the retrieval pipeline that inform the agent's response.
    """
    result_id: str = Field(..., description="Unique identifier for this result")
    query_embedding: List[float] = Field(..., description="Embedding of the original query")
    retrieved_chunks: List[Dict[str, Any]] = Field(default_factory=list, description="List of retrieved content chunks")
    similarity_scores: List[float] = Field(default_factory=list, description="Similarity scores for each chunk")
    collection_name: str = Field(..., description="Name of the vector collection used")
    retrieval_time_ms: float = Field(..., description="Time taken for retrieval operation", ge=0.0)
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional retrieval metadata")


class AgentSession(BaseModel):
    """
    Represents a session of interactions with the AI agent (for potential conversation support).
    """
    session_id: str = Field(..., description="Unique identifier for the session")
    created_at: datetime = Field(..., description="When the session was created")
    last_interaction: datetime = Field(..., description="When the last interaction occurred")
    interaction_count: int = Field(default=0, description="Number of interactions in this session", ge=0)
    user_id: Optional[str] = Field(None, description="Optional user identifier")
    context_history: List[Dict[str, str]] = Field(default_factory=list, description="History of query-response pairs")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional session metadata")


class APIResponse(BaseModel):
    """
    Standardized response format for the FastAPI endpoints.
    """
    status: str = Field(..., description="Status of the response (success/error)")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    error: Optional[Dict[str, str]] = Field(None, description="Error information if status is error")
    request_id: str = Field(..., description="Unique identifier for the request")
    timestamp: datetime = Field(..., description="When the response was generated")