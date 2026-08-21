# AI Infrastructure — Inference Serving Sample App

A working prototype demonstrating **inference serving**, **Docker deployment**, and **Kubernetes patterns** from Day 04.

> **Building on Day 03**: This app takes the multi-agent system and adds production infrastructure — containerization, orchestration, and inference optimization.

## Architecture

```
                    Load Balancer
                         │
                         ▼
              ┌─────────────────────┐
              │   Inference API     │
              │   (FastAPI)         │
              ├─────────────────────┤
              │   Model Manager     │
              │   (vLLM/SGLang)     │
              ├─────────────────────┤
              │   Health & Metrics  │
              │   (Prometheus)      │
              └──────────┬──────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │     GPU      │
                  │   (CUDA)     │
                  └──────────────┘
```

## Project Structure

```
sample-app/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI inference server
│   ├── models.py            # Pydantic models
│   ├── inference.py         # Model inference engine
│   ├── health.py            # Health checks & metrics
│   └── batch.py             # Batching scheduler
├── config/
│   ├── settings.py          # Configuration management
│   └── .env.example         # Environment variables template
├── docker/
│   ├── Dockerfile           # GPU-enabled container
│   └── docker-compose.yml   # Local development stack
├── k8s/
│   ├── deployment.yaml      # Kubernetes deployment
│   ├── service.yaml         # Kubernetes service
│   ├── hpa.yaml             # Horizontal pod autoscaler
│   └── node-pool.yaml       # GPU node pool config
├── scripts/
│   ├── benchmark.py         # Performance benchmarking
│   ├── load-test.py         # Concurrency testing
│   └── measure_latency.py   # Latency measurement
├── benchmarks/
│   └── results.md           # Benchmark results template
├── requirements.txt
└── test_inference.py        # Test script
```

## Quick Start

### 1. Install Dependencies

```bash
cd 04-ai-infrastructure/sample-app
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp config/.env.example config/.env
# Edit config/.env with your configuration
```

### 3. Start the Server (CPU Mode)

```bash
uvicorn app.main:app --reload --port 8003
```

### 4. Test the API

```bash
python test_inference.py
```

Or manually:

```bash
# Health check
curl http://localhost:8003/health

# Single inference
curl -X POST http://localhost:8003/inference \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain the concept of containerization", "max_tokens": 200}'

# Batch inference
curl -X POST http://localhost:8003/inference/batch \
  -H "Content-Type: application/json" \
  -d '{"prompts": ["What is Docker?", "What is Kubernetes?", "What is vLLM?"], "max_tokens": 100}'

# Streaming
curl -X POST http://localhost:8003/inference/stream \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write a short story about a robot", "max_tokens": 300}'

# Metrics
curl http://localhost:8003/metrics
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check with GPU status |
| `/inference` | POST | Single prompt inference |
| `/inference/stream` | POST | Streaming inference |
| `/inference/batch` | POST | Batch inference (multiple prompts) |
| `/metrics` | GET | Performance metrics (Prometheus format) |
| `/model/info` | GET | Model information and configuration |
| `/model/reload` | POST | Hot-reload model (admin) |

## Docker Deployment

### Build the Image

```bash
docker build -f docker/Dockerfile -t ai-inference:latest .
```

### Run with Docker Compose

```bash
cd docker
docker-compose up -d
```

This starts:
- Inference server (port 8003)
- Prometheus (port 9090)
- Grafana (port 3000)

### GPU Support

```bash
# With NVIDIA GPU
docker run --gpus all -p 8003:8003 ai-inference:latest

# With specific GPU
docker run --gpus '"device=0"' -p 8003:8003 ai-inference:latest
```

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster with GPU nodes
- NVIDIA device plugin installed
- kubectl configured

### Deploy

```bash
# Create namespace
kubectl create namespace ai-inference

# Apply manifests
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml

# Check status
kubectl get pods -n ai-inference
kubectl get svc -n ai-inference
```

### GPU Node Pool

```bash
# GKE
gcloud container node-pools create gpu-pool \
  --cluster=my-cluster \
  --machine-type=n1-standard-8 \
  --accelerator=type=nvidia-tesla-t4,count=1 \
  --num-nodes=3

# EKS
eksctl create nodegroup \
  --cluster=my-cluster \
  --name=gpu-nodes \
  --instance-type=p3.2xlarge \
  --nodes=3
```

## Performance Benchmarking

### Run Benchmark

```bash
python scripts/benchmark.py
```

### Metrics Collected

- **Throughput**: Requests per second
- **Latency**: Time to first token (TTFT), total latency
- **GPU Utilization**: Memory and compute usage
- **Batch Efficiency**: Optimal batch size analysis

### Sample Results

| Metric | Value |
|--------|-------|
| Throughput | 45 req/s |
| TTFT | 120ms |
| Total Latency (500 tokens) | 2.1s |
| GPU Memory | 12.4 GB |
| GPU Utilization | 78% |

## Configuration

### Environment Variables

```bash
# Model Configuration
MODEL_NAME=meta-llama/Llama-2-7b-hf
MODEL_DEVICE=cuda
MAX_TOKENS=2048
TEMPERATURE=0.7

# Server Configuration
WORKERS=4
BATCH_SIZE=16
MAX_CONCURRENT_REQUESTS=100

# Monitoring
ENABLE_METRICS=true
METRICS_PORT=9090
```

## Architecture Patterns Demonstrated

| Pattern | Implementation |
|---------|----------------|
| **Inference Serving** | Optimized model execution |
| **Batching** | Dynamic request batching |
| **Health Checks** | Liveness & readiness probes |
| **Auto-scaling** | HPA based on GPU metrics |
| **Observability** | Prometheus metrics, Grafana dashboards |
| **Containerization** | Docker with GPU support |
| **Orchestration** | Kubernetes deployment |

## Key Concepts (Day 04)

This sample app demonstrates:

1. **Inference Serving** — Turning models into production services
2. **Batching** — Optimizing GPU utilization through request batching
3. **Containerization** — Docker images with GPU support
4. **Orchestration** — Kubernetes deployments for AI workloads
5. **Auto-scaling** — Scaling based on GPU metrics
6. **Observability** — Monitoring inference performance
7. **Benchmarking** — Measuring latency, throughput, and utilization
