# Context Diagram — Enterprise AI Knowledge Assistant

## System Context

This diagram shows the high-level system context for the Enterprise AI Knowledge Assistant, identifying external actors, system boundaries, and data flows.

## Actors

| Actor | Role | Interaction |
|-------|------|-------------|
| Employee | End user | Asks questions, receives answers |
| HR/Admin | Content manager | Uploads documents, manages policies |
| IT Admin | System administrator | Configures models, monitors system |
| Security | Auditor | Reviews access logs, enforces policies |

## Context Diagram

```
                    ┌─────────────────────────────────────────┐
                    │            EXTERNAL ACTORS              │
                    ├─────────────────────────────────────────┤
                    │                                         │
                    │   ┌───────────┐     ┌───────────┐      │
                    │   │ Employee  │     │ HR/Admin  │      │
                    │   │ (10,000)  │     │           │      │
                    │   └─────┬─────┘     └─────┬─────┘      │
                    │         │                 │             │
                    └─────────┼─────────────────┼─────────────┘
                              │                 │
                              ▼                 ▼
                    ┌─────────────────────────────────────────┐
                    │         ENTERPRISE AI KNOWLEDGE         │
                    │              ASSISTANT                  │
                    │                                         │
                    │  ┌─────────────────────────────────┐   │
                    │  │        System Boundary           │   │
                    │  │                                  │   │
                    │  │  API Gateway                     │   │
                    │  │       │                          │   │
                    │  │  AI Gateway                      │   │
                    │  │       │                          │   │
                    │  │  ┌────┴────┐                     │   │
                    │  │  │         │                     │   │
                    │  │  RAG    Agents                   │   │
                    │  │  │         │                     │   │
                    │  │  └────┬────┘                     │   │
                    │  │       │                          │   │
                    │  │  Model Gateway                   │   │
                    │  │       │                          │   │
                    │  └───────┼──────────────────────────┘   │
                    │          │                              │
                    └──────────┼──────────────────────────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │  Model APIs  │  │  Vector DB   │  │  Document    │
    │  (OpenAI,    │  │  (ChromaDB,  │  │  Storage     │
    │  Anthropic)  │  │  Pinecone)   │  │  (S3, GCS)   │
    └──────────────┘  └──────────────┘  └──────────────┘
```

## External Integrations

| Integration | Direction | Purpose |
|-------------|-----------|---------|
| SSO/Identity Provider | Inbound | Authentication |
| Model APIs (OpenAI, Anthropic) | Outbound | LLM inference |
| Vector Database | Bidirectional | Document storage/retrieval |
| Document Storage (S3) | Inbound | Document ingestion |
| Monitoring (Prometheus) | Inbound | Metrics collection |
| Audit Log (ELK) | Outbound | Security logging |

## System Boundaries

- **Inside boundary**: API Gateway, AI Gateway, RAG pipeline, Agent system, Model Gateway
- **Outside boundary**: Model APIs, Vector DB, Document Storage, Identity Provider
- **Data sensitivity**: All queries and responses contain internal company data — must stay within corporate network or approved cloud services
