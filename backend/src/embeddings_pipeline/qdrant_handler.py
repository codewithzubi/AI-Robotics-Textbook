"""
Module for handling Qdrant vector database operations.
"""
from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Optional, Any
from src.config import settings
import time
import logging


def initialize_qdrant_client() -> Optional[QdrantClient]:
    """
    Initialize the Qdrant client with proper configuration.

    Returns:
        Qdrant client instance or None if connection fails
    """
    if not settings.QDRANT_URL:
        print("Error: QDRANT_URL not set in environment variables")
        return None

    try:
        # Determine if we're connecting to a local instance or cloud
        is_local = settings.QDRANT_URL.startswith('http://localhost') or \
                   settings.QDRANT_URL.startswith('localhost') or \
                   settings.QDRANT_URL.startswith('127.0.0.1')

        if settings.QDRANT_API_KEY and not is_local:
            # Cloud instance with API key
            # Parse URL to extract host and port if needed
            from urllib.parse import urlparse
            parsed_url = urlparse(settings.QDRANT_URL)
            if parsed_url.scheme and parsed_url.netloc:
                client = QdrantClient(
                    url=settings.QDRANT_URL,
                    api_key=settings.QDRANT_API_KEY,
                    timeout=30  # Increased timeout for cloud operations
                )
            else:
                # Handle case where URL is just the host
                client = QdrantClient(
                    url=settings.QDRANT_URL,
                    api_key=settings.QDRANT_API_KEY,
                    timeout=30
                )
        elif is_local:
            # Local instance
            client = QdrantClient(
                host=settings.QDRANT_URL.replace('http://', '').split(':')[0] if '://' in settings.QDRANT_URL else settings.QDRANT_URL,
                timeout=30
            )
        else:
            # Cloud instance without API key (shouldn't happen with Qdrant Cloud)
            client = QdrantClient(
                url=settings.QDRANT_URL,
                timeout=30
            )

        # Test the connection
        client.get_collections()
        print("Successfully connected to Qdrant")
        return client
    except Exception as e:
        print(f"Error initializing Qdrant client: {e}")
        return None


def create_collection(
    collection_name: str = None,
    vector_size: int = 1024,  # Default size for Cohere embeddings
    distance: str = "Cosine",
    recreate: bool = False
) -> bool:
    """
    Create a Qdrant collection for storing embeddings with proper configuration for RAG.

    Args:
        collection_name: Name of the collection to create (default from settings)
        vector_size: Size of the embedding vectors
        distance: Distance metric for similarity search
        recreate: Whether to recreate the collection if it already exists

    Returns:
        True if collection was created successfully, False otherwise
    """
    if collection_name is None:
        collection_name = settings.QDRANT_COLLECTION_NAME

    client = initialize_qdrant_client()
    if not client:
        return False

    try:
        # Check if collection already exists
        collections = client.get_collections()
        existing_collections = [col.name for col in collections.collections]

        if collection_name in existing_collections:
            if recreate:
                print(f"Collection '{collection_name}' already exists, recreating...")
                client.delete_collection(collection_name)
            else:
                print(f"Collection '{collection_name}' already exists")
                return True

        # Create the collection with configuration optimized for RAG
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=distance  # Pass distance as string directly, not as models.Distance[distance]
            ),
            # Additional configuration for better performance
            optimizers_config=models.OptimizersConfigDiff(
                memmap_threshold=20000,  # Recommended for better performance
                indexing_threshold=20000  # Recommended for better performance
            )
        )

        print(f"Successfully created collection '{collection_name}' with {vector_size}d vectors using {distance} distance")
        return True
    except Exception as e:
        print(f"Error creating collection '{collection_name}': {e}")
        return False


