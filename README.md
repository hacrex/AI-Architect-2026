# AI Architect 2026 — 12-Day Learning Series

A practical 12-day roadmap for engineers who want to move from building AI features to designing production-ready AI systems.

## Who is this for?

- Cloud Engineers
- DevOps Engineers
- Platform Engineers
- Software Engineers
- Data Engineers
- ML Engineers
- AI Engineers

## The goal

By the end of 12 days, you should be able to reason about an AI system as an architect:

- Understand the AI and data foundations
- Design LLM and agentic architectures
- Design AI infrastructure and deployment platforms
- Evaluate technology choices
- Design for scale, reliability, and failure
- Model AI costs and apply FinOps thinking
- Build observability into AI systems
- Design security and governance
- Connect architecture decisions to business outcomes
- Document decisions with diagrams, ADRs, trade-off analyses, and success metrics

## Repository structure

```
ai-architect-2026/
├── README.md
├── requirements.txt                  # Python dependencies for all sample-apps
│
├── 01-foundations/                   # Technical vocabulary and architecture mindset
│   ├── notes.md
│   ├── architecture.md
│   ├── exercise.md
│   └── sample-app/
│
├── 02-ai-ml/                         # AI/ML & LLM fundamentals
│   ├── notes.md
│   ├── architecture.md
│   ├── exercise.md
│   └── sample-app/
│
├── 03-llm-engineering/               # RAG, agents, tool use, context engineering
│   ├── notes.md
│   ├── architecture.md
│   ├── exercise.md
│   └── sample-app/
│
├── 04-ai-infrastructure/             # GPUs, Kubernetes, inference serving
│   ├── notes.md
│   ├── architecture.md
│   ├── exercise.md
│   └── sample-app/
│
├── 05-data-architecture/             # Data systems, streaming, vector retrieval
│   ├── notes.md
│   ├── architecture.md
│   ├── exercise.md
│   └── sample-app/
│
├── 06-mlops-platform/                # MLOps lifecycle and platform engineering
│   ├── notes.md
│   ├── architecture.md
│   ├── exercise.md
│   └── sample-app/
│
├── 07-system-architecture/           # End-to-end system design
│   ├── notes.md
│   ├── architecture.md
│   ├── exercise.md
│   └── sample-app/
│
├── 08-technology-decisions/          # Build vs buy, ADRs, trade-off analysis
│   ├── notes.md
│   ├── exercise.md
│   ├── ADR-001-model-selection.md
│   └── sample-app/
│
├── 09-scale-finops/                  # Scaling, reliability, cost modeling
│   ├── notes.md
│   ├── cost-model.md
│   ├── exercise.md
│   └── sample-app/
│
├── 10-observability/                 # Monitoring, metrics, alerting
│   ├── notes.md
│   ├── architecture.md
│   ├── exercise.md
│   └── sample-app/
│
├── 11-security-governance/           # Threat modeling, governance, compliance
│   ├── notes.md
│   ├── threat-model.md
│   ├── exercise.md
│   └── sample-app/
│
├── 12-business-architecture/         # ROI, business value, portfolio
│   ├── notes.md
│   ├── architecture.md
│   ├── exercise.md
│   ├── portfolio-structure.md
│   └── sample-app/
│
├── architecture/                     # Architecture diagrams and documentation
│   ├── context-diagram/
│   ├── logical-architecture/
│   ├── deployment-architecture/
│   ├── data-flow/
│   └── security-architecture/
│
└── capstone/                         # Final project artifacts
    ├── architecture.md
    ├── business-case.md
    ├── cost-model.md
    ├── observability.md
    ├── requirements.md
    ├── threat-model.md
    └── ADRs/
```

## 12-Day Path

| Day | Topic | Primary Outcome | Sample App |
|-----|-------|-----------------|------------|
| 01 | Foundations for AI Architecture | Engineering, AI, cloud, data foundation | Enterprise AI Knowledge Assistant |
| 02 | AI/ML & LLM Fundamentals | Models, transformers, embeddings, inference | Model comparison & routing |
| 03 | LLM Engineering | RAG, tool use, context, routing, agents | Multi-agent system with tools |
| 04 | AI Infrastructure | GPUs, inference serving, Kubernetes | vLLM inference server |
| 05 | Data Architecture | Data, streaming, retrieval, vector systems | RAG pipeline with permissions |
| 06 | MLOps & AI Platform Engineering | Production lifecycle around models | Model registry, evaluation, deployment |
| 07 | AI System Architecture | Resilient end-to-end AI systems | Full system with gateway, RAG, agents |
| 08 | Technology Selection & Build vs Buy | Architecture decisions with trade-offs | Decision engine with ADRs |
| 09 | Scale, Reliability & AI FinOps | Traffic, failure, latency, cost | Cache, circuit breaker, cost tracker |
| 10 | AI Observability | System, model, retrieval, quality signals | Metrics, tracing, alerts, SLOs |
| 11 | AI Security, Governance & Responsible AI | Trustworthy enterprise AI | Auth, prompt guard, PII, audit |
| 12 | Business Alignment & Architecture Portfolio | ROI, business value, portfolio | Portfolio, ADRs, cost model, briefs |

