# ADR-004: Vector Database Strategy — Qdrant

## Status

Accepted

## Date

2026-08-21

## Context

The Enterprise AI Knowledge Assistant requires vector storage for document embeddings. We need to support:

- 10,000+ documents with incremental updates
- Department-level namespace isolation
- Hybrid search (semantic + keyword)
- High availability with replication
- Cost-effective at scale

## Options

| Option | Pros | Cons |
|--------|------|------|
| Pinecone | Fully managed, simple | Expensive at scale, vendor lock-in |
| Qdrant | Open source, performant, namespaces | Self-hosted operations |
| Weaviate | Feature-rich, GraphQL | Learning curve, heavier resource usage |
| pgvector | Existing PostgreSQL | Performance limits at scale |

## Decision

We will use **Qdrant** with department-level namespaces.

## Rationale

- Open source — no vendor lock-in
- Good performance at our scale (10K-50K documents)
- Native namespace support for department isolation without separate clusters
- Hybrid search support (semantic + keyword)
- Active community and good Kubernetes integration

## Consequences

### Positive

- Full control over data and infrastructure
- Namespace isolation without additional cost
- Hybrid search built-in
- Kubernetes-native deployment

### Negative

- Self-hosted operations required
- Team needs to learn Qdrant-specific concepts
- Backup and recovery responsibility

## Review Date

2026-11-21 (3 months post-launch)