def save_chunk_to_qdrant(
    chunk: Dict[str, any],
    embedding: List[float],
    collection_name: str = None,
    max_retries: int = 3
) -> bool:
    """
    Save a single chunk and its embedding to Qdrant with error handling and logging.

    Args:
        chunk: Chunk dictionary with content and metadata
        embedding: Embedding vector to store
        collection_name: Name of the collection to store in (default from settings)
        max_retries: Maximum number of retry attempts

    Returns:
        True if successfully saved, False otherwise
    """
    if collection_name is None:
        collection_name = settings.QDRANT_COLLECTION_NAME

    client = initialize_qdrant_client()
    if not client:
        print(f"Failed to connect to Qdrant, cannot save chunk {chunk.get('id', 'unknown')}")
        return False

    # Set up logging
    logger = logging.getLogger('embeddings_pipeline.qdrant_handler')
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    retry_count = 0
    while retry_count < max_retries:
        try:
            # Prepare the record
            record = models.PointStruct(
                id=chunk['id'],  # Use the chunk's ID as the point ID
                vector=embedding,
                payload={
                    'content': chunk.get('content', ''),
                    'source_url': chunk.get('source_url', ''),
                    'module': chunk.get('module', ''),
                    'chapter': chunk.get('chapter', ''),
                    'chunk_index': chunk.get('chunk_index', 0),
                    'created_at': time.strftime('%Y-%m-%d %H:%M:%S')
                }
            )

            # Upsert the record
            client.upsert(
                collection_name=collection_name,
                points=[record]
            )

            logger.info(f"Successfully saved chunk {chunk['id']} to Qdrant collection '{collection_name}'")
            return True

        except Exception as e:
            retry_count += 1
            error_msg = f"Error saving chunk {chunk.get('id', 'unknown')} to Qdrant (attempt {retry_count}): {e}"
            logger.error(error_msg)

            if retry_count < max_retries:
                time.sleep(2 ** retry_count)  # Exponential backoff
            else:
                logger.error(f"Failed to save chunk {chunk.get('id', 'unknown')} to Qdrant after {max_retries} attempts")
                return False


def save_chunks_to_qdrant(
    chunks: List[Dict[str, any]],
    embeddings: List[Dict[str, any]],
    collection_name: str = None
) -> int:
    """
    Save multiple chunks and their embeddings to Qdrant.

    Args:
        chunks: List of chunk dictionaries
        embeddings: List of embedding dictionaries
        collection_name: Name of the collection to store in (default from settings)

    Returns:
        Number of chunks successfully saved
    """
    if collection_name is None:
        collection_name = settings.QDRANT_COLLECTION_NAME

    client = initialize_qdrant_client()
    if not client:
        return 0

    # Create a mapping from chunk_id to chunk data
    chunk_map = {chunk['id']: chunk for chunk in chunks}

    successful_saves = 0

    try:
        # Prepare all records
        records = []
        for emb_data in embeddings:
            chunk_id = emb_data['chunk_id']
            if chunk_id in chunk_map:
                chunk = chunk_map[chunk_id]
                record = models.PointStruct(
                    id=chunk['id'],
                    vector=emb_data['vector'],
                    payload={
                        'content': chunk.get('content', ''),
                        'source_url': chunk.get('source_url', ''),
                        'module': chunk.get('module', ''),
                        'chapter': chunk.get('chapter', ''),
                        'chunk_index': chunk.get('chunk_index', 0),
                        'created_at': emb_data.get('created_at', time.strftime('%Y-%m-%d %H:%M:%S'))
                    }
                )
                records.append(record)

        # Upsert all records in batches (Qdrant performs better with batches)
        batch_size = 64
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            client.upsert(
                collection_name=collection_name,
                points=batch
            )
            successful_saves += len(batch)

        print(f"Successfully saved {successful_saves} chunks to Qdrant collection '{collection_name}'")
        return successful_saves
    except Exception as e:
        print(f"Error saving chunks to Qdrant: {e}")
        return successful_saves


def search_in_qdrant(
    query_embedding: List[float],
    collection_name: str = None,
    limit: int = 5,
    filters: Optional[models.Filter] = None
) -> List[Dict[str, any]]:
    """
    Search for similar content in Qdrant.

    Args:
        query_embedding: Embedding vector to search for similar items
        collection_name: Name of the collection to search in (default from settings)
        limit: Maximum number of results to return
        filters: Optional filters to apply to the search

    Returns:
        List of similar chunks with their content and metadata
    """
    if collection_name is None:
        collection_name = settings.QDRANT_COLLECTION_NAME

    client = initialize_qdrant_client()
    if not client:
        return []

    try:
        # Search for similar vectors
        search_results = client.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=limit,
            query_filter=filters  # Apply filters if provided
        )

        results = []
        for hit in search_results:
            result = {
                'id': hit.id,
                'content': hit.payload.get('content', ''),
                'source_url': hit.payload.get('source_url', ''),
                'module': hit.payload.get('module', ''),
                'chapter': hit.payload.get('chapter', ''),
                'chunk_index': hit.payload.get('chunk_index', 0),
                'score': hit.score,
                'created_at': hit.payload.get('created_at', '')
            }
            results.append(result)

        return results
    except Exception as e:
        print(f"Error searching in Qdrant: {e}")
        return []


