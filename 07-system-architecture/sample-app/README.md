# AI System Architecture — Sample App

A working prototype demonstrating **complete AI system architecture** — gateway, RAG, agents, model routing, context assembly, observability, and security from Day 07.

> **Building on Day 06**: This app takes the MLOps platform and connects all layers into one coherent system — where every component has defined boundaries, relationships, and controls.

## Architecture

```
                         USERS
                           │
                           ▼
                    ┌─────────────┐
                    │ API Gateway │  Auth, Rate Limit
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ AI Gateway  │  Routing, Policy
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
             RAG         Agents       Models
              │            │            │
              ▼            ▼            ▼
          Retrieval      Tools       Fallback
              │            │            │
              └────────────┼────────────┘
                           ▼
                    Context Assembly
                           │
                           ▼
                    ┌─────────────┐
                    │Model Gateway│
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
          Managed     Self-hosted   Fallback
```

## Project Structure

```
sample-app/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── gateway.py           # AI Gateway (rate limit, policy)
│   ├── rag.py               # RAG subsystem (retrieval, rerank, context)
│   ├── agents.py            # Agent subsystem (planning, tools, guardrails)
│   ├── model_router.py      # Multi-provider model routing with fallback
│   ├── context.py           # Context assembly
│   ├── observability.py     # Tracing, metrics, cost tracking
│   └── security.py          # Auth, authorization, audit
├── config/
│   ├── settings.py          # Configuration
│   └── .env.example         # Environment template
├── pipelines/
│   ├── __init__.py
│   ├── request_pipeline.py  # End-to-end request pipeline
│   └── adr_manager.py       # Architecture Decision Records
├── scripts/
│   ├── query.py             # Test a complete AI query
│   ├── ingest.py            # Ingest documents
│   └── status.py            # View system status
├── requirements.txt
└── test_system.py           # Test all components
```

## Quick Start

```bash
# 1. Navigate to sample-app
cd 07-system-architecture/sample-app

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the API
uvicorn app.main:app --reload --port 8080

# 5. Open API docs
# http://localhost:8080/docs
```

## Core Components

### 1. AI Gateway

Central entry point for all AI requests:

- Authentication validation
- Rate limiting per user
- Policy enforcement (blocked patterns, token limits)
- Request logging

```python
from app.gateway import AIGateway
from app.models import AIRequest, SecurityContext

gw = AIGateway()
sec_ctx = SecurityContext(user_id="user-001", roles=["employee"], rate_limit=100)
request = AIRequest(query="What is our policy?", user_id="user-001")

result = gw.process_request(request, sec_ctx)
# {"allowed": True, "request_id": "gw-abc123"}
```

### 2. RAG Subsystem

Complete retrieval-augmented generation:

- Vector store with metadata filtering
- Reranking
- Context building with token budgets
- Document-level permissions

```python
from app.rag import RAGService

rag = RAGService()
result = rag.retrieve(query="remote work policy", user_roles=["employee"])
# {"chunks": [...], "sources": [...], "tokens_used": 150}
```

### 3. Agent Subsystem

Autonomous agent with tool access:

- Planning with step limits
- Tool registry with permissions
- Guardrails for blocked actions
- Human approval for sensitive operations

```python
from app.agents import AgentService

agent = AgentService()
result = agent.run(query="search for expense policy", user_roles=["employee"])
# {"plan_steps": 3, "tools_needed": ["search"], "final_answer": "..."}
```

### 4. Model Router

Multi-provider routing with fallback:

- Priority-based selection
- Circuit breaker pattern
- Cost estimation
- Automatic fallback chain

```python
from app.model_router import ModelRouter

router = ModelRouter()
model = router.select_model()
cost = router.estimate_cost("gpt-4", 1000, 500)
```

### 5. Observability

Complete request tracing and cost tracking:

- Distributed tracing with spans
- Metrics collection (latency, tokens, cost)
- Cost tracking per user and model
- Dashboard with summaries

```python
from app.observability import ObservabilityService

obs = ObservabilityService()
obs.record_request("req-001", "user-001", "gpt-4", "openai", 500, 200, 450.0, 0.045)
dashboard = obs.get_dashboard()
```

### 6. Security

Enterprise security subsystem:

- Identity provider simulation
- Role-based access control
- Document-level permissions
- Full audit logging

```python
from app.security import SecurityService

sec = SecurityService()
auth = sec.authenticate("alice@company.com", "password")
sec_ctx = sec.get_security_context("user-001")
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | System health check |
| POST | /auth/login | Authenticate user |
| POST | /ai/query | Process AI query |
| GET | /rag/stats | RAG statistics |
| POST | /rag/ingest | Ingest document |
| GET | /agents/tools | List available tools |
| GET | /agents/stats | Agent statistics |
| GET | /models/routes | Model routing table |
| GET | /models/stats | Model router stats |
| GET | /observability/dashboard | Observability dashboard |
| GET | /observability/traces | Request traces |
| GET | /observability/costs | Cost report |
| GET | /security/audit | Audit log |
| GET | /system/architecture | Architecture overview |

## Request Flow

```
User Question
    │
    ▼
API Gateway (auth, rate limit)
    │
    ▼
AI Gateway (routing decision, policy)
    │
    ├── RAG (query → embed → retrieve → rerank → context)
    │
    ├── Agent (plan → tool select → execute) [if needed]
    │
    ▼
Context Assembly
    │
    ▼
Model Gateway (route to best model)
    │
    ▼
Inference → Response + Sources + Metadata
```

## Key Concepts Demonstrated

| Concept | Implementation |
|---------|----------------|
| AI Gateway | Central routing, rate limiting, policy enforcement |
| RAG Subsystem | Retrieval, reranking, context building with permissions |
| Agent Subsystem | Planning, tool authorization, guardrails, human approval |
| Model Routing | Multi-provider, circuit breaker, fallback chain |
| Context Assembly | Token-budget-aware prompt construction |
| Observability | Tracing, metrics, cost tracking, dashboard |
| Security | Identity, RBAC, document permissions, audit logging |
| Architecture Decision Records | Documented trade-offs and decisions |

## Running the Tests

```bash
# Run all tests
python test_system.py

# Test a complete query
python scripts/query.py

# Ingest documents
python scripts/ingest.py

# View system status
python scripts/status.py
```

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
# Gateway
GATEWAY_RATE_LIMIT=100
GATEWAY_RATE_WINDOW=60

# RAG
RAG_TOP_K=5
RAG_MAX_CONTEXT_TOKENS=4096

# Model Router
MODEL_ROUTER_TIMEOUT=30
MODEL_CIRCUIT_BREAKER_THRESHOLD=3

# Context
CONTEXT_MAX_TOKENS=4096

# Security
SECURITY_DEFAULT_BUDGET_USD=10.0

# Cost
COST_ALERT_THRESHOLD_USD=50.0
```

## Next Steps

After running this sample app, you should understand:

1. How an AI Gateway centralizes cross-cutting concerns
2. How RAG works as an independent subsystem
3. How agents interact with tools through controlled interfaces
4. How model routing provides flexibility and fallback
5. How context assembly respects token budgets
6. How observability traces the entire request path
7. How security follows every boundary

Move to **Day 08 → Technology Decisions, Build vs Buy & Architecture Trade-offs** to learn which technologies to choose and why.
