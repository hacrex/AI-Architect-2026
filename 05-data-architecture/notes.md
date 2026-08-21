# Day 05 — Data Architecture for AI

> **Building on Day 04**: Yesterday we built the infrastructure layer for our AI platform — GPUs, Kubernetes, inference serving, and deployment patterns. Today we move to one of the most important layers underneath it: Data.

AI systems are often described as model-centric systems. In production, they are usually data-centric systems with models in the middle. A powerful model with poor, stale, inaccessible, or incorrectly governed data can still produce a poor system.

Today, we build the data architecture that makes AI systems trustworthy.

---

## Table of Contents

1. [The AI Data Architecture](#1-the-ai-data-architecture)
2. [Why Data Architecture Matters](#2-why-data-architecture-matters)
3. [Structured vs Unstructured Data](#3-structured-vs-unstructured-data)
4. [Data Lake, Warehouse and Lakehouse](#4-data-lake-warehouse-and-lakehouse)
5. [Data Ingestion](#5-data-ingestion)
6. [Freshness Is an Architecture Requirement](#6-freshness-is-an-architecture-requirement)
7. [RAG Data Pipeline](#7-rag-data-pipeline)
8. [Chunking](#8-chunking)
9. [Metadata](#9-metadata)
10. [Vector Databases](#10-vector-databases)
11. [Don't Treat Vector Search as the Only Search](#11-dont-treat-vector-search-as-the-only-search)
12. [Reranking](#12-reranking)
13. [Data Lineage](#13-data-lineage)
14. [Versioning](#14-versioning)
15. [The Security Problem](#15-the-security-problem)
16. [Multi-Tenant AI Data](#16-multi-tenant-ai-data)
17. [Kafka and AI](#17-kafka-and-ai)
18. [Batch vs Streaming Data](#18-batch-vs-streaming-data)
19. [Data Governance](#19-data-governance)
20. [Our Enterprise AI Knowledge Assistant](#20-our-enterprise-ai-knowledge-assistant)
21. [Day 05 Hands-On Lab](#21-day-05-hands-on-lab)
22. [Day 05 Experiment](#22-day-05-experiment)
23. [Day 05 Security Experiment](#23-day-05-security-experiment)
24. [Day 05 Architect Questions](#24-day-05-architect-questions)
25. [Day 05 Deliverables](#25-day-05-deliverables)
26. [Key Takeaways](#26-key-takeaways)

> **Sample App**: See `sample-app/` for a working data pipeline implementation.

## The Goal of Day 05

You do not need to become a database administrator or data engineer.

You need to understand:

- How data architecture shapes AI architecture
- Why data quality is the foundation of AI quality
- How to design ingestion, processing, and retrieval pipelines
- Why chunking and metadata are architectural decisions
- How to enforce authorization at the data layer
- How to handle versioning, freshness, and deletion
- Why data governance and AI cannot be separated

---

## Objective

Understand how data architecture shapes AI architecture — from ingestion to retrieval to governance.

## 1. The AI Data Architecture

Start with the basic picture:

```
                    DATA SOURCES
                         │
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
       Documents      Databases       APIs
          │              │              │
          └──────────────┼──────────────┘
                         ↓
                  Data Ingestion
                         │
                         ↓
                  Data Processing
                         │
             ┌───────────┴───────────┐
             ↓                       ↓
        Structured Data        Unstructured Data
             │                       │
             ↓                       ↓
        Data Warehouse          Object Storage
             │                       │
             └───────────┬───────────┘
                         ↓
                   AI Data Layer
                         │
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
       Metadata       Embeddings      Features
          │              │              │
          └──────────────┼──────────���──┘
                         ↓
                  AI Applications
```

This is much broader than a vector database.

## 2. Why Data Architecture Matters

Consider our Enterprise AI Knowledge Assistant.

We have:

- Company policies
- Engineering documentation
- HR documents
- Security standards
- Internal wiki pages
- Incident reports
- Technical manuals

Suppose the LLM is excellent. But the source data is:

- Outdated
- Duplicated
- Incorrectly indexed
- Missing permissions
- Poorly chunked
- Incomplete

The system can still fail.

The real pipeline is:

```
Data Quality → Retrieval Quality → Context Quality
           → Model Response Quality → User Trust
```

This is why AI quality begins before the model.

## 3. Structured vs Unstructured Data

AI platforms usually deal with both.

**Structured:**

```
Customer
---------
ID
Name
Email
Plan
Status
```

Examples: PostgreSQL, MySQL, financial records, customer records, transactions, metrics

**Unstructured:**

Examples: PDFs, Word documents, presentations, emails, wiki pages, tickets, source code, images, audio

AI applications often need to combine both. For example:

> "Explain the customer's current contract and compare it with our latest pricing policy."

That might require:

```
CRM Database + Contract PDF + Pricing Documentation → AI
```

## 4. Data Lake, Warehouse and Lakehouse

Understand the architectural concepts.

**Data Warehouse:**

```
Applications → ETL/ELT → Data Warehouse → Analytics/BI
```

Optimized primarily for structured analytical workloads.

**Data Lake:**

```
Data Sources → Object Storage → Raw/Processed Data
```

Stores large volumes of raw or semi-structured data.

**Lakehouse:**

Attempts to combine characteristics of lakes and warehouses.

The architect's question is not "Which architecture is fashionable?" It's "What data workloads do we actually have?"

## 5. Data Ingestion

Our AI system needs a reliable way to get data into the platform.

```
                         Sources
                            │
       ┌────────────────────┼────────────────────┐
       ↓                    ↓                    ↓
     GitHub               Wiki                Database
       │                    │                    │
       └────────────────────┼────────────────────┘
                            ↓
                       Ingestion
                            │
                            ↓
                       Processing
```

Ingestion may be:

**Batch:**

```
Every night → Collect data → Process data
```

**Streaming:**

```
Event → Kafka → Processing → Destination
```

**Event-driven:**

```
Document Updated → Event → Embedding Pipeline → Vector Store Updated
```

The correct approach depends on how quickly your AI system needs to reflect changes.

## 6. Freshness Is an Architecture Requirement

Imagine an HR policy changes at 10:00 AM. But your AI system still has the old version at 4:00 PM. A technically healthy AI system can still provide the wrong answer.

Define: **How fresh does the data need to be?**

| Freshness Level | Update Frequency | Use Case |
|----------------|------------------|----------|
| Low | Once per day | Static policies, historical data |
| Medium | Every few hours | Engineering docs, wiki pages |
| High | Near real-time | Incident reports, active projects |
| Critical | Event-driven | Security alerts, compliance changes |

This gives us another architectural dimension:

```
Freshness ↔ Complexity ↔ Cost
```

## 7. RAG Data Pipeline

Yesterday we built the RAG application. Today, look at what happens before retrieval.

```
                 Documents
                     │
                     ▼
              Ingestion Layer
                     │
                     ▼
               Parse / OCR
                     │
                     ▼
                Cleaning
                     │
                     ▼
                 Chunking
                     │
                     ▼
                Embeddings
                     │
              ┌──────┴──────┐
              ↓             ↓
          Vector DB      Metadata DB
```

This is the RAG data pipeline.

## 8. Chunking

Suppose you have a 200-page PDF. You don't want to embed the entire PDF as one giant object. You divide it into meaningful chunks.

```
200-page Document → Chunking → [C1, C2, C3, C4, ...]
```

But chunking isn't simply "Every 500 characters." Good chunking should consider:

- Document structure
- Paragraphs
- Headings
- Tables
- Sections
- Semantic boundaries
- Metadata

Poor chunking can damage retrieval quality.

## 9. Metadata

One of the most underrated parts of RAG architecture.

Each chunk should carry useful metadata:

```
Document:    Security Policy
Department:  Security
Classification: Confidential
Owner:       Security Team
Version:     3.2
Created:     2026-07-15
Updated:     2026-08-10
Access:      Security + Engineering
```

Now retrieval can use more than semantic similarity. It can use:

```
Semantic Similarity + Metadata Filtering + Authorization
```

This dramatically changes the quality and safety of enterprise retrieval.

## 10. Vector Databases

Yesterday we treated the vector database as a component. Today, understand what problem it actually solves.

**Embedding pipeline:**

```
Document → Embedding Model → Vector → Vector Database
```

**Query:**

```
User Question → Embedding Model → Query Vector → Similarity Search → Relevant Chunks
```

Possible technologies: PostgreSQL + pgvector, Qdrant, Milvus, Weaviate, Pinecone

The architect needs to evaluate: latency, scale, filtering, availability, persistence, indexing, operational complexity, cost.

## 11. Don't Treat Vector Search as the Only Search

Semantic search is powerful. But it isn't always enough.

> "Find incident INC-4821." — Keyword search may be better.

> "Why did the payment system experience repeated failures?" — Semantic search becomes more useful.

Enterprise retrieval may use:

```
                    Query
                      │
             ┌────────┴────────┐
             ↓                 ↓
       Keyword Search     Vector Search
             │                 │
             └────────┬────────┘
                      ↓
                 Hybrid Search
                      ↓
                  Reranking
                      ↓
                Top Results
```

This is hybrid retrieval.

## 12. Reranking

Suppose retrieval returns Documents A, B, C, D, E. The first retrieval stage may not perfectly rank them. A reranker can evaluate relevance more deeply.

```
Query → Initial Retrieval → Top 50 Documents → Reranking → Top 5 Documents → LLM
```

This can improve retrieval quality at the cost of additional computation and latency. Architecture = trade-offs.

## 13. Data Lineage

Now imagine someone asks: "Where did this answer come from?"

Your system should ideally be able to trace:

```
Answer → Retrieved Chunk → Document → Source System → Original Record
```

This is data lineage. It becomes important for:

- Debugging
- Compliance
- Auditability
- Trust
- Data quality
- Incident investigation

For enterprise AI, citations and source attribution can be architectural features rather than just UI features.

## 14. Versioning

Documents change:

```
Security Policy v1 → Security Policy v2 → Security Policy v3
```

What happens to old embeddings? You need a strategy for:

- Versioning
- Re-embedding
- Invalidation
- Deletion
- Rollback

A robust pipeline:

```
Document Updated → Change Event → Invalidate Old Version
→ Process New Version → Generate Embedding → Update Vector Store → Update Metadata
```

This is where AI data architecture starts looking like classic platform engineering.

## 15. The Security Problem

Consider document permissions:

- Employee A → Engineering Documents only
- Employee B → HR Documents only
- Admin → Everything

Your RAG pipeline must preserve those permissions.

**Dangerous design:**

```
All Documents → Shared Vector DB → LLM → Any User
```

**Safer design:**

```
User → Identity → Authorization Context → Filtered Retrieval
     → Authorized Chunks → Context → LLM
```

Security must follow the data.

## 16. Multi-Tenant AI Data

Imagine you're building an AI SaaS platform:

```
Tenant A
├── Documents
├── Users
└── Embeddings

Tenant B
├── Documents
├── Users
└── Embeddings
```

You must prevent Tenant A from accessing Tenant B's data.

Isolation strategies: separate databases, separate schemas, tenant IDs, metadata filtering, separate vector namespaces, infrastructure isolation.

The correct choice depends on: risk, scale, compliance, cost, operational complexity.

## 17. Kafka and AI

Streaming becomes important when AI systems need near-real-time data.

```
Application → Event → Kafka → AI Processing → Embedding/Classification → Vector Store
```

Example: A new security incident is created → Kafka Event → Processing Pipeline → Embedding → Knowledge Base Updated.

Now your AI assistant can discover the new information without waiting for a nightly batch process.

## 18. Batch vs Streaming Data

We saw this concept on Day 3 for inference. It applies to data too.

**Batch:**

```
Documents → Nightly Processing → Embeddings → Vector DB
```

**Streaming:**

```
Document Change → Event → Processing → Embedding → Vector DB
```

Streaming gives freshness. Batch can be simpler and cheaper. The architect decides based on requirements.

## 19. Data Governance

Move beyond engineering:

- Who owns the data?
- Who can access it?
- How long should it be retained?
- Can users request deletion?
- Where is it stored?
- Can it cross regions?
- Can it be sent to an external model provider?

```
Data
├── Ownership
├── Classification
├── Access
├── Retention
├── Lineage
├── Residency
├── Quality
└── Deletion
```

AI architecture and data governance cannot be separated in serious enterprise systems.

## 20. Our Enterprise AI Knowledge Assistant

Let's evolve our architecture again.

**Previous architecture:**

```
User → API Gateway → AI Gateway → Model Gateway → Inference → GPU
```

**Now introduce the data platform:**

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

And behind the data layer:

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

Now we're building a real AI data architecture.

## 21. Day 05 Hands-On Lab

Today, create an Enterprise AI Knowledge Pipeline.

Use a small dataset:

```
docs/
├── security-policy.pdf
├── kubernetes-guide.md
├── leave-policy.pdf
├── cloud-policy.md
└── incident-response.md
```

Build:

```
Documents → Parser → Chunker → Embedding Model → Vector DB → Metadata
```

Then test:

```
Question → Embedding → Hybrid/Vector Retrieval → Metadata Filtering → Top-K → LLM
```

## 22. Day 05 Experiment

Take one document and deliberately create three versions:

- **Version A**: Poor chunking
- **Version B**: Fixed-size chunks
- **Version C**: Structure-aware chunks

Then compare: retrieval relevance, answer quality, context size, latency.

The goal is to understand: **Data preparation is an architectural variable that affects AI quality.**

## 23. Day 05 Security Experiment

Create two users:

- User A → Engineering
- User B → HR

Create Engineering and HR documents.

Ask both users the same questions. Verify that:

- User A → Engineering ✓, User A → HR ✕
- User B → HR ✓, User B → Engineering ✕

This is one of the most valuable exercises you can perform during this series.

## 24. Day 05 Architect Questions

Answer these before moving on:

1. What is the difference between a data lake and data warehouse?
2. When would you use batch ingestion?
3. When would you use streaming?
4. Why does data freshness matter for AI?
5. What is chunking?
6. Why is metadata important in RAG?
7. What is hybrid search?
8. Why might reranking improve retrieval?
9. How should document updates affect embeddings?
10. How do you handle document deletion?
11. How do you enforce document-level authorization?
12. How would you isolate tenants?
13. Why does data lineage matter?
14. What happens if the source system changes?
15. What happens if your vector database becomes unavailable?
16. How would you design the data layer for 100 million documents?
17. Where would Kafka fit into an AI architecture?
18. What data should never be sent to an external LLM provider?

## 25. Day 05 Deliverables

By the end of today, create:

### 1. Data Architecture Diagram

Include: data sources, ingestion, processing, storage, embeddings, vector DB, metadata, retrieval.

### 2. RAG Data Pipeline

```
Source → Ingestion → Processing → Chunking → Embedding → Vector Store
```

### 3. Data Security Model

Document: users, roles, permissions, tenant isolation, document classification.

### 4. Retrieval Experiment

Compare at least two retrieval approaches.

### 5. Data Architecture Decision Record

Answer: Why did you choose this data architecture for the AI Knowledge Assistant?

## 26. Key Takeaways

```
┌─────────────────────────────────────────────────────────────────┐
│                     DAY 05 KEY TAKEAWAYS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. AI systems are data-centric systems with models in the      │
│     middle                                                      │
│                                                                 │
│  2. Data Quality → Retrieval Quality → Context Quality →        │
│     Model Quality → User Trust                                  │
│                                                                 │
│  3. Chunking and metadata are architectural decisions that      │
│     affect AI quality                                           │
│                                                                 │
│  4. Hybrid search (keyword + vector) beats pure semantic        │
│     search for many enterprise use cases                        │
│                                                                 │
│  5. Security must follow the data — authorization at the        │
│     retrieval level                                             │
│                                                                 │
│  6. Freshness is an architecture requirement — define SLAs      │
│                                                                 │
│  7. Versioning and deletion are platform engineering problems   │
│                                                                 │
│  8. Data governance and AI cannot be separated in enterprise    │
│     systems                                                     │
│                                                                 │
│  9. An AI system is only as trustworthy as the data             │
│     architecture behind it                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

> **Next**: See Day 06 (`06-mlops-platform/`) to understand MLOps and AI Platform Engineering.
