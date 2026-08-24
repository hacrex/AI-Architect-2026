# System Architecture — Exercise

## Task

Design the complete Enterprise AI Knowledge Platform for 10,000 employees.

Stop building individual components. Design the system.

---

## Scenario

**Enterprise AI Knowledge Platform**

An enterprise AI assistant that helps 10,000 employees find and understand internal company information.

### Requirements

- 10,000 users
- RAG capabilities
- Agent capabilities
- Multiple model providers
- Role-based access control
- Document-level permissions
- High availability (99.9%)
- Model fallback
- Asynchronous document ingestion
- Kubernetes-based infrastructure
- GPU inference
- Managed model fallback
- Evaluation pipeline
- CI/CD
- Observability
- Cost tracking
- Auditability

---

## Exercise 1: System Context Diagram

Create a system context diagram showing who interacts with the system.

### Include

- Users (employees, admins, developers)
- External systems (identity provider, model providers, document systems)
- The AI platform boundary

### Deliverable

A context diagram with all actors and external dependencies.

---

## Exercise 2: Logical Architecture

Design the logical architecture showing all major components.

### Must Include

- API Gateway
- AI Gateway (model routing, rate limiting, policy)
- RAG subsystem (retriever, reranker, vector DB)
- Agent subsystem (planning, tools, guardrails)
- Model Gateway (managed + self-hosted + fallback)
- Context Assembly
- Data Layer (vector DB, relational DB, object storage)
- Platform Layer (registry, evaluation, CI/CD)
- Cross-cutting concerns (security, observability, governance)

### Deliverable

A layered architecture diagram with component relationships.

---

## Exercise 3: Data Flow Diagram

Design the request flow from user question to response.

### Trace the Path

```
User Question
    ↓
API Gateway (auth, rate limit)
    ↓
AI Gateway (routing decision)
    ↓
RAG (query → embedding → retrieve → rerank → context)
    ↓
Agent (plan → tool select → execute) [if needed]
    ↓
Context Assembly
    ↓
Model Gateway (route to best model)
    ↓
Inference
    ↓
Response + Sources + Metadata
```

### Also Design

The document ingestion flow:

```
Document Updated → Event → Queue → Worker → Embedding → Vector Store
```

### Deliverable

Two flow diagrams: request path and ingestion path.

---

## Exercise 4: Deployment Architecture

Design the deployment architecture.

### Must Include

- Kubernetes cluster layout
- GPU node pool
- Service replicas
- Data services (vector DB, relational DB, cache)
- Observability stack
- External service dependencies

### Deliverable

A deployment diagram showing where components run.

---

## Exercise 5: Security Architecture

Design the security architecture that follows the entire request.

### At Each Boundary, Define

| Boundary | Who | What | How |
|----------|-----|------|-----|
| API Gateway | User | Authenticate | SSO/OAuth |
| AI Gateway | Application | Authorize | Policy engine |
| RAG | User | Document access | Doc-level perms |
| Agent | Agent | Tool access | Tool authorization |
| Data | Service | Data access | Encryption + ACL |
| Model | Gateway | Model access | Provider keys |

### Deliverable

A security architecture diagram with enforcement points.

---

## Exercise 6: Architecture Decision Records

Create three ADRs.

### ADR-001: Model Strategy

**Context**: Multiple AI workloads with different quality and latency requirements.

**Document**:
- Options considered
- Decision made
- Consequences (benefits and costs)

### ADR-002: Data / Vector Strategy

**Context**: Need to store and retrieve embeddings for RAG across multiple document types.

**Document**:
- Options considered
- Decision made
- Consequences

### ADR-003: Managed vs Self-Hosted

**Context**: Balance cost, control, and operational complexity.

**Document**:
- Options considered
- Decision made
- Consequences

### Deliverable

Three complete ADR documents.

---

## Exercise 7: Failure Matrix

Document at least 10 failure scenarios.

### Template

| Component | Failure Mode | Impact | Mitigation | Recovery |
|-----------|-------------|--------|------------|----------|
| Model Provider | API down | No inference | Fallback model | Auto-retry |
| Vector DB | Unavailable | No retrieval | Cached embeddings | Auto-reconnect |
| ... | ... | ... | ... | ... |