## How to use the series

Spend roughly 60-120 minutes per day.

For every day:

1. Read `notes.md` for concepts
2. Study `architecture.md` for patterns
3. Complete `exercise.md`
4. Run the sample app
5. Produce the requested artifact
6. Add the artifact to your personal AI Architecture portfolio

### Running Sample Apps

Each day includes a working sample app. To run any sample app:

```bash
cd <day-folder>/sample-app
pip install -r requirements.txt
python test_system.py
```

### Sample Apps

| Day | Folder | Tests | Key Components |
|-----|--------|-------|----------------|
| 01 | `01-foundations/sample-app/` | ✅ | RAG, auth, model gateway, observability |
| 02 | `02-ai-ml/sample-app/` | ✅ | Model comparator, router, gateway |
| 03 | `03-llm-engineering/sample-app/` | ✅ | Agents, tools, orchestrator |
| 04 | `04-ai-infrastructure/sample-app/` | ✅ | Inference server, health, benchmarks |
| 05 | `05-data-architecture/sample-app/` | ✅ | Chunker, embeddings, vectordb, ingestion |
| 06 | `06-mlops-platform/sample-app/` | ✅ | Registry, evaluation, deployment, monitoring |
| 07 | `07-system-architecture/sample-app/` | ✅ | Full system: gateway, RAG, agents, security |
| 08 | `08-technology-decisions/sample-app/` | ✅ | ADR manager, decision engine, build vs buy |
| 09 | `09-scale-finops/sample-app/` | ✅ | Cache, circuit breaker, rate limiter, cost tracker |
| 10 | `10-observability/sample-app/` | ✅ | Metrics, logger, tracer, alerts, SLOs, drift |
| 11 | `11-security-governance/sample-app/` | ✅ | Auth, prompt guard, PII, audit, compliance |
| 12 | `12-business-architecture/sample-app/` | ✅ | Portfolio, ADRs, cost model, trade-offs, briefs |

## Architecture Portfolio

The `architecture/` folder contains detailed architecture documentation:

| Document | Content |
|----------|---------|
| `context-diagram/` | System context, actors, external integrations |
| `logical-architecture/` | Component diagram, API contracts, data stores |
| `deployment-architecture/` | Infrastructure topology, Kubernetes, networking |
| `data-flow/` | Ingestion, query, agent, and storage patterns |
| `security-architecture/` | Auth, authz, encryption, audit, compliance |

## Capstone

The `capstone/` folder contains the complete reference architecture:

| Document | Content |
|----------|---------|
| `architecture.md` | Reference architecture with all components |
| `business-case.md` | ROI, financial analysis, risk assessment |
| `cost-model.md` | Detailed cost breakdown, scaling projections |
| `observability.md` | Dashboards, alerting, SLOs, feedback loops |
| `requirements.md` | Functional and non-functional requirements |
| `threat-model.md` | 12 threats with mitigations and controls |
| `ADRs/` | 7 Architecture Decision Records |

## Suggested portfolio artifacts

By the end of the series, aim to have:

- 5 architecture diagrams (in `architecture/`)
- 7 Architecture Decision Records (in `capstone/ADRs/`)
- 1 cost model (`capstone/cost-model.md`)
- 1 threat model (`capstone/threat-model.md`)
- 1 observability plan (`capstone/observability.md`)
- 1 business case (`capstone/business-case.md`)
- 1 complete reference architecture (`capstone/architecture.md`)
- 12 working sample-apps with passing tests

## Core principle

An AI Architect does not simply ask:

> "Which model or framework should I use?"

The architect asks:

> "What system should we design, why is this the right trade-off, how will it scale, what will it cost, what can fail, how will we govern it, and what business outcome will it produce?"

## Progress Tracker

```
Day 01: [ ] Notes  [ ] Architecture  [ ] Exercise  [ ] Sample App
Day 02: [ ] Notes  [ ] Architecture  [ ] Exercise  [ ] Sample App
Day 03: [ ] Notes  [ ] Architecture  [ ] Exercise  [ ] Sample App
Day 04: [ ] Notes  [ ] Architecture  [ ] Exercise  [ ] Sample App
Day 05: [ ] Notes  [ ] Architecture  [ ] Exercise  [ ] Sample App
Day 06: [ ] Notes  [ ] Architecture  [ ] Exercise  [ ] Sample App
Day 07: [ ] Notes  [ ] Architecture  [ ] Exercise  [ ] Sample App
Day 08: [ ] Notes  [ ] Exercise  [ ] ADR  [ ] Sample App
Day 09: [ ] Notes  [ ] Cost Model  [ ] Exercise  [ ] Sample App
Day 10: [ ] Notes  [ ] Architecture  [ ] Exercise  [ ] Sample App
Day 11: [ ] Notes  [ ] Threat Model  [ ] Exercise  [ ] Sample App
Day 12: [ ] Notes  [ ] Architecture  [ ] Exercise  [ ] Sample App
```

---

**12 Days Complete.** Learn → Design → Build → Measure → Document → Review → Repeat.
