import os
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
BOOK_BASE_URL = os.getenv("BOOK_BASE_URL", "https://ai-robotics-textbook-ten.vercel.app/")
SITEMAP_URL = os.getenv("SITEMAP_URL", "https://ai-robotics-textbook-ten.vercel.app/sitemap.xml")

# Default Cohere model for embeddings
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "embed-english-v3.0")

# Qdrant collection name
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "rag_embeddings")

# Text chunking parameters
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))

# Request timeout settings
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))


class Settings:
    def __init__(self):
        self.COHERE_API_KEY = os.getenv("COHERE_API_KEY")
        self.QDRANT_URL = os.getenv("QDRANT_URL")
        self.QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
        self.BOOK_BASE_URL = os.getenv("BOOK_BASE_URL", "https://ai-robotics-textbook-ten.vercel.app/")
        self.SITEMAP_URL = os.getenv("SITEMAP_URL", "https://ai-robotics-textbook-ten.vercel.app/sitemap.xml")
        self.EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "embed-english-v3.0")
        self.QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "rag_embeddings")
        self.CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
        self.CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))
        self.REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))

        # AI Agent settings
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.AGENT_MODEL = os.getenv("AGENT_MODEL", "gpt-4-turbo-preview")
        self.AGENT_INSTRUCTIONS = os.getenv(
            "AGENT_INSTRUCTIONS",
            "You are an AI assistant for the AI Robotics textbook. Answer questions based only on the provided context from the textbook. Do not hallucinate information."
        )
        self.DEFAULT_TOP_K = int(os.getenv("DEFAULT_TOP_K", "5"))
        self.SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.5"))
        self.RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
        self.CONTENT_GROUNDING_ENABLED = os.getenv("CONTENT_GROUNDING_ENABLED", "true").lower() == "true"
        self.HALLUCINATION_DETECTION_ENABLED = os.getenv("HALLUCINATION_DETECTION_ENABLED", "true").lower() == "true"


# Create a settings instance
settings = Settings()