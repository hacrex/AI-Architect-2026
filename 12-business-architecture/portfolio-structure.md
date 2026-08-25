# AI Architecture Portfolio Structure

## Portfolio Overview

Three to five strong projects are better than twenty shallow ones.

Each project demonstrates architectural thinking across business, technical, and operational dimensions.

---

## Project 1 — Enterprise AI Knowledge Platform

### Business Context

- **Users:** 10,000 employees across engineering, HR, finance, legal
- **Problem:** Information scattered across 15+ systems, 40% of employee time spent searching
- **Goal:** Reduce search time by 50%, improve knowledge accuracy

### Architecture

```
User → Identity (SSO) → API Gateway → AI Gateway → RAG Pipeline → Model Gateway → Inference
                                        ↓
                            Document Ingestion → Embedding → Vector Store
                                        ↓
                            Observability → Metrics, Logs, Traces
                                        ↓
                            Security → IAM, Authorization, Audit
```

### Key Components

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Gateway | FastAPI + Redis | Request routing, rate limiting |
| RAG | LlamaIndex / LangChain | Retrieval orchestration |
| Vector Store | Qdrant / Weaviate | Document embeddings |
| Models | GPT-4o, Claude, Llama | Multi-model inference |
| Observability | OpenTelemetry | Metrics, logs, traces |
| Security | Keycloak, OPA | IAM, authorization |

### Key Decisions

1. **Multi-model routing** — Cost optimization + fallback
2. **Hybrid search** — Semantic + keyword for precision
3. **Async ingestion** — Non-blocking document updates
4. **Department-level authorization** — Data isolation without full tenant system

### Demonstrates

- RAG architecture at enterprise scale
- Multi-model strategy
- Enterprise IAM integration
- Observability architecture
- FinOps implementation

---

## Project 2 — AI Inference Platform

### Business Context

- **Users:** 5 internal teams, 20+ applications
- **Problem:** Each team manages model deployments independently, duplicating effort
- **Goal:** Shared platform serving 50+ models with unified operations

### Architecture

```
Applications → AI Gateway → Model Router → Model Registry
                         ↓
                    Auto-Scaler → GPU Cluster (A100, H100)
                         ↓
                    Model Cache → Redis
                         ↓
                    Fallback Router → Managed APIs
```

### Key Components

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Gateway | Custom + Envoy | Request routing, auth |
| Router | Weighted routing + health checks | Model selection |
| Orchestrator | Kubernetes + KubeFlow | GPU scheduling |
| Cache | Redis + semantic similarity | Redundant inference reduction |
| Monitoring | Prometheus + Grafana | GPU utilization, latency |

### Key Decisions

1. **Gateway pattern** — Single entry point for all model access
2. **Semantic caching** — 30-40% cost reduction for similar queries
3. **GPU time-sharing** — Dynamic allocation across teams
4. **Fallback strategy** — Self-hosted primary, managed fallback

### Demonstrates

- Platform architecture
- GPU infrastructure management
- Cost optimization at scale
- Multi-tenant model serving

---

## Project 3 — Agent Platform

### Business Context

- **Users:** Enterprise automation teams
- **Problem:** Ad-hoc agent implementations with no governance
- **Goal:** Controlled, auditable, cost-managed agent execution

### Architecture

```
Applications → Agent Runtime → Policy Engine → Tool Registry
                                      ↓
                              Authorization → Tool-level permissions
                                      ↓
                              Audit Logger → Every tool call logged
                                      ↓
                        ┌─────────────┼─────────────┐
                        ↓             ↓             ↓
                    Vector DB      APIs        Databases
```

### Key Components

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Runtime | Custom async runner | Agent execution loop |
| Policy | OPA / Cedar | Authorization policies |
| Registry | FastAPI service | Tool metadata, permissions |
| Audit | Append-only store | Complete tool call history |
| Circuit Breaker | Hystrix pattern | Prevent cascade failures |

### Key Decisions

