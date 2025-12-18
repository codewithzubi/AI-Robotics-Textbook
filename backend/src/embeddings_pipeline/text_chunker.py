"""
Module for chunking text content into semantically meaningful segments.
"""
import re
import uuid
from typing import List, Dict, Optional
from src.config import settings


def chunk_text(
    content: str,
    source_url: str = "",
    module: str = "Unknown Module",
    chapter: str = "Unknown Chapter",
    max_chunk_size: int = None,
    overlap_size: int = None
) -> List[Dict[str, str]]:
    """
    Split text content into smaller, semantically meaningful chunks.

    Args:
        content: The text content to chunk
        source_url: URL where the content originated
        module: Module identifier
        chapter: Chapter identifier
        max_chunk_size: Maximum size of each chunk (default from settings)
        overlap_size: Overlap size between chunks (default from settings)

    Returns:
        List of chunk dictionaries with id, content, and metadata
    """
    if max_chunk_size is None:
        max_chunk_size = settings.CHUNK_SIZE
    if overlap_size is None:
        overlap_size = settings.CHUNK_OVERLAP

    if not content:
        return []

    # Split content into sentences to maintain semantic meaning
    sentences = split_into_sentences(content)

    chunks = []
    current_chunk = ""
    chunk_index = 0

    for sentence in sentences:
        # If adding the sentence would exceed the chunk size
        if len(current_chunk) + len(sentence) > max_chunk_size and current_chunk:
            # Add the current chunk to the list
            chunk_data = {
                'id': str(uuid.uuid4()),
                'content': current_chunk.strip(),
                'source_url': source_url,
                'module': module,
                'chapter': chapter,
                'chunk_index': chunk_index,
                'metadata': {
                    'source_url': source_url,
                    'module': module,
                    'chapter': chapter
                }
            }
            chunks.append(chunk_data)

            # Start a new chunk with overlap
            if overlap_size > 0:
                # Get the end of the current chunk for overlap
                overlap_start = max(0, len(current_chunk) - overlap_size)
                current_chunk = current_chunk[overlap_start:] + sentence
            else:
                current_chunk = sentence

            chunk_index += 1
        else:
            # Add the sentence to the current chunk
            current_chunk += " " + sentence

    # Add the last chunk if it has content
    if current_chunk.strip():
        chunk_data = {
            'id': str(uuid.uuid4()),
            'content': current_chunk.strip(),
            'source_url': source_url,
            'module': module,
            'chapter': chapter,
            'chunk_index': chunk_index,
            'metadata': {
                'source_url': source_url,
                'module': module,
                'chapter': chapter
            }
        }
        chunks.append(chunk_data)

    return chunks


def split_into_sentences(text: str) -> List[str]:
    """
    Split text into sentences while preserving context.

    Args:
        text: Text to split into sentences

    Returns:
        List of sentences
    """
    # Handle common abbreviations to avoid false sentence breaks
    text = re.sub(r'\b([A-Z]\.)+\b', lambda m: m.group().replace('.', '<!DOT!>'), text)
    text = re.sub(r'\b([A-Z][a-z]+\.)(?=\s+[A-Z])', lambda m: m.group().replace('.', '<!DOT!>'), text)

    # Split on sentence endings followed by whitespace and capital letter
    sentences = re.split(r'[.!?]+\s+(?=[A-Z])|[.!?]+(?=\s+[A-Z][a-z])|(?<=[.!?])\s+(?=[A-Z])', text)

    # Restore the dots in abbreviations
    sentences = [s.replace('<!DOT!>', '.') for s in sentences]

    # Clean up sentences
    sentences = [s.strip() for s in sentences if s.strip()]

    return sentences


def chunk_by_paragraphs(
    content: str,
    source_url: str = "",
    module: str = "Unknown Module",
    chapter: str = "Unknown Chapter",
    max_chunk_size: int = None
) -> List[Dict[str, str]]:
    """
    Alternative chunking method that splits by paragraphs first.

    Args:
        content: The text content to chunk
        source_url: URL where the content originated
        module: Module identifier
        chapter: Chapter identifier
        max_chunk_size: Maximum size of each chunk (default from settings)

    Returns:
        List of chunk dictionaries with id, content, and metadata
    """
    if max_chunk_size is None:
        max_chunk_size = settings.CHUNK_SIZE

    # Split by paragraphs first
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]

    chunks = []
    current_chunk = ""
    chunk_index = 0

    for paragraph in paragraphs:
        # If this paragraph alone is too large, split it by sentences
        if len(paragraph) > max_chunk_size:
            sub_chunks = chunk_text(
                paragraph,
                source_url,
                module,
                chapter,
                max_chunk_size,
                overlap_size=0
            )
            for sub_chunk in sub_chunks:
                sub_chunk['chunk_index'] = chunk_index
                import uuid
                sub_chunk['id'] = str(uuid.uuid4())
                chunks.append(sub_chunk)
                chunk_index += 1
            continue

        # If adding the paragraph would exceed the chunk size
        if len(current_chunk) + len(paragraph) > max_chunk_size and current_chunk:
            # Add the current chunk to the list
            chunk_data = {
                'id': str(uuid.uuid4()),
                'content': current_chunk.strip(),
                'source_url': source_url,
                'module': module,
                'chapter': chapter,
                'chunk_index': chunk_index,
                'metadata': {
                    'source_url': source_url,
                    'module': module,
                    'chapter': chapter
                }
            }
            chunks.append(chunk_data)

            current_chunk = paragraph
            chunk_index += 1
        else:
            # Add the paragraph to the current chunk
            if current_chunk:
                current_chunk += "\n\n" + paragraph
            else:
                current_chunk = paragraph

    # Add the last chunk if it has content
    if current_chunk.strip():
        chunk_data = {
            'id': str(uuid.uuid4()),
            'content': current_chunk.strip(),
            'source_url': source_url,
            'module': module,
            'chapter': chapter,
            'chunk_index': chunk_index,
            'metadata': {
                'source_url': source_url,
                'module': module,
                'chapter': chapter
            }
        }
        chunks.append(chunk_data)

    return chunks


