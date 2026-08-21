# Day 05 — Architecture: Data Architecture for AI

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Data Architecture Diagram](#2-data-architecture-diagram)
3. [Component Responsibilities](#3-component-responsibilities)
4. [Data Flow](#4-data-flow)
5. [Failure Scenarios](#5-failure-scenarios)
6. [Security Architecture](#6-security-architecture)
7. [Scaling Considerations](#7-scaling-considerations)
8. [Cost Model](#8-cost-model)
9. [Key Takeaways](#9-key-takeaways)

---

## 1. System Overview

### Day 05 Enterprise AI Knowledge Assistant — Data Layer

```
                           Users
                             │
                             ▼
                       API Gateway
                             │
                             ▼
                        AI Gateway
                             │
                             ▼
                          RAG
                             │
                      ┌──────┴──────┐
                      ↓             ↓
                  Retriever      Metadata
                      │
             ┌────────┴─────────┐
             ↓                  ↓
        Vector Store        Source Data
             │                  │
             └────────┬─────────┘
                      ↓
                 Context
                      ↓
                Model Gateway
                      ↓
               Model / Inference
```

### Data Platform Layer

```
Documents / APIs / Databases
             ↓
       Ingestion Pipeline
             ↓
        Processing / OCR
             ↓
          Chunking
             ↓
         Embeddings
             ↓
       Vector + Metadata
```

---

## 2. Data Architecture Diagram

### End-to-End Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                       DATA SOURCES                              │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │Documents │  │ Databases│  │   APIs   │  │   Wiki   │       │
│  │ (PDFs,   │  │(Postgres,│  │(Internal,│  │(Confluence│      │
│  │  Word)   │  │  MySQL)  │  │ External)│  │ Notion)  │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
│       └──────────────┼─────────────┼──────────────┘             │
└──────────────────────┼─────────────┼────────────────────────────┘
                       │             │
┌──────────────────────┼─────────────┼────────────────────────────┐
│                 INGESTION LAYER                                 │
├──────────────────────┼─────────────┼────────────────────────────┤
│                      ↓             ↓                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Ingestion Pipeline                         │   │
│  │  - Batch (nightly)                                      │   │
│  │  - Streaming (Kafka)                                    │   │
│  │  - Event-driven (webhooks)                              │   │
│  └─────────────────────────┬───────────────────────────────┘   │
└────────────────────────────┼────────────────────────────────────┘
                             │
┌────────────────────────────┼────────────────────────────────────┐
│                 PROCESSING LAYER                                │
├────────────────────────────┼────────────────────────────────────┤
│                             ↓                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │  Parse   │  │ Cleaning │  │ Chunking │  │ Metadata │       │
│  │  / OCR   │  │          │  │          │  │ Extract  │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
│       └──────────────┼─────────────┼──────────────┘             │
└──────────────────────┼─────────────┼────────────────────────────┘
                       │             │
┌──────────────────────┼─────────────┼────────────────────────────┐
│                 STORAGE LAYER                                   │
├──────────────────────┼─────────────┼────────────────────────────┤
│                      ↓             ↓                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Embedding Pipeline                         │   │
│  │  - Embedding Model (OpenAI, Cohere, self-hosted)       │   │
│  │  - Vector dimensions: 1536 (ada-002), 768, 1024        │   │
│  └─────────────────────────┬───────────────────────────────┘   │
│                             ↓                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Vector DB   │  │ Metadata DB  │  │ Document     │         │
│  │  (Pinecone,  │  │ (PostgreSQL) │  │ Storage (S3) │         │
│  │  Qdrant,     │  │              │  │              │         │
│  │  Weaviate)   │  │              │  │              │         │
│  └──────┬───────┘  └──────┬───────┘  └──────────────┘         │
│         │                  │                                    │
│         └────────┬─────────┘                                    │
│                  ↓                                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Retrieval Layer                            │   │
│  │  - Hybrid Search (keyword + vector)                     │   │
│  │  - Metadata Filtering                                   │   │
│  │  - Permission Filtering                                 │   │
│  │  - Reranking                                            │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Component Responsibilities

### Ingestion Pipeline

| Component | Responsibility |
|-----------|---------------|
| Document Parser | Extract text from PDFs, Word docs, images |
| OCR | Convert images to text |
| ETL/ELT | Transform data for AI consumption |
| Change Detection | Detect document updates/deletions |
| Deduplication | Remove duplicate content |

### Processing Layer

| Component | Responsibility |
|-----------|---------------|
| Chunking | Split documents into meaningful segments |
| Metadata Extraction | Extract department, classification, owner, dates |
| Embedding Generation | Convert text to vectors |
| Quality Validation | Verify chunk quality and completeness |

### Storage Layer

| Component | Responsibility |
|-----------|---------------|
| Vector DB | Store and search document embeddings |
| Metadata DB | Store document metadata and permissions |
| Document Storage | Store original documents |
| Cache | Cache frequent queries and results |

### Retrieval Layer

| Component | Responsibility |
|-----------|---------------|
| Hybrid Search | Combine keyword and semantic search |
| Metadata Filtering | Filter by department, classification, date |
| Permission Filtering | Enforce document-level access control |
| Reranking | Reorder results by relevance |

---

## 4. Data Flow

### Ingestion Flow

```
1. Document uploaded/updated
         ↓
2. Change event emitted
         ↓
3. Ingestion pipeline triggered
         ↓
4. Document parsed (text extraction)
         ↓
5. Content cleaned (formatting, noise)
         ↓
6. Document chunked (structure-aware)
         ↓
7. Metadata extracted (department, classification, dates)
         ↓
8. Embeddings generated
         ↓
9. Vector DB updated
         ↓
10. Metadata DB updated
         ↓
11. Old version invalidated
         ↓
12. Audit log updated
```

### Query Flow

```
1. User asks question
         ↓
2. Authentication + authorization
         ↓
3. Query embedded
         ↓
4. Hybrid search (keyword + vector)
         ↓
5. Metadata filtering (department, classification)
         ↓
6. Permission filtering (user access level)
         ↓
7. Top 50 results retrieved
         ↓
8. Reranking applied
         ↓
9. Top 5 results selected
         ↓
10. Context assembled (query + results + history)
         ↓
11. LLM generates answer
         ↓
12. Response validated
         ↓
13. Answer + citations returned
         ↓
14. Audit log updated
```

---

## 5. Failure Scenarios

| Component | Failure | Impact | Mitigation |
|-----------|---------|--------|------------|
| Ingestion Pipeline | Pipeline down | Stale data | Alert, manual trigger, queue retries |
| Document Parser | Parse failure | Missing content | Fallback parser, manual review queue |
| Chunking | Poor chunks | Bad retrieval | Quality validation, chunk size limits |
| Embedding Model | Model unavailable | No new embeddings | Queue for retry, alternate model |
| Vector DB | Database down | No retrieval | Cached responses, graceful degradation |
| Metadata DB | Database down | No filtering | Default to least-privilege, alert |
| Change Detection | Missed updates | Stale embeddings | Periodic re-indexing, change events |
| Permission Sync | Outdated permissions | Data leakage | Real-time sync, periodic validation |
| Reranking | Reranker slow/failed | Degraded ranking | Skip reranking, use initial ranking |
| Deduplication | Duplicates | Wasted storage, confusion | Hash-based dedup, merge strategy |

---

## 6. Security Architecture

### Authorization at the Retrieval Level

```
User → Identity → Authorization Context
         ↓
Query → Hybrid Search → Metadata Filtering
         ↓
Permission Filtering → Authorized Chunks
         ↓
Context Assembly → LLM → Response
```

### Document Classification

| Level | Examples | Access |
|-------|----------|--------|
| Public | Public policies, FAQs | All authenticated users |
| Internal | Internal docs, procedures | Department members |
| Confidential | Financial data, legal docs | Authorized roles only |
| Restricted | Employee PII, trade secrets | Specific individuals |

### Permission Model

```
Document
├── classification: public | internal | confidential | restricted
├── department: engineering | hr | finance | legal
├── owner: creator employee ID
├── viewers: [role, department, specific_users]
└── last_updated: timestamp
```

### Multi-Tenant Isolation

| Strategy | Isolation Level | Cost | Complexity |
|----------|----------------|------|------------|
| Separate databases | Highest | Highest | High |
| Separate schemas | High | High | Medium |
| Tenant ID filtering | Medium | Low | Low |
| Separate vector namespaces | High | Medium | Medium |
| Infrastructure isolation | Highest | Highest | Highest |

---

## 7. Scaling Considerations

| Documents | Strategy |
|-----------|----------|
| 1,000 | Single vector DB, basic chunking |
| 10,000 | Metadata filtering, incremental indexing |
| 100,000 | Sharded vector DB, parallel ingestion |
| 1,000,000 | Distributed vector DB, streaming ingestion |
| 100,000,000 | Multi-cluster, tiered storage, hybrid search |

### Scaling Bottlenecks

| Component | Bottleneck | Solution |
|-----------|-----------|----------|
| Ingestion | Parse speed | Parallel processing, distributed workers |
| Embedding | Generation time | Batch embedding, GPU acceleration |
| Vector DB | Search latency | Sharding, indexing optimization |
| Metadata DB | Query complexity | Caching, denormalization |
| Reranking | Latency | Async reranking, model optimization |

---

## 8. Cost Model

### Per-Component Estimates (100,000 documents, 50,000 queries/day)

| Component | Cost Driver | Unit Cost | Monthly Estimate | Optimization |
|-----------|-------------|-----------|------------------|--------------|
| Embedding API | Per token | $0.0001/1K tokens | $100-300 | Batch processing, caching |
| Vector DB | Per million vectors | $70/M vectors | $200-500 | Tiered storage |
| Metadata DB | Per GB stored | $0.10/GB | $50-100 | Compression |
| Document Storage | Per GB | $0.02/GB | $20-50 | Lifecycle policies |
| Ingestion Compute | Per hour | $0.10/hr | $72-150 | Auto-scaling |
| Reranking | Per query | $0.001/query | $1,500 | Selective reranking |
| Kafka | Per million events | $1/M events | $50-100 | Batching |

### Total Monthly Estimate

| Documents | Queries/Day | Est. Monthly Cost |
|-----------|-------------|-------------------|
| 1,000 | 500 | $100-300 |
| 10,000 | 5,000 | $500-1,500 |
| 100,000 | 50,000 | $2,000-5,000 |
| 1,000,000 | 500,000 | $8,000-20,000 |

### Key Cost Drivers

1. **Embedding generation** — 25-35% of total cost
2. **Reranking** — 20-30% of total cost
3. **Vector DB storage** — 15-25% of total cost
4. **Ingestion compute** — 10-20% of total cost

### Cost Optimization Strategies

| Strategy | Potential Savings | Complexity |
|----------|-------------------|------------|
| Batch embedding | 30-50% | Low |
| Selective reranking | 20-30% | Medium |
| Semantic caching | 15-25% | Low |
| Tiered vector storage | 10-20% | Medium |
| Incremental indexing | 10-15% | Medium |

---

## Key Takeaways

```
┌─────────────────────────────────────────────────────────────────┐
│                DAY 05 ARCHITECTURE TAKEAWAYS                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Data architecture is the foundation of AI quality           │
│                                                                 │
│  2. Ingestion → Processing → Storage → Retrieval is the core   │
│     pipeline                                                    │
│                                                                 │
│  3. Chunking and metadata are architectural decisions           │
│                                                                 │
│  4. Hybrid search (keyword + vector) outperforms pure semantic  │
│                                                                 │
│  5. Authorization must happen at the retrieval level            │
│                                                                 │
│  6. Freshness SLAs drive ingestion architecture                 │
│                                                                 │
│  7. Versioning and deletion are platform engineering problems   │
│                                                                 │
│  8. Multi-tenant isolation requires careful design              │
│                                                                 │
│  9. Data governance and AI cannot be separated                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```
