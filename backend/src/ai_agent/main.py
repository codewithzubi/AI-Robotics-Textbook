"""
Main Application Entry Point for AI Agent Service

This module creates the FastAPI application and registers all endpoints.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api_endpoints import router as ai_agent_router
from ..config.settings import settings


# Create the FastAPI application
app = FastAPI(
    title="AI Agent with Retrieval API",
    description="An AI agent service that answers questions based on AI Robotics textbook content using retrieval-augmented generation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=getattr(settings, 'ALLOWED_ORIGINS', ["*"]),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Add any additional security headers as needed
)


# Register the AI agent routes
app.include_router(ai_agent_router)


@app.get("/")
async def root():
    """
    Root endpoint for the AI agent service.
    """
    return {
        "message": "AI Agent with Retrieval Service",
        "version": "1.0.0",
        "description": "An AI agent that answers questions based on AI Robotics textbook content"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for the service.
    """
    return {
        "status": "healthy",
        "timestamp": __import__('datetime').datetime.utcnow().isoformat(),
        "service": "AI Agent with Retrieval"
    }


# Additional application startup/shutdown events can be added here if needed
@app.on_event("startup")
async def startup_event():
    """
    Actions to perform when the application starts up.
    """
    print("AI Agent service starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Actions to perform when the application shuts down.
    """
    print("AI Agent service shutting down...")