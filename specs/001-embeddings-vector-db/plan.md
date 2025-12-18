# Implementation Plan: Deploy Website URLs, Generate Embeddings, and Store in Vector Database

**Branch**: `001-embeddings-vector-db` | **Date**: 2025-12-15 | **Spec**: [link](./spec.md)
**Input**: Feature specification from `/specs/001-embeddings-vector-db/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build an embeddings pipeline that extracts content from book URLs (deployed at https://ai-robotics-textbook-ten.vercel.app/), processes it through Cohere embeddings API, and stores the vectors in Qdrant vector database. The system will include functions for getting all URLs from the sitemap (https://ai-robotics-textbook-ten.vercel.app/sitemap.xml), extracting text, chunking content, generating embeddings, creating a Qdrant collection, and saving chunks to the database.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: requests, cohere, qdrant-client, beautifulsoup4, python-dotenv
**Storage**: Qdrant vector database (Cloud Free Tier)
**Testing**: pytest for unit and integration tests
**Target Platform**: Linux server environment (Vercel deployment)
**Project Type**: Backend service for embeddings pipeline
**Performance Goals**: Process 1000+ book sections within 1 week timeline, with 95% retrieval accuracy
**Constraints**: Must work within Cohere API rate limits and Qdrant Cloud Free Tier storage limits
**Scale/Scope**: Handle entire AI Robotics textbook content (~25,000-35,000 words across multiple modules)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Initial Check (Pre-Design)
- Technical accuracy: Solution uses official APIs (Cohere, Qdrant) with proper documentation
- Educational clarity: Code will be well-documented for student understanding
- Modular structure: Implementation will follow the Panaversity course outline structure
- Reusability: Embeddings pipeline optimized for Claude Code Subagents integration
- AI-Native Design: System designed for RAG compatibility with proper metadata embedding
- Source verification: All API integrations will follow official documentation

### Post-Design Check (After Phase 1)
- Technical accuracy: ✅ Using official Cohere and Qdrant APIs with proper integration patterns
- Educational clarity: ✅ Modular code structure with clear function responsibilities (get_all_urls, extract_text_from_url, chunk_text, embed, create_collection, save_chunk_to_qdrant)
- Modular structure: ✅ Follows curriculum structure with separate modules for each pipeline step
- Reusability: ✅ Pipeline components designed as reusable functions for Claude Code Subagents
- AI-Native Design: ✅ System designed for RAG with proper metadata embedding and Qdrant storage
- Source verification: ✅ All implementations follow official API documentation

## Project Structure

### Documentation (this feature)

```text
specs/001-embeddings-vector-db/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
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
│   ├── unit/
│   ├── integration/
│   └── __init__.py
├── requirements.txt
├── .env.example
└── README.md
```

**Structure Decision**: Backend service structure selected to handle the embeddings pipeline. The service will have dedicated modules for each step of the process: URL extraction, text extraction, text chunking, embedding generation, and Qdrant storage. This modular approach follows the educational clarity principle from the constitution.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| External API dependencies | Cohere and Qdrant APIs required for core functionality | Using local embedding models would require significant computational resources and expertise |
| Multi-step pipeline | Each step (URL extraction, text processing, embedding, storage) requires separate modules | Single monolithic function would be harder to debug and maintain |