1. **Policy-based tool authorization** — RBAC + data scope
2. **Mandatory audit logging** — Every tool call recorded
3. **Cost budgets per agent** — Token and call limits
4. **Human approval for high-risk actions** — Write, delete, deploy

### Questions Answered

1. How are agents authenticated? → Service tokens + user context
2. How are tools authorized? → Policy engine with RBAC
3. How are tool calls audited? → Append-only audit log
4. How do you stop loops? → Max steps + timeout
5. How do you limit cost? → Token budgets + rate limiting
6. How do you evaluate agent performance? → Task completion + human feedback
7. What requires human approval? → Destructive actions, data writes

### Demonstrates

- Modern AI architecture beyond LLM APIs
- Policy-driven security
- Audit and governance
- Cost control mechanisms

---

## Project 4 — AI Platform Cost Architecture

### Business Context

- **Users:** Finance, engineering leadership
- **Problem:** No visibility into AI spending, unpredictable costs
- **Goal:** Transparent, predictable, optimizable AI cost model

### Cost Flow

```
Requests → Tokens → Model Selection → Inference → GPU Hours → Storage → Total Cost
```

### Comparison Model

| Approach | Fixed Cost | Variable Cost | Break-Even |
|----------|-----------|---------------|------------|
| Managed (GPT-4o) | $0 | $30/1M tokens | N/A |
| Self-Hosted (Llama 70B) | $15,000/mo (GPU) | $0.50/1M tokens | 500M tokens/mo |
| Hybrid | $7,500/mo | Mixed | 250M tokens/mo |

### Key Metrics

| Metric | Definition |
|--------|-----------|
| Cost per request | Total cost / total requests |
| Cost per successful task | Total cost / successful tasks |
| Cost per user | Total cost / active users |
| GPU utilization | Active GPU hours / available GPU hours |
| Cache hit rate | Cached responses / total requests |

### Demonstrates

- Economic analysis of AI architecture
- Break-even modeling
- Cost optimization strategies
- FinOps implementation

---

## Project 5 — AI Security Architecture

### Business Context

- **Users:** Security team, compliance, all AI system users
- **Problem:** AI introduces new attack surfaces without existing controls
- **Goal:** Comprehensive security posture for AI systems

### Threat Model

| Threat | Impact | Likelihood | Mitigation |
|--------|--------|------------|------------|
| Prompt injection | Critical | High | Input validation, guardrails |
| Indirect injection | Critical | Medium | Document scanning, content policy |
| Data leakage | High | Medium | Output filtering, PII detection |
| Excessive permissions | High | Medium | Least privilege, policy engine |
| Credential compromise | Critical | Low | Secret management, rotation |
| Malicious dependencies | High | Low | Supply chain verification |
| Unauthorized retrieval | High | High | Authorization-aware retrieval |
| Sensitive logging | Medium | Medium | Data redaction, access control |

### Security Architecture

```
User → Authentication (IAM) → Authorization (RBAC) → Prompt Guard → Data Classifier
                                    ↓
                              Agent Permissions → Policy Engine
                                    ↓
                              Audit Logger → Compliance Tracker
```

### Controls

| Control | Purpose | Implementation |
|---------|---------|---------------|
| IAM | Identity management | SSO + JWT |
| Authorization | Access control | RBAC + department filtering |
| Prompt Guard | Injection detection | Pattern matching + ML |
| Data Classifier | PII detection | Regex + heuristics |
| Agent Permissions | Tool authorization | Policy engine |
| Audit Logger | Audit trail | Append-only log |
| Compliance | Regulatory tracking | Requirement management |

### Demonstrates

- Threat modeling methodology
- Defense in depth
- Security control implementation
- Compliance tracking

---

## Architecture Decision Records

### ADR-001: Managed vs Self-Hosted Models

**Status:** Accepted

**Context:** Need to serve multiple AI models for internal applications.

**Options:**

| Option | Pros | Cons |
|--------|------|------|
| Managed (OpenAI, Anthropic) | Simple, fast, no ops | Higher per-token cost, vendor lock-in |
| Self-Hosted (Llama, Mistral) | Lower marginal cost, control | High fixed cost, GPU ops burden |
| Hybrid | Flexibility, fallback | Complexity |

