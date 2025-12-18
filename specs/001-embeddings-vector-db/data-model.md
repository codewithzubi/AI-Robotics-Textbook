# Data Model: Deploy Website URLs, Generate Embeddings, and Store in Vector Database

## Entities

### BookContent
**Description**: Represents the source material from the AI Robotics textbook
- **Fields**:
  - `url` (string): The URL where the book content is accessible
  - `title` (string): Title of the book section/chapter
  - `content` (string): Raw text content extracted from the URL
  - `module` (string): Module identifier (e.g., "Module 1: ROS 2")
  - `chapter` (string): Chapter identifier within the module
  - `created_at` (datetime): Timestamp when content was extracted
  - `updated_at` (datetime): Timestamp when content was last updated

### TextChunk
**Description**: Represents a segment of book content after text processing
- **Fields**:
  - `id` (string): Unique identifier for the chunk
  - `content` (string): The text content of the chunk
  - `source_url` (string): URL from which this chunk originated
  - `module` (string): Module identifier
  - `chapter` (string): Chapter identifier
  - `chunk_index` (integer): Position of this chunk within the source document
  - `metadata` (object): Additional metadata about the chunk
  - `created_at` (datetime): Timestamp when chunk was created

### Embedding
**Description**: Represents the vector embedding of a text chunk
- **Fields**:
  - `id` (string): Unique identifier matching the text chunk
  - `vector` (array of floats): The embedding vector from Cohere API
  - `chunk_id` (string): Reference to the original text chunk
  - `model` (string): Name of the model used to generate the embedding
  - `created_at` (datetime): Timestamp when embedding was generated

### QdrantRecord
**Description**: Represents a record stored in Qdrant vector database
- **Fields**:
  - `id` (string): Unique identifier for the record
  - `payload` (object): Contains the original text chunk and metadata
    - `content`: The original text content
    - `source_url`: URL from which content originated
    - `module`: Module identifier
    - `chapter`: Chapter identifier
    - `chunk_index`: Position of the chunk in the source document
  - `vector` (array of floats): The embedding vector
  - `created_at` (datetime): Timestamp when record was stored in Qdrant

## Relationships

### BookContent → TextChunk
- One BookContent can generate multiple TextChunks
- Relationship: One-to-Many
- The content from a single URL can be split into multiple chunks

### TextChunk → Embedding
- One TextChunk generates one Embedding
- Relationship: One-to-One
- Each chunk has exactly one corresponding embedding

### Embedding → QdrantRecord
- One Embedding becomes one QdrantRecord
- Relationship: One-to-One
- Embedding data is stored as a record in Qdrant

## Validation Rules

### BookContent Validation
- `url` must be a valid, accessible URL
- `content` must not be empty
- `module` and `chapter` must match the expected curriculum structure

### TextChunk Validation
- `content` length must be within Cohere API limits (typically < 4096 tokens)
- `chunk_index` must be a non-negative integer
- `metadata` must include source reference information

### Embedding Validation
- `vector` must be an array of floats with consistent dimensions
- `model` must match the Cohere model being used
- `chunk_id` must reference an existing TextChunk

### QdrantRecord Validation
- `id` must be unique within the collection
- `vector` dimensions must match the collection schema
- `payload` must contain all required metadata fields

## State Transitions

### BookContent States
1. `EXTRACTED` - Content has been successfully retrieved from URL
2. `PROCESSED` - Content has been prepared for chunking

### TextChunk States
1. `CREATED` - Chunk has been created from book content
2. `EMBEDDED` - Embedding has been generated for this chunk

### Embedding States
1. `GENERATED` - Embedding vector has been created
2. `STORED` - Embedding has been saved to Qdrant