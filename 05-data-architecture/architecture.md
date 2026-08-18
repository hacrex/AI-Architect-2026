# Data Architecture — Data Flow Diagram

## Enterprise knowledge assistant data flow

```
┌─────────────┐   ┌──────────────┐   ┌──────────────┐
│ Source       │──▶│ Ingestion    │──▶│ Transform    │
│ Systems     │   │ (Kafka)      │   │ (ETL/ELT)   │
│ (Confluence,│   └──────────────┘   └──────┬───────┘
│  SharePoint,│                              │
│  S3, DBs)   │                    ┌─────────┴─────────┐
└─────────────┘                    │                   │
                                   ▼                   ▼
                          ┌──────────────┐   ┌──────────────┐
                          │ Document     │   │ Metadata     │
                          │ Storage      │   │ Store        │
                          └──────┬───────┘   └──────┬───────┘
                                 │                   │
                                 ▼                   │
                          ┌──────────────┐           │
                          │ Embedding    │◀──────────┘
                          │ Pipeline     │
                          └──────┬───────┘
                                 │
                                 ▼
                          ┌──────────────┐
                          │ Vector DB    │◀──── Retrieval Query
                          │ (Pinecone,   │
                          │  Weaviate)   │
                          └──────────────┘
```

## Key considerations

- **Access control:** Filter by document permissions at query time
- **Audit trail:** Log all retrieval events
- **Freshness:** Re-embed when source documents change
- **Deletion:** Propagate source deletions to vector index
