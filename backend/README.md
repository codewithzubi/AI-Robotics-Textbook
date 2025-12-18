# AI Robotics Textbook Embeddings Pipeline

This project implements an embeddings pipeline that extracts content from the AI Robotics textbook URLs, processes it through Cohere embeddings API, and stores the vectors in Qdrant vector database.

## Overview

The embeddings pipeline performs the following steps:
1. Fetches all book content URLs from the sitemap
2. Extracts text content from each URL
3. Chunks the text into semantically meaningful segments
4. Generates embeddings using Cohere API
5. Stores embeddings in Qdrant vector database with metadata

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file based on `.env.example` and add your API keys:
   ```bash
   cp .env.example .env
   # Edit .env and add your actual API keys
   ```

## Usage

Run the complete pipeline:
```bash
cd backend
python -m src.embeddings_pipeline.main
```

## Project Structure

```
backend/
├── src/
│   ├── embeddings_pipeline/
│   │   ├── __init__.py
│   │   ├── url_extractor.py      # get_all_urls function
│   │   ├── text_extractor.py     # extract_text_from_url function
│   │   ├── text_chunker.py       # chunk_text function
│   │   ├── embedding_generator.py # embed function
│   │   ├── qdrant_handler.py     # create_collection and save_chunk_to_qdrant functions
│   │   └── main.py               # main function orchestrating the pipeline
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── tests/
├── requirements.txt
├── .env.example
└── README.md
```

## Environment Variables

- `COHERE_API_KEY`: Your Cohere API key
- `QDRANT_URL`: Your Qdrant cluster URL
- `QDRANT_API_KEY`: Your Qdrant API key
- `BOOK_BASE_URL`: Base URL for the textbook (default: https://ai-robotics-textbook-ten.vercel.app/)
- `SITEMAP_URL`: Sitemap URL to discover all content URLs (default: https://ai-robotics-textbook-ten.vercel.app/sitemap.xml)

## API Contract

The pipeline exposes the following endpoints (when run as a service):
- GET `/extract-content` - Extract content from URLs
- POST `/chunk-text` - Split text into chunks
- POST `/embeddings` - Generate embeddings for text chunks
- POST `/qdrant/create-collection` - Create Qdrant collection
- POST `/qdrant/save-embeddings` - Save embeddings to Qdrant
- POST `/pipeline/run` - Execute complete pipeline