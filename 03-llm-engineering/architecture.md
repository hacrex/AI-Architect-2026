# Day 03 — Architecture: LLM Engineering Patterns

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Component Responsibilities](#2-component-responsibilities)
3. [Data Flow](#3-data-flow)
4. [Failure Scenarios](#4-failure-scenarios)
5. [Security Architecture](#5-security-architecture)
6. [Scaling Considerations](#6-scaling-considerations)
7. [Cost Model](#7-cost-model)
8. [Key Takeaways](#8-key-takeaways)

---

## 1. System Overview

### Day 03 Production AI Platform

```
                           User
                            │
                            ▼
                     ┌─────────────┐
                     │ API Gateway │
                     └──────┬──────┘
                            │
                            ▼
                     ┌─────────────┐
                     │ AI Gateway  │
                     └──────┬──────┘
                            │
              ┌─────────────┼─────────────┐
              ↓             ↓             ↓
             RAG          Agent          Router
              │             │             │
              ↓             ↓             ↓
         Retriever        Tools        Models
              │             │             │
              ↓             ↓             │
          Vector DB       APIs             │
              │             │              │
              └─────────────┼──────────────┘
                            ↓
                    Context Assembly
                            ↓
                     Model Gateway
                            ↓
                  ┌─────────┼─────────┐
                  ↓         ↓         ↓
               Small      Medium     Large
```

---

## 2. Component Responsibilities

### API Gateway
- Authentication verification
- Rate limiting per user/team
- Request validation
- Request/response logging

### AI Gateway
- Model routing based on complexity
- Token tracking and budget enforcement
- Policy enforcement
- Provider abstraction
- Fallback handling

### RAG Pipeline
- Document ingestion and chunking
- Embedding generation
- Semantic search
- Metadata filtering
- Reranking
- Permission filtering

### Agent System
- Task reasoning and planning
- Tool invocation
- State management
- Multi-agent orchestration
- Handoffs between agents

### Model Gateway
- Provider abstraction (OpenAI, Anthropic, self-hosted)
- Load balancing across providers
- Cost optimization through routing
- Latency-based routing
- Automatic failover

---

## 3. Data Flow

```
1. User sends request
         ↓
2. API Gateway authenticates + rate limits
         ↓
3. AI Gateway classifies request complexity
         ↓
4. Router selects appropriate model tier
         ↓
5. RAG pipeline retrieves relevant documents
         ↓
6. Agent processes task (if complex)
         ↓
7. Context Assembly combines all information
         ↓
8. Model Gateway routes to selected provider
         ↓
9. LLM generates response
         ↓
10. Response validated + logged
         ↓
11. Answer returned to user
```

---

## 4. Failure Scenarios

| Component | Failure | Impact | Mitigation |
|-----------|---------|--------|------------|
| RAG retrieval | Vector DB down | No relevant context | Return cached responses or "unable to search" message |
| RAG retrieval | Poor retrieval quality | Wrong answers | Reranking, hybrid search, feedback loop |
| Agent | Agent timeout | Incomplete task | Fallback to default response, retry with backoff |
| Agent | Agent error | Wrong tool call | Validation, approval workflows, rollback |
| Agent | Agent unavailable | No response | Route to alternate agent or human escalation |
| Tool | Tool invocation fails | Action not completed | Retry, graceful degradation, alert |
| Tool | Malicious prompt | Unauthorized action | Input validation, least privilege, audit logging |
| Model Gateway | Primary provider down | No inference | Automatic failover to secondary provider |
| Model Gateway | All providers down | Complete failure | Cached responses, queue for retry, alert |
| Context | Context window overflow | Truncated information | Context compression, prioritization, summarization |
| State | State store down | Lost conversation | Stateless fallback, session recovery |

---

## 5. Security Architecture

```
User → Identity Provider → JWT Validation
         ↓
API Gateway → Authorization Check
         ↓
AI Gateway → Policy Enforcement
         ↓
    ┌────┴────┐
    ↓         ↓
  RAG       Agent
    │         │
    ↓         ↓
Permission  Tool Auth
 Filtering  + Validation
    │         │
    └────┬────┘
         ↓
    Audit Logging
```

### Security Boundaries

| Boundary | Controls |
|----------|----------|
| API Gateway | JWT validation, rate limiting, input sanitization |
| RAG Pipeline | Permission filtering, document-level access control |
| Agent System | Tool authorization, least privilege, approval workflows |
| Tool Layer | Authentication, input validation, output filtering, audit logging |
| Model Gateway | Data sensitivity routing, PII detection, output filtering |

---

## 6. Scaling Considerations

| Users | Concurrent | Strategy |
|-------|------------|----------|
| 100 | 10 | Single instance, basic RAG, one model |
| 1,000 | 100 | Horizontal scaling, semantic caching, model routing |
| 10,000 | 500 | Load balancing, request queuing, multi-model gateway |
| 100,000 | 5,000 | Multi-region, distributed RAG, GPU inference, CDN |

### Scaling Bottlenecks

| Component | Bottleneck | Solution |
|-----------|-----------|----------|
| RAG | Vector search latency | Sharding, indexing optimization, caching |
| Agent | Orchestration overhead | Async processing, parallel tool calls |
| Context | Window limits | Context compression, summarization |
| Model | Inference latency | Batching, model routing, multiple endpoints |

---

## 7. Cost Model

### Per-Component Estimates (10,000 users, 50,000 requests/day)

| Component | Cost Driver | Unit Cost | Monthly Estimate | Optimization |
|-----------|-------------|-----------|------------------|--------------|
| LLM API | Per token | $0.03/1K input, $0.06/1K output | $2,000-5,000 | Model routing, semantic caching |
| Embeddings | Per document | $0.0001/doc | $50-100 | Batch processing |
| Vector DB | Per GB stored | $0.25/GB | $100-300 | Tiered storage, compression |
| Agent Compute | Per request | $0.001/request | $1,500 | Simplified workflows, caching |
| Model Gateway | Per routing decision | Negligible | $50 | - |
| API Gateway | Per request | $1/1M requests | $50 | Caching |
| Storage | Per GB | $0.02/GB | $20 | Lifecycle policies |

### Total Monthly Estimate

| Scenario | Users | Requests/Day | Est. Monthly Cost |
|----------|-------|--------------|-------------------|
| **Pilot** | 100 | 500 | $300-600 |
| **Small** | 1,000 | 5,000 | $1,000-2,500 |
| **Medium** | 10,000 | 50,000 | $4,000-8,000 |
| **Large** | 100,000 | 500,000 | $15,000-30,000 |

### Key Cost Drivers

1. **LLM API calls** — 40-55% of total cost
2. **Agent orchestration** — 15-25% of total cost
3. **Compute (RAG + routing)** — 10-20% of total cost
4. **Vector DB storage** — 5-10% of total cost

### Cost Optimization Strategies

| Strategy | Potential Savings | Complexity |
|----------|-------------------|------------|
| Model routing (simple → cheap model) | 40-60% | Medium |
| Semantic caching (avoid re-querying) | 20-30% | Low |
| Agent simplification (fewer steps) | 15-25% | Low |
| Context compression | 10-15% | Medium |
| Batch embedding | 5-10% | Low |

---

## Key Takeaways

```
┌─────────────────────────────────────────────────────────────────┐
│                DAY 03 ARCHITECTURE TAKEAWAYS                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Production AI = API Gateway + AI Gateway + RAG + Agents    │
│     + Tools + Model Gateway + Context Assembly                  │
│                                                                 │
│  2. Every component creates architectural decisions             │
│                                                                 │
│  3. Tools are security boundaries — they need auth, validation │
│     least privilege, audit logging, approval workflows          │
│                                                                 │
│  4. Multi-agent adds latency, failure points, cost — only use  │
│     when value justifies complexity                             │
│                                                                 │
│  5. AI Gateway is the control point for routing, auth, rate    │
│     limiting, token tracking, fallback, provider abstraction    │
│                                                                 │
│  6. Provider abstraction = loose coupling = resilience          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```
