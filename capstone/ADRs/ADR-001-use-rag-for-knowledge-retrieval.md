# ADR-001: Use RAG for Knowledge Retrieval

## Status

Accepted

## Date

2026-08-21

## Context

The Enterprise AI Knowledge Assistant needs to answer employee questions using internal company documentation. The company has:

- 10,000+ documents (PDFs, wiki pages, policies, technical docs)
- Documents update frequently (weekly policy changes, daily technical updates)
- Questions require accurate citations from source documents
- Access control varies by document classification and employee role

We need to choose between:

1. **RAG (Retrieval-Augmented Generation)** — Retrieve relevant documents at query time
2. **Fine-tuning** — Train the model on company documentation
3. **Context stuffing** — Include all documents in the prompt
4. **Direct search** — Keyword search without LLM generation

## Decision

We will use **RAG** as the primary knowledge retrieval mechanism.

## Rationale

### Why RAG?

| Criterion | RAG | Fine-tuning | Context Stuffing | Direct Search |
|-----------|-----|-------------|------------------|---------------|
| Knowledge freshness | Real-time | Stale after training | Always current | Always current |
| Citation support | Native | Poor | Possible | Native |
| Cost at scale | Low | High (retraining) | High (tokens) | Low |
| Accuracy | High | Medium | High | Low |
| Implementation complexity | Medium | High | Low | Low |

### Why Not Fine-tuning?

- Documents update weekly — retraining is expensive and slow
- Fine-tuning changes model behavior, not just knowledge
- Citation from fine-tuned models is unreliable
- Access control cannot be enforced at the model level

### Why Not Context Stuffing?

- 10,000 documents exceed any context window
- Cost would be prohibitive ($100+ per query)
- Latency would be unacceptable (minutes per query)

### Why Not Direct Search?

- No natural language understanding
- No synthesis across multiple documents
- Poor user experience

## Consequences

### Positive

- Real-time knowledge updates (no retraining)
- Native citation support
- Cost-effective at scale
- Access control at retrieval level
- Works with multiple model providers

### Negative

- Retrieval quality directly impacts answer quality
- Requires embedding infrastructure
- Requires vector database
- More complex than simple prompt engineering

### Risks

| Risk | Mitigation |
|------|-----------|
| Poor retrieval quality | Hybrid search, reranking, feedback loops |
| Vector DB outage | Cached responses, graceful degradation |
| Stale embeddings | Incremental re-indexing on document change |
| Permission leakage | Permission filtering in retrieval pipeline |

## Alternatives Considered

### Hybrid RAG + Fine-tuning

Considered for future: fine-tune for style/behavior while using RAG for knowledge. Not needed for initial launch.

### GraphRAG

Considered for complex queries requiring relationship understanding. Deferred to Phase 2.

## Review Date

2026-11-21 (3 months post-launch)
