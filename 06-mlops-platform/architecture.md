# MLOps — Platform Architecture

## Platform Capabilities Matrix

| Capability | Tool/Service | Description |
|------------|--------------|-------------|
| Experiment tracking | MLflow, W&B | Log params, metrics, artifacts |
| Model registry | MLflow, Vertex | Versioned model storage |
| Pipeline orchestration | Kubeflow, Airflow | Automated data→model pipelines |
| Deployment | KServe, Seldon | Model serving with traffic splitting |
| Monitoring | Prometheus, Grafana | Infrastructure + model metrics |
| CI/CD | GitHub Actions | Automated testing and deployment |
| Data versioning | DVC, LakeFS | Reproducible data snapshots |
| Evaluation | Ragas, DeepEval | AI-specific quality metrics |
| Feature Store | Feast, Tecton | Reusable feature serving |
| LLM Observability | LangSmith, Phoenix | Traces, evals, prompt tracking |

---

## Full Platform Architecture

```
                         Developers
                             │
                             ▼
                    ┌─────────────────┐
                    │  Developer       │
                    │  Portal / CLI    │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
         ┌─────────┐   ┌─────────┐   ┌─────────┐
         │Templates │   │  APIs   │   │  SDKs   │
         └────┬────┘   └────┬────┘   └────┬────┘
              └──────────────┼──────────────┘
                             ▼
                    ┌─────────────────┐
                    │  AI Control     │
                    │  Plane          │
                    └────────┬────────┘
                             │
       ┌─────────────────────┼─────────────────────┐
       ▼                     ▼                     ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Model     │     │ Evaluation  │     │ Governance  │
│   Registry  │     │  Platform   │     │  & Policy   │
│             │     │             │     │             │
│ • Versions  │     │ • Quality   │     │ • IAM       │
│ • Approvals │     │ • Safety    │     │ • Audit     │
│ • Lineage   │     │ • Cost      │     │ • Compliance│
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       └─────────────────────┼─────────────────────┘
                             ▼
                    ┌─────────────────┐
                    │  AI Data Plane  │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                  ▼
     ┌─────────┐       ┌─────────┐       ┌─────────┐
     │  RAG    │       │ Agents  │       │Inference│
     │         │       │         │       │         │
     │ • Vector│       │ • Tools │       │ • vLLM  │
     │ • Rerank│       │ • Routes│       │ • Triton│
     │ • Store │       │ • Guard │       │ • API   │
     └────┬────┘       └────┬────┘       └────┬────┘
          └──────────────────┼──────────────────┘
                             ▼
                    ┌─────────────────┐
                    │    AI Data      │
                    │    Platform     │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                  ▼
     ┌─────────┐       ┌─────────┐       ┌─────────┐
     │Ingestion│       │ Feature │       │ Vector  │
     │Pipeline │       │  Store  │       │    DB   │
     └─────────┘       └─────────┘       └─────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Infrastructure │
                    │  Kubernetes+GPU │
                    └─────────────────┘
```

---

## CI/CD Pipeline for AI

```
                 Git Push
                    │
                    ▼
            ┌───────────────┐
            │   Build/Test   │
            └───────┬───────┘
                    │
                    ▼
            ┌───────────────┐
            │ Security Scan │
            └───────┬───────┘
                    │
                    ▼
            ┌───────────────┐
            │ AI Evaluation │
            │ ┌─────┬─────┐ │
            │ │Qual │Safe │ │
            │ │Cost │Perf │ │
            │ └─────┴─────┘ │
            └───────┬───────┘
                    │
             ┌──────┴──────┐
             ▼             ▼
           PASS          FAIL
             │             │
             ▼             ▼
      ┌────────────┐     STOP
      │  Registry  │
      └─────┬──────┘
            │
            ▼
      ┌────────────┐
      │  Staging   │
      └─────┬──────┘
            │
            ▼
      ┌────────────┐
      │  Canary    │  5% → 25% → 50% → 100%
      └─────┬──────┘
            │
            ▼
      ┌────────────┐
      │ Production │
      └─────┬──────┘
            │
            ▼
      ┌────────────┐
      │ Monitoring │
      └────────────┘
```

---

