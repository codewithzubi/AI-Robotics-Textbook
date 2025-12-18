#!/usr/bin/env python3
"""
Script to check and fix Qdrant Cloud Free Tier setup issues
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from src.embeddings_pipeline.qdrant_handler import (
    initialize_qdrant_client,
    create_collection,
    verify_embedding_storage
)
from src.config.settings import settings

def check_qdrant_connection():
    """Check if Qdrant connection is working"""
    print("🔍 Checking Qdrant connection...")

    # Check if required environment variables are set
    if not settings.QDRANT_URL:
        print("❌ Error: QDRANT_URL is not set in environment variables")
        return False

    if not settings.QDRANT_API_KEY:
        print("❌ Error: QDRANT_API_KEY is not set in environment variables")
        return False

    print(f"✅ QDRANT_URL: {settings.QDRANT_URL}")
    print(f"✅ QDRANT_COLLECTION_NAME: {settings.QDRANT_COLLECTION_NAME}")

    # Try to initialize client
    client = initialize_qdrant_client()
    if not client:
        print("❌ Failed to connect to Qdrant")
        return False

    print("✅ Successfully connected to Qdrant")
    return client

def check_collection_exists(client):
    """Check if the collection exists"""
    print(f"\n🔍 Checking if collection '{settings.QDRANT_COLLECTION_NAME}' exists...")

    try:
        collections = client.get_collections()
        collection_names = [col.name for col in collections.collections]

        if settings.QDRANT_COLLECTION_NAME in collection_names:
            print(f"✅ Collection '{settings.QDRANT_COLLECTION_NAME}' exists")

            # Get collection info
            collection_info = client.get_collection(settings.QDRANT_COLLECTION_NAME)
            print(f"   - Points count: {collection_info.points_count}")
            print(f"   - Vector size: {collection_info.config.params.vectors.size}")
            print(f"   - Distance: {collection_info.config.params.vectors.distance}")

            return True
        else:
            print(f"❌ Collection '{settings.QDRANT_COLLECTION_NAME}' does not exist")
            return False
    except Exception as e:
        print(f"❌ Error checking collection: {e}")
        return False

def create_missing_collection(client):
    """Create the collection if it doesn't exist"""
    print(f"\n🔧 Creating collection '{settings.QDRANT_COLLECTION_NAME}'...")

    success = create_collection(
        collection_name=settings.QDRANT_COLLECTION_NAME,
        vector_size=1024,  # Standard size for Cohere embeddings
        distance="Cosine",
        recreate=False
    )

    if success:
        print(f"✅ Collection '{settings.QDRANT_COLLECTION_NAME}' created successfully")
        return True
    else:
        print(f"❌ Failed to create collection '{settings.QDRANT_COLLECTION_NAME}'")
        return False

def verify_embeddings_storage():
    """Verify that embeddings are stored correctly"""
    print(f"\n🔍 Verifying embeddings storage in '{settings.QDRANT_COLLECTION_NAME}'...")

    verification_result = verify_embedding_storage(
        collection_name=settings.QDRANT_COLLECTION_NAME,
        sample_size=5
    )

    if verification_result['success']:
        print(f"✅ Embedding storage verification successful")
        print(f"   - Total points in collection: {verification_result['total_count']}")
        print(f"   - Sample records checked: {verification_result['sample_size']}")

        if verification_result['sample_records']:
            print("   - Sample record structure:")
            for i, record in enumerate(verification_result['sample_records']):
                print(f"     Record {i+1}: ID={record['id']}, Vector Length={record['vector_length']}, Payload Keys={record['payload_keys']}")

        return verification_result['total_count'] > 0
    else:
        print(f"❌ Embedding storage verification failed: {verification_result.get('error', 'Unknown error')}")
        return False

def main():
    print("🚀 Qdrant Cloud Free Tier Setup Checker")
    print("=" * 50)

    # Check Qdrant connection
    client = check_qdrant_connection()
    if not client:
        print("\n❌ Cannot proceed without Qdrant connection")
        return False

    # Check if collection exists
    collection_exists = check_collection_exists(client)

    # If collection doesn't exist, create it
    if not collection_exists:
        success = create_missing_collection(client)
        if not success:
            print("\n❌ Cannot proceed without a collection")
            return False
    else:
        print(f"\n✅ Collection '{settings.QDRANT_COLLECTION_NAME}' is ready")

    # Verify embeddings storage
    has_embeddings = verify_embeddings_storage()

    print("\n" + "=" * 50)
    print("📋 SUMMARY:")

    if collection_exists or create_missing_collection(client):
        print("✅ Collection is available")
    else:
        print("❌ Collection issue detected")

    if has_embeddings:
        print("✅ Embeddings are stored correctly")
    else:
        print("❌ No embeddings found or storage issue detected")

    print("\n💡 If embeddings are missing, run the embeddings pipeline to populate the database:")
    print("   python -m src.embeddings_pipeline.main")

    return True

if __name__ == "__main__":
    main()