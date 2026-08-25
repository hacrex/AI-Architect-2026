# Capstone — Reference Architecture

## System Overview

Enterprise AI Knowledge Assistant — a RAG-based system serving 10,000 employees across engineering, HR, finance, and legal departments. Provides accurate, citation-backed answers from internal documentation with enterprise-grade security, observability, and cost control.

## Architecture Diagram

```
User (Employee)
    │
    ▼
┌─────────────┐
│ Identity    │ ← SSO (Okta/Azure AD), JWT
│ (SSO/IAM)   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ API Gateway │ ← Rate limiting, request validation
│ (nginx)     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ AI Gateway  │ ← Routing, fallback, cost tracking
│             │   Semantic caching
└──────┬──────┘
       │
  ┌────┴────────────────────────────────┐
  │                                     │
  ▼                                     ▼
┌──────────┐                      ┌──────────┐
│ RAG      │ ← Embedding,         │ Agent    │ ← Orchestrator,
│ Pipeline │   retrieval,         │ System   │   tool use
│          │   reranking          │          │
└────┬─────┘                      └────┬─────┘
     │                                 │
     │        ┌────────────────────────┘
     │        │
     ▼        ▼
┌─────────────────────────────────────────────┐
│              Model Gateway                   │
│  ┌──────────┬──────────┬──────────────────┐ │
│  │ OpenAI   │ Anthropic│ Self-hosted      │ │
│  │ (GPT-4o) │ (Claude) │ (Llama via vLLM) │ │
│  └──────────┴──────────┴──────────────────┘ │
└─────────────────────────────────────────────┘
       │
       ▼
┌─────────────┐
│ Observability│ ← Metrics, logs, traces
│ (OTel+Grafana)│
└─────────────┘
```

## Component Inventory

| Component | Purpose | Technology | Owner |
|-----------|---------|------------|-------|
| API Gateway | Request routing, rate limiting | nginx + FastAPI | Platform |
| AI Gateway | Model routing, caching, fallback | Custom Python | Platform |
| RAG Pipeline | Document retrieval and reranking | LlamaIndex / custom | Platform |
| Agent System | Multi-step reasoning, tool use | Custom async runtime | Platform |
| Model Gateway | Provider abstraction, load balancing | Custom adapter pattern | Platform |
| Vector Store | Document embeddings | Qdrant | Data |
| Metadata DB | User data, conversation history | PostgreSQL | Data |
| Session Cache | Semantic cache, sessions | Redis | Data |
| Document Store | Raw documents | S3 | Data |
| Observability | Metrics, logs, traces | OpenTelemetry + Grafana | SRE |
| Security | Auth, authz, audit | Keycloak, OPA | Security |
| Monitoring | Alerting, dashboards | Prometheus + Grafana | SRE |

## Key Decisions

| # | Decision | ADR |
|---|----------|-----|
| 1 | Use RAG for knowledge retrieval | ADR-001 |
| 2 | Multi-agent orchestration for complex queries | ADR-002 |
| 3 | Model gateway with provider abstraction | ADR-003 |
| 4 | Qdrant vector database with namespaces | ADR-004 |
| 5 | Semantic caching for cost optimization | ADR-005 |

## Trade-off Summary

| Decision | Chosen | Rejected | Rationale |
|----------|--------|----------|-----------|
| Knowledge retrieval | RAG | Fine-tuning, context stuffing | Real-time freshness, citations, cost |
| Query handling | Hybrid multi-agent | Single agent, deterministic | 80% simple queries bypass agents |
| Model access | Custom gateway | Direct API, provider SDK | No lock-in, fallback, cost tracking |
| Vector database | Qdrant | Pinecone, Weaviate, pgvector | Open source, performance, namespaces |
| Caching | Semantic (Redis) | Exact match, none | 30-40% cost reduction |
| Authorization | Policy engine (OPA) | Static whitelist | Fine-grained, auditable |

## Risks and Mitigations

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| Model provider outage | High | Medium | Multi-provider fallback, self-hosted backup |
| Prompt injection | Critical | High | Input validation, guardrails, output filtering |
| Data leakage | Critical | Medium | Authorization-aware retrieval, PII detection |
| Cost overrun | Medium | Medium | Budget alerts, semantic caching, model routing |
| Retrieval quality degradation | High | Medium | Hybrid search, reranking, feedback loops |
| Vector DB failure | High | Low | Replication, cached responses, graceful degradation |
| Agent infinite loops | Medium | Medium | Max steps, timeout, circuit breaker |
| Sensitive data in logs | High | Medium | Data redaction, access controls, retention policies |

## Success Criteria

| Metric | Baseline | Target |
|--------|----------|--------|
| Resolution time | 20 min | 10 min |
| Task success rate | 65% | 85% |
| User adoption | 0% | 70% |
| Cost per task | $8.50 | $2.00 |
| Response latency (p95) | N/A | < 2s |
| System availability | N/A | 99.9% |
| Human escalation rate | 100% | 30% |
