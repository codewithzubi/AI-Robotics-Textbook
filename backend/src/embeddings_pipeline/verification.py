"""
Verification module for testing vector insertion and retrieval.
"""
from typing import List, Dict, Any
import random
from src.embeddings_pipeline.qdrant_handler import search_in_qdrant, initialize_qdrant_client
from src.embeddings_pipeline.embedding_generator import embed_single_text
from src.config import settings


def verify_vector_insertion_and_retrieval(
    sample_texts: List[str],
    collection_name: str = None
) -> Dict[str, Any]:
    """
    Verify that vectors are properly inserted and can be retrieved from Qdrant.

    Args:
        sample_texts: List of sample texts to test insertion and retrieval
        collection_name: Name of the collection to test (default from settings)

    Returns:
        Dictionary with verification results
    """
    if collection_name is None:
        collection_name = settings.QDRANT_COLLECTION_NAME

    client = initialize_qdrant_client()
    if not client:
        return {
            'success': False,
            'error': 'Could not connect to Qdrant',
            'tests_run': 0,
            'tests_passed': 0
        }

    try:
        # Generate embeddings for sample texts
        verification_results = []
        for i, text in enumerate(sample_texts):
            # Generate embedding for the text
            embedding_vector = embed_single_text(text)
            if not embedding_vector:
                verification_results.append({
                    'text_index': i,
                    'text_preview': text[:50],
                    'embedding_success': False,
                    'retrieval_success': False,
                    'error': 'Could not generate embedding'
                })
                continue

            # Try to retrieve similar items using the same text as query
            search_results = search_in_qdrant(
                query_embedding=embedding_vector,
                collection_name=collection_name,
                limit=5
            )

            # Check if the original text or similar text is in the results
            found_in_results = False
            for result in search_results:
                if text[:20] in result.get('content', '') or \
                   result.get('content', '')[:20] in text:
                    found_in_results = True
                    break

            verification_results.append({
                'text_index': i,
                'text_preview': text[:50],
                'embedding_success': embedding_vector is not None,
                'retrieval_success': found_in_results,
                'retrieved_count': len(search_results),
                'top_score': search_results[0]['score'] if search_results else 0
            })

        # Calculate overall results
        total_tests = len(verification_results)
        passed_tests = sum(1 for r in verification_results if r['retrieval_success'])

        return {
            'success': True,
            'tests_run': total_tests,
            'tests_passed': passed_tests,
            'success_rate': passed_tests / total_tests if total_tests > 0 else 0,
            'results': verification_results
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'tests_run': 0,
            'tests_passed': 0
        }


def run_sample_verification() -> Dict[str, Any]:
    """
    Run a sample verification test with predefined texts.

    Returns:
        Dictionary with verification results
    """
    # Sample texts for testing
    sample_texts = [
        "Introduction to Artificial Intelligence and Robotics",
        "ROS 2 framework for robotic applications",
        "Sensor fusion techniques in autonomous systems",
        "Machine learning algorithms for robot perception",
        "Path planning and navigation in dynamic environments",
        "Human-robot interaction principles",
        "Computer vision for robotic applications",
        "Reinforcement learning in robotic control",
        "Multi-robot coordination and communication",
        "Ethics in AI and robotics"
    ]

    print("Running sample verification test...")
    print(f"Testing with {len(sample_texts)} sample texts")

    results = verify_vector_insertion_and_retrieval(sample_texts)

    if results['success']:
        print(f"✓ Verification completed: {results['tests_passed']}/{results['tests_run']} tests passed")
        print(f"Success rate: {results['success_rate']:.2%}")
    else:
        print(f"✗ Verification failed: {results.get('error', 'Unknown error')}")

    return results


def create_sample_lookup_test() -> Dict[str, Any]:
    """
    Create and run a comprehensive sample lookup verification.

    Returns:
        Dictionary with comprehensive test results
    """
    # Create diverse sample texts that might be in the textbook
    sample_texts = [
        "What is the definition of a robot in modern robotics?",
        "Explain the architecture of ROS 2 and its key components.",
        "How does sensor fusion improve robotic perception?",
        "Describe the differences between forward and inverse kinematics.",
        "What are the main challenges in SLAM for mobile robots?",
        "How does deep learning enhance computer vision in robotics?",
        "Explain the concept of path planning in autonomous navigation.",
        "What are the safety considerations in human-robot collaboration?",
        "Describe the working principles of LIDAR sensors in robotics.",
        "How does reinforcement learning apply to robotic control systems?"
    ]

    print("Creating comprehensive sample lookup verification...")
    print(f"Testing retrieval with {len(sample_texts)} diverse queries")

    results = verify_vector_insertion_and_retrieval(sample_texts)

    if results['success']:
        successful_retrievals = [r for r in results['results'] if r['retrieval_success']]
        print(f"✓ {len(successful_retrievals)}/{len(sample_texts)} queries successfully retrieved relevant content")
        print(f"Average success rate: {results['success_rate']:.2%}")

        # Show some sample results
        print("\nSample results:")
        for i, result in enumerate(results['results'][:3]):  # Show first 3 results
            status = "✓" if result['retrieval_success'] else "✗"
            print(f"  {status} Query {result['text_index']}: '{result['text_preview']}...' - "
                  f"Retrieved: {result['retrieved_count']}, Top Score: {result['top_score']:.3f}")
    else:
        print(f"✗ Sample lookup verification failed: {results.get('error', 'Unknown error')}")

    return results


if __name__ == "__main__":
    # Run the sample verification
    run_sample_verification()
    print("\n" + "="*50 + "\n")
    create_sample_lookup_test()