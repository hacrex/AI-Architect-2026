# MLOps & AI Platform — Sample App

A working prototype demonstrating **experiment tracking**, **model registry**, **evaluation pipeline**, **CI/CD for AI**, **canary deployment**, and **monitoring** from Day 06.

> **Building on Day 05**: This app takes the data architecture and adds the operational layer — lifecycle management, evaluation gates, deployment strategies, and monitoring.

## Architecture

```
                         Developer
                             │
                             ▼
                    ┌─────────────────┐
                    │  Experiment     │
                    │  Tracker        │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Evaluation     │
                    │  Pipeline       │
                    │  ┌─────┐        │
                    │  │Gate │        │
                    │  └─────┘        │
                    └────────┬────────┘
                             │
                     ┌───────┴───────┐
                     ▼               ▼
                  PASS             FAIL
                     │               │
                     ▼               ▼
              ┌────────────┐      STOP
              │  Model     │
              │  Registry  │
              └─────┬──────┘
                    │
                    ▼
              ┌────────────┐
              │ Deployment │
              │ Engine     │
              ├────────────┤
              │ Staging    │
              │ Canary     │
              │ Production │
              └─────┬──────┘
                    │
                    ▼
              ┌────────────┐
              │ Monitoring │
              │ & Drift    │
              └────────────┘
```

## Project Structure

```
sample-app/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI platform API
│   ├── models.py            # Pydantic models
│   ├── registry.py          # Model registry
│   ├── evaluation.py        # Evaluation pipeline
│   ├── deployment.py        # Deployment engine
│   ├── monitoring.py        # Monitoring & drift detection
│   └── experiment.py        # Experiment tracking
├── config/
│   ├── settings.py          # Configuration
│   └── .env.example         # Environment template
├── pipelines/
│   ├── cicd_pipeline.py     # CI/CD pipeline simulation
│   └── promotion.py         # Model promotion workflow
├── scripts/
│   ├── register_model.py    # Register a model
│   ├── evaluate.py          # Run evaluation
│   ├── deploy.py            # Deploy model
│   └── monitor.py           # Check monitoring
├── requirements.txt
└── test_platform.py         # Test script
```

## Quick Start

```bash
# 1. Navigate to sample-app
cd 06-mlops-platform/sample-app

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the platform API
uvicorn app.main:app --reload --port 8080

# 5. Open API docs
# http://localhost:8080/docs
```

## Core Components

### 1. Experiment Tracking

Track every experiment with:

- Dataset version
- Model configuration
- Prompt template
- Parameters
- Evaluation results

```python
from app.experiment import ExperimentTracker

tracker = ExperimentTracker()

experiment = tracker.create_experiment(
    name="rag-v1",
    dataset_version="2024-01-15",
    model="gpt-4",
    prompt_template="Answer based on context: {context}",
    parameters={"temperature": 0.2, "max_tokens": 500}
)

tracker.log_results(
    experiment_id=experiment.id,
    metrics={"accuracy": 0.91, "latency_ms": 450}
)
```

### 2. Model Registry

Central registry for all model versions:

```python
from app.registry import ModelRegistry

registry = ModelRegistry()

# Register a model
model = registry.register(
    name="enterprise-rag",
    version="1.0.0",
    source_experiment="exp-001",
    metrics={"accuracy": 0.91},
    artifacts={"prompt": "v1.txt", "config": "config.yaml"}
)

# Get model versions
versions = registry.list_versions("enterprise-rag")

# Promote model
registry.promote(
    name="enterprise-rag",
    version="1.0.0",
    stage="staging"
)
```

### 3. Evaluation Pipeline

Run evaluations before deployment:

```python
from app.evaluation import EvaluationPipeline

evaluator = EvaluationPipeline()

# Run evaluation
results = evaluator.evaluate(
    model="enterprise-rag",
    version="1.0.0",
    test_dataset="test-v1.json",
    metrics=["accuracy", "safety", "cost", "latency"]
)

# Check gates
if results.passed_all_gates():
    print("Ready for deployment")
else:
    print(f"Failed: {results.failed_gates}")
```

