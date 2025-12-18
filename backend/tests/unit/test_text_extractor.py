"""
Unit tests for the text extractor module.
"""
import unittest
from unittest.mock import patch, MagicMock
from src.embeddings_pipeline.text_extractor import (
    extract_text_from_url, extract_module_chapter_info, clean_text
)


class TestTextExtractor(unittest.TestCase):
    """Test cases for text extractor functions."""

    @patch('src.embeddings_pipeline.text_extractor.requests.get')
    @patch('src.embeddings_pipeline.text_extractor.BeautifulSoup')
    def test_extract_text_from_url_success(self, mock_bs, mock_get):
        """Test successful text extraction from a URL."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.content = b"<html><head><title>Test Title</title></head><body><p>Test content</p></body></html>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Mock BeautifulSoup
        mock_bs_instance = MagicMock()
        mock_title = MagicMock()
        mock_title.get_text.return_value = "Test Title"
        mock_bs_instance.find.return_value = mock_title
        mock_bs_instance.get_text.return_value = "Test Title Test content"
        mock_bs.return_value = mock_bs_instance

        result = extract_text_from_url("https://example.com")
        self.assertIsNotNone(result)
        self.assertEqual(result['title'], "Test Title")
        self.assertIn("Test content", result['content'])

    @patch('src.embeddings_pipeline.text_extractor.requests.get')
    def test_extract_text_from_url_failure(self, mock_get):
        """Test text extraction failure handling."""
        mock_get.side_effect = Exception("Connection failed")

        result = extract_text_from_url("https://example.com")
        self.assertIsNone(result)

    def test_extract_module_chapter_info_from_url(self):
        """Test extracting module and chapter info from URL."""
        url = "https://example.com/module2/chapter3/content"
        module, chapter = extract_module_chapter_info(url, "Irrelevant Title")
        self.assertEqual(module, "Module 2")
        self.assertEqual(chapter, "Chapter 3")

    def test_extract_module_chapter_info_from_title(self):
        """Test extracting module and chapter info from title."""
        url = "https://example.com/page"
        title = "Module 3: Introduction to Robotics - Chapter 5: Sensors"
        module, chapter = extract_module_chapter_info(url, title)
        self.assertEqual(module, "Module 3")
        self.assertEqual(chapter, "Chapter Chapter")

    def test_clean_text(self):
        """Test text cleaning functionality."""
        dirty_text = "  This   is  \n\n  a   test\t\ttext  "
        clean = clean_text(dirty_text)
        self.assertEqual(clean, "This is a test text")

        # Test with None input
        self.assertEqual(clean_text(None), "")
        self.assertEqual(clean_text(""), "")


if __name__ == '__main__':
    unittest.main()