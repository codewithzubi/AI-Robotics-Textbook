"""
Hugging Face Spaces Application Entry Point

This file provides a compatible entry point for Hugging Face Spaces deployment.
"""
from src.ai_agent.main import app

# This allows Hugging Face Spaces to automatically detect and run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)