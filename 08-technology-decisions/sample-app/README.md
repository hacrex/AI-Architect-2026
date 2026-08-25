# Technology Decisions — Sample App

A working prototype demonstrating **technology decision-making** — decision matrices, Build vs Buy analysis, ADR management, constraint validation, and architecture trade-off evaluation from Day 08.

> **Building on Day 07**: This app takes the complete AI system architecture and adds structured decision-making — where every technology choice is documented, evaluated, and defensible.

## Architecture

```
                        USERS
                          │
                          ▼
                   ┌─────────────┐
                   │  FastAPI    │
                   └──────┬──────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
    Decision Engine   ADR Manager   Build/Buy Analyzer
          │               │               │
          ▼               ▼               ▼
    Weighted Scoring  Full ADR      Cost Calculator
          │           Template          │
          ▼               │             ▼
    Constraint         Revisit     Competitive
    Validator        Conditions    Advantage Filter
          │               │               │
          └───────────────┼───────────────┘
                          ▼
                  Decision Pipeline
                          │
                          ▼
                  Architecture Overview
```

## Project Structure

```
sample-app/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application
│   ├── models.py                  # Pydantic models
│   ├── decision_engine.py         # Decision matrices with weighted scoring
│   ├── adr_manager.py             # Architecture Decision Records
│   ├── build_buy_analyzer.py      # Build vs Buy analysis
│   └── constraint_validator.py    # Hard constraint management
├── config/
│   ├── settings.py                # Configuration
│   └── .env.example               # Environment template
├── pipelines/
│   ├── __init__.py
│   └── decision_pipeline.py       # End-to-end decision workflow
├── scripts/
│   ├── status.py                  # View all decisions and status
│   ├── query.py                   # Run complete evaluation workflow
│   └── matrix.py                  # Display decision matrices
├── requirements.txt
└── test_system.py                 # Test all components
```

## Quick Start

```bash
# 1. Navigate to sample-app
cd 08-technology-decisions/sample-app

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

### 1. Decision Engine

Technology selection with weighted scoring and hard constraint validation:

```python
from app.decision_engine import DecisionEngine

engine = DecisionEngine()
matrices = engine.list_matrices()
for m in matrices:
    print(f"{m.title}: {m.selected_option}")
```

### 2. ADR Manager

Architecture Decision Records with full template:

```python
from app.adr_manager import ADRManager

mgr = ADRManager()
adrs = mgr.list_adrs()
for adr in adrs:
    print(f"{adr.id}: {adr.title}")
    print(f"  Decision: {adr.decision}")
    print(f"  Revisit conditions: {len(adr.revisit_conditions)}")

# Get formatted markdown
markdown = mgr.format_adr_markdown("ADR-001")
print(markdown)
```

### 3. Build vs Buy Analyzer

Full cost analysis for build vs buy decisions:

```python
from app.build_buy_analyzer import BuildBuyAnalyzer

analyzer = BuildBuyAnalyzer()
analyses = analyzer.list_analyses()
for a in analyses:
    comparisons = analyzer.compare_options(a.id)
    print(f"{a.component}: {a.recommendation}")
    for c in comparisons:
        print(f"  {c['name']}: ${c['total_5yr_cost']:,.0f}")
```

### 4. Constraint Validator

Hard constraint management for technology decisions:

```python
from app.constraint_validator import ConstraintManager

mgr = ConstraintManager()
constraints = mgr.get_all_constraints()

result = mgr.validate_option("Managed LLM", "External API service")
print(f"Valid: {result['is_valid']}")
print(f"Violations: {result['violations']}")
```

### 5. Decision Pipeline

End-to-end technology decision workflow:

```python
from pipelines.decision_pipeline import DecisionPipeline

pipeline = DecisionPipeline()
summary = pipeline.run_full_evaluation()

