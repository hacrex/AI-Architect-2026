# Day 05 — Data Architecture for AI: Exercise

**Estimated Time**: 4-5 hours total

| Exercise | Task | Time |
|----------|------|------|
| A | Build a RAG data pipeline | 60 min |
| B | Chunking experiment | 45 min |
| C | Security experiment | 40 min |
| D | Data architecture diagram | 40 min |
| E | Data architecture decision record | 30 min |
| - | Run sample app | 20 min |

## Overview

Today's exercises focus on **data ingestion**, **chunking strategies**, **security at the data layer**, and **data architecture design**. You'll build the data pipeline that feeds your AI system.

---

## Exercise A: Build a RAG Data Pipeline

### Objective

Implement a complete data pipeline from documents to searchable embeddings.

### Architecture

```
Documents → Parser → Chunker → Embedding Model → Vector DB → Metadata
```

### Steps

1. **Collect documents** — Gather 5-10 documents of different types:

```
docs/
├── security-policy.pdf
├── kubernetes-guide.md
├── leave-policy.pdf
├── cloud-policy.md
└── incident-response.md
```

2. **Implement parsing** — Extract text from each format:

| Format | Parser |
|--------|--------|
| PDF | PyPDF2, pdfplumber, or Tika |
| Markdown | Direct read |
| Word | python-docx |
| HTML | BeautifulSoup |

3. **Implement chunking** — Split documents into chunks:

```python
def chunk_document(text, chunk_size=500, overlap=50):
    """
    Split text into chunks with overlap.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks
```

4. **Generate embeddings** — Use an embedding model:

```python
def generate_embeddings(chunks, model="text-embedding-ada-002"):
    """
    Generate embeddings for each chunk.
    """
    embeddings = []
    for chunk in chunks:
        embedding = openai.Embedding.create(
            input=chunk,
            model=model
        )
        embeddings.append(embedding['data'][0]['embedding'])
    return embeddings
```

5. **Store in vector DB** — Index with metadata:

```python
def store_in_vectordb(chunks, embeddings, metadata):
    """
    Store chunks with embeddings and metadata.
    """
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        vectordb.upsert(
            id=f"chunk_{i}",
            vector=embedding,
            metadata={
                "text": chunk,
                "department": metadata["department"],
                "classification": metadata["classification"],
                "source": metadata["source"],
                "updated_at": metadata["updated_at"]
            }
        )
```

### Measurement Template

| Metric | Value |
|--------|-------|
| Documents ingested | |
| Total chunks created | |
| Average chunk size (tokens) | |
| Embedding dimensions | |
| Vector DB size | |
| Ingestion time | |

### Deliverable

Working data pipeline with 5 documents ingested and searchable.

---

## Exercise B: Chunking Experiment

### Objective

Compare different chunking strategies and their impact on retrieval quality.

### Setup

Take one document and create three versions:

#### Version A: Poor Chunking

Split every 100 characters with no overlap:

```python
def poor_chunking(text):
    return [text[i:i+100] for i in range(0, len(text), 100)]
```

#### Version B: Fixed-Size Chunking

Split every 500 tokens with 50-token overlap:

```python
def fixed_chunking(text, chunk_size=500, overlap=50):
    # Split by token count
    pass
```

#### Version C: Structure-Aware Chunking

Split by sections, paragraphs, and semantic boundaries:

```python
def structure_aware_chunking(text):
    # Split by headings
    # Split by paragraphs
    # Respect semantic boundaries
    pass
```

### Test Queries

Run these queries against each version:

1. "What is our Kubernetes security policy?"
2. "How do I request access to AWS?"
3. "What is the incident response process?"

### Measurement Template

| Metric | Version A | Version B | Version C |
|--------|-----------|-----------|-----------|
| Number of chunks | | | |
| Average chunk size | | | |
| Retrieval relevance (1-5) | | | |
| Answer quality (1-5) | | | |
| Context size (tokens) | | | |
| Latency (ms) | | | |

### Deliverable

Comparison table with your findings and recommendation for which chunking strategy to use.

---

## Exercise C: Security Experiment

### Objective

Verify that document-level authorization works at the retrieval level.

### Setup

1. **Create two users:**

```python
users = {
    "user_a": {
        "name": "Alice (Engineering)",
        "department": "engineering",
        "clearance": "internal"
    },
    "user_b": {
        "name": "Bob (HR)",
        "department": "hr",
        "clearance": "internal"
    }
}
```

2. **Create documents with different permissions:**

```python
documents = {
    "eng-doc-1": {
        "title": "Kubernetes Deployment Guide",
        "department": "engineering",
        "classification": "internal"
    },
    "hr-doc-1": {
        "title": "Leave Policy 2026",
        "department": "hr",
        "classification": "internal"
    }
}
```

3. **Implement permission filtering:**

```python
def filter_by_permissions(chunks, user_context):
    """
    Filter chunks based on user permissions.
    """
    return [
        chunk for chunk in chunks
        if has_permission(user_context, chunk)
    ]

def has_permission(user_context, chunk):
    """
    Check if user has access to chunk.
    """
    if chunk["classification"] == "public":
        return True
    if chunk["department"] == user_context["department"]:
        return True
    if user_context["clearance"] == "admin":
        return True
    return False
```

