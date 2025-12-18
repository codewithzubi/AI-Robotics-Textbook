"""
Main pipeline orchestrator for the embeddings pipeline.
Executes the complete workflow: URL extraction → Text extraction → Chunking → Embedding → Storage
"""
import sys
import os
import time
import logging
from typing import List, Dict, Any
from src.config import settings
from src.embeddings_pipeline.url_extractor import (
    get_all_urls, filter_book_urls, validate_urls_batch, handle_inaccessible_urls
)
from src.embeddings_pipeline.text_extractor import extract_text_from_url
from src.embeddings_pipeline.text_chunker import chunk_text, prepare_chunks_for_cohere
from src.embeddings_pipeline.embedding_generator import embed, validate_embeddings_batch
from src.embeddings_pipeline.qdrant_handler import (
    create_collection, save_chunks_to_qdrant, verify_embedding_storage
)
from src.utils.helpers import setup_logging


def run_pipeline(
    base_url: str = None,
    sitemap_url: str = None,
    collection_name: str = None,
    model: str = None,
    recreate_collection: bool = False
) -> Dict[str, Any]:
    """
    Execute the complete embeddings pipeline.

    Args:
        base_url: Base URL for the textbook (default from settings)
        sitemap_url: Sitemap URL to discover all content URLs (default from settings)
        collection_name: Qdrant collection name (default from settings)
        model: Cohere model to use (default from settings)
        recreate_collection: Whether to recreate the Qdrant collection

    Returns:
        Dictionary with pipeline execution summary
    """
    if base_url is None:
        base_url = settings.BOOK_BASE_URL
    if sitemap_url is None:
        sitemap_url = settings.SITEMAP_URL
    if collection_name is None:
        collection_name = settings.QDRANT_COLLECTION_NAME
    if model is None:
        model = settings.EMBEDDING_MODEL

    # Set up logging
    logger = setup_logging()
    logger.info("Starting embeddings pipeline execution...")

    start_time = time.time()

    try:
        # Phase 1: URL Extraction and Validation
        logger.info("Phase 1: Extracting and validating URLs...")
        all_urls = get_all_urls(sitemap_url)
        book_urls = filter_book_urls(all_urls, base_url)

        if not book_urls:
            logger.warning(f"No book URLs found from sitemap: {sitemap_url}")
            return {
                'success': False,
                'error': f'No book URLs found from sitemap: {sitemap_url}',
                'summary': {}
            }

        logger.info(f"Found {len(book_urls)} book URLs from sitemap")

        # Validate URLs with batch processing
        validation_results = validate_urls_batch(book_urls[:100])  # Limit for initial validation
        inaccessible = handle_inaccessible_urls(validation_results)
        accessible_urls = [r['url'] for r in validation_results if r.get('valid', False)]

        if not accessible_urls:
            logger.error("No accessible URLs found after validation")
            return {
                'success': False,
                'error': 'No accessible URLs found after validation',
                'summary': {}
            }

        logger.info(f"Successfully validated {len(accessible_urls)} accessible URLs")

        # Phase 2: Text Extraction
        logger.info("Phase 2: Extracting text content from URLs...")
        extracted_contents = []
        for i, url in enumerate(accessible_urls):
            logger.info(f"Processing URL {i+1}/{len(accessible_urls)}: {url}")
            content = extract_text_from_url(url)
            if content:
                extracted_contents.append(content)
            else:
                logger.warning(f"Failed to extract content from {url}")

        if not extracted_contents:
            logger.error("No content extracted from URLs")
            return {
                'success': False,
                'error': 'No content extracted from URLs',
                'summary': {}
            }

        logger.info(f"Successfully extracted content from {len(extracted_contents)} URLs")

        # Phase 3: Text Chunking
        logger.info("Phase 3: Chunking text content...")
        all_chunks = []
        for content in extracted_contents:
            chunks = chunk_text(
                content=content['content'],
                source_url=content['url'],
                module=content.get('module', 'Unknown Module'),
                chapter=content.get('chapter', 'Unknown Chapter')
            )
            all_chunks.extend(chunks)

        logger.info(f"Created {len(all_chunks)} text chunks")

        # Prepare chunks for Cohere API
        logger.info("Preparing chunks for Cohere API...")
        prepared_chunks = prepare_chunks_for_cohere(all_chunks)
        logger.info(f"Prepared {len(prepared_chunks)} chunks for embedding")

        # Phase 4: Embedding Generation
        logger.info("Phase 4: Generating embeddings...")
        embeddings = embed(prepared_chunks, model=model)
        logger.info(f"Generated {len(embeddings)} embeddings")

        # Validate embeddings quality
        quality_report = validate_embeddings_batch(embeddings)
        logger.info(f"Embedding quality report: {quality_report}")

        if quality_report['invalid_count'] > 0:
            logger.warning(f"Found {quality_report['invalid_count']} invalid embeddings out of {quality_report['total_embeddings']}")

        # Phase 5: Qdrant Storage
        logger.info("Phase 5: Storing embeddings in Qdrant...")

        # Create Qdrant collection
        collection_success = create_collection(
            collection_name=collection_name,
            recreate=recreate_collection
        )

        if not collection_success:
            logger.error("Failed to create Qdrant collection")
            return {
                'success': False,
                'error': 'Failed to create Qdrant collection',
                'summary': {}
            }

        # Save embeddings to Qdrant
        saved_count = save_chunks_to_qdrant(prepared_chunks, embeddings, collection_name)
        logger.info(f"Successfully saved {saved_count} embeddings to Qdrant")

        # Verify storage
        verification = verify_embedding_storage(collection_name)
        logger.info(f"Storage verification: {verification}")

        # Calculate execution time
        end_time = time.time()
        duration = end_time - start_time

        # Prepare summary
        summary = {
            'urls_processed': len(accessible_urls),
            'content_extracted': len(extracted_contents),
            'chunks_created': len(all_chunks),
            'chunks_prepared': len(prepared_chunks),
            'embeddings_generated': len(embeddings),
            'embeddings_saved': saved_count,
            'start_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)),
            'end_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time)),
            'duration_seconds': round(duration, 2),
            'embedding_quality': quality_report
        }

        logger.info("Pipeline execution completed successfully!")
        return {
            'success': True,
            'summary': summary
        }

    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        end_time = time.time()
        return {
            'success': False,
            'error': str(e),
            'summary': {
                'start_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)),
                'end_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time)),
                'duration_seconds': round(end_time - start_time, 2)
            }
        }


