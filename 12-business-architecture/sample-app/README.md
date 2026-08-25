# AI Business Architecture Portfolio Demo

Business alignment, cost modeling, trade-off analysis, and architecture decision management for AI systems.

## Quick Start

```bash
pip install -r requirements.txt
python test_system.py
python scripts/status.py
python scripts/portfolio_demo.py
python scripts/adr_demo.py
```

## Project Structure

```
sample-app/
├── app/
│   ├── __init__.py
│   ├── models.py           # 14 Pydantic models
│   ├── portfolio.py        # Project & use case management
│   ├── adr.py              # Architecture Decision Records
│   ├── cost_model.py       # Cost tracking & ROI analysis
│   ├── business_metrics.py # Business value measurement
│   ├── trade_off.py        # Trade-off analysis
│   ├── review.py           # Architecture review & checklist
│   ├── executive_brief.py  # One-page executive briefs
│   ├── orchestrator.py     # Unified orchestrator
│   └── main.py             # FastAPI application
├── config/
│   ├── settings.py         # Configuration
│   └── .env.example        # Environment template
├── pipelines/
│   ├── __init__.py
│   └── portfolio_pipeline.py # Business architecture pipeline
├── scripts/
│   ├── status.py           # Portfolio status report
│   ├── portfolio_demo.py   # Portfolio & cost analysis demo
│   └── adr_demo.py         # ADR viewer
├── test_system.py          # Comprehensive tests
├── requirements.txt
└── README.md
```

## Components

| Component | Purpose | File |
|-----------|---------|------|
| PortfolioManager | Projects & use case prioritization | portfolio.py |
| ADRManager | Architecture Decision Records | adr.py |
| CostManager | Cost models & ROI calculation | cost_model.py |
| BusinessMetricsManager | Business value measurement | business_metrics.py |
| TradeOffAnalyzer | Trade-off analysis | trade_off.py |
| ReviewManager | Architecture review & checklist | review.py |
| ExecutiveBriefManager | One-page executive briefs | executive_brief.py |
| PortfolioOrchestrator | Unified orchestrator | orchestrator.py |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service status |
| `/portfolio/summary` | GET | Portfolio summary |
| `/portfolio/projects` | GET | List projects |
| `/portfolio/use-cases` | GET | List use cases |
| `/portfolio/prioritize` | GET | Prioritized use cases |
| `/portfolio/project/{id}/cost-analysis` | GET | Project cost analysis |
| `/portfolio/report` | GET | Full portfolio report |
| `/adrs` | GET | List ADRs |
| `/adrs/{id}` | GET | Get ADR |
| `/adrs/{id}/formatted` | GET | Formatted ADR |
| `/costs/summary` | GET | Cost summary |
| `/costs/model/{id}` | GET | Cost model details |
| `/metrics/summary` | GET | Business metrics summary |
| `/metrics/value/{id}` | GET | Business value details |
| `/trade-offs` | GET | List trade-offs |
| `/trade-offs/{id}` | GET | Get trade-off |
| `/trade-offs/{id}/evaluate` | GET | Evaluate trade-off |
| `/reviews/checklist` | GET | 14-question review checklist |
| `/reviews/summary` | GET | Review summary |
| `/briefs` | GET | List executive briefs |
| `/briefs/{name}` | GET | Get executive brief |
| `/briefs/{name}/formatted` | GET | Formatted brief |
| `/status` | GET | Full system status |

## Portfolio Projects

| # | Project | Demonstrates |
|---|---------|-------------|
| 1 | Enterprise AI Knowledge Platform | RAG, Enterprise IAM, Multi-model, Observability, FinOps |
| 2 | AI Inference Platform | Platform architecture, GPU management, Cost optimization |
| 3 | Agent Platform | Modern AI, Policy-driven security, Audit, Cost controls |
| 4 | AI Platform Cost Architecture | Economic analysis, Cost optimization, FinOps |
| 5 | AI Security Architecture | Threat modeling, Security controls, Compliance |

## 7 ADRs Included

| ADR | Decision |
|-----|----------|
| ADR-001 | Managed vs Self-Hosted Models → Hybrid |
| ADR-002 | Vector Database Strategy → Qdrant |
| ADR-003 | Model Gateway → Centralized with caching |
| ADR-004 | Kubernetes vs Managed Inference → Kubernetes |
| ADR-005 | Multi-Provider Strategy → Abstract interface |
| ADR-006 | Semantic Caching → Redis-based |
| ADR-007 | Agent Tool Authorization → Policy engine |

## 5 Trade-off Analyses

| Analysis | Winner |
|----------|--------|
| Model Strategy | Hybrid |
| Vector Database | Qdrant |
| Agent Authorization | Policy Engine |
| Caching Strategy | Semantic Cache |
| Observability Stack | OpenTelemetry + Grafana |
