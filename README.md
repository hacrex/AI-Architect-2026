# AI Architect 2026 — 12-Day Learning Series

A practical 12-day roadmap for engineers who want to move from building AI features to designing production-ready AI systems.

## Who is this for?

This roadmap is designed for:

- Cloud Engineers
- DevOps Engineers
- Platform Engineers
- Software Engineers
- Data Engineers
- ML Engineers
- AI Engineers

## The goal

By the end of 12 days, you should be able to reason about an AI system as an architect:

- understand the AI and data foundations
- design LLM and agentic architectures
- design AI infrastructure and deployment platforms
- evaluate technology choices
- design for scale, reliability, and failure
- model AI costs and apply FinOps thinking
- build observability into AI systems
- design security and governance
- connect architecture decisions to business outcomes
- document decisions with diagrams, ADRs, trade-off analyses, and success metrics

## Repository structure

```
ai-architect-2026/
│
├── README.md
│
├── 01-foundations/          # Technical vocabulary and architecture mindset
│   ├── notes.md
│   ├── architecture.md
│   └── exercise.md
│
├── 02-ai-ml/               # AI/ML & LLM fundamentals
│   ├── notes.md
│   ├── architecture.md
│   └── exercise.md
│
├── 03-llm-engineering/     # RAG, agents, tool use, context engineering
│   ├── notes.md
│   ├── architecture.md
│   └── exercise.md
│
├── 04-ai-infrastructure/   # GPUs, Kubernetes, inference serving
│   ├── notes.md
│   ├── architecture.md
│   └── exercise.md
│
├── 05-data-architecture/   # Data systems, streaming, vector retrieval
│   ├── notes.md
│   ├── architecture.md
│   └── exercise.md
│
├── 06-mlops-platform/      # MLOps lifecycle and platform engineering
│   ├── notes.md
│   ├── architecture.md
│   └── exercise.md
│
├── 07-system-architecture/ # End-to-end system design
│   ├── notes.md
│   ├── architecture.md
│   └── exercise.md
│
├── 08-technology-decisions/# Build vs buy, ADRs, trade-off analysis
│   ├── notes.md
│   ├── exercise.md
│   └── ADR-001-model-selection.md
│
├── 09-scale-finops/        # Scaling, reliability, cost modeling
│   ├── notes.md
│   ├── cost-model.md
│   └── exercise.md
│
├── 10-observability/       # Monitoring, metrics, alerting
│   ├── notes.md
│   ├── architecture.md
│   └── exercise.md
│
├── 11-security-governance/ # Threat modeling, governance, compliance
│   ├── notes.md
│   ├── threat-model.md
│   └── exercise.md
│
├── 12-business-architecture/ # ROI, business value, portfolio
│   ├── notes.md
│   ├── architecture.md
│   └── exercise.md
│
├── architecture/           # Architecture diagrams
│   ├── context-diagram/
│   ├── logical-architecture/
│   ├── deployment-architecture/
│   ├── data-flow/
│   └── security-architecture/
│
└── capstone/               # Final project artifacts
    ├── architecture.md
    ├── requirements.md
    ├── ADRs/
    ├── cost-model.md
    ├── threat-model.md
    ├── observability.md
    └── business-case.md
```

## 12-Day Path

| Day | Topic | Primary Outcome |
|---|---|---|
| 01 | Foundations for AI Architecture | Establish the engineering, AI, cloud, and data foundation |
| 02 | AI/ML & LLM Fundamentals | Understand models, transformers, embeddings, and inference |
| 03 | LLM Engineering | Design RAG, tool use, context, routing, and agentic systems |
| 04 | AI Infrastructure | Understand GPUs, inference serving, Kubernetes, and scaling |
| 05 | Data Architecture for AI | Design data, streaming, retrieval, and vector architectures |
| 06 | MLOps & AI Platform Engineering | Build the production lifecycle around models |
| 07 | AI System Architecture | Design resilient end-to-end AI systems |
| 08 | Technology Selection & Build vs Buy | Make architecture decisions using explicit trade-offs |
| 09 | Scale, Reliability & AI FinOps | Design for traffic, failure, latency, and cost |
| 10 | AI Observability | Measure system, model, retrieval, quality, and cost signals |
| 11 | AI Security, Governance & Responsible AI | Design trustworthy enterprise AI |
| 12 | Business Alignment & Architecture Portfolio | Connect AI architecture to ROI and demonstrate readiness |

## How to use the series

Spend roughly 60–120 minutes per day.

For every day:

1. Read `notes.md` for concepts
2. Study `architecture.md` for patterns
3. Complete `exercise.md`
4. Produce the requested artifact
5. Add the artifact to your personal AI Architecture portfolio

The objective is not to memorize tools. The objective is to develop architectural judgment.

## Suggested portfolio artifacts

By the end of the series, aim to have:

- 3–5 architecture diagrams (in `architecture/`)
- 2–3 Architecture Decision Records (in `08-technology-decisions/` or `capstone/ADRs/`)
- 1 cost model (`09-scale-finops/cost-model.md` or `capstone/cost-model.md`)
- 1 reliability/scaling plan
- 1 AI security and governance checklist (`11-security-governance/threat-model.md`)
- 1 business-value scorecard (`12-business-architecture/architecture.md`)
- 1 complete reference architecture (`capstone/architecture.md`)

## Core principle

An AI Architect does not simply ask:

> "Which model or framework should I use?"

The architect asks:

> "What system should we design, why is this the right trade-off, how will it scale, what will it cost, what can fail, how will we govern it, and what business outcome will it produce?"

## Source basis

This series synthesizes the architectural progression in the accompanying roadmap material: technical and data foundations, system architecture, technology selection, scale and cost, and governance/business alignment, combined with a practical AI infrastructure and platform-engineering track.
