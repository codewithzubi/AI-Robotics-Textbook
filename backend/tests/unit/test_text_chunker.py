"""
Unit tests for the text chunker module.
"""
import unittest
from src.embeddings_pipeline.text_chunker import (
    chunk_text, split_into_sentences, chunk_by_paragraphs, validate_chunk_size
)


class TestTextChunker(unittest.TestCase):
    """Test cases for text chunker functions."""

    def test_split_into_sentences(self):
        """Test sentence splitting functionality."""
        text = "This is sentence one. This is sentence two! Is this sentence three? Yes, it is."
        sentences = split_into_sentences(text)
        self.assertEqual(len(sentences), 4)
        self.assertIn("This is sentence one", sentences[0])
        self.assertIn("This is sentence two", sentences[1])

    def test_chunk_text_basic(self):
        """Test basic text chunking."""
        content = "This is a sample text. " * 50  # Create a longer text
        chunks = chunk_text(
            content=content,
            source_url="https://example.com",
            module="Module 1",
            chapter="Chapter 1",
            max_chunk_size=100
        )
        self.assertGreater(len(chunks), 1)  # Should be split into multiple chunks
        for chunk in chunks:
            self.assertLessEqual(len(chunk['content']), 100)

    def test_chunk_by_paragraphs(self):
        """Test paragraph-based chunking."""
        content = "Paragraph 1 with some text.\n\nParagraph 2 with more text.\n\nParagraph 3 with final text."
        chunks = chunk_by_paragraphs(
            content=content,
            source_url="https://example.com",
            module="Module 1",
            chapter="Chapter 1"
        )
        self.assertGreaterEqual(len(chunks), 1)

    def test_validate_chunk_size(self):
        """Test chunk size validation."""
        chunk = {
            'content': "This is a test chunk",
            'source_url': "https://example.com",
            'module': "Module 1",
            'chapter': "Chapter 1"
        }
        self.assertTrue(validate_chunk_size(chunk, max_size=100))
        self.assertFalse(validate_chunk_size(chunk, max_size=5))  # Too small


if __name__ == '__main__':
    unittest.main()