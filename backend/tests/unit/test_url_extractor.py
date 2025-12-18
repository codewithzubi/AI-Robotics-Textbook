"""
Unit tests for the URL extractor module.
"""
import unittest
from unittest.mock import patch, MagicMock
from src.embeddings_pipeline.url_extractor import (
    get_all_urls, is_valid_url, filter_book_urls,
    validate_url_accessibility, validate_urls_batch,
    validate_book_content_entity
)


class TestUrlExtractor(unittest.TestCase):
    """Test cases for URL extractor functions."""

    def test_is_valid_url_valid(self):
        """Test that valid URLs are correctly identified."""
        valid_urls = [
            "https://example.com",
            "http://example.com",
            "https://subdomain.example.com/path",
            "http://localhost:8080"
        ]

        for url in valid_urls:
            with self.subTest(url=url):
                self.assertTrue(is_valid_url(url))

    def test_is_valid_url_invalid(self):
        """Test that invalid URLs are correctly identified."""
        invalid_urls = [
            "not_a_url",
            "",
            "htp://example.com",  # typo
            "example.com",  # missing protocol
            "https://",  # incomplete
        ]

        for url in invalid_urls:
            with self.subTest(url=url):
                self.assertFalse(is_valid_url(url))

    def test_filter_book_urls(self):
        """Test filtering URLs by base domain."""
        urls = [
            "https://ai-robotics-textbook-ten.vercel.app/chapter1",
            "https://ai-robotics-textbook-ten.vercel.app/chapter2",
            "https://other-site.com/chapter1",
            "https://ai-robotics-textbook-ten.vercel.app/module1/lesson1"
        ]

        filtered = filter_book_urls(urls, "https://ai-robotics-textbook-ten.vercel.app/")
        self.assertEqual(len(filtered), 3)
        for url in filtered:
            self.assertIn("ai-robotics-textbook-ten.vercel.app", url)

    @patch('src.embeddings_pipeline.url_extractor.requests.get')
    def test_validate_url_accessibility_success(self, mock_get):
        """Test URL accessibility validation with successful response."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = validate_url_accessibility("https://example.com")
        self.assertTrue(result['accessible'])
        self.assertEqual(result['status_code'], 200)

    @patch('src.embeddings_pipeline.url_extractor.requests.get')
    def test_validate_url_accessibility_failure(self, mock_get):
        """Test URL accessibility validation with failed response."""
        mock_get.side_effect = Exception("Connection failed")

        result = validate_url_accessibility("https://example.com")
        self.assertFalse(result['accessible'])
        self.assertIsNotNone(result['error'])

    def test_validate_book_content_entity(self):
        """Test BookContent entity validation."""
        valid_content = {
            'url': 'https://example.com',
            'content': 'Sample content',
            'title': 'Sample Title',
            'module': 'Module 1',
            'chapter': 'Chapter 1'
        }
        self.assertTrue(validate_book_content_entity(valid_content))

        invalid_content = {
            'url': 'https://example.com',
            # Missing content
        }
        self.assertFalse(validate_book_content_entity(invalid_content))

        invalid_url = {
            'url': 'not_a_valid_url',
            'content': 'Sample content'
        }
        self.assertFalse(validate_book_content_entity(invalid_url))


if __name__ == '__main__':
    unittest.main()