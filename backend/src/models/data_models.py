"""
Data models for the embeddings pipeline.
"""
from datetime import datetime
from typing import Dict, List, Optional, Any
import uuid
from src.config import settings


class BookContent:
    """
    Represents the source material from the AI Robotics textbook.
    """
    def __init__(
        self,
        url: str,
        title: str = "",
        content: str = "",
        module: str = "",
        chapter: str = "",
        created_at: datetime = None,
        updated_at: datetime = None
    ):
        self.id = str(uuid.uuid4())
        self.url = url
        self.title = title
        self.content = content
        self.module = module
        self.chapter = chapter
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'url': self.url,
            'title': self.title,
            'content': self.content,
            'module': self.module,
            'chapter': self.chapter,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BookContent':
        content = cls(
            url=data['url'],
            title=data.get('title', ''),
            content=data.get('content', ''),
            module=data.get('module', ''),
            chapter=data.get('chapter', '')
        )
        content.id = data.get('id', str(uuid.uuid4()))
        return content

    def validate(self) -> bool:
        """
        Validate the BookContent instance.

        Returns:
            True if valid, False otherwise
        """
        if not self.url:
            return False
        if not self.content:
            return False
        return True


class TextChunk:
    """
    Represents a segment of book content after text processing.
    """
    def __init__(
        self,
        content: str,
        source_url: str = "",
        module: str = "",
        chapter: str = "",
        chunk_index: int = 0,
        metadata: Dict[str, Any] = None,
        created_at: datetime = None
    ):
        self.id = str(uuid.uuid4())
        self.content = content
        self.source_url = source_url
        self.module = module
        self.chapter = chapter
        self.chunk_index = chunk_index
        self.metadata = metadata or {}
        self.created_at = created_at or datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'content': self.content,
            'source_url': self.source_url,
            'module': self.module,
            'chapter': self.chapter,
            'chunk_index': self.chunk_index,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TextChunk':
        chunk = cls(
            content=data['content'],
            source_url=data.get('source_url', ''),
            module=data.get('module', ''),
            chapter=data.get('chapter', ''),
            chunk_index=data.get('chunk_index', 0),
            metadata=data.get('metadata', {})
        )
        chunk.id = data.get('id', str(uuid.uuid4()))
        return chunk

    def validate(self) -> bool:
        """
        Validate the TextChunk instance.

        Returns:
            True if valid, False otherwise
        """
        if not self.content:
            return False
        if self.chunk_index < 0:
            return False
        # Check if content length is within Cohere API limits
        if len(self.content) > 4096:  # Approximate token limit
            return False
        return True


class Embedding:
    """
    Represents the vector embedding of a text chunk.
    """
    def __init__(
        self,
        vector: List[float],
        chunk_id: str,
        model: str = "",
        created_at: datetime = None
    ):
        self.id = str(uuid.uuid4())
        self.vector = vector
        self.chunk_id = chunk_id
        self.model = model
        self.created_at = created_at or datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'vector': self.vector,
            'chunk_id': self.chunk_id,
            'model': self.model,
            'created_at': self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Embedding':
        embedding = cls(
            vector=data['vector'],
            chunk_id=data['chunk_id'],
            model=data.get('model', '')
        )
        embedding.id = data.get('id', str(uuid.uuid4()))
        return embedding

    def validate(self) -> bool:
        """
        Validate the Embedding instance according to data-model.md specifications.

        Returns:
            True if valid, False otherwise
        """
        if not self.vector:
            print("Validation failed: Vector is required for Embedding")
            return False
        if not self.chunk_id:
            print("Validation failed: chunk_id is required for Embedding")
            return False
        if not self.model:
            print("Validation failed: model is required for Embedding")
            return False

        # Check for NaN or infinite values in vector
        import math
        for value in self.vector:
            if math.isnan(value) or math.isinf(value):
                print("Validation failed: Vector contains NaN or infinite values")
                return False

        # Validate vector dimensions (should match Cohere model dimensions)
        expected_dims = {
            'embed-english-v3.0': 1024,
            'embed-multilingual-v3.0': 1024,
            'embed-english-light-v3.0': 384,
            'embed-multilingual-light-v3.0': 384
        }

        expected_dim = expected_dims.get(self.model, 1024)  # Default to 1024 if unknown model
        if len(self.vector) != expected_dim:
            print(f"Validation failed: Vector dimension mismatch. Expected {expected_dim}, got {len(self.vector)} for model {self.model}")
            return False

        return True


class QdrantRecord:
    """
    Represents a record stored in Qdrant vector database.
    """
    def __init__(
        self,
        payload: Dict[str, Any],
        vector: List[float],
        record_id: str = None,
        created_at: datetime = None
    ):
        self.id = record_id or str(uuid.uuid4())
        self.payload = payload
        self.vector = vector
        self.created_at = created_at or datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'payload': self.payload,
            'vector': self.vector,
            'created_at': self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'QdrantRecord':
        record = cls(
            payload=data['payload'],
            vector=data['vector']
        )
        record.id = data.get('id', str(uuid.uuid4()))
        return record

    def validate(self) -> bool:
        """
        Validate the QdrantRecord instance according to data-model.md specifications.

        Returns:
            True if valid, False otherwise
        """
        if not self.payload:
            print("Validation failed: Payload is required for QdrantRecord")
            return False
        if not self.vector:
            print("Validation failed: Vector is required for QdrantRecord")
            return False
        if 'content' not in self.payload:
            print("Validation failed: Payload must contain 'content' field")
            return False

        # Validate required fields in payload according to data-model.md
        required_payload_fields = ['content', 'source_url', 'module', 'chapter', 'chunk_index']
        for field in required_payload_fields:
            if field not in self.payload:
                print(f"Validation failed: Payload missing required field '{field}'")
                return False

        # Check for NaN or infinite values in vector
        import math
        for value in self.vector:
            if math.isnan(value) or math.isinf(value):
                print("Validation failed: Vector contains NaN or infinite values")
                return False

        # Validate vector dimensions match expected size for Cohere embeddings
        expected_dims = {
            settings.COHERE_MODEL: 1024 if 'v3.0' in settings.COHERE_MODEL else 384
        }
        expected_dim = expected_dims.get(settings.COHERE_MODEL, 1024)
        if len(self.vector) != expected_dim:
            print(f"Validation failed: Vector dimension mismatch. Expected {expected_dim}, got {len(self.vector)}")
            return False

        return True