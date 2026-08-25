# ADR-006: Kubernetes for Infrastructure Orchestration

## Status

Accepted

## Date

2026-08-21

## Context

We need to orchestrate multiple services: API gateway, AI application, RAG pipeline, agent system, model serving, and supporting infrastructure. Requirements include:

- Auto-scaling based on load
- GPU scheduling for model inference
- Service discovery and load balancing
- Rolling deployments with zero downtime
- Multi-AZ high availability

## Options

| Option | Pros | Cons |
|--------|------|------|
| Kubernetes (EKS) | Existing expertise, flexible, GPU support | Operational complexity |
| ECS Fargate | Simpler, serverless | Less control, GPU limitations |
| EC2 instances | Full control | Manual scaling, no orchestration |
| Managed inference (SageMaker) | Purpose-built | Expensive, limited flexibility |

## Decision

We will use **Kubernetes (EKS)** with GPU node pools.

## Rationale

- Existing team Kubernetes expertise
- Flexible GPU scheduling with node pools
- Cost control through spot instances and right-sizing
- Rich ecosystem for observability, security, and networking

## Consequences

### Positive

- Leverages existing team skills
- GPU time-sharing across workloads
- Rich ecosystem of operators and tools
- Consistent deployment model

### Negative

- Operational complexity
- Kubernetes learning curve for new team members
- GPU operator expertise needed

## Review Date

2026-11-21 (3 months post-launch)