### Must Cover

- Model provider failures
- Vector DB failures
- Queue overflow
- GPU exhaustion
- Network issues
- Identity provider failures
- Storage issues
- Agent tool failures

### Deliverable

A complete failure matrix with at least 10 scenarios.

---

## Exercise 8: Architecture Review

Perform a self-review of your architecture.

### Requirements Review

- [ ] Did I define the workload?
- [ ] Did I define scale?
- [ ] Did I define latency targets?
- [ ] Did I define availability targets?

### Data Review

- [ ] Where does data originate?
- [ ] How fresh is it?
- [ ] How is it authorized?

### AI Review

- [ ] Why RAG?
- [ ] Why agents?
- [ ] Why these models?
- [ ] Why model routing?

### Infrastructure Review

- [ ] Why Kubernetes?
- [ ] Why GPUs?
- [ ] How does scaling work?

### Reliability Review

- [ ] What fails?
- [ ] What is the fallback?
- [ ] What is the recovery strategy?

### Security Review

- [ ] What can each user access?
- [ ] What can agents do?

### Platform Review

- [ ] How are changes deployed?
- [ ] How are models evaluated?
- [ ] How do we roll back?

### Cost Review

- [ ] What is expensive?
- [ ] How do we control it?

### Deliverable

Completed review checklist with answers for each item.

---

## Deliverable Checklist

Create these artifacts:

### 1. System Context Diagram

- [ ] Users identified
- [ ] External systems mapped
- [ ] Boundaries defined

### 2. Logical Architecture

- [ ] Gateway layer
- [ ] AI layer (RAG, Agents, Tools)
- [ ] Model layer (routing, fallback)
- [ ] Data layer
- [ ] Platform layer
- [ ] Cross-cutting concerns

### 3. Data Flow Diagrams

- [ ] Request path (user → response)
- [ ] Ingestion path (document → vector store)

### 4. Deployment Architecture

- [ ] Kubernetes layout
- [ ] GPU node pool
- [ ] Service replicas
- [ ] Data services
- [ ] Observability stack

### 5. Security Architecture

- [ ] Identity enforcement
- [ ] Authorization model
- [ ] Data access control
- [ ] Agent permissions
- [ ] Audit logging

### 6. Three ADRs

- [ ] ADR-001: Model Strategy
- [ ] ADR-002: Data / Vector Strategy
- [ ] ADR-003: Managed vs Self-Hosted

### 7. Failure Matrix

- [ ] At least 10 failure scenarios
- [ ] Impact documented
- [ ] Mitigation strategies
- [ ] Recovery procedures

### 8. Architecture Review

- [ ] All checklist items answered

---

## Architect Questions

Answer these before moving on:

1. What is the difference between a collection of technologies and an architecture?
2. Why do we define the business problem before choosing technologies?
3. What is the difference between functional and non-functional requirements?
4. Why are architecture boundaries important?
5. How do architecture layers relate to each other?
6. Why is the AI Gateway an architectural boundary?
7. How does treating RAG as a subsystem improve the architecture?
8. When should you use synchronous vs asynchronous processing?
9. What is event-driven AI architecture?
10. How do you design for model provider failure?
11. What are failure domains?
12. Why should security follow the entire request?
13. How do you control agent autonomy?
14. Why is observability a system architecture concern?
15. What is AI cost architecture?
16. What is an Architecture Decision Record?
17. Why should architecture decisions be documented?
18. How do you know when an architecture is complete?

---

## Success Criteria

Your exercise is complete when you can:

1. Design a complete AI system from users to infrastructure
2. Define boundaries, interfaces, and controls
3. Document architecture decisions with ADRs
4. Design reliability and fallback strategies
5. Design security architecture
6. Perform an architecture review
7. Answer all architect questions

---

## Next Steps

After completing Day 07, move to:

**Day 08 → Technology Selection & Build vs Buy**

We stop asking "What technologies can we use?" and start asking "Which technology should we choose, and why?"
