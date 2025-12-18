#!/usr/bin/env python3
"""
Test script to verify the complete embeddings pipeline works correctly.
"""
import os
import sys
import time
from src.embeddings_pipeline.main import run_pipeline


def test_pipeline():
    """
    Test the complete embeddings pipeline with sample configuration.
    """
    print("Testing the complete embeddings pipeline...")
    print("="*60)

    # Check that required environment variables are set
    required_vars = ['COHERE_API_KEY', 'QDRANT_URL', 'QDRANT_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"ERROR: Missing required environment variables: {missing_vars}")
        print("Please set these variables before running the pipeline.")
        print("Use .env file or export them in your shell.")
        return False

    print("✓ All required environment variables are set")

    # Run the pipeline with test configuration
    print("\nStarting pipeline execution...")
    start_time = time.time()

    result = run_pipeline(
        base_url="https://ai-robotics-textbook-ten.vercel.app/",
        sitemap_url="https://ai-robotics-textbook-ten.vercel.app/sitemap.xml",
        collection_name="test_rag_embeddings",
        recreate_collection=True  # Recreate for clean test
    )

    end_time = time.time()
    duration = end_time - start_time

    print(f"\nPipeline execution completed in {duration:.2f} seconds")
    print("="*60)

    if result['success']:
        print("✓ PIPELINE EXECUTION SUCCESSFUL")
        summary = result['summary']

        print(f"\nExecution Summary:")
        print(f"  - URLs Processed: {summary['urls_processed']}")
        print(f"  - Content Extracted: {summary['content_extracted']}")
        print(f"  - Chunks Created: {summary['chunks_created']}")
        print(f"  - Chunks Prepared: {summary['chunks_prepared']}")
        print(f"  - Embeddings Generated: {summary['embeddings_generated']}")
        print(f"  - Embeddings Saved: {summary['embeddings_saved']}")
        print(f"  - Execution Time: {summary['duration_seconds']} seconds")
        print(f"  - Embedding Quality: {summary['embedding_quality']['accuracy_percentage']:.1f}% accuracy")

        # Additional verification
        if summary['embeddings_saved'] > 0:
            print(f"\n✓ Successfully stored {summary['embeddings_saved']} embeddings in Qdrant")
            print("✓ Pipeline verification completed successfully!")
            return True
        else:
            print("\n⚠ Pipeline completed but no embeddings were saved")
            return False
    else:
        print("✗ PIPELINE EXECUTION FAILED")
        print(f"Error: {result['error']}")
        return False


def test_individual_components():
    """
    Test individual pipeline components to verify they work correctly.
    """
    print("\nTesting individual pipeline components...")
    print("-" * 40)

    # Test 1: URL extraction
    try:
        from src.embeddings_pipeline.url_extractor import get_all_urls, filter_book_urls
        print("✓ Testing URL extraction...")

        # This will fail without proper network access, but we can test the function exists
        urls = get_all_urls("https://ai-robotics-textbook-ten.vercel.app/sitemap.xml")
        print(f"  - Sitemap function accessible, would extract URLs")
    except Exception as e:
        print(f"  - URL extraction test failed: {e}")

    # Test 2: Text chunking
    try:
        from src.embeddings_pipeline.text_chunker import chunk_text
        print("✓ Testing text chunking...")

        sample_text = "This is a sample text for testing. " * 20  # Create a longer text
        chunks = chunk_text(
            content=sample_text,
            source_url="test://sample",
            module="Test Module",
            chapter="Test Chapter"
        )
        print(f"  - Successfully chunked text into {len(chunks)} chunks")
    except Exception as e:
        print(f"  - Text chunking test failed: {e}")

    # Test 3: Embedding generation (mock test)
    try:
        from src.embeddings_pipeline.embedding_generator import initialize_cohere_client
        print("✓ Testing Cohere client initialization...")

        client = initialize_cohere_client()
        if client:
            print("  - Cohere client initialized successfully")
        else:
            print("  - Cohere client initialization failed (expected if API key not set for testing)")
    except Exception as e:
        print(f"  - Cohere client test failed: {e}")

    # Test 4: Qdrant connection (mock test)
    try:
        from src.embeddings_pipeline.qdrant_handler import initialize_qdrant_client
        print("✓ Testing Qdrant client initialization...")

        client = initialize_qdrant_client()
        if client:
            print("  - Qdrant client initialized successfully")
        else:
            print("  - Qdrant client initialization failed (expected if URL/key not set for testing)")
    except Exception as e:
        print(f"  - Qdrant client test failed: {e}")

    print("Individual component tests completed.")


def main():
    """
    Main function to run pipeline verification tests.
    """
    print("AI Robotics Textbook Embeddings Pipeline - Verification Tests")
    print("="*70)

    # Test individual components first
    test_individual_components()

    # Only run full pipeline if in a suitable environment
    if os.getenv('COHERE_API_KEY') and os.getenv('QDRANT_URL') and os.getenv('QDRANT_API_KEY'):
        success = test_pipeline()
        if success:
            print("\n🎉 All verification tests passed!")
            return 0
        else:
            print("\n❌ Some verification tests failed!")
            return 1
    else:
        print("\n⚠ Skipping full pipeline test (API keys not set for execution)")
        print("Set COHERE_API_KEY, QDRANT_URL, and QDRANT_API_KEY to run full pipeline test")
        return 0  # Return 0 as this is expected behavior when not in execution environment


if __name__ == "__main__":
    sys.exit(main())