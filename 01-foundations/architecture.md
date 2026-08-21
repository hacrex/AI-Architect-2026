# Day 01 — Architecture: AI Knowledge Assistant

## Table of Contents

1. [The Problem](#1-the-problem)
2. [Requirements](#2-requirements)
3. [Architecture Evolution](#3-architecture-evolution)
4. [Component Details](#4-component-details)
5. [Data Flow](#5-data-flow)
6. [Failure Scenarios](#6-failure-scenarios)
7. [Scaling Considerations](#7-scaling-considerations)
8. [Security Architecture](#8-security-architecture)
9. [Cost Model](#9-cost-model)
10. [Key Takeaways](#10-key-takeaways)

## 1. The Problem

Design an internal AI Knowledge Assistant for a company.

Employees should be able to ask:
- "What is our leave policy?"
- "How do I request access to AWS?"
- "What is the company's security policy?"

The system should answer using internal documentation.

---

## Requirements

| Category | Requirement |
|----------|-------------|
| Users | 10,000 employees |
| Data source | Internal company documents |
| Approach | RAG-based answers |
| Access control | Role-based document access |
| Model strategy | Multiple LLM providers |
| Compliance | Audit logging |
| Uptime | High availability |
| Budget | Cost monitoring |

---

## Architecture Evolution

### Stage 1: Basic Architecture

Don't worry about implementation yet. Draw:

```
                  Employee
                     │
                     ▼
              ┌─────────────┐
              │ Application │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │ API Gateway │
              └──────┬──────┘
                     │
                     ▼
             ┌──────────────┐
             │ AI Assistant │
             └──────┬───────┘
                    │
              ┌─────┴─────┐
              ▼           ▼
        Retrieval       LLM
              │           │
              ▼           │
        Vector Store      │
              │           │
              └─────┬─────┘
                    ▼
                 Answer
```

Don't worry if this looks basic. Today we're learning to see the system.

### Stage 2: Add Architecture Concerns

Now add:
- Authentication
- Authorization
- Logging
- Metrics
- Tracing
- Caching
- Rate Limiting
- Secrets Management
- Audit Logs

Your architecture starts becoming:

```
                       Employee
                           │
                           ▼
                    Authentication
                           │
                           ▼
                     API Gateway
                           │
               ┌───────────┴───────────┐
               │                       │
               ▼                       ▼
        AI Application             Observability
               │
        ┌──────┴───────┐
        │              │
        ▼              ▼
    Retrieval        Model Gateway
        │              │
        ▼         ┌────┴────┐
   Vector DB      │         │
                  ▼         ▼
              Managed    Self-hosted
                LLM         LLM
```

**Now you're starting to think like an architect.**

---

## Component Details

### API Gateway
- Rate limiting per user/team
- Request routing
- Authentication verification
- Request/response logging

### AI Application
- Query understanding
- Intent classification
- Response synthesis
- Error handling

### Retrieval Layer
- Query embedding
- Vector similarity search
- Metadata filtering
- Reranking

### Model Gateway
- Provider routing (OpenAI, Anthropic, self-hosted)
- Fallback logic
- Cost tracking
- Load balancing

### Observability
- Request tracing (OpenTelemetry)
- Latency metrics
- Error rates
- Token consumption
- User satisfaction signals

---

## Data Flow

```
1. Employee asks question
         ↓
2. Authentication + Authorization check
         ↓
3. API Gateway validates + rate limits
         ↓
4. AI Application processes query
         ↓
5. Query embedding generated
         ↓
6. Vector DB retrieves relevant documents
         ↓
7. Context assembled (query + retrieved docs)
         ↓
8. Model Gateway selects provider
         ↓
9. LLM generates answer
         ↓
10. Response validated + logged
         ↓
11. Answer returned to employee
```

---

## Failure Scenarios

| Failure | Impact | Mitigation |
|---------|--------|------------|
| LLM provider down | No answers | Fallback to secondary provider or cached responses |
| Vector DB down | No retrieval | Return cached answers or "unable to search" message |
| Model takes 30s | Poor UX | Timeout + streaming response |
| Rate limit hit | Blocked users | Queue + priority routing |
| Bad data in docs | Wrong answers | Source attribution + feedback loop |
| Prompt injection | Security risk | Input validation + output filtering |

---

## Scaling Considerations

| Users | Strategy |
|-------|----------|
| 100 | Single instance, basic caching |
| 1,000 | Horizontal scaling, CDN for static content |
| 10,000 | Load balancing, request queuing, model caching |
| 100,000 | Multi-region, model routing, semantic caching |

---

## Security Architecture

```
Employee
    │
    ▼
SSO / Identity Provider
    │
    ▼
API Gateway (JWT validation)
    │
    ▼
Authorization Service (role + document permissions)
    │
    ▼
AI Application
    │
    ├── Audit Log (every query + response)
    ├── Input Validation (prompt injection prevention)
    └── Output Filtering (sensitive data redaction)
```

---

## Cost Model

### Per-Component Estimates

| Component | Cost Driver | Unit Cost | Monthly (10K users) | Optimization |
|-----------|-------------|-----------|---------------------|--------------|
| LLM API | Per token | $0.03/1K input, $0.06/1K output | $150-450 | Semantic caching, model routing |
| Embedding | Per document | $0.0001/doc | $50 | Batch processing |
| Vector DB | Per GB stored | $0.25/GB | $25-100 | Tiered storage |
| Compute | Per hour | $0.10/hr (2 instances) | $144 | Auto-scaling |
| Storage | Per GB | $0.02/GB | $10 | Lifecycle policies |
| Auth/API Gateway | Per request | $1/1M requests | $10 | Caching |

### Total Monthly Estimate

| Scenario | Users | Requests/Day | Est. Monthly Cost |
|----------|-------|--------------|-------------------|
| **Pilot** | 100 | 500 | $200-400 |
| **Small** | 1,000 | 5,000 | $500-1,000 |
| **Medium** | 10,000 | 50,000 | $1,500-3,000 |
| **Large** | 100,000 | 500,000 | $8,000-15,000 |

### Key Cost Drivers

1. **LLM API calls** — 40-60% of total cost
2. **Compute (GPU/CPU)** — 20-30% of total cost
3. **Vector DB storage** — 5-10% of total cost

### Cost Optimization Strategies

| Strategy | Potential Savings |
|----------|-------------------|
| Model routing (simple → cheap model) | 40-60% |
| Semantic caching (avoid re-querying) | 20-30% |
| Prompt compression | 10-15% |
| Batch embedding | 5-10% |

---

## Today's Architect Questions

Before moving to Day 2, answer these yourself.

### Architecture
1. Why do we need an API Gateway?
2. Why should the model be behind a Model Gateway?
3. Where should authentication happen?
4. Where should authorization happen?
5. Where should conversation state live?

### Data
6. Where are documents stored?
7. Where are embeddings stored?
8. How do we handle document updates?
9. How do we handle document deletion?

### Reliability
10. What happens if the LLM provider goes down?
11. What happens if the vector database goes down?
12. What happens if the model takes 30 seconds to respond?

### Security
13. Can every employee access every document?
14. How do we prevent sensitive data from entering prompts?

### Cost
15. What happens when usage increases 100x?
16. How do we control token consumption?

### Business
17. How do we know this system is actually useful?

---

## Day 01 Challenge

**Design the architecture for:**

An enterprise AI assistant used by 10,000 employees.

**Requirements:**
- 10,000 users
- Internal company documents
- RAG-based answers
- Role-based document access
- Multiple LLM providers
- Audit logging
- High availability
- Cost monitoring

**Don't design the perfect architecture. Design the architecture you can defend.**

---

## 10. Key Takeaways

```
┌─────────────────────────────────────────────────────────────────┐
│              DAY 01 ARCHITECTURE KEY TAKEAWAYS                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Start with requirements, not technology choices             │
│                                                                 │
│  2. Architecture evolves: Basic → Concerns → Production         │
│                                                                 │
│  3. Every component creates architectural decisions             │
│                                                                 │
│  4. Failure scenarios drive resilience design                   │
│                                                                 │
│  5. Security is not an afterthought — design it in              │
│                                                                 │
│  6. Cost model must be understood before scaling                │
│                                                                 │
│  7. Design the architecture you can defend, not the perfect one │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```
