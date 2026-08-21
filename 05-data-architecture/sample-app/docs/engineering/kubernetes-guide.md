# Kubernetes Deployment Guide

Version: 2.1
Created: 2026-07-15
Updated: 2026-08-10
Department: Engineering
Classification: Internal

## Overview

This guide covers best practices for deploying applications to our Kubernetes clusters.

## Prerequisites

- Access to the `engineering` namespace
- kubectl configured with cluster credentials
- Docker image pushed to our registry

## Deployment Process

### Step 1: Build and Push Image

```bash
docker build -t registry.company.com/app:latest .
docker push registry.company.com/app:latest
```

### Step 2: Update Deployment

```bash
kubectl set image deployment/myapp myapp=registry.company.com/app:latest -n engineering
```

### Step 3: Verify Deployment

```bash
kubectl get pods -n engineering
kubectl logs -f deployment/myapp -n engineering
```

## Health Checks

All deployments must include:

- **Liveness probe**: `/health/live`
- **Readiness probe**: `/health/ready`
- **Startup probe**: `/health/startup`

## Resource Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| CPU | 100m | 500m |
| Memory | 128Mi | 512Mi |
| GPU | None | T4 (if ML workload) |

## Rolling Updates

We use rolling updates with:

- `maxSurge: 25%`
- `maxUnavailable: 0`

This ensures zero-downtime deployments.

## Rollback

If issues occur:

```bash
kubectl rollout undo deployment/myapp -n engineering
```

## Monitoring

Deployments are monitored via:

- Prometheus metrics
- Grafana dashboards
- PagerDuty alerts