def validate_chunk_size(chunk: Dict[str, str], max_size: int = None) -> bool:
    """
    Validate that a chunk is within the expected size limits.

    Args:
        chunk: Chunk dictionary to validate
        max_size: Maximum allowed size (default from settings)

    Returns:
        True if chunk is valid, False otherwise
    """
    if max_size is None:
        max_size = settings.CHUNK_SIZE

    content = chunk.get('content', '')
    return len(content) <= max_size


def prepare_chunks_for_cohere(chunks: List[Dict[str, str]], max_tokens: int = 4000) -> List[Dict[str, str]]:
    """
    Prepare chunks specifically for Cohere API by ensuring they meet token limits.

    Args:
        chunks: List of chunks to prepare
        max_tokens: Maximum tokens allowed per chunk (default is conservative for Cohere)

    Returns:
        List of chunks prepared for Cohere API
    """
    import math

    prepared_chunks = []

    for chunk in chunks:
        content = chunk.get('content', '')

        # Estimate token count (roughly 1 token per 4 characters for English text)
        estimated_tokens = len(content) // 4

        if estimated_tokens > max_tokens:
            # If chunk is too large, split it further
            sub_chunks = split_large_chunk_for_cohere(content, max_tokens)
            for i, sub_chunk in enumerate(sub_chunks):
                new_chunk = chunk.copy()
                new_chunk['content'] = sub_chunk
                new_chunk['id'] = str(uuid.uuid4())
                new_chunk['chunk_index'] = f"{chunk['chunk_index']}.{i}"
                prepared_chunks.append(new_chunk)
        else:
            prepared_chunks.append(chunk)

    return prepared_chunks


def split_large_chunk_for_cohere(content: str, max_tokens: int = 4000) -> List[str]:
    """
    Split a large chunk into smaller pieces suitable for Cohere API.

    Args:
        content: Content to split
        max_tokens: Maximum tokens per split (default is conservative for Cohere)

    Returns:
        List of content strings within token limits
    """
    import math

    # Estimate of characters per token (typically 4 characters per token for English)
    chars_per_token = 4
    max_chars = max_tokens * chars_per_token

    if len(content) <= max_chars:
        return [content]

    # Split by sentences first to maintain semantic meaning
    sentences = split_into_sentences(content)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # If adding this sentence would exceed the limit
        if len(current_chunk) + len(sentence) > max_chars and current_chunk:
            # Add the current chunk to the list
            chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            # Add the sentence to the current chunk
            if current_chunk:
                current_chunk += " " + sentence
            else:
                current_chunk = sentence

    # Add the last chunk if it has content
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    # If any chunk is still too large, split by paragraphs
    final_chunks = []
    for chunk in chunks:
        if len(chunk) > max_chars:
            # Split by paragraphs
            paragraphs = chunk.split('\n\n')
            temp_chunk = ""

            for paragraph in paragraphs:
                if len(temp_chunk) + len(paragraph) > max_chars and temp_chunk:
                    final_chunks.append(temp_chunk.strip())
                    temp_chunk = paragraph
                else:
                    if temp_chunk:
                        temp_chunk += "\n\n" + paragraph
                    else:
                        temp_chunk = paragraph

            if temp_chunk.strip():
                final_chunks.append(temp_chunk.strip())
        else:
            final_chunks.append(chunk)

    return final_chunks


if __name__ == "__main__":
    # Example usage
    sample_text = """
    This is the first sentence of the first paragraph. It contains important information about robotics.
    This is the second sentence in the same paragraph, building on the first sentence.

    This is a new paragraph with different content. It discusses artificial intelligence in robotics.
    The field of AI robotics combines many disciplines including computer science and mechanical engineering.

    Here is the third paragraph. It focuses on practical applications of AI robotics.
    These applications range from manufacturing to healthcare robotics.
    """

    chunks = chunk_text(
        sample_text,
        source_url="https://example.com/sample",
        module="Module 1",
        chapter="Chapter 1"
    )

    print(f"Created {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i}: {len(chunk['content'])} chars - {chunk['content'][:50]}...")