**Decision:** Hybrid approach — managed for development and fallback, self-hosted for production scale.

**Rationale:** Development velocity requires managed models. Production economics require self-hosted. Hybrid provides both.

**Consequences:** More complex routing, need model gateway, dual monitoring.

**Revisit:** When self-hosted model quality matches managed, or when managed costs decrease significantly.

---

### ADR-002: Vector Database Strategy

**Status:** Accepted

**Context:** Need vector storage for RAG across multiple departments.

**Options:**

| Option | Pros | Cons |
|--------|------|------|
| Pinecone | Fully managed, simple | Expensive at scale, vendor lock-in |
| Qdrant | Open source, performant | Self-hosted ops |
| Weaviate | Feature-rich, GraphQL | Learning curve |
| pgvector | Existing PostgreSQL | Performance limits |

**Decision:** Qdrant with department-level namespaces.

**Rationale:** Open source, good performance, namespace isolation without separate clusters.

**Consequences:** Self-hosted operations, but manageable with Kubernetes.

---

### ADR-003: Model Gateway

**Status:** Accepted

**Context:** Multiple applications need access to multiple models.

**Decision:** Centralized model gateway with semantic caching.

**Rationale:** Single entry point for routing, caching, fallback, and monitoring.

**Consequences:** Additional infrastructure, but significant operational benefits.

---

### ADR-004: Kubernetes vs Managed Inference

**Status:** Accepted

**Context:** Need GPU infrastructure for self-hosted models.

**Decision:** Kubernetes with GPU node pools.

**Rationale:** Existing Kubernetes expertise, flexible scheduling, cost control.

**Consequences:** Need GPU operator expertise, but leverages existing platform.

---

### ADR-005: Multi-Provider Strategy

**Status:** Accepted

**Context:** Need to avoid vendor lock-in for model providers.

**Decision:** Abstract model interface with provider-specific adapters.

**Rationale:** Flexibility to switch providers, negotiate pricing, maintain fallback.

**Consequences:** Adapter maintenance, but significant strategic value.

---

### ADR-006: Semantic Caching

**Status:** Accepted

**Context:** High volume of similar queries causing redundant inference.

**Decision:** Redis-based semantic cache with embedding similarity.

**Rationale:** 30-40% cost reduction for common query patterns.

**Consequences:** Cache invalidation complexity, but significant cost savings.

---

### ADR-007: Agent Tool Authorization

**Status:** Accepted

**Context:** Agents need access to tools but must be controlled.

**Decision:** Policy-based authorization with tool-level permissions.

**Rationale:** Fine-grained control, audit trail, human approval for high-risk actions.

**Consequences:** Policy management overhead, but essential for security.

---

## Portfolio Best Practices

### Don't Just Show Technologies

**Weak:** Kubernetes, Terraform, Python, LLM, AWS

**Strong:** Problem → Requirements → Constraints → Options → Trade-offs → Architecture → Implementation → Results

### Three to Five Strong Projects

| Projects | Coverage |
|----------|----------|
| 1 | Knowledge Platform (RAG + Enterprise) |
| 2 | Inference Platform (GPU + Multi-model) |
| 3 | Agent Platform (Modern AI) |
| 4 | FinOps (Cost Architecture) |
| 5 | Security (Threat Model + Controls) |

### Architecture Review Checklist

| Question | Purpose |
|----------|---------|
| What problem are we solving? | Business alignment |
| Who benefits? | User understanding |
| How will we measure success? | Outcome definition |
| Where does information come from? | Data architecture |
| Why does AI need to be involved? | AI justification |
| Why are these components? | Architecture rationale |
| Why these technologies? | Technology selection |
| What happens at 10x traffic? | Scale planning |
| What happens when dependencies fail? | Reliability design |
| What can users/agents access? | Security posture |
| Who owns the system? | Governance model |
| What will it cost? | Economic model |
| How do we know it's failing? | Observability |
| What happens when things change? | Adaptability |
