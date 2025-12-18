"""
Module for extracting text content from URLs.
"""
import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
import re
from src.config import settings


def extract_text_from_url(url: str) -> Optional[Dict[str, str]]:
    """
    Extract text content from a given URL.

    Args:
        url: The URL to extract content from.

    Returns:
        Dictionary containing 'title', 'content', 'module', 'chapter' if successful, None otherwise.
    """
    try:
        response = requests.get(url, timeout=settings.REQUEST_TIMEOUT)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract title
        title = soup.find('title')
        title = title.get_text().strip() if title else "Untitled"

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Extract main content - look for main content areas
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'content|main|article')) or soup

        # Get text content
        text_content = main_content.get_text(separator=' ')

        # Clean up text: remove extra whitespace
        text_content = re.sub(r'\s+', ' ', text_content).strip()

        # Try to extract module and chapter information from the URL or content
        module, chapter = extract_module_chapter_info(url, title)

        return {
            'url': url,
            'title': title,
            'content': text_content,
            'module': module,
            'chapter': chapter
        }
    except requests.RequestException as e:
        print(f"Error fetching content from {url}: {e}")
        return None
    except Exception as e:
        print(f"Error extracting text from {url}: {e}")
        return None


def extract_module_chapter_info(url: str, title: str) -> tuple:
    """
    Extract module and chapter information from URL or title.

    Args:
        url: The URL of the page
        title: The title of the page

    Returns:
        Tuple of (module, chapter) strings
    """
    # Extract from URL path
    url_parts = url.lower().split('/')

    # Look for module and chapter patterns in the URL
    module = "Unknown Module"
    chapter = "Unknown Chapter"

    for i, part in enumerate(url_parts):
        if 'module' in part and i + 1 < len(url_parts):
            # Look for the next part which might be the module name or number
            next_part = url_parts[i + 1]
            if next_part.isdigit():
                module = f"Module {next_part}"
            elif next_part:
                module = f"Module {next_part.capitalize()}"

        if any(keyword in part for keyword in ['chapter', 'lesson', 'topic']):
            next_part = url_parts[i + 1] if i + 1 < len(url_parts) else ""
            if next_part:
                chapter = f"Chapter {next_part.capitalize()}"

    # If we couldn't extract from URL, try to extract from title
    if module == "Unknown Module" or chapter == "Unknown Chapter":
        title_lower = title.lower()

        # Look for module pattern in title
        module_match = re.search(r'module\s+(\d+|[a-zA-Z]+)', title_lower)
        if module_match:
            module_num = module_match.group(1)
            module = f"Module {module_num.capitalize()}"

        # Look for chapter/lesson pattern in title
        chapter_patterns = [
            r'chapter\s+(\d+|[a-zA-Z]+)',
            r'lesson\s+(\d+|[a-zA-Z]+)',
            r'topic\s+(\d+|[a-zA-Z]+)'
        ]

        for pattern in chapter_patterns:
            chapter_match = re.search(pattern, title_lower)
            if chapter_match:
                chapter_val = chapter_match.group(1)
                chapter = f"Chapter {chapter_val.capitalize()}"
                break

    return module, chapter


def clean_text(text: str) -> str:
    """
    Clean extracted text by removing unnecessary whitespace and special characters.

    Args:
        text: Raw extracted text

    Returns:
        Cleaned text
    """
    if not text:
        return ""

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)

    # Remove leading/trailing whitespace
    text = text.strip()

    # Replace common special characters that might interfere with processing
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

    return text


if __name__ == "__main__":
    # Example usage
    sample_url = "https://ai-robotics-textbook-ten.vercel.app/"
    result = extract_text_from_url(sample_url)

    if result:
        print(f"Title: {result['title']}")
        print(f"Module: {result['module']}")
        print(f"Chapter: {result['chapter']}")
        print(f"Content preview: {result['content'][:200]}...")
    else:
        print("Failed to extract content")