## Model Lifecycle

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Experiment  │────▶│   Evaluate   │────▶│   Register   │
│              │     │              │     │              │
│ • Dataset    │     │ • Quality    │     │ • Version    │
│ • Parameters │     │ • Safety     │     │ • Approvals  │
│ • Prompt     │     │ • Cost       │     │ • Lineage    │
│ • Model      │     │ • Latency    │     │ • Status     │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                  │
                                                  ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Improve    │◀────│   Monitor    │◀────│    Deploy    │
│              │     │              │     │              │
│ • Feedback   │     │ • Drift      │     │ • Staging    │
│ • Retrain    │     │ • Quality    │     │ • Canary     │
│ • New Data   │     │ • Cost       │     │ • Production │
│ • Prompts    │     │ • Usage      │     │ • Rollback   │
└──────────────┘     └──────────────┘     └──────────────┘
```

---

## Control Plane vs Data Plane

```
┌─────────────────────────────────────────────────────┐
│                  AI CONTROL PLANE                    │
│                                                     │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐      │
│  │  Registry │  │  Policy   │  │ Deployment│      │
│  └───────────┘  └───────────┘  └───────────┘      │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐      │
│  │ Evaluation│  │Governance │  │   Users   │      │
│  └───────────┘  └───────────┘  └───────────┘      │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│                  AI DATA PLANE                       │
│                                                     │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐      │
│  │   RAG     │  │  Agents   │  │ Inference │      │
│  └───────────┘  └───────────┘  └───────────┘      │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐      │
│  │  Tools    │  │  Models   │  │   Data    │      │
│  └───────────┘  └───────────┘  └───────────┘      │
└─────────────────────────────────────────────────────┘
```

---

## Platform API (Conceptual)

```yaml
# Application Management
POST   /api/v1/applications          # Create new AI application
GET    /api/v1/applications          # List applications
GET    /api/v1/applications/{id}     # Get application details
DELETE /api/v1/applications/{id}     # Decommission application

# Model Registry
POST   /api/v1/models                # Register new model version
GET    /api/v1/models                # List models
GET    /api/v1/models/{id}           # Get model details
POST   /api/v1/models/{id}/promote   # Promote to next stage
POST   /api/v1/models/{id}/rollback  # Rollback to previous version

# Deployment
POST   /api/v1/deployments           # Create deployment
GET    /api/v1/deployments           # List deployments
GET    /api/v1/deployments/{id}      # Get deployment status
PUT    /api/v1/deployments/{id}      # Update deployment
DELETE /api/v1/deployments/{id}      # Tear down deployment

# Evaluation
POST   /api/v1/evaluations           # Run evaluation
GET    /api/v1/evaluations           # List evaluations
GET    /api/v1/evaluations/{id}      # Get evaluation results

# Observability
GET    /api/v1/metrics               # Get platform metrics
GET    /api/v1/traces                # Get traces
GET    /api/v1/alerts                # Get active alerts

# Operations
POST   /api/v1/rollback              # Rollback a deployment
POST   /api/v1/pause                 # Pause traffic to a service
POST   /api/v1/resume                # Resume traffic
```

---

## Deployment Strategies

### Blue-Green

```
         ┌──────────────────┐
         │   Load Balancer  │
         └────────┬─────────┘
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
  ┌───────────┐       ┌───────────┐
  │   Blue    │       │   Green   │
  │  (v1)     │       │  (v2)     │
  │  ACTIVE   │       │  STANDBY  │
  └───────────┘       └───────────┘

Switch: instant cutover
Rollback: instant switch back
```

### Canary

```
         ┌──────────────────┐
         │   Load Balancer  │
         └────────┬─────────┘
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
  ┌───────────┐       ┌───────────┐
  │   v1      │       │   v2      │
  │  95%      │       │   5%      │
  │  traffic  │       │  traffic  │
  └───────────┘       └───────────┘

Observe → Expand → Full rollout
```

### Shadow

```
         ┌──────────────────┐
         │   Load Balancer  │
         └────────┬─────────┘
                  │
                  ├─── 100% ──→ ┌───────────┐
                  │              │    v1     │
                  │              │  (live)   │
                  │              └───────────┘
                  │
                  └─── copy ───→ ┌───────────┐
                                 │    v2     │
                                 │ (shadow)  │
                                 └───────────┘
```
