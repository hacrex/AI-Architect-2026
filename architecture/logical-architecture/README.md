# Logical Architecture — Enterprise AI Knowledge Assistant

## System Components

This document describes the internal system components, their responsibilities, and how they interact.

## Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        API LAYER                                │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │   nginx     │  │   Rate      │  │   Authentication        │ │
│  │   Ingress   │  │   Limiter   │  │   (JWT Validation)      │ │
│  └──────┬──────┘  └──────┬──────┘  └───────────┬─────────────┘ │
│         └────────────────┼─────────────────────┘               │
└──────────────────────────┼──────────────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────────┐
│                     AI GATEWAY                                  │
├──────────────────────────┼──────────────────────────────────────┤
│  ┌───────────────────────┴──────────────────────────────────┐  │
│  │              Request Router                              │  │
│  │  - Complexity classification                             │  │
│  │  - Model selection                                        │  │
│  │  - Policy enforcement                                     │  │
│  └───────────────────────┬──────────────────────────────────┘  │
│                          │                                     │
│  ┌───────────┐  ┌────────┴────────┐  ┌────────────────────┐   │
│  │ Token     │  │ Fallback        │  │ Audit              │   │
│  │ Tracker   │  │ Handler         │  │ Logger             │   │
│  └───────────┘  └─────────────────┘  └────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────────┐
│                  APPLICATION LAYER                              │
├──────────────────────────┼──────────────────────────────────────┤
│                          │                                     │
│  ┌───────────────────────┴──────────────────────────────────┐  │
│  │              Context Assembly                            │  │
│  │  - Query understanding                                   │  │
│  │  - Context window management                             │  │
│  │  - Priority ordering                                      │  │
│  └───────────────────────┬──────────────────────────────────┘  │
│                          │                                     │
│  ┌──────────────┐  ┌────┴──────────┐  ┌──────────────────┐   │
│  │ RAG Pipeline │  │ Agent System  │  │ Tool Registry    │   │
│  │              │  │               │  │                  │   │
│  │ - Chunking   │  │ - Orchestrator│  │ - search_docs    │   │
│  │ - Embedding  │  │ - Support     │  │ - lookup_orders  │   │
│  │ - Retrieval  │  │ - Billing     │  │ - code_search    │   │
│  │ - Reranking  │  │ - Tech        │  │ - get_status     │   │
│  └──────────────┘  └───────────────┘  └──────────────────┘   │
│                                                               │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────────┐
│                    MODEL LAYER                                  │
├──────────────────────────┼──────────────────────────────────────┤
│  ┌───────────────────────┴──────────────────────────────────┐  │
│  │              Model Gateway                               │  │
│  │  - Provider abstraction                                  │  │
│  │  - Load balancing                                        │  │
│  │  - Cost optimization                                     │  │
│  └───────────────────────┬──────────────────────────────────┘  │
│                          │                                     │
│  ┌───────────┐  ┌────────┴────────┐  ┌────────────────────┐   │
│  │ OpenAI    │  │ Anthropic       │  │ Self-hosted        │   │
│  │ API       │  │ API             │  │ (vLLM)             │   │
│  └───────────┘  └─────────────────┘  └────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────────┘
```

## API Contracts

### API Gateway

| Endpoint | Method | Purpose | Auth |
|----------|--------|---------|------|
| `/api/v1/query` | POST | Ask a question | JWT |
| `/api/v1/documents` | POST | Upload document | JWT + Admin |
| `/api/v1/documents` | GET | List documents | JWT |
| `/api/v1/health` | GET | Health check | None |
| `/api/v1/metrics` | GET | Prometheus metrics | Internal |

### AI Gateway

| Interface | Method | Purpose |
|-----------|--------|---------|
| `route(request)` | sync | Route request to appropriate model |
| `classify(prompt)` | sync | Classify request complexity |
| `track_usage(model, tokens)` | sync | Track token consumption |

### RAG Pipeline

| Interface | Method | Purpose |
|-----------|--------|---------|
| `ingest(document)` | async | Ingest document into vector DB |
| `retrieve(query, filters)` | sync | Retrieve relevant documents |
| `rerank(query, documents)` | sync | Rerank retrieved documents |

### Agent System

| Interface | Method | Purpose |
|-----------|--------|---------|
| `orchestrate(goal)` | async | Orchestrate multi-agent task |
| `delegate(agent, task)` | sync | Delegate task to specific agent |
| `handoff(agent, context)` | sync | Hand off conversation to agent |

## Data Stores

| Store | Technology | Purpose | Access Pattern |
|-------|-----------|---------|----------------|
| Vector DB | ChromaDB / Pinecone | Document embeddings | Read-heavy |
| Metadata DB | PostgreSQL | Document metadata, user data | Read/write |
| Session Store | Redis | Conversation state, cache | Read/write |
| Audit Log | Elasticsearch | Security audit trail | Write-once |
| Document Store | S3 | Raw documents | Write-once, read-many |

## Message Queues

| Queue | Purpose | Consumers |
|-------|---------|-----------|
| `ingest` | Document ingestion | RAG pipeline |
| `agent-tasks` | Agent task queue | Agent orchestrator |
| `audit` | Audit events | Audit logger |

## External Integrations

| System | Protocol | Purpose |
|--------|----------|---------|
| SSO (Okta/Azure AD) | OIDC | Authentication |
| Model APIs | HTTPS | LLM inference |
| Vector DB | gRPC/HTTPS | Embedding storage/retrieval |
| Monitoring | HTTP | Metrics export |