### 4. Deployment Engine

Deploy with canary strategy:

```python
from app.deployment import DeploymentEngine

deployer = DeploymentEngine()

# Deploy to staging
deployer.deploy(
    model="enterprise-rag",
    version="1.0.0",
    environment="staging"
)

# Canary to production
deployer.canary(
    model="enterprise-rag",
    version="1.0.0",
    initial_percentage=5,
    increment=25,
    observation_period_seconds=60
)

# Rollback if needed
deployer.rollback(
    model="enterprise-rag",
    reason="quality_degradation"
)
```

### 5. Monitoring & Drift Detection

Monitor deployed models:

```python
from app.monitoring import Monitor

monitor = Monitor()

# Check model health
health = monitor.check_health("enterprise-rag")
print(f"Status: {health.status}")
print(f"Quality: {health.quality_score}")
print(f"Drift: {health.drift_detected}")

# Get drift report
report = monitor.get_drift_report(
    model="enterprise-rag",
    time_range="7d"
)
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /experiments | Create experiment |
| GET | /experiments | List experiments |
| POST | /registry/register | Register model |
| GET | /registry/models | List models |
| POST | /registry/promote | Promote model |
| POST | /registry/rollback | Rollback model |
| POST | /evaluate | Run evaluation |
| GET | /evaluations | List evaluations |
| POST | /deploy | Deploy model |
| GET | /deployments | List deployments |
| GET | /monitor/{model} | Get model health |
| GET | /drift/{model} | Get drift report |

## CI/CD Pipeline

The `pipelines/cicd_pipeline.py` simulates a complete AI CI/CD pipeline:

```
Git Push
  │
  ▼
Build/Test
  │
  ▼
Security Scan
  │
  ▼
AI Evaluation
  │
  ├── Quality Gate (accuracy > 85%)
  ├── Safety Gate (toxicity < 5%)
  ├── Cost Gate (tokens < 1000)
  └── Latency Gate (p95 < 2000ms)
  │
  ▼
Registry
  │
  ▼
Staging
  │
  ▼
Canary (5% → 25% → 50% → 100%)
  │
  ▼
Production
```

## Model Promotion Flow

```
Experiment
    │
    ▼
Evaluate
    │
    ├── Pass → Register
    │              │
    │              ▼
    │          Staging
    │              │
    │              ▼
    │          Canary
    │              │
    │              ▼
    │          Production
    │
    └── Fail → Stop
```

## Key Concepts Demonstrated

| Concept | Implementation |
|---------|----------------|
| Experiment Tracking | Track all experiments with parameters and results |
| Model Registry | Version, store, and promote models |
| Evaluation Gates | Quality, safety, cost, latency checks |
| Canary Deployment | Gradual rollout with health checks |
| Drift Detection | Monitor for quality and behavior changes |
| Rollback | Instant rollback on failure |
| GitOps | Version-controlled deployments |

## Running the Tests

```bash
# Run all tests
python test_platform.py

# Run specific test
python -m pytest test_platform.py -v
```

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
# Registry
REGISTRY_BACKEND=sqlite
REGISTRY_DB_PATH=./data/registry.db

# Evaluation
EVAL_QUALITY_THRESHOLD=0.85
EVAL_SAFETY_THRESHOLD=0.95
EVAL_COST_THRESHOLD=1000
EVAL_LATENCY_THRESHOLD=2000

# Deployment
DEPLOY_STAGING_URL=http://localhost:8081
DEPLOY_PRODUCTION_URL=http://localhost:8082
CANARY_INITIAL_PERCENTAGE=5
CANARY_INCREMENT=25
CANARY_OBSERVATION_PERIOD=60

# Monitoring
MONITOR_CHECK_INTERVAL=60
DRIFT_THRESHOLD=0.1
```

## Next Steps

After running this sample app, you should understand:

1. How to track experiments
2. How to register and version models
3. How to run evaluations before deployment
4. How to deploy with canary strategy
5. How to monitor for drift
6. How to rollback on failure

Move to **Day 07 → AI System Architecture** to learn how all these layers become one coherent system.
