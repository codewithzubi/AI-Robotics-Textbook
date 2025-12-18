# Quickstart: Deploy Website URLs, Generate Embeddings, and Store in Vector Database

## Overview
This guide will help you set up and run the embeddings pipeline that extracts content from book URLs, processes it through Cohere embeddings API, and stores the vectors in Qdrant vector database.

## Prerequisites
- Python 3.11+
- pip package manager
- Cohere API key
- Qdrant Cloud account and API key
- Access to the book URLs (https://ai-robotics-textbook-ten.vercel.app/)

## Setup

### 1. Clone the Repository
```bash
git clone [repository-url]
cd [repository-name]
```

### 2. Create Backend Directory
```bash
mkdir backend
cd backend
```

### 3. Set up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies
Create a `requirements.txt` file with the following content:

```txt
requests==2.31.0
cohere==4.9.0
qdrant-client==1.9.2
beautifulsoup4==4.12.2
python-dotenv==1.0.0
pytest==8.0.0
```

Then install:
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Create a `.env` file in the backend directory:

```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
BOOK_BASE_URL=https://ai-robotics-textbook-ten.vercel.app/
SITEMAP_URL=https://ai-robotics-textbook-ten.vercel.app/sitemap.xml
```

## Project Structure
After setup, your directory should look like this:

```
backend/
├── src/
│   ├── embeddings_pipeline/
│   │   ├── __init__.py
│   │   ├── url_extractor.py
│   │   ├── text_extractor.py
│   │   ├── text_chunker.py
│   │   ├── embedding_generator.py
│   │   ├── qdrant_handler.py
│   │   └── main.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── tests/
├── requirements.txt
├── .env
└── .env.example
```

## Running the Embeddings Pipeline

### 1. Create Configuration File
Create `backend/src/config/settings.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
BOOK_BASE_URL = os.getenv("BOOK_BASE_URL", "https://ai-robotics-textbook-ten.vercel.app/")
SITEMAP_URL = os.getenv("SITEMAP_URL", "https://ai-robotics-textbook-ten.vercel.app/sitemap.xml")
```

### 2. Run the Main Pipeline
```bash
cd backend
python -m src.embeddings_pipeline.main
```

## Key Functions Overview

### URL Extraction
- `get_all_urls()`: Discovers and returns all book content URLs from the base URL

### Text Extraction
- `extract_text_from_url(url)`: Extracts clean text content from a given URL

### Text Chunking
- `chunk_text(text)`: Splits large text into smaller, semantically meaningful chunks

### Embedding Generation
- `embed(text_chunks)`: Generates vector embeddings for text chunks using Cohere API

### Qdrant Operations
- `create_collection()`: Creates a Qdrant collection for storing embeddings
- `save_chunk_to_qdrant(chunk, embedding)`: Saves a text chunk and its embedding to Qdrant

## Verification

After running the pipeline, verify that:
1. All book URLs were successfully accessed
2. Text content was properly extracted and chunked
3. Embeddings were generated for all chunks
4. All embeddings were stored in Qdrant
5. Sample retrieval works correctly

## Next Steps
1. Run the full pipeline with `python -m src.embeddings_pipeline.main`
2. Verify embeddings in Qdrant dashboard
3. Test retrieval with sample queries
4. Monitor API usage to stay within rate limits