# Challenge a decision
challenge = pipeline.challenge_decision("matrix-001")
print(f"Selected: {challenge['selected_option']}")
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | System health check |
| GET | /decisions/matrices | List all decision matrices |
| GET | /decisions/matrices/{id} | Get matrix with scores |
| POST | /decisions/matrices/{id}/score | Score an option |
| POST | /decisions/matrices/{id}/select | Select best option |
| GET | /decisions/challenge/{id} | Challenge a decision |
| GET | /adr | List all ADRs |
| GET | /adr/{id} | Get ADR details |
| GET | /adr/{id}/markdown | Get ADR as markdown |
| POST | /adr | Create new ADR |
| PUT | /adr/{id}/status | Update ADR status |
| GET | /build-buy | List Build vs Buy analyses |
| GET | /build-buy/{id} | Get analysis with comparisons |
| GET | /constraints | List all constraints |
| POST | /constraints/validate | Validate option against constraints |
| GET | /evaluation/summary | Full evaluation summary |
| GET | /evaluation/model-hosting | Model hosting evaluation |
| GET | /evaluation/vector-storage | Vector storage evaluation |
| GET | /evaluation/inference-platform | Inference platform evaluation |
| GET | /evaluation/build-buy | Build vs Buy summary |
| GET | /architecture/overview | Architecture overview |

## Decision Flow

```
Define Requirements
        │
        ▼
Identify Hard Constraints
        │
        ▼
List Technology Options
        │
        ▼
Create Decision Matrix
        │
        ▼
Score Options (1-10)
        │
        ▼
Validate Against Constraints
        │
        ▼
Eliminate Disqualified Options
        │
        ▼
Calculate Weighted Scores
        │
        ▼
Select Highest Scoring Option
        │
        ▼
Document as ADR
        │
        ▼
Define Revisit Conditions
        │
        ▼
Challenge Your Own Decision
```

## Key Concepts Demonstrated

| Concept | Implementation |
|---------|----------------|
| Decision Matrices | Weighted scoring across multiple criteria |
| Hard Constraints | Automatic elimination of invalid options |
| Build vs Buy | Full 5-year cost analysis |
| ADRs | Complete template with revisit conditions |
| Competitive Advantage | Filter for Build vs Buy decisions |
| Decision Challenge | Devil's advocate analysis |
| Technology Maturity | Evaluation framework |
| Team Capability | Constraint on technology selection |

## Running the Tests

```bash
# Run all tests
python test_system.py

# View all decisions and status
python scripts/status.py

# Run complete evaluation workflow
python scripts/query.py

# Display decision matrices
python scripts/matrix.py
```

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
# Decision Engine
DECISION_DEFAULT_WEIGHT_SUM=1.0
DECISION_MIN_SCORE=1.0
DECISION_MAX_SCORE=10.0

# Build vs Buy
BUILDBUY_HOURLY_RATE=150.0
BUILDBUY_DEFAULT_MIGRATION_COST=20000.0
BUILDBUY_ANNUAL_PRICE_INCREASE_PCT=5.0

# Constraints
CONSTRAINT_HARD_WEIGHT=1.0
CONSTRAINT_SOFT_WEIGHT=0.5

# Budget
MONTHLY_BUDGET_LIMIT_USD=15000.0

# Latency
LATENCY_P95_TARGET_MS=200.0
```

## Pre-seeded Decisions

The sample app comes pre-configured with:

### Decision Matrices
1. **Model Hosting** — Managed vs Self-Hosted vs Hybrid
2. **Vector Storage** — PostgreSQL + pgvector vs Pinecone vs Weaviate
3. **Inference Platform** — Managed API vs vLLM vs KServe vs Hybrid

### ADRs
1. **ADR-001: Model Hosting Strategy** — Hybrid architecture
2. **ADR-002: Vector Storage Strategy** — PostgreSQL + pgvector
3. **ADR-003: Inference Platform Strategy** — Hybrid platform

### Build vs Buy Analyses
1. **Vector Search** — Custom vs Pinecone vs pgvector
2. **Model Gateway** — Custom vs Managed vs LiteLLM
3. **Observability** — Custom vs Datadog vs Prometheus/Grafana

### Hard Constraints
1. Data Cannot Leave VPC
2. SOC 2 Compliance Required
3. Team Can Operate Technology
4. Budget Limit ($15,000/month)
5. Latency Requirement (< 200ms p95)
6. No Single Provider Dependency
7. Enterprise IAM Integration

## Next Steps

After running this sample app, you should understand:

1. How to evaluate technology options systematically
2. How to use weighted scoring with hard constraints
3. How to perform Build vs Buy analysis with full cost calculation
4. How to document decisions as ADRs with revisit conditions
5. How to challenge your own architectural decisions
6. How team capability influences technology selection

Move to **Day 09 → Scale, Reliability & AI FinOps** to learn about scaling AI systems.
