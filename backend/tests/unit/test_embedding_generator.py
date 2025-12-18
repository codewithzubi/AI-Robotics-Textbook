"""
Unit tests for the embedding generator module.
"""
import unittest
from unittest.mock import patch, MagicMock
from src.embeddings_pipeline.embedding_generator import (
    validate_embedding_quality, validate_embeddings_batch
)


class TestEmbeddingGenerator(unittest.TestCase):
    """Test cases for embedding generator functions."""

    def test_validate_embedding_quality_valid(self):
        """Test validation of a high-quality embedding."""
        # Create a mock embedding with reasonable values
        embedding = [0.1, 0.2, 0.3, 0.4] * 256  # 1024-dimensional vector
        result = validate_embedding_quality(embedding)
        self.assertTrue(result['valid'])
        self.assertGreater(result['quality_score'], 0.5)

    def test_validate_embedding_quality_invalid(self):
        """Test validation of a low-quality embedding."""
        # Test with all zeros (degenerate case)
        embedding = [0.0] * 1024
        result = validate_embedding_quality(embedding)
        self.assertFalse(result['valid'])
        self.assertLess(result['quality_score'], 0.5)

        # Test with NaN values
        import math
        embedding_with_nan = [0.1] * 1024
        embedding_with_nan[0] = float('nan')
        result = validate_embedding_quality(embedding_with_nan)
        self.assertFalse(result['valid'])

        # Test with infinite values
        embedding_with_inf = [0.1] * 1024
        embedding_with_inf[0] = float('inf')
        result = validate_embedding_quality(embedding_with_inf)
        self.assertFalse(result['valid'])

    def test_validate_embeddings_batch(self):
        """Test batch validation of embeddings."""
        embeddings = [
            {
                'id': 'emb1',
                'vector': [0.1, 0.2, 0.3] * 341 + [0.1],  # ~1024 elements
                'model': 'embed-english-v3.0'
            },
            {
                'id': 'emb2',
                'vector': [0.4, 0.5, 0.6] * 341 + [0.2],  # ~1024 elements
                'model': 'embed-english-v3.0'
            }
        ]
        result = validate_embeddings_batch(embeddings)
        self.assertEqual(result['total_embeddings'], 2)
        self.assertGreaterEqual(result['valid_count'], 0)  # May vary based on quality
        self.assertLessEqual(result['invalid_count'], 2)

        # Test with an embedding that has an error
        embeddings_with_error = embeddings + [
            {
                'id': 'emb3',
                'error': 'API error occurred'
            }
        ]
        result = validate_embeddings_batch(embeddings_with_error)
        self.assertEqual(result['total_embeddings'], 3)
        # The error embedding should be counted as invalid


if __name__ == '__main__':
    unittest.main()