### Test Queries

Ask both users the same questions:

1. "What is our deployment process?"
2. "What is our leave policy?"
3. "How do I request time off?"
4. "How do I deploy to production?"

### Expected Results

| Query | User A (Engineering) | User B (HR) |
|-------|---------------------|-------------|
| Deployment process | ✓ Should see | ✕ Should NOT see |
| Leave policy | ✕ Should NOT see | ✓ Should see |
| Request time off | ✕ Should NOT see | ✓ Should see |
| Deploy to production | ✓ Should see | ✕ Should NOT see |

### Measurement Template

| Query | User A Results | User B Results | Correct Filtering? |
|-------|---------------|----------------|-------------------|
| | | | |

### Deliverable

Completed test results verifying permission filtering works correctly.

---

## Exercise D: Data Architecture Diagram

### Objective

Design the complete data architecture for the Enterprise AI Knowledge Assistant.

### Template

Include these components:

```
Data Sources
├── Documents (PDFs, Word, Markdown)
├── Databases (PostgreSQL, MySQL)
├── APIs (Internal, External)
└── Wiki (Confluence, Notion)

Ingestion Layer
├── Batch Pipeline (nightly)
├── Streaming (Kafka)
└── Event-driven (webhooks)

Processing Layer
├── Document Parser
├── OCR
├── Cleaning
├── Chunking
└── Metadata Extraction

Storage Layer
├── Embedding Model
├── Vector DB
├── Metadata DB
└── Document Storage (S3)

Retrieval Layer
├── Hybrid Search
├── Metadata Filtering
├── Permission Filtering
└── Reranking

Security Layer
├── Authentication
├── Authorization
├── Audit Logging
└── Data Classification
```

### Deliverable

Complete data architecture diagram with all components and data flows.

---

## Exercise E: Data Architecture Decision Record

### Objective

Write a decision document explaining your data architecture choices.

### Template

```
## Why This Data Architecture?

[Explain why this architecture is appropriate for your use case]

## Ingestion Strategy

- Batch: [frequency]
- Streaming: [use cases]
- Event-driven: [use cases]
- Why: [reasoning]

## Chunking Strategy

- Method: [structure-aware / fixed-size / semantic]
- Chunk size: [tokens]
- Overlap: [tokens]
- Why: [reasoning]

## Vector DB Choice

- Database: [name]
- Index type: [type]
- Why: [reasoning]

## Metadata Strategy

- Fields: [list]
- Why: [reasoning]

## Security Model

- Authorization level: [document / chunk / query]
- Why: [reasoning]

## Freshness Requirements

- Update frequency: [real-time / hourly / daily]
- Why: [reasoning]

## What Would Make Me Change This Architecture?

- [ ] More documents (scale)
- [ ] Different data types (images, audio)
- [ ] Real-time requirements
- [ ] Multi-tenant requirements
- [ ] Compliance requirements

## Cost Estimate

- Monthly embedding cost: $[amount]
- Monthly vector DB cost: $[amount]
- Monthly ingestion cost: $[amount]
- Total: $[amount]
```

### Deliverable

Completed data architecture decision document.

---

## Day 05 Final Deliverables

By the end of Day 05, you should have:

1. **Working Data Pipeline** (Exercise A)
2. **Chunking Comparison** (Exercise B)
3. **Security Verification** (Exercise C)
4. **Data Architecture Diagram** (Exercise D)
5. **Data Architecture Decision Record** (Exercise E)
6. **Sample App Running** (see sample-app/README.md)

### Self-Assessment Questions

Answer these before moving to Day 06:

### Data Architecture
1. What is the difference between a data lake and data warehouse?
2. When would you use batch ingestion?
3. When would you use streaming?
4. Why does data freshness matter for AI?

### RAG Data Pipeline
5. What is chunking and why does it matter?
6. Why is metadata important in RAG?
7. What is hybrid search?
8. Why might reranking improve retrieval?

### Data Lifecycle
9. How should document updates affect embeddings?
10. How do you handle document deletion?
11. Why does data lineage matter?

### Security
12. How do you enforce document-level authorization?
13. How would you isolate tenants?
14. What data should never be sent to an external LLM provider?

### Scaling
15. How would you design the data layer for 100 million documents?
16. Where would Kafka fit into an AI architecture?

---

## Key Takeaways

```
┌─────────────────────────────────────────────────────────────────┐
│              DAY 05 EXERCISE KEY TAKEAWAYS                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Data preparation is an architectural variable that affects  │
│     AI quality                                                  │
│                                                                 │
│  2. Chunking strategy directly impacts retrieval quality        │
│                                                                 │
│  3. Metadata enables filtering, authorization, and freshness    │
│                                                                 │
│  4. Security must be enforced at the data retrieval level       │
│                                                                 │
│  5. Measure before deciding — don't guess on chunking           │
│                                                                 │
│  6. Authorization filtering prevents data leakage               │
│                                                                 │
│  7. Data architecture decisions have long-term cost implications│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```
