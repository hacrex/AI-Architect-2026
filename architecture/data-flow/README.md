# Data Flow — Enterprise AI Knowledge Assistant

## Data Movement

This document describes how data flows through the Enterprise AI Knowledge Assistant, from ingestion to retrieval to response generation.

## Ingestion Flow

```
HR/Admin Uploads Documents
         │
         ▼
    ┌─────────┐
    │ API GW  │ ← Authentication
    └────┬────┘
         │
         ▼
    ┌─────────────┐
    │ Ingestion   │
    │ Pipeline    │
    └────┬────────┘
         │
    ┌────┴────────────────┐
    │                     │
    ▼                     ▼
┌─────────┐        ┌──────────┐
│ Chunking │        │ Metadata │
│ (500 tok)│        │ Extraction│
└────┬────┘        └────┬─────┘
     │                  │
     └────────┬─────────┘
              │
              ▼
       ┌──────────────┐
       │  Embedding   │
       │  Model       │
       └──────┬───────┘
              │
         ┌────┴────┐
         ▼         ▼
    ┌─────────┐ ┌─────────┐
    │Vector DB│ │ Document│
    │(store)  │ │ Metadata│
    └─────────┘ └─────────┘
```

## Query Flow

```
Employee Asks Question
         │
         ▼
    ┌─────────┐
    │ API GW  │ ← JWT Validation + Rate Limiting
    └────┬────┘
         │
         ▼
    ┌─────────────┐
    │ AI Gateway  │ ← Request Classification
    └────┬────────┘
         │
    ┌────┴────────────────┐
    │                     │
    ▼                     ▼
┌──────────────┐   ┌──────────────┐
│ Query        │   │ Authorization│
│ Embedding    │   │ Context      │
└──────┬───────┘   └──────┬───────┘
       │                  │
       └────────┬─────────┘
                │
                ▼
         ┌──────────────┐
         │  Vector DB   │ ← Permission Filtered Search
         │  Retrieval   │
         └──────┬───────┘
                │
                ▼
         ┌──────────────┐
         │  Reranking   │
         └──────┬───────┘
                │
                ▼
         ┌──────────────┐
         │   Context    │ ← Query + Retrieved Docs + History
         │   Assembly   │
         └──────┬───────┘
                │
                ▼
         ┌──────────────┐
         │ Model Gateway│ ← Provider Selection
         └──────┬───────┘
                │
                ▼
         ┌──────────────┐
         │     LLM      │
         └──────┬───────┘
                │
                ▼
         ┌──────────────┐
         │  Validation  │ ← PII Filter + Safety Check
         └──────┬───────┘
                │
                ▼
         ┌──────────────┐
         │   Response   │
         └──────┬───────┘
                │
                ▼
         ┌──────────────┐
         │  Audit Log   │ ← Every query + response logged
         └──────────────┘
```

## Agent Flow (Complex Requests)

```
Complex Request
       │
       ▼
┌──────────────┐
│   Agent      │
│ Orchestrator │
└──────┬───────┘
       │
  ┌────┴─────────────┐
  │                  │
  ▼                  ▼
┌──────────┐   ┌──────────┐
│ Research │   │ Database │
│ Agent    │   │ Agent    │
└────┬─────┘   └────┬─────┘
     │              │
     ▼              ▼
┌──────────┐   ┌──────────┐
│ Search   │   │ Order    │
│ Tool     │   │ Lookup   │
└────┬─────┘   └────┬─────┘
     │              │
     └──────┬───────┘
            │
            ▼
     ┌──────────────┐
     │ Shared State │
     └──────┬───────┘
            │
            ▼
     ┌──────────────┐
     │  Response    │
     │  Assembly    │
     └──────────────┘
```

## Data Storage Patterns

| Data Type | Storage | Retention | Access Pattern |
|-----------|---------|-----------|----------------|
| Documents | S3/GCS | Permanent | Write-once, read-many |
| Embeddings | Vector DB | Until re-indexed | Read-heavy |
| Metadata | PostgreSQL | Permanent | Read/write balanced |
| Conversation History | Redis/PostgreSQL | 30 days | Write-once, read-mostly |
| Audit Logs | Elasticsearch | 1 year | Write-once, read-rarely |
| Cache | Redis | 1 hour | Read-heavy |

## Output Delivery

| Delivery | Use Case | Latency |
|----------|----------|---------|
| Streaming | Interactive chat | TTFT < 500ms |
| Synchronous | API integrations | < 5s |
| Asynchronous | Batch processing | Minutes to hours |
| Webhook | Long-running agents | Event-driven |