def main():
    """Main entry point for the embeddings pipeline."""
    import argparse

    parser = argparse.ArgumentParser(description='AI Robotics Textbook Embeddings Pipeline')
    parser.add_argument('--base-url', default=None, help='Base URL for the textbook')
    parser.add_argument('--sitemap-url', default=None, help='Sitemap URL to discover content')
    parser.add_argument('--collection-name', default=None, help='Qdrant collection name')
    parser.add_argument('--model', default=None, help='Cohere model to use')
    parser.add_argument('--recreate', action='store_true', help='Recreate Qdrant collection')
    parser.add_argument('--log-level', default='INFO', help='Logging level')

    args = parser.parse_args()

    # Set up logging with specified level
    logger = setup_logging(args.log_level)

    logger.info("Starting AI Robotics Textbook Embeddings Pipeline...")
    logger.info(f"Base URL: {args.base_url or settings.BOOK_BASE_URL}")
    logger.info(f"Sitemap URL: {args.sitemap_url or settings.SITEMAP_URL}")
    logger.info(f"Collection: {args.collection_name or settings.QDRANT_COLLECTION_NAME}")
    logger.info(f"Model: {args.model or settings.EMBEDDING_MODEL}")

    result = run_pipeline(
        base_url=args.base_url,
        sitemap_url=args.sitemap_url,
        collection_name=args.collection_name,
        model=args.model,
        recreate_collection=args.recreate
    )

    if result['success']:
        logger.info("Pipeline completed successfully!")
        summary = result['summary']
        print(f"\nPipeline Summary:")
        print(f"  URLs Processed: {summary['urls_processed']}")
        print(f"  Content Extracted: {summary['content_extracted']}")
        print(f"  Chunks Created: {summary['chunks_created']}")
        print(f"  Chunks Prepared: {summary['chunks_prepared']}")
        print(f"  Embeddings Generated: {summary['embeddings_generated']}")
        print(f"  Embeddings Saved: {summary['embeddings_saved']}")
        print(f"  Duration: {summary['duration_seconds']} seconds")
        print(f"  Embedding Quality: {summary['embedding_quality']['accuracy_percentage']:.1f}% accuracy")
    else:
        logger.error(f"Pipeline failed: {result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()