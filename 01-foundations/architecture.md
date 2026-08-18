# Day 01 — Architecture: AI Knowledge Assistant

## The Problem

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

| Component | Cost Driver | Optimization |
|-----------|-------------|--------------|
| LLM API | Per token | Semantic caching, model routing |
| Embedding | Per document | Batch processing |
| Vector DB | Per GB stored | Tiered storage |
| Compute | Per hour | Auto-scaling |
| Storage | Per GB | Lifecycle policies |

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
