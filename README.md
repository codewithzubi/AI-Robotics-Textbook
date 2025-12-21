# AI Robotics Textbook

This project implements an AI-powered robotics textbook with embeddings pipeline, RAG (Retrieval Augmented Generation) capabilities, and vector database storage.

## Project Structure

- `backend/` - Python backend with embeddings pipeline and Qdrant integration
- `my-website/` - Docusaurus-based frontend documentation website
- `specs/` - Project specifications and planning documents
- `history/` - Historical records and architecture decision records

## Backend Setup

The backend handles content extraction, text processing, embeddings generation, and vector storage.

### Prerequisites

- Python 3.8+
- Node.js (for the frontend)

### Backend Installation

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on the template:
   ```bash
   cp .env.example .env
   # Edit .env and add your actual API keys
   ```

### Required Environment Variables

You'll need to set up the following API keys:

#### Qdrant Vector Database
1. Sign up at [Qdrant Cloud](https://cloud.qdrant.io/)
2. Create a new cluster
3. Copy the REST URL (format: `https://xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.us-east4-0.gcp.cloud.qdrant.io:6333`)
4. Create an API key in the dashboard
5. Add to your `.env` file:
   ```
   QDRANT_URL=your_cluster_url_here
   QDRANT_API_KEY=your_api_key_here
   ```

#### API Keys
- **Cohere API Key**: Get from [Cohere Dashboard](https://dashboard.cohere.com/)
- **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/)

Add to your `.env` file:
```
COHERE_API_KEY=your_cohere_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### Running the Qdrant Setup Checker

After setting up your environment variables, you can run the Qdrant setup checker:

```bash
python check_qdrant_setup.py
```

This will verify your Qdrant connection and ensure the required collection exists.

### Running the Embeddings Pipeline

To run the complete embeddings pipeline:

```bash
python -m src.embeddings_pipeline.main
```

This will:
1. Fetch all book content URLs from the sitemap
2. Extract text content from each URL
3. Chunk the text into semantically meaningful segments
4. Generate embeddings using Cohere API
5. Store embeddings in Qdrant vector database with metadata

## Frontend Setup (Docusaurus)

1. Navigate to the website directory:
   ```bash
   cd my-website
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## Troubleshooting

### Qdrant Connection Issues
If you get "QDRANT_URL is not set in environment variables" error:
1. Make sure you have created the `.env` file in the backend directory
2. Verify that the QDRANT_URL and QDRANT_API_KEY values are correctly set
3. Ensure you're running the script from the backend directory where the `.env` file is located

### API Key Issues
- Ensure your API keys are valid and have the necessary permissions
- Check that there are no extra spaces or characters in your environment variables
- Verify that your API providers (Cohere, OpenAI) have not rate-limited your account

## Contributing

For detailed setup instructions and contribution guidelines, see the backend README and project specifications in the `specs/` directory.