# Quickstart: AI Agent with Retrieval

## Overview

This guide provides a quick start for implementing and using the AI agent with retrieval functionality. The system creates an AI agent that answers questions based only on the AI Robotics textbook content using OpenAI's Agents SDK and FastAPI.

## Prerequisites

- Python 3.11 or higher
- pip package manager
- Git for version control
- OpenAI API key
- Access to existing Qdrant vector database (from Spec-2)
- Access to Cohere API key (for consistent embeddings)

## Setup

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

First, update requirements.txt to include new dependencies:

```bash
# Add to backend/requirements.txt
openai==1.12.0
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.0
python-multipart==0.0.9
```

Then install all dependencies:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create or update your `.env` file in the backend directory:

```bash
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
COHERE_API_KEY=your_cohere_api_key
EMBEDDING_MODEL=embed-multilingual-v3.0
COLLECTION_NAME=robotics_textbook_chunks
AGENT_INSTRUCTIONS="You are an AI assistant for the AI Robotics textbook. Answer questions based only on the provided context from the textbook. Do not hallucinate information."
```

## Basic Usage

### 1. Start the FastAPI Server

```bash
cd src
uvicorn ai_agent.main:app --reload --port 8000
```

### 2. Test the Agent

Once the server is running, you can test the agent using curl:

```bash
curl -X POST "http://localhost:8000/api/v1/agent/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is inverse kinematics in robotics?",
    "max_tokens": 500,
    "temperature": 0.7
  }'
```

Or using Python:

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/agent/query",
    json={
        "query": "What is inverse kinematics in robotics?",
        "max_tokens": 500,
        "temperature": 0.7
    }
)
print(response.json())
```

### 3. Check Health Status

```bash
curl -X GET "http://localhost:8000/health"
```

## Core Components

### Agent Creation

The agent is created using OpenAI's Assistants API with specific instructions:

```python
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)

agent = client.beta.assistants.create(
    name="AI Robotics Textbook Assistant",
    instructions="Answer questions based only on the provided textbook content. Do not hallucinate.",
    model="gpt-4-turbo-preview"
)
```

### Retrieval Integration

The system integrates with the existing RAG pipeline to retrieve relevant content:

```python
from ai_agent.retrieval_integrator import RetrievalIntegrator

retriever = RetrievalIntegrator()
context = retriever.retrieve_context("What is robot kinematics?")
```

### API Models

The system uses Pydantic models for request/response validation:

```python
from ai_agent.api_models import QueryRequest, AgentResponse

request = QueryRequest(
    query="What is forward kinematics?",
    max_tokens=300,
    temperature=0.5
)
```

## Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for agent functionality | Required |
| `QDRANT_URL` | Qdrant instance URL | Required |
| `QDRANT_API_KEY` | Qdrant API key | Required |
| `COHERE_API_KEY` | Cohere API key for embeddings | Required |
| `EMBEDDING_MODEL` | Cohere model for embeddings | embed-multilingual-v3.0 |
| `COLLECTION_NAME` | Qdrant collection name | robotics_textbook_chunks |
| `AGENT_INSTRUCTIONS` | Instructions for the AI agent | "Answer from textbook only..." |

### API Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `query` | string | Natural language question | Required |
| `max_tokens` | integer | Maximum tokens in response | 500 |
| `temperature` | float | Response creativity (0.0-1.0) | 0.7 |

## Testing the Agent

### Single Query Test

```bash
python -c "
from ai_agent.agent import AI_Agent
agent = AI_Agent()
response = agent.process_query('What is PID control in robotics?')
print(response.answer)
"
```

### Batch Query Test

Create a file with multiple queries:

```bash
# queries.txt
What is robot kinematics?
Explain inverse kinematics
What are Jacobian matrices?
```

Process batch queries programmatically:

```python
queries = [
    'What is robot kinematics?',
    'Explain inverse kinematics',
    'What are Jacobian matrices?'
]

for query in queries:
    response = agent.process_query(query)
    print(f'Q: {query}')
    print(f'A: {response.answer[:100]}...')
    print('---')
```

## API Response Format

The API returns responses in a standardized format:

```json
{
  "status": "success",
  "data": {
    "response_id": "unique-response-id",
    "query": "What is inverse kinematics?",
    "answer": "Inverse kinematics is the mathematical process...",
    "sources": ["Chapter 3: Kinematics", "Section 3.2: Inverse Kinematics"],
    "confidence_score": 0.92,
    "processing_time_ms": 1250,
    "retrieval_context": ["Context snippets used..."],
    "timestamp": "2025-12-15T10:30:00Z",
    "metadata": {}
  },
  "error": null,
  "request_id": "unique-request-id",
  "timestamp": "2025-12-15T10:30:00Z"
}
```

## Troubleshooting

### Common Issues

1. **OpenAI API Rate Limiting**: If you encounter rate limiting errors, reduce the query frequency or upgrade your OpenAI plan.

2. **Qdrant Connection Issues**: Verify that your QDRANT_URL and QDRANT_API_KEY are correct and that the Qdrant instance is accessible.

3. **No Relevant Results**: If the agent responds with "I don't know" frequently, check that the vector database has been properly populated with textbook content.

4. **Agent Hallucination**: If the agent is providing information not in the textbook, verify that the retrieval integration is working properly and the agent instructions are being enforced.

### Debugging

Enable debug logging:

```bash
export LOG_LEVEL=DEBUG
uvicorn ai_agent.main:app --reload --port 8000
```

Check the health of integrated services:

```bash
curl -X GET "http://localhost:8000/health"
```

## Next Steps

1. Integrate the AI agent with your application frontend
2. Set up monitoring for agent usage and performance
3. Configure rate limiting for production use
4. Implement caching for frequently asked questions
5. Add conversation history for multi-turn interactions