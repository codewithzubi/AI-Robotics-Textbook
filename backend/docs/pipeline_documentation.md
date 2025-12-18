# AI Robotics Textbook Embeddings Pipeline Documentation

## Overview

The AI Robotics Textbook Embeddings Pipeline is a system designed to extract content from the AI Robotics textbook URLs, generate semantic embeddings using Cohere API, and store them in a Qdrant vector database for efficient retrieval. This system enables semantic search capabilities for the AI Robotics textbook content.

## Architecture

The pipeline consists of the following main components:

1. **URL Extractor**: Fetches all textbook URLs from the sitemap
2. **Text Extractor**: Extracts clean text content from each URL
3. **Text Chunker**: Splits text into semantically meaningful chunks
4. **Embedding Generator**: Creates vector embeddings using Cohere API
5. **Qdrant Handler**: Stores embeddings in Qdrant vector database
6. **Main Pipeline**: Orchestrates the complete workflow

## Components

### URL Extractor (`url_extractor.py`)

The URL extractor module handles discovery and validation of textbook URLs.

#### Key Functions:
- `get_all_urls(sitemap_url)`: Fetches all URLs from the provided sitemap
- `filter_book_urls(urls, base_url)`: Filters URLs to only include those from the textbook domain
- `validate_url_accessibility(url)`: Checks if a URL is accessible with retry logic
- `validate_urls_batch(urls)`: Validates multiple URLs in parallel
- `validate_book_content_entity(content_data)`: Validates BookContent entity according to specifications

### Text Extractor (`text_extractor.py`)

The text extractor module extracts clean text content from URLs.

#### Key Functions:
- `extract_text_from_url(url)`: Extracts text content from a given URL
- `extract_module_chapter_info(url, title)`: Extracts module and chapter information
- `clean_text(text)`: Cleans extracted text by removing unnecessary whitespace

### Text Chunker (`text_chunker.py`)

The text chunker module splits text into appropriately sized chunks for embedding generation.

#### Key Functions:
- `chunk_text(content, ...)`: Splits text into semantically meaningful chunks
- `prepare_chunks_for_cohere(chunks)`: Prepares chunks for Cohere API compatibility
- `validate_chunk_size(chunk)`: Validates chunk size against limits

### Embedding Generator (`embedding_generator.py`)

The embedding generator module creates vector embeddings using Cohere API.

#### Key Functions:
- `initialize_cohere_client()`: Initializes Cohere API client with proper configuration
- `embed(chunks, model)`: Generates embeddings for text chunks
- `validate_embedding_quality(embedding)`: Validates quality of generated embeddings
- `validate_embeddings_batch(embeddings)`: Validates a batch of embeddings

### Qdrant Handler (`qdrant_handler.py`)

The Qdrant handler module manages storage and retrieval of embeddings.

#### Key Functions:
- `initialize_qdrant_client()`: Initializes Qdrant client with proper configuration
- `create_collection(collection_name)`: Creates a Qdrant collection for embeddings
- `save_chunk_to_qdrant(chunk, embedding)`: Saves a chunk and its embedding to Qdrant
- `search_in_qdrant(query_embedding)`: Searches for similar content in Qdrant
- `verify_embedding_storage(collection_name)`: Verifies embeddings are stored correctly

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
BOOK_BASE_URL=https://ai-robotics-textbook-ten.vercel.app/
SITEMAP_URL=https://ai-robotics-textbook-ten.vercel.app/sitemap.xml
COHERE_MODEL=embed-english-v3.0
QDRANT_COLLECTION_NAME=rag_embeddings
CHUNK_SIZE=1000
CHUNK_OVERLAP=100
REQUEST_TIMEOUT=30
```

### Settings

The pipeline uses settings defined in `src/config/settings.py` which can be overridden via environment variables.

## Usage

### Running the Complete Pipeline

```bash
cd backend
python -m src.embeddings_pipeline.main
```

### Command Line Options

The main pipeline supports the following command-line options:

```bash
python -m src.embeddings_pipeline.main --help

# Examples:
python -m src.embeddings_pipeline.main --collection-name my_collection
python -m src.embeddings_pipeline.main --model embed-multilingual-v3.0
python -m src.embeddings_pipeline.main --recreate  # Recreate collection
python -m src.embeddings_pipeline.main --log-level DEBUG
```

### Running Individual Components

You can also run individual components for testing:

```bash
# Test URL extraction
python -c "from src.embeddings_pipeline.url_extractor import get_all_urls; print(get_all_urls())"

# Test text extraction
python -c "from src.embeddings_pipeline.text_extractor import extract_text_from_url; print(extract_text_from_url('https://ai-robotics-textbook-ten.vercel.app/'))"

# Test embedding generation
python -c "from src.embeddings_pipeline.embedding_generator import embed_single_text; print(embed_single_text('Sample text'))"
```

## Data Models

### BookContent
Represents source material from the AI Robotics textbook
- `url`: URL where content is accessible
- `title`: Title of the section/chapter
- `content`: Raw text content
- `module`: Module identifier
- `chapter`: Chapter identifier

### TextChunk
Represents a segment of book content after processing
- `content`: Text content of the chunk
- `source_url`: Origin URL
- `module`: Module identifier
- `chapter`: Chapter identifier
- `chunk_index`: Position in source document

### Embedding
Represents vector embedding of a text chunk
- `vector`: Embedding vector from Cohere API
- `chunk_id`: Reference to original chunk
- `model`: Model used for generation

### QdrantRecord
Represents a record in Qdrant vector database
- `payload`: Contains original content and metadata
- `vector`: Embedding vector
- `id`: Unique identifier

## Error Handling

The pipeline includes comprehensive error handling:

1. **URL Validation**: Validates URLs before processing with retry logic
2. **API Rate Limiting**: Handles Cohere API rate limits with exponential backoff
3. **Connection Resilience**: Reconnects to services when connections fail
4. **Batch Processing**: Processes items in batches to handle failures gracefully
5. **Logging**: Comprehensive logging for debugging and monitoring

## Testing

### Unit Tests

Run unit tests for individual components:

```bash
cd backend
python -m pytest tests/unit/ -v
```

### Integration Tests

Run integration tests for component interactions:

```bash
cd backend
python -m pytest tests/integration/ -v
```

### Verification Tests

Run verification tests to ensure vectors are properly stored and retrievable:

```bash
python -m src.embeddings_pipeline.verification
```

## Performance Considerations

1. **Batch Processing**: The pipeline processes items in batches to optimize API usage
2. **Parallel Processing**: URL validation and other operations are performed in parallel
3. **Memory Management**: Large texts are chunked to avoid memory issues
4. **Rate Limiting**: API calls are rate-limited to respect service limits

## Security

1. **API Keys**: Store API keys in environment variables, never in code
2. **Input Validation**: All inputs are validated before processing
3. **Sanitization**: Text content is sanitized before processing
4. **Access Control**: Use appropriate API keys with minimal required permissions

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure COHERE_API_KEY and QDRANT_API_KEY are set correctly
2. **URL Access Issues**: Check that the textbook URLs are accessible
3. **Rate Limiting**: If encountering rate limit errors, reduce the batch size or add delays
4. **Memory Issues**: For large documents, ensure proper chunking parameters

### Logging

The pipeline logs detailed information that can help with troubleshooting:

- Set `--log-level DEBUG` for detailed logs
- Check for specific error messages in the logs
- Monitor API response times and error rates