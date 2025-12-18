"""
Settings for AI Agent with Retrieval

This module defines the configuration settings for the AI agent service.
"""
import os
from typing import Optional


class AgentSettings:
    """
    Settings class for the AI agent configuration.
    """

    def __init__(self):
        # OpenAI configuration
        self.OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
        self.AGENT_MODEL: str = os.getenv("AGENT_MODEL", "gpt-4-turbo-preview")

        # Agent instructions
        self.AGENT_INSTRUCTIONS: str = os.getenv(
            "AGENT_INSTRUCTIONS",
            "You are an AI assistant for the AI Robotics textbook. Answer questions based only on the provided context from the textbook. Do not hallucinate information."
        )

        # Retrieval settings
        self.DEFAULT_TOP_K: int = int(os.getenv("DEFAULT_TOP_K", "5"))
        self.SIMILARITY_THRESHOLD: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.5"))

        # Response settings
        self.DEFAULT_MAX_TOKENS: int = int(os.getenv("DEFAULT_MAX_TOKENS", "500"))
        self.DEFAULT_TEMPERATURE: float = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))

        # Rate limiting
        self.RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))

        # Performance settings
        self.RESPONSE_TIMEOUT_SECONDS: int = int(os.getenv("RESPONSE_TIMEOUT_SECONDS", "30"))

        # Validation settings
        self.CONTENT_GROUNDING_ENABLED: bool = os.getenv("CONTENT_GROUNDING_ENABLED", "true").lower() == "true"
        self.HALLUCINATION_DETECTION_ENABLED: bool = os.getenv("HALLUCINATION_DETECTION_ENABLED", "true").lower() == "true"

        # API settings
        self.ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "*").split(",")

        # Qdrant settings (inherited from main settings)
        self.QDRANT_URL: str = os.getenv("QDRANT_URL", "")
        self.QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")
        self.COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "robotics_textbook_chunks")


# Create a global settings instance
settings = AgentSettings()


def validate_settings() -> list:
    """
    Validate the configuration settings.

    Returns:
        List[str]: List of validation errors
    """
    errors = []

    if not settings.OPENAI_API_KEY:
        errors.append("OPENAI_API_KEY is required")

    if not settings.QDRANT_URL:
        errors.append("QDRANT_URL is required")

    if settings.DEFAULT_TOP_K <= 0:
        errors.append("DEFAULT_TOP_K must be greater than 0")

    if not 0.0 <= settings.SIMILARITY_THRESHOLD <= 1.0:
        errors.append("SIMILARITY_THRESHOLD must be between 0.0 and 1.0")

    if not 0.0 <= settings.DEFAULT_TEMPERATURE <= 1.0:
        errors.append("DEFAULT_TEMPERATURE must be between 0.0 and 1.0")

    if settings.DEFAULT_MAX_TOKENS <= 0:
        errors.append("DEFAULT_MAX_TOKENS must be greater than 0")

    return errors