# Day 04 — AI Infrastructure Architecture

> **Building on Day 03**: Yesterday we designed the AI application layer with RAG, agents, and model routing. Today we design the infrastructure that makes it production-ready.

---

## Day 04 Enterprise AI Knowledge Assistant

### Infrastructure Diagram

```
                         Users
                           │
                           ▼
                     API Gateway
                           │
                           ▼
                      AI Gateway
                           │
                           ▼
                     Model Gateway
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
         Managed LLM  Inference     Fallback
              │        Platform         │
              │            │            │
              │       ┌────┴────┐       │
              │       │ K8s     │       │
              │       └────┬────┘       │
              │            │            │
              │    ┌───────┼───────┐    │
              │    ▼       ▼       ▼    │
              │  GPU     GPU     GPU    │
              │  Node    Node    Node   │
              │    │       │       │    │
              │  vLLM   vLLM    vLLM  │
              │  KServe KServe  KServe │
              │    │       │       │    │
              │    └───────┼───────┘    │
              │            ▼            │
              │         Models          │
              └────────────┼────────────┘
                           ▼
                        Response
```

### Cross-Cutting Concerns

```
┌─────────────────────────────────────────────────────────┐
│                    Security                              │
├─────────────────────────────────────────────────────────┤
│                  Observability                           │
├─────────────────────────────────────────────────────────┤
│                    Reliability                           │
├─────────────────────────────────────────────────────────┤
│                   Governance                             │
├─────────────────────────────────────────────────────────┤
│                     FinOps                               │
└─────────────────────────────────────────────────────────┘
```

## Full Stack View

```
                         Business
                            │
                         Product
                            │
                       Application
                            │
                       AI Gateway
                            │
                     Model Gateway
                            │
                 ┌──────────┴──────────┐
                 │                     │
              Managed              Self-hosted
               Models                 Models
                                       │
                                  Kubernetes
                                       │
                                    GPU Pool
                                       │
                              Inference Servers
                                       │
                                    Models
```

## Deployment Comparison

### Option A: Managed Model API

```
┌──────────┐    ┌──────────┐    ┌─────────────────┐
│  Client  │───▶│ Gateway  │───▶│ Provider API    │
└──────────┘    └──────────┘    │ (OpenAI/Anthropic)│
                                └─────────────────┘
```

**Pros:** Fast adoption, low ops burden, strong capabilities
**Cons:** Per-token cost, vendor dependency, API limits, data privacy concerns

### Option B: Self-Hosted Open-Weight Model

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌─────────┐
│  Client  │───▶│ Gateway  │───▶│ K8s + GPU│───▶│ Model   │
└──────────┘    └──────────┘    │ Cluster  │    │ (vLLM)  │
                                └──────────┘    └─────────┘
```

**Pros:** Full control, data locality, customization, predictable economics at scale
**Cons:** GPU costs, operations, upgrades, reliability, security, platform engineering

### Option C: Hybrid Architecture

```
                    AI Gateway
                        │
             ┌──────────┼──────────┐
             ▼          ▼          ▼
          Cloud      Self-hosted   Cloud
          Model        Model       Model
              │            │            │
              ▼            ▼            ▼
         Provider     Kubernetes    Provider
            GPU           GPU          GPU
```

## Comparison Matrix

| Factor | Managed API | Self-Hosted | Hybrid |
|--------|------------|-------------|--------|
| Cost at low volume | Lower | Higher | Mixed |
| Cost at high volume | Higher | Lower | Optimized |
| Latency | Network-dependent | Local, lower | Mixed |
| Privacy | Provider sees data | Full control | Workload-dependent |
| Scaling | Automatic | Manual design | Mixed |
| Operations | None | Significant | Moderate |
| Vendor lock-in | High | Low | Medium |

## Capacity Plan

### Expected Traffic

| Metric | Value |
|--------|-------|
| Total users | 10,000 |
| Peak concurrent | 500 |
| Average requests/user/day | 20 |
| Peak requests/second | ~50 |
| Average input tokens | 500 |
| Average output tokens | 200 |

### GPU Requirements

| Model | Size | GPUs Required | Instances |
|-------|------|---------------|-----------|
| Primary inference | 70B | 2 GPUs | 4 |
| Fallback | 7B | 1 GPU | 2 |
| Classification | 7B | 1 GPU | 2 |

### Latency Targets

| Metric | Target |
|--------|--------|
| TTFT | < 500ms |
| Total latency (500 tokens) | < 5s |
| Availability | 99.9% |

### Scaling Strategy

- **Horizontal:** Add GPU pods based on queue depth
- **Vertical:** Scale model size based on quality requirements
- **Hybrid:** Route to managed APIs during peak load

## Infrastructure Decision Record

### Decision: Managed, Self-Hosted, or Hybrid Inference

**Context:** Enterprise AI Knowledge Assistant serving 10,000 users with multiple LLM workloads.

**Decision:** Hybrid architecture with self-hosted primary inference and managed fallback.

**Rationale:**

- Sensitive workloads (internal data) → Self-hosted for data locality
- General workloads → Managed for simplicity
- High-volume workloads → Self-hosted for cost optimization
- Complex reasoning → Premium managed model for quality
- Peak overflow → Managed APIs for elastic capacity

**Consequences:**

- Requires Kubernetes expertise
- Need to manage GPU infrastructure
- Must implement intelligent routing
- Need to monitor both managed and self-hosted costs
- Requires fallback mechanisms

## Architectural Trade-offs

### Throughput vs Latency

Higher batching → Higher throughput → Potentially higher latency

### Cost vs Quality

Quantization → Lower cost → Potentially lower quality

### Control vs Operations

Self-hosted → More control → More operational burden

### Scale vs Complexity

Multi-model → More capabilities → More complexity

### Availability vs Cost

Redundancy → Higher availability → Higher cost
