# AI Knowledge Assistant — Sample App

A working prototype of the Enterprise AI Knowledge Assistant architecture from Day 01.

## Architecture

```
Employee
    │
    ▼
Authentication (JWT)
    │
    ▼
API Gateway (FastAPI)
    │
    ├──▶ /health      → Health checks
    ├──▶ /query       → RAG query with auth
    ├──▶ /query/stream → Streaming response
    ├──▶ /ingest      → Document ingestion (admin)
    └──▶ /metrics     → Observability (admin)
    │
    ▼
AI Application
    │
    ├──▶ RAG Pipeline (ChromaDB)
    │       ├── Query embedding
    │       ├── Vector search
    │       └── Context assembly
    │
    └──▶ Model Gateway
            ├── Primary: GPT-4
            └── Fallback: GPT-3.5-turbo
```

## Project Structure

```
sample-app/
├── app/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── rag.py               # RAG pipeline (ChromaDB)
│   ├── model_gateway.py     # LLM provider with fallback
│   ├── auth.py              # Authentication + authorization
│   └── observability.py     # Metrics collection
├── config/
│   ├── settings.py          # Configuration management
│   └── .env.example         # Environment variables template
├── docs/
│   └── sample-documents.json # Sample knowledge base
├── data/                    # ChromaDB storage (created at runtime)
├── requirements.txt         # Python dependencies
├── seed.py                  # Seed database with sample docs
└── test_app.py              # Test script
```

## Quick Start

### 1. Install Dependencies

```bash
cd 01-foundations/sample-app
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp config/.env.example config/.env
# Edit config/.env with your API keys
```

### 3. Seed the Knowledge Base

```bash
python seed.py
```

### 4. Start the Server

```bash
uvicorn app.main:app --reload --port 8000
```

### 5. Test the API

```bash
python test_app.py
```

Or manually:

```bash
# Health check
curl http://localhost:8000/health

# Query (use your auth token)
curl -X POST http://localhost:8000/query \
  -H "Authorization: Bearer user-001" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the leave policy?"}'
```

## API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/health` | GET | No | Health check with component status |
| `/query` | POST | Yes | RAG query with sources |
| `/query/stream` | POST | Yes | Streaming RAG response |
| `/ingest` | POST | Admin | Add document to knowledge base |
| `/metrics` | GET | Admin | Observability metrics |

## Authentication

Sample users for testing:

| Token | User | Permissions | Admin |
|-------|------|-------------|-------|
| `user-001` | John Doe | hr, engineering, general | No |
| `user-002` | Jane Admin | all departments | Yes |
| `user-003` | Bob Limited | general only | No |

## Architecture Patterns Demonstrated

| Pattern | Implementation |
|---------|----------------|
| RAG | ChromaDB + query embedding |
| Model Gateway | OpenAI with fallback |
| Authentication | JWT bearer tokens |
| Authorization | Role-based + document permissions |
| Observability | Request latency, success rate, token tracking |
| Loose Coupling | Model gateway abstracts provider |
| Failure Handling | Fallback model on primary failure |

## Sample Queries

```json
{"query": "What is the leave policy?"}
{"query": "How do I request AWS access?"}
{"query": "What is the security policy?"}
{"query": "Can I work remotely?"}
{"query": "What is the expense policy?"}
```

## Key Concepts (Day 01)

This sample app demonstrates:

1. **API Gateway pattern** — Single entry point with rate limiting
2. **Model Gateway** — Provider abstraction with fallback
3. **RAG Pipeline** — Retrieval + context assembly
4. **Role-based access** — Document-level permissions
5. **Observability** — Metrics and health checks
6. **Loose coupling** — Easy to swap model providers
7. **Failure handling** — Graceful degradation
