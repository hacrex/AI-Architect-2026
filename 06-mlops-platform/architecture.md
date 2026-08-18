# MLOps — Platform Architecture

## Platform capabilities matrix

| Capability | Tool/Service | Description |
|------------|--------------|-------------|
| Experiment tracking | MLflow, W&B | Log params, metrics, artifacts |
| Model registry | MLflow, Vertex | Versioned model storage |
| Pipeline orchestration | Kubeflow, Airflow | Automated data→model pipelines |
| Deployment | KServe, Seldon | Model serving with traffic splitting |
| Monitoring | Prometheus, Grafana | Infrastructure + model metrics |
| CI/CD | GitHub Actions | Automated testing and deployment |
| Data versioning | DVC, LakeFS | Reproducible data snapshots |

## Platform architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Developer Interface                    │
│  (CLI, UI, API)                                         │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  Platform Services                       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │Registry  │ │Pipeline  │ │Evaluate  │ │Deploy    │  │
│  │Service   │ │Service   │ │Service   │ │Service   │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                 Infrastructure Layer                     │
│  (Kubernetes, GPUs, Storage, Networking)                 │
└─────────────────────────────────────────────────────────┘
```
