"""
Unit tests for the data models.
"""
import unittest
from datetime import datetime
from src.models.data_models import BookContent, TextChunk, Embedding, QdrantRecord


class TestModels(unittest.TestCase):
    """Test cases for data models."""

    def test_book_content_model(self):
        """Test BookContent model functionality."""
        content = BookContent(
            url="https://example.com",
            title="Test Title",
            content="Test content",
            module="Module 1",
            chapter="Chapter 1"
        )

        self.assertEqual(content.url, "https://example.com")
        self.assertEqual(content.title, "Test Title")
        self.assertEqual(content.content, "Test content")
        self.assertEqual(content.module, "Module 1")
        self.assertEqual(content.chapter, "Chapter 1")

        # Test to_dict and from_dict
        data = content.to_dict()
        self.assertEqual(data['url'], "https://example.com")
        self.assertEqual(data['title'], "Test Title")

        content2 = BookContent.from_dict(data)
        self.assertEqual(content2.url, "https://example.com")

        # Test validation
        self.assertTrue(content.validate())

        # Test validation with missing URL
        invalid_content = BookContent(url="", content="Test content")
        self.assertFalse(invalid_content.validate())

    def test_text_chunk_model(self):
        """Test TextChunk model functionality."""
        chunk = TextChunk(
            content="Test chunk content",
            source_url="https://example.com",
            module="Module 1",
            chapter="Chapter 1",
            chunk_index=0
        )

        self.assertEqual(chunk.content, "Test chunk content")
        self.assertEqual(chunk.source_url, "https://example.com")
        self.assertEqual(chunk.module, "Module 1")
        self.assertEqual(chunk.chapter, "Chapter 1")
        self.assertEqual(chunk.chunk_index, 0)

        # Test validation
        self.assertTrue(chunk.validate())

        # Test validation with empty content
        invalid_chunk = TextChunk(content="", source_url="https://example.com")
        self.assertFalse(invalid_chunk.validate())

    def test_embedding_model(self):
        """Test Embedding model functionality."""
        embedding = Embedding(
            vector=[0.1, 0.2, 0.3],
            chunk_id="chunk_123",
            model="test-model"
        )

        self.assertEqual(embedding.vector, [0.1, 0.2, 0.3])
        self.assertEqual(embedding.chunk_id, "chunk_123")
        self.assertEqual(embedding.model, "test-model")

        # Test validation
        self.assertTrue(embedding.validate())

        # Test validation with invalid vector (NaN)
        import math
        invalid_embedding = Embedding(
            vector=[0.1, float('nan'), 0.3],
            chunk_id="chunk_123",
            model="test-model"
        )
        self.assertFalse(invalid_embedding.validate())

    def test_qdrant_record_model(self):
        """Test QdrantRecord model functionality."""
        record = QdrantRecord(
            payload={
                'content': 'Test content',
                'source_url': 'https://example.com',
                'module': 'Module 1',
                'chapter': 'Chapter 1',
                'chunk_index': 0
            },
            vector=[0.1, 0.2, 0.3]
        )

        self.assertEqual(record.payload['content'], 'Test content')
        self.assertEqual(record.vector, [0.1, 0.2, 0.3])

        # Test validation
        self.assertTrue(record.validate())

        # Test validation with missing required payload field
        invalid_record = QdrantRecord(
            payload={'content': 'Test content'},  # Missing required fields
            vector=[0.1, 0.2, 0.3]
        )
        self.assertFalse(invalid_record.validate())


if __name__ == '__main__':
    unittest.main()