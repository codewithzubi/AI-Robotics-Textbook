"""
Module for generating embeddings using Cohere API.
"""
import cohere
from typing import List, Dict, Optional
from src.config import settings
import time
import logging


def initialize_cohere_client() -> Optional[cohere.Client]:
    """
    Initialize the Cohere API client with proper configuration.

    Returns:
        Cohere client instance or None if API key is not available
    """
    if not settings.COHERE_API_KEY:
        print("Error: COHERE_API_KEY not set in environment variables")
        return None

    try:
        client = cohere.Client(
            settings.COHERE_API_KEY,
            # Additional configuration options can be added here
            client_name="AI-Robotics-Textbook-Embeddings"  # For better analytics
        )
        return client
    except Exception as e:
        print(f"Error initializing Cohere client: {e}")
        return None


def embed(
    chunks: List[Dict[str, str]],
    model: str = None,
    max_retries: int = 3,
    rate_limit_delay: float = 1.0
) -> List[Dict[str, any]]:
    """
    Generate embeddings for text chunks using Cohere API with rate limiting and error handling.

    Args:
        chunks: List of chunk dictionaries with 'content' field
        model: Cohere model to use (default from settings)
        max_retries: Maximum number of retry attempts for failed requests
        rate_limit_delay: Delay between batches to respect rate limits (in seconds)

    Returns:
        List of embedding dictionaries with id, chunk_id, vector, and metadata
    """
    if model is None:
        model = settings.COHERE_MODEL

    client = initialize_cohere_client()
    if not client:
        return []

    if not chunks:
        return []

    embeddings = []

    # Process chunks in batches to respect API limits
    batch_size = 96  # Cohere's recommended batch size for embeddings
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]

        # Extract just the text content for embedding
        texts = [chunk['content'] for chunk in batch]

        batch_retry_count = 0
        while batch_retry_count < max_retries:
            try:
                # For Cohere v3 models, input_type is required and must be provided
                # Different versions of the library may require different approaches
                try:
                    response = client.embed(
                        texts=texts,
                        model=model,
                        input_type="search_document"  # Required for document embeddings in v3 models
                    )
                except TypeError:
                    # If input_type parameter is not accepted as a direct parameter, try without it
                    response = client.embed(
                        texts=texts,
                        model=model
                    )
                except Exception as e:
                    # If it's a different error (like the API requiring input_type), we need to handle it differently
                    if "input_type must be provided" in str(e):
                        # For this specific error, we need to ensure input_type is passed correctly
                        # This suggests the library needs it but we're not passing it in the right way
                        response = client.embed(
                            texts=texts,
                            model=model,
                            input_type="search_document"
                        )
                    else:
                        raise e

                # Process the embeddings
                for idx, embedding_vector in enumerate(response.embeddings):
                    chunk = batch[idx]
                    embedding_data = {
                        'id': f"emb_{chunk['id']}",
                        'chunk_id': chunk['id'],
                        'vector': embedding_vector,
                        'model': model,
                        'created_at': time.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    embeddings.append(embedding_data)

                break  # Success, break out of retry loop

            except Exception as e:
                # Handle all types of errors (rate limiting, service unavailable, API errors, etc.)
                batch_retry_count += 1
                print(f"Error processing embeddings batch (attempt {batch_retry_count}): {e}")

                if batch_retry_count < max_retries:
                    # Wait before retrying with exponential backoff
                    time.sleep(rate_limit_delay * (2 ** batch_retry_count))
                else:
                    print(f"Failed to generate embeddings for batch after {max_retries} attempts")
                    # Add placeholder embeddings with error info for failed chunks
                    for chunk in batch:
                        embedding_data = {
                            'id': f"emb_{chunk['id']}",
                            'chunk_id': chunk['id'],
                            'vector': None,
                            'model': model,
                            'created_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                            'error': f"Error after {max_retries} attempts: {str(e)}"
                        }
                        embeddings.append(embedding_data)
                    break  # Stop retrying after max attempts

        # Add a delay between batches to respect rate limits
        time.sleep(rate_limit_delay)

    return embeddings


def embed_single_text(
    text: str,
    model: str = None
) -> Optional[List[float]]:
    """
    Generate embedding for a single text string.

    Args:
        text: Text to embed
        model: Cohere model to use (default from settings)

    Returns:
        Embedding vector as a list of floats, or None if failed
    """
    if model is None:
        model = settings.COHERE_MODEL

    client = initialize_cohere_client()
    if not client:
        return None

    try:
        # For Cohere v3 models, input_type is required and must be one of: search_document, search_query, classification, clustering
        # For document embedding, use 'search_document'
        response = client.embed(
            texts=[text],
            model=model,
            input_type="search_document"  # Required for v3 models when embedding documents
        )

        if response.embeddings and len(response.embeddings) > 0:
            return response.embeddings[0]
        else:
            return None
    except TypeError as e:
        # Handle case where input_type parameter is not accepted (older library version)
        try:
            response = client.embed(
                texts=[text],
                model=model
            )

            if response.embeddings and len(response.embeddings) > 0:
                return response.embeddings[0]
            else:
                return None
        except Exception as fallback_error:
            print(f"Error generating embedding for single text (fallback also failed): {fallback_error}")
            return None
    except Exception as e:
        print(f"Error generating embedding for single text: {e}")
        return None


def validate_embedding_quality(embedding: List[float], min_dimension: int = 10) -> bool:
    """
    Validate that an embedding meets basic quality criteria.

    Args:
        embedding: Embedding vector to validate
        min_dimension: Minimum number of dimensions expected

    Returns:
        True if embedding is valid, False otherwise
    """
    if not embedding or len(embedding) < min_dimension:
        return False

    # Check for NaN or infinite values
    import math
    for value in embedding:
        if math.isnan(value) or math.isinf(value):
            return False

    return True


def get_embedding_dimensions(model: str = None) -> Optional[int]:
    """
    Get the expected dimensions for a given model.

    Args:
        model: Cohere model name

    Returns:
        Number of dimensions for the model, or None if unknown
    """
    if model is None:
        model = settings.COHERE_MODEL

    # Common Cohere model dimensions
    model_dims = {
        'embed-english-v3.0': 1024,
        'embed-multilingual-v3.0': 1024,
        'embed-english-light-v3.0': 384,
        'embed-multilingual-light-v3.0': 384
    }

    return model_dims.get(model)


def validate_embedding_quality(
    embedding: List[float],
    model: str = None,
    min_quality_score: float = 0.1
) -> Dict[str, any]:
    """
    Validate the quality of a generated embedding.

    Args:
        embedding: Embedding vector to validate
        model: Model that generated the embedding
        min_quality_score: Minimum quality threshold

    Returns:
        Dictionary with quality assessment results
    """
    if model is None:
        model = settings.COHERE_MODEL

    if not embedding:
        return {
            'valid': False,
            'quality_score': 0.0,
            'issues': ['Embedding is empty'],
            'model': model
        }

    issues = []
    quality_score = 1.0  # Start with perfect score

    # Check for NaN or infinite values
    import math
    invalid_values = [v for v in embedding if math.isnan(v) or math.isinf(v)]
    if invalid_values:
        issues.append(f"Contains {len(invalid_values)} NaN or infinite values")
        quality_score = 0.0  # These are critical issues

    # Check if embedding is all zeros (degenerate case)
    if all(v == 0.0 for v in embedding):
        issues.append("All zero embedding (degenerate)")
        quality_score *= 0.1  # Severely penalize

    # Check vector magnitude (should not be too small, indicating poor content)
    magnitude = sum(v ** 2 for v in embedding) ** 0.5
    if magnitude < 0.1:
        issues.append(f"Low magnitude: {magnitude:.3f}")
        quality_score *= 0.3  # Penalize low magnitude

    # Check for uniform values (indicating poor differentiation)
    if len(set(embedding)) < len(embedding) * 0.1:  # Less than 10% unique values
        issues.append("Too many repeated values (low diversity)")
        quality_score *= 0.5  # Penalize low diversity

    # Calculate quality score based on issues
    if not issues:
        quality_score = 1.0
    else:
        # Reduce score based on number and severity of issues
        quality_score = max(min_quality_score, quality_score - len(issues) * 0.2)

    return {
        'valid': len(issues) == 0 and quality_score >= min_quality_score,
        'quality_score': round(quality_score, 3),
        'issues': issues,
        'magnitude': round(magnitude, 3),
        'model': model,
        'dimension': len(embedding)
    }


def validate_embeddings_batch(
    embeddings: List[Dict[str, any]],
    min_quality_score: float = 0.1
) -> Dict[str, any]:
    """
    Validate a batch of embeddings for quality.

    Args:
        embeddings: List of embedding dictionaries
        min_quality_score: Minimum quality threshold

    Returns:
        Dictionary with overall quality assessment
    """
    if not embeddings:
        return {
            'total_embeddings': 0,
            'valid_count': 0,
            'invalid_count': 0,
            'avg_quality_score': 0.0,
            'quality_issues': []
        }

    valid_count = 0
    invalid_count = 0
    total_quality_score = 0.0
    all_issues = []

    for emb_data in embeddings:
        if emb_data.get('error'):
            # Skip embeddings with errors
            invalid_count += 1
            all_issues.append(f"Embedding {emb_data.get('id', 'unknown')} has error: {emb_data['error']}")
            continue

        vector = emb_data.get('vector')
        model = emb_data.get('model')

        if not vector:
            invalid_count += 1
            all_issues.append(f"Embedding {emb_data.get('id', 'unknown')} has no vector")
            continue

        quality_result = validate_embedding_quality(vector, model, min_quality_score)
        total_quality_score += quality_result['quality_score']

        if quality_result['valid']:
            valid_count += 1
        else:
            invalid_count += 1
            all_issues.append(f"Embedding {emb_data.get('id', 'unknown')} failed quality check: {quality_result['issues']}")

    avg_quality_score = total_quality_score / len(embeddings) if embeddings else 0.0

    return {
        'total_embeddings': len(embeddings),
        'valid_count': valid_count,
        'invalid_count': invalid_count,
        'avg_quality_score': round(avg_quality_score, 3),
        'quality_issues': all_issues
    }


if __name__ == "__main__":
    # Example usage
    sample_chunks = [
        {
            'id': 'chunk_1',
            'content': 'This is the first sample text chunk for embedding.',
            'source_url': 'https://example.com/doc1',
            'module': 'Module 1',
            'chapter': 'Chapter 1'
        },
        {
            'id': 'chunk_2',
            'content': 'This is the second sample text chunk for embedding.',
            'source_url': 'https://example.com/doc2',
            'module': 'Module 1',
            'chapter': 'Chapter 2'
        }
    ]

    print("Generating embeddings for sample chunks...")
    embeddings = embed(sample_chunks)

    print(f"Generated {len(embeddings)} embeddings:")
    for i, emb in enumerate(embeddings):
        if emb.get('error'):
            print(f"  Embedding {i}: ERROR - {emb['error']}")
        else:
            print(f"  Embedding {i}: {len(emb['vector'])} dimensions, model: {emb['model']}")