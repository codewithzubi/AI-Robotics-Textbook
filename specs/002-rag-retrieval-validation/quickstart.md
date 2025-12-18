# Quickstart: RAG Retrieval Validation

## Overview

This guide provides a quick start for implementing and using the RAG retrieval validation system. The system validates that stored embeddings in Qdrant can be properly retrieved based on semantic similarity queries.

## Prerequisites

- Python 3.11 or higher
- pip package manager
- Git for version control
- Cohere API key
- Qdrant Cloud account and API key
- Access to the AI Robotics textbook content (already embedded)

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd AI-Book
```

### 2. Create Virtual Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the `backend` directory:

```bash
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
EMBEDDING_MODEL=embed-multilingual-v3.0
COLLECTION_NAME=robotics_textbook_chunks
```

## Basic Usage

### 1. Run Validation Tests

Execute the validation pipeline with a simple test query:

```bash
cd src
python -m rag_validation.main --query "What is robot kinematics?" --top-k 5
```

### 2. Run Unit Tests

Validate individual components:

```bash
cd backend
python -m pytest tests/validation/unit/ -v
```

### 3. Run Integration Tests

Test the complete validation pipeline:

```bash
cd backend
python -m pytest tests/validation/integration/ -v
```

## Validation Pipeline Components

### Query Processor

The query processor handles natural language queries and generates embeddings:

```python
from rag_validation.query_processor import QueryProcessor

processor = QueryProcessor()
query_obj = processor.process_query("What is inverse kinematics?")
```

### Vector Search

The vector search component performs semantic similarity searches in Qdrant:

```python
from rag_validation.vector_search import VectorSearch

search = VectorSearch()
results = search.search(query_obj.embedding, top_k=10)
```

### Content Validator

The content validator validates retrieved results against original content:

```python
from rag_validation.content_validator import ContentValidator

validator = ContentValidator()
validation_result = validator.validate_retrieved_content(
    query="What is inverse kinematics?",
    retrieved_content=results[0].content,
    original_content=original_content
)
```

### Metrics Calculator

The metrics calculator computes retrieval quality metrics:

```python
from rag_validation.metrics_calculator import MetricsCalculator

calculator = MetricsCalculator()
metrics = calculator.calculate_retrieval_metrics(
    query_id=query_obj.query_id,
    results=results,
    validations=[validation_result]
)
```

## Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `COHERE_API_KEY` | Cohere API key for embeddings | Required |
| `QDRANT_URL` | Qdrant instance URL | Required |
| `QDRANT_API_KEY` | Qdrant API key | Required |
| `EMBEDDING_MODEL` | Cohere model for embeddings | embed-multilingual-v3.0 |
| `COLLECTION_NAME` | Qdrant collection name | robotics_textbook_chunks |
| `TOP_K` | Number of results to retrieve | 10 |
| `SIMILARITY_THRESHOLD` | Minimum similarity threshold | 0.7 |

### Command Line Options

The main validation script accepts the following options:

```bash
python -m rag_validation.main --help
```

- `--query`: Query text to validate
- `--top-k`: Number of results to retrieve (default: 10)
- `--similarity-threshold`: Minimum similarity threshold (default: 0.7)
- `--collection-name`: Qdrant collection name (default: robotics_textbook_chunks)
- `--output-format`: Output format (json, text, csv) (default: json)

## Running Validation Tests

### Single Query Validation

```bash
python -m rag_validation.main --query "Explain PID controllers in robotics" --top-k 5
```

### Batch Validation

Create a file with multiple queries:

```bash
# queries.txt
What is forward kinematics?
Explain inverse kinematics
What are Jacobian matrices?
```

Run batch validation:

```bash
python -m rag_validation.main --batch-file queries.txt --output results.json
```

### Performance Testing

Test retrieval performance:

```bash
python -m rag_validation.main --query "What is robot dynamics?" --performance-test
```

## Output Format

The validation system outputs results in JSON format:

```json
{
  "query_id": "unique-query-id",
  "query_text": "What is robot kinematics?",
  "retrieved_results": [
    {
      "vector_id": "vector-id",
      "content": "Retrieved content text...",
      "similarity_score": 0.85,
      "validation_result": {
        "is_valid": true,
        "semantic_similarity": 0.92,
        "content_accuracy": 0.88
      }
    }
  ],
  "metrics": {
    "retrieval_accuracy": 0.95,
    "mean_similarity_score": 0.82,
    "response_time_ms": 450,
    "failure_count": 0,
    "mrr_score": 0.89
  },
  "timestamp": "2025-12-15T10:30:00Z"
}
```

## Troubleshooting

### Common Issues

1. **API Rate Limiting**: If you encounter rate limiting errors, reduce the query frequency or upgrade your API plan.

2. **Qdrant Connection Issues**: Verify that your QDRANT_URL and QDRANT_API_KEY are correct and that the Qdrant instance is accessible.

3. **Invalid Embeddings**: Ensure that the EMBEDDING_MODEL matches the model used for the stored embeddings.

### Debugging

Enable debug logging:

```bash
export LOG_LEVEL=DEBUG
python -m rag_validation.main --query "test query"
```

## Next Steps

1. Integrate the validation system with your RAG application
2. Set up automated validation tests for continuous monitoring
3. Configure alerts for when retrieval quality falls below acceptable thresholds
4. Implement custom validation rules based on your specific requirements