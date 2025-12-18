"""
Integration tests for the embeddings pipeline.
"""
import unittest
from unittest.mock import patch, MagicMock
from src.embeddings_pipeline.text_chunker import chunk_text
from src.embeddings_pipeline.embedding_generator import embed
from src.embeddings_pipeline.qdrant_handler import save_chunks_to_qdrant


class TestPipelineIntegration(unittest.TestCase):
    """Integration tests for pipeline components."""

    @patch('src.embeddings_pipeline.embedding_generator.initialize_cohere_client')
    def test_chunk_to_embedding_flow(self, mock_init_client):
        """Test the flow from text chunking to embedding generation."""
        # Mock Cohere client
        mock_client = MagicMock()
        mock_client.embed.return_value = MagicMock()
        mock_client.embed.return_value.embeddings = [[0.1, 0.2, 0.3]]  # Mock embedding
        mock_init_client.return_value = mock_client

        # Test content
        content = "This is a test sentence. Here is another test sentence."

        # Chunk the text
        chunks = chunk_text(
            content=content,
            source_url="https://example.com",
            module="Module 1",
            chapter="Chapter 1"
        )

        self.assertGreater(len(chunks), 0)

        # Generate embeddings for the chunks
        embeddings = embed(chunks, model="test-model", max_retries=1)

        # Note: Since we're mocking, we expect the embed function to return mocked data
        # In a real scenario, this would generate actual embeddings

    def test_chunk_validation_flow(self):
        """Test the flow with validation at each step."""
        content = "This is test content for validation purposes."

        # Chunk the text
        chunks = chunk_text(
            content=content,
            source_url="https://example.com",
            module="Module 1",
            chapter="Chapter 1"
        )

        # Validate chunks
        from src.models.data_models import TextChunk
        for chunk_data in chunks:
            chunk = TextChunk(
                content=chunk_data['content'],
                source_url=chunk_data['source_url'],
                module=chunk_data['module'],
                chapter=chunk_data['chapter'],
                chunk_index=chunk_data['chunk_index']
            )
            self.assertTrue(chunk.validate())


if __name__ == '__main__':
    unittest.main()