def verify_retrieval_accuracy(
    test_queries: List[Dict[str, any]],
    collection_name: str = None
) -> Dict[str, any]:
    """
    Verify retrieval accuracy by testing with known queries.

    Args:
        test_queries: List of test queries with expected results
        collection_name: Name of the collection to test (default from settings)

    Returns:
        Dictionary with retrieval accuracy metrics
    """
    if collection_name is None:
        collection_name = settings.QDRANT_COLLECTION_NAME

    client = initialize_qdrant_client()
    if not client:
        return {'success': False, 'error': 'Could not connect to Qdrant'}

    try:
        correct_retrievals = 0
        total_tests = len(test_queries)

        for query_data in test_queries:
            query_embedding = query_data.get('embedding')
            expected_content = query_data.get('expected_content', '')
            expected_source = query_data.get('expected_source', '')

            if not query_embedding:
                continue

            # Perform search
            results = search_in_qdrant(query_embedding, collection_name, limit=5)

            # Check if expected content is in top results
            found_expected = False
            for result in results:
                if (expected_content and expected_content in result.get('content', '')) or \
                   (expected_source and expected_source in result.get('source_url', '')):
                    found_expected = True
                    break

            if found_expected:
                correct_retrievals += 1

        accuracy = correct_retrievals / total_tests if total_tests > 0 else 0

        return {
            'success': True,
            'total_tests': total_tests,
            'correct_retrievals': correct_retrievals,
            'accuracy': round(accuracy, 3),
            'accuracy_percentage': round(accuracy * 100, 1)
        }

    except Exception as e:
        return {'success': False, 'error': str(e)}


def verify_embedding_storage(
    collection_name: str = None,
    sample_size: int = 5
) -> Dict[str, any]:
    """
    Verify that embeddings have been stored correctly by retrieving sample records.

    Args:
        collection_name: Name of the collection to verify (default from settings)
        sample_size: Number of sample records to retrieve

    Returns:
        Dictionary with verification results
    """
    if collection_name is None:
        collection_name = settings.QDRANT_COLLECTION_NAME

    client = initialize_qdrant_client()
    if not client:
        return {'success': False, 'error': 'Could not connect to Qdrant'}

    try:
        # Get collection info
        collection_info = client.get_collection(collection_name)
        total_count = collection_info.points_count

        # Sample some points
        sample_points = client.scroll(
            collection_name=collection_name,
            limit=sample_size
        )

        sample_records = []
        for point in sample_points[0]:  # scroll returns (points, next_page_offset)
            record = {
                'id': point.id,
                'payload_keys': list(point.payload.keys()) if point.payload else [],
                'vector_length': len(point.vector) if point.vector else 0
            }
            sample_records.append(record)

        return {
            'success': True,
            'total_count': total_count,
            'sample_size': len(sample_records),
            'sample_records': sample_records
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


def delete_collection(collection_name: str = None) -> bool:
    """
    Delete a Qdrant collection (use with caution).

    Args:
        collection_name: Name of the collection to delete (default from settings)

    Returns:
        True if successfully deleted, False otherwise
    """
    if collection_name is None:
        collection_name = settings.QDRANT_COLLECTION_NAME

    client = initialize_qdrant_client()
    if not client:
        return False

    try:
        client.delete_collection(collection_name)
        print(f"Successfully deleted collection '{collection_name}'")
        return True
    except Exception as e:
        print(f"Error deleting collection '{collection_name}': {e}")
        return False


if __name__ == "__main__":
    # Example usage
    print("Testing Qdrant connection and operations...")

    # Test initialization
    client = initialize_qdrant_client()
    if client:
        print("Successfully connected to Qdrant")

        # Test creating a collection
        success = create_collection("test_embeddings", vector_size=1024)
        if success:
            print("Collection created successfully")

            # Test saving a sample record
            sample_chunk = {
                'id': 'test_chunk_1',
                'content': 'This is a test chunk for Qdrant storage',
                'source_url': 'https://example.com/test',
                'module': 'Test Module',
                'chapter': 'Test Chapter',
                'chunk_index': 0
            }
            sample_embedding = [0.1] * 1024  # Sample embedding vector

            save_success = save_chunk_to_qdrant(sample_chunk, sample_embedding, "test_embeddings")
            if save_success:
                print("Sample chunk saved successfully")

                # Verify storage
                verification = verify_embedding_storage("test_embeddings", sample_size=1)
                print(f"Verification result: {verification}")
    else:
        print("Failed to connect to Qdrant")