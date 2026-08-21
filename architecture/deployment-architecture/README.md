# Deployment Architecture — Enterprise AI Knowledge Assistant

## Infrastructure Topology

This document describes the deployment infrastructure for the Enterprise AI Knowledge Assistant.

## Cloud Provider

Primary: AWS (can be adapted to Azure/GCP)

## Production Deployment

```
                         Internet
                            │
                            ▼
                    ┌──────────────┐
                    │     WAF      │
                    └──────┬───────┘
                            │
                    ┌───────┴───────┐
                    │  CloudFront   │
                    │  (CDN)        │
                    └───────┬───────┘
                            │
                    ┌───────┴───────┐
                    │     ALB       │
                    │ (Load Balancer)│
                    └───────┬───────┘
                            │
               ┌────────────┼────────────┐
               ▼            ▼            ▼
        ┌────────────┐┌────────────┐┌────────────┐
        │  EKS       ││  EKS       ││  EKS       │
        │  Node 1    ││  Node 2    ││  GPU Node  │
        │  (API GW)  ││  (AI App)  ││  (Models)  │
        └─────┬──────┘└─────┬──────┘└─────┬──────┘
              │             │             │
              ▼             ▼             ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │  nginx   │ │ FastAPI  │ │  vLLM    │
        │  ingress │ │ app      │ │  server  │
        └──────────┘ └──────────┘ └──────────┘
```

## Kubernetes Cluster

### Node Pools

| Node Pool | Instance Type | Count | Purpose |
|-----------|--------------|-------|---------|
| API | m6i.xlarge | 2 | API Gateway, AI Gateway |
| Application | m6i.2xlarge | 3 | RAG pipeline, Agent system |
| GPU | g5.2xlarge | 2 | Model inference (A10G) |
| System | m6i.large | 3 | Monitoring, logging, DB |

### Namespaces

```
ai-knowledge-assistant
├── api-gateway       (nginx ingress, API GW)
├── ai-app            (FastAPI, RAG, Agents)
├── model-serving     (vLLM, model gateway)
├── data              (Redis, PostgreSQL)
├── monitoring        (Prometheus, Grafana)
└── security          (vault, cert-manager)
```

## Managed Services

| Service | Purpose | Configuration |
|---------|---------|---------------|
| RDS PostgreSQL | Metadata, conversation history | db.r6g.xlarge, Multi-AZ |
| ElastiCache Redis | Session cache, semantic cache | cache.r6g.large, cluster mode |
| S3 | Document storage | Standard, versioning enabled |
| OpenSearch | Audit logs, search | 3-node cluster |
| CloudWatch | Metrics, logs | Custom dashboards |
| Secrets Manager | API keys, credentials | Automatic rotation |

## GPU Instances

| Instance | GPU | Memory | Purpose |
|----------|-----|--------|---------|
| g5.2xlarge | 1x A10G | 24GB | Small models (7B-13B) |
| g5.4xlarge | 1x A10G | 24GB | Medium models (13B-30B) |
| p4d.24xlarge | 8x A100 | 320GB | Large models (70B+) |

## Network Topology

```
VPC (10.0.0.0/16)
├── Public Subnets (10.0.1.0/24, 10.0.2.0/24)
│   └── ALB, NAT Gateway
├── Private Subnets (10.0.10.0/24, 10.0.20.0/24)
│   ├── API nodes
│   └── Application nodes
└── Private Subnets (10.0.30.0/24, 10.0.40.0/24)
    ├── GPU nodes (isolated)
    └── Data nodes (isolated)
```

## Scaling Strategy

| Component | Scaling Type | Trigger | Min/Max |
|-----------|-------------|---------|---------|
| API Gateway | HPA | CPU > 70% | 2/6 |
| Application | HPA | CPU > 70%, queue depth | 3/10 |
| GPU Inference | KEDA | Queue depth, GPU util | 1/4 |
| PostgreSQL | Vertical | Connection count | Single/Multi-AZ |
| Redis | Cluster mode | Memory > 70% | 3/9 shards |

## High Availability

- **Multi-AZ**: All stateful services run across 3 AZs
- **Pod Disruption Budgets**: Minimum 2 replicas for critical services
- **Health Checks**: Liveness + readiness probes on all services
- **Failover**: Automatic failover for RDS, Redis, and ALB
- **Backup**: Daily snapshots, 30-day retention
