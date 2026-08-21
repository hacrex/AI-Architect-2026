"""Chunking comparison tool."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.chunker import chunk_document


SAMPLE_TEXT = """
# Kubernetes Deployment Guide

## Overview

Kubernetes is an open-source container orchestration platform that automates the deployment, scaling, and management of containerized applications.

## Prerequisites

Before deploying to Kubernetes, ensure you have:

- kubectl installed and configured
- Access to the cluster
- Docker image built and pushed to registry

## Deployment Process

### Step 1: Build Image

Build your Docker image:

```bash
docker build -t myapp:latest .
```

### Step 2: Push to Registry

Push the image to our container registry:

```bash
docker push registry.company.com/myapp:latest
```

### Step 3: Apply Deployment

Apply the Kubernetes deployment manifest:

```bash
kubectl apply -f deployment.yaml -n engineering
```

### Step 4: Verify

Check that pods are running:

```bash
kubectl get pods -n engineering
```

## Health Checks

All deployments must include health checks:

- Liveness probe: /health/live
- Readiness probe: /health/ready

## Monitoring

Deployments are monitored via Prometheus and Grafana.
"""


def main():
    print("=== Chunking Comparison ===\n")
    
    strategies = ["fixed", "semantic", "structure"]
    
    results = {}
    
    for strategy in strategies:
        chunks = chunk_document(SAMPLE_TEXT, strategy=strategy)
        
        avg_size = sum(c["token_count"] for c in chunks) / len(chunks) if chunks else 0
        
        results[strategy] = {
            "chunk_count": len(chunks),
            "avg_size": avg_size,
            "chunks": chunks,
        }
        
        print(f"Strategy: {strategy}")
        print(f"  Chunks: {len(chunks)}")
        print(f"  Avg size: {avg_size:.1f} tokens")
        print()
    
    print("=== Comparison Results ===\n")
    
    print("| Strategy | Chunks | Avg Size |")
    print("|----------|--------|----------|")
    for strategy, data in results.items():
        print(f"| {strategy:10} | {data['chunk_count']:6} | {data['avg_size']:8.1f} |")
    
    print("\n=== Sample Chunks (Structure) ===\n")
    
    for i, chunk in enumerate(results["structure"]["chunks"][:3]):
        print(f"Chunk {i+1} ({chunk['token_count']} tokens):")
        print(f"  {chunk['text'][:100]}...")
        print()


if __name__ == "__main__":
    main()
