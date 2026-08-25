# ADR-005: Semantic Caching for Cost Optimization

## Status

Accepted

## Date

2026-08-21

## Context

The system handles 50,000+ requests/day. Many queries are similar or identical (e.g., "What is our vacation policy?"). Each request costs $0.003-$0.010 in model inference. We need to reduce redundant inference without sacrificing freshness.

## Options

| Option | Pros | Cons |
|--------|------|------|
| No caching | Simple, no stale data | Full cost per query |
| Exact match cache | Simple, no false positives | Low hit rate for similar queries |
| Semantic cache (Redis) | High hit rate, cost savings | Complexity, stale data risk |

## Decision

We will use **Redis-based semantic caching** with embedding similarity matching.

## Rationale

- 30-40% cost reduction for common query patterns
- Redis already in the stack for session management
- Embedding similarity handles paraphrased queries
- TTL-based expiry manages freshness

## Architecture

```
Query → Embedding → Redis Similarity Search
                         │
              ┌──────────┴──────────┐
              ↓                     ↓
         Cache Hit              Cache Miss
              │                     │
              ↓                     ↓
         Return cached         Full RAG pipeline
         response                    │
                                     ↓
                              Store in cache
```

## Configuration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Similarity threshold | 0.92 | Balance between hit rate and accuracy |
| TTL | 1 hour | Documents update frequently |
| Max cache size | 10GB | Cost-effective Redis allocation |
| Eviction policy | LRU | Most-used queries stay cached |

## Consequences

### Positive

- 30-40% reduction in model API costs
- Faster response times for cached queries
- Reduced load on model providers

### Negative

- Stale responses possible (mitigated by TTL)
- Cache invalidation complexity
- Additional Redis memory cost

## Review Date

2026-11-21 (3 months post-launch)
