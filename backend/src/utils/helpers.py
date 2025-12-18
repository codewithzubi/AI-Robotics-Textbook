"""
Utility functions for the embeddings pipeline.
"""
import time
import logging
from typing import Any, Dict, List
from urllib.parse import urlparse
import hashlib
import re


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Set up logging for the application.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger('embeddings_pipeline')
    logger.setLevel(getattr(logging, log_level.upper()))

    # Avoid adding multiple handlers if logger already has handlers
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def validate_url(url: str) -> bool:
    """
    Validate if a string is a properly formatted URL.

    Args:
        url: URL string to validate

    Returns:
        True if valid URL, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def generate_id(content: str, prefix: str = "") -> str:
    """
    Generate a unique ID based on content.

    Args:
        content: Content to generate ID from
        prefix: Optional prefix for the ID

    Returns:
        Generated ID string
    """
    content_hash = hashlib.md5(content.encode()).hexdigest()[:12]
    if prefix:
        return f"{prefix}_{content_hash}"
    return content_hash


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """
    Decorator to retry a function on failure.

    Args:
        max_retries: Maximum number of retry attempts
        delay: Delay between retries in seconds
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        time.sleep(delay * (2 ** attempt))  # Exponential backoff
                    else:
                        print(f"Function {func.__name__} failed after {max_retries} attempts")
                        raise last_exception
            return None
        return wrapper
    return decorator


def sanitize_text(text: str) -> str:
    """
    Sanitize text by removing or replacing problematic characters.

    Args:
        text: Text to sanitize

    Returns:
        Sanitized text
    """
    if not text:
        return ""

    # Remove null bytes
    text = text.replace('\x00', '')

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)

    # Remove control characters except common ones
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', ' ', text)

    return text.strip()


def format_module_chapter(module_str: str, chapter_str: str) -> tuple:
    """
    Format module and chapter strings to follow consistent naming.

    Args:
        module_str: Raw module string
        chapter_str: Raw chapter string

    Returns:
        Tuple of formatted (module, chapter) strings
    """
    # Format module
    if module_str and not module_str.lower().startswith('module'):
        module_str = f"Module {module_str}"

    # Format chapter
    if chapter_str and not chapter_str.lower().startswith(('chapter', 'lesson', 'topic')):
        chapter_str = f"Chapter {chapter_str}"

    return module_str, chapter_str


def calculate_similarity_score(text1: str, text2: str) -> float:
    """
    Calculate a basic similarity score between two texts.
    This is a simple implementation - for production, consider using more sophisticated methods.

    Args:
        text1: First text string
        text2: Second text string

    Returns:
        Similarity score between 0 and 1
    """
    if not text1 or not text2:
        return 0.0

    # Simple word overlap similarity
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())

    if not words1 and not words2:
        return 1.0
    if not words1 or not words2:
        return 0.0

    intersection = words1.intersection(words2)
    union = words1.union(words2)

    return len(intersection) / len(union)


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split a list into chunks of specified size.

    Args:
        lst: List to chunk
        chunk_size: Size of each chunk

    Returns:
        List of chunked sublists
    """
    if chunk_size <= 0:
        raise ValueError("Chunk size must be positive")

    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def time_it(func):
    """
    Decorator to measure execution time of a function.
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper


def validate_embedding_vector(vector: List[float], expected_dimension: int = None) -> bool:
    """
    Validate that an embedding vector is properly formatted.

    Args:
        vector: Embedding vector to validate
        expected_dimension: Expected number of dimensions (optional)

    Returns:
        True if valid, False otherwise
    """
    if not vector:
        return False

    if expected_dimension and len(vector) != expected_dimension:
        return False

    # Check for NaN or infinite values
    import math
    for value in vector:
        if math.isnan(value) or math.isinf(value):
            return False

    return True


def normalize_text_for_embedding(text: str) -> str:
    """
    Normalize text to prepare for embedding generation.

    Args:
        text: Text to normalize

    Returns:
        Normalized text
    """
    if not text:
        return ""

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)

    # Remove special characters that might interfere with embedding
    # Keep letters, numbers, basic punctuation, and spaces
    text = re.sub(r'[^\w\s\.\!\?,:;\'\"-]', ' ', text)

    # Normalize whitespace again after cleaning
    text = re.sub(r'\s+', ' ', text).strip()

    return text


if __name__ == "__main__":
    # Example usage of utility functions
    logger = setup_logging()
    logger.info("Testing utility functions...")

    # Test URL validation
    print(f"Valid URL 'https://example.com': {validate_url('https://example.com')}")
    print(f"Invalid URL 'not_a_url': {validate_url('not_a_url')}")

    # Test ID generation
    test_id = generate_id("sample content for id generation")
    print(f"Generated ID: {test_id}")

    # Test text sanitization
    dirty_text = "This\x00 is\x0B a\x0C test\x7F text with\x00 problems"
    clean_text = sanitize_text(dirty_text)
    print(f"Sanitized text: '{clean_text}'")

    # Test similarity
    similarity = calculate_similarity_score("this is a test", "this is another test")
    print(f"Similarity score: {similarity:.2f}")

    # Test list chunking
    test_list = list(range(10))
    chunks = chunk_list(test_list, 3)
    print(f"Chunked list: {chunks}")