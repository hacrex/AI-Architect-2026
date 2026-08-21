# Data Architecture — Data Pipeline Sample App

A working prototype demonstrating **data ingestion**, **chunking strategies**, **metadata extraction**, **vector storage**, and **permission-filtered retrieval** from Day 05.

> **Building on Day 04**: This app takes the production infrastructure and adds the data layer — ingestion, processing, storage, and retrieval with security.

## Architecture

```
                    Documents
                        │
                        ▼
               ┌─────────────────┐
               │ Ingestion       │
               │ Pipeline        │
               ├─────────────────┤
               │ Parser/OCR      │
               │ Chunker         │
               │ Metadata        │
               │ Embedding       │
               └────────┬────────┘
                        │
            ┌───────────┴───────────┐
            ▼                       ▼
      ┌──────────┐           ┌──────────┐
      │ Vector   │           │ Metadata │
      │ DB       │           │ DB       │
      └────┬─────┘           └────┬─────┘
           │                      │
           └──────────┬───────────┘
                      │
                      ▼
               ┌──────────────┐
               │ Retrieval    │
               │ Layer        │
               ├──────────────┤
               │ Hybrid Search│
               │ Permissions  │
               │ Reranking    │
               └──────────────┘
```

## Project Structure

```
sample-app/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── ingestion.py         # Document ingestion pipeline
│   ├── chunker.py           # Chunking strategies
│   ├── metadata.py          # Metadata extraction
│   ├── embeddings.py        # Embedding generation
│   ├── vectordb.py          # Vector database operations
│   ├── retrieval.py         # Hybrid search + permissions
│   └── auth.py              # Authentication & authorization
├── config/
│   ├── settings.py          # Configuration management
│   └── .env.example         # Environment variables template
├── docs/
│   ├── engineering/
│   │   ├── kubernetes-guide.md
│   │   └── deployment-process.md
│   ├── hr/
│   │   ├── leave-policy.md
│   │   └── onboarding.md
│   └── security/
│       ├── security-policy.md
│       └── incident-response.md
├── scripts/
│   ├── ingest.py            # Bulk ingestion script
│   ├── compare_chunking.py  # Chunking comparison tool
│   └── test_permissions.py  # Permission verification
├── requirements.txt
└── test_pipeline.py         # Test script
```

## Quick Start

### 1. Install Dependencies

```bash
cd 05-data-architecture/sample-app
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp config/.env.example config/.env
# Edit config/.env with your API keys
```

### 3. Ingest Documents

```bash
python scripts/ingest.py
```

### 4. Start the Server

```bash
uvicorn app.main:app --reload --port 8005
```

### 5. Test the API

```bash
python test_pipeline.py
```

Or manually:

```bash
# Health check
curl http://localhost:8005/health

# Ingest a document
curl -X POST http://localhost:8005/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "eng-001",
    "title": "Kubernetes Guide",
    "content": "Kubernetes is an container orchestration platform...",
    "department": "engineering",
    "classification": "internal"
  }'

# Query with permissions
curl -X POST http://localhost:8005/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "query": "How do I deploy to Kubernetes?",
    "user_id": "alice@company.com"
  }'

# Compare chunking strategies
curl -X POST http://localhost:8005/chunking/compare \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "eng-001",
    "strategies": ["fixed", "semantic", "structure"]
  }'

# Get ingestion stats
curl http://localhost:8005/stats
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check with DB status |
| `/ingest` | POST | Ingest a single document |
| `/ingest/batch` | POST | Ingest multiple documents |
| `/query` | POST | Query with permission filtering |
| `/chunking/compare` | POST | Compare chunking strategies |
| `/documents` | GET | List all documents |
| `/documents/{id}` | GET | Get document metadata |
| `/documents/{id}` | DELETE | Delete a document |
| `/stats` | GET | Ingestion and storage statistics |
| `/users` | GET | List users and permissions |

## Chunking Strategies

### Fixed-Size Chunking

```python
def fixed_chunking(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks
```

### Semantic Chunking

```python
def semantic_chunking(text):
    # Split by paragraph boundaries
    # Split by sentence boundaries
    # Group related sentences
    pass
```

### Structure-Aware Chunking

```python
def structure_aware_chunking(text):
    # Split by headings (##, ###)
    # Split by sections
    # Respect document structure
    pass
```

## Permission Model

### User Roles

| Role | Access Level |
|------|-------------|
| `engineering` | Engineering documents only |
| `hr` | HR documents only |
| `security` | Security documents only |
| `admin` | All documents |

### Document Classification

| Level | Description |
|-------|-------------|
| `public` | All authenticated users |
| `internal` | Department members only |
| `confidential` | Authorized roles only |
| `restricted` | Specific individuals only |

## Configuration

### Environment Variables

```bash
# Database
CHROMA_HOST=localhost
CHROMA_PORT=8000
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ai_data

# Embedding
EMBEDDING_MODEL=text-embedding-ada-002
EMBEDDING_DIMENSIONS=1536

# Chunking
DEFAULT_CHUNK_SIZE=500
DEFAULT_CHUNK_OVERLAP=50

# Retrieval
DEFAULT_TOP_K=10
RERANKING_ENABLED=true

# Auth
JWT_SECRET=your-secret-key
```

## Architecture Patterns Demonstrated

| Pattern | Implementation |
|---------|----------------|
| **Ingestion Pipeline** | Parse → Clean → Chunk → Embed → Store |
| **Multiple Chunking Strategies** | Fixed-size, semantic, structure-aware |
| **Metadata Extraction** | Department, classification, dates, owner |
| **Hybrid Search** | Keyword + vector search combined |
| **Permission Filtering** | Document-level authorization |
| **Reranking** | Reorder results by relevance |
| **Versioning** | Document version tracking |
| **Deletion Propagation** | Remove from vector DB on delete |

## Key Concepts (Day 05)

This sample app demonstrates:

1. **Data Ingestion** — Parsing documents from multiple formats
2. **Chunking Strategies** — Different approaches to splitting content
3. **Metadata Extraction** — Extracting structured data from documents
4. **Embedding Generation** — Converting text to vectors
5. **Vector Storage** — Indexing embeddings for similarity search
6. **Hybrid Search** — Combining keyword and semantic search
7. **Permission Filtering** — Enforcing document-level access control
8. **Reranking** — Improving retrieval quality with rerankers
9. **Versioning** — Handling document updates and deletions
10. **Data Lineage** — Tracking where answers come from
