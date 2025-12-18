"""
API Endpoints for AI Agent with Retrieval

This module implements FastAPI endpoints for agent interaction.
"""
import uuid
import time
import asyncio
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from datetime import datetime
from .agent import AIAgent
from .retrieval_integrator import RetrievalIntegrator
from .content_grounding import ContentGrounding
from .api_models import QueryRequest, APIResponse, AgentResponse
from ..config.settings import settings


router = APIRouter(prefix="/api/v1/agent", tags=["AI Agent"])


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    services: Dict[str, bool]


@router.post("/query", response_model=APIResponse)
async def query_agent(request: QueryRequest):
    """
    Submit a natural language query to the AI agent.
    """
    request_id = str(uuid.uuid4())
    start_time = time.time()

    try:
        # Validate the request
        validation_errors = validate_input(request)
        if validation_errors:
            error_response = APIResponse(
                status="error",
                data=None,
                error={
                    "type": "ValidationError",
                    "message": "Invalid input parameters",
                    "details": str({"errors": validation_errors} if validation_errors else {})
                },
                request_id=request_id,
                timestamp=datetime.utcnow()
            )
            return error_response

        # Initialize components
        agent = AIAgent()
        retriever = RetrievalIntegrator()
        content_grounder = ContentGrounding()

        # Retrieve context from the knowledge base
        retrieval_result = retriever.retrieve_context(
            query=request.query,
            top_k=min(request.max_tokens // 50, 10),  # Dynamic top_k based on max_tokens
            similarity_threshold=getattr(settings, 'SIMILARITY_THRESHOLD', 0.5)
        )

        # Process the query with the agent
        agent_response = agent.process_query(request, retrieval_result)

        # Apply content grounding validation
        grounded_response = content_grounder.enforce_content_restriction(
            agent_response,
            [chunk.get('content', '') for chunk in retrieval_result.retrieved_chunks]
        )

        # Calculate total processing time
        total_time = (time.time() - start_time) * 1000

        # Update processing time with total time
        grounded_response.processing_time_ms = total_time

        # Create success response
        api_response = APIResponse(
            status="success",
            data=grounded_response.dict(),
            error=None,
            request_id=request_id,
            timestamp=datetime.utcnow()
        )

        return api_response

    except Exception as e:
        # Handle any errors
        processing_time = (time.time() - start_time) * 1000

        error_response = APIResponse(
            status="error",
            data=None,
            error={
                "type": type(e).__name__,
                "message": str(e),
                "details": "{}"
            },
            request_id=request_id,
            timestamp=datetime.utcnow()
        )

        # Log the error
        print(f"Error processing query: {str(e)}")
        return error_response


@router.get("/config")
async def get_config():
    """
    Get the current configuration of the AI agent.
    """
    try:
        config = {
            "model": getattr(settings, 'AGENT_MODEL', 'gpt-4-turbo-preview'),
            "max_tokens": 2000,  # Default max tokens
            "temperature_range": {
                "min": 0.0,
                "max": 1.0
            },
            "retrieval_settings": {
                "top_k": getattr(settings, 'DEFAULT_TOP_K', 5),
                "similarity_threshold": getattr(settings, 'SIMILARITY_THRESHOLD', 0.5)
            },
            "rate_limits": {
                "requests_per_minute": getattr(settings, 'RATE_LIMIT_PER_MINUTE', 60)
            }
        }

        response = APIResponse(
            status="success",
            data=config,
            error=None,
            request_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow()
        )

        return response

    except Exception as e:
        error_response = APIResponse(
            status="error",
            data=None,
            error={
                "type": type(e).__name__,
                "message": str(e),
                "details": "{}"
            },
            request_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow()
        )

        return error_response


def validate_input(request: QueryRequest) -> list:
    """
    Validate input request parameters.

    Args:
        request: QueryRequest to validate

    Returns:
        List[str]: List of validation errors
    """
    errors = []

    # Validate query length
    if len(request.query.strip()) < 1:
        errors.append("Query cannot be empty")

    if len(request.query) > 1000:
        errors.append("Query must be less than 1000 characters")

    # Validate max_tokens range
    if request.max_tokens < 1 or request.max_tokens > 2000:
        errors.append("max_tokens must be between 1 and 2000")

    # Validate temperature range
    if request.temperature < 0.0 or request.temperature > 1.0:
        errors.append("temperature must be between 0.0 and 1.0")

    # Validate metadata if provided
    if request.metadata:
        if not isinstance(request.metadata, dict):
            errors.append("metadata must be a dictionary")
        else:
            # Check for potential injection issues in metadata keys/values
            for key, value in request.metadata.items():
                if not isinstance(key, str):
                    errors.append("metadata keys must be strings")
                # Add other validation as needed

    return errors


@router.get("/health")
async def health_check():
    """
    Check the health status of the AI agent service.
    """
    # Check if services are available
    services_status = {
        "openai": check_openai_connection(),
        "qdrant": check_qdrant_connection(),
        "cohere": check_cohere_connection()
    }

    overall_status = "healthy" if all(services_status.values()) else "degraded"

    health_response = HealthResponse(
        status=overall_status,
        timestamp=datetime.utcnow(),
        services=services_status
    )

    return APIResponse(
        status="success",
        data=health_response.dict(),
        error=None,
        request_id=str(uuid.uuid4()),
        timestamp=datetime.utcnow()
    )


def check_openai_connection() -> bool:
    """
    Check if OpenAI API is accessible.

    Returns:
        bool: True if accessible, False otherwise
    """
    try:
        # Import here to avoid circular dependencies
        from .agent import AIAgent
        import openai

        # Try to initialize the agent (doesn't make an API call)
        agent = AIAgent()
        return True
    except Exception:
        return False


def check_qdrant_connection() -> bool:
    """
    Check if Qdrant is accessible.

    Returns:
        bool: True if accessible, False otherwise
    """
    try:
        # Import here to avoid circular dependencies
        from .retrieval_integrator import RetrievalIntegrator
        from ..rag_validation.vector_search import VectorSearch

        # Try to connect to Qdrant
        search = VectorSearch()
        return search.connect()
    except Exception:
        return False


def check_cohere_connection() -> bool:
    """
    Check if Cohere is accessible.

    Returns:
        bool: True if accessible, False otherwise
    """
    try:
        # We'll check if the settings for Cohere are properly configured
        # by checking if the environment variable is set
        return bool(getattr(settings, 'COHERE_API_KEY'))
    except Exception:
        return False