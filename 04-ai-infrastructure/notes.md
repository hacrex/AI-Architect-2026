# Day 04 — AI Infrastructure

> **Building on Day 03**: Yesterday we learned LLM engineering patterns — RAG, agents, tool use, and model routing. Today we go one layer deeper into the infrastructure that makes those patterns production-ready.

An AI Architect doesn't just design applications. An AI Architect understands the infrastructure that runs those applications reliably at scale.

Today, we reach the layer where AI meets your strongest engineering territory.

---

## Table of Contents

1. [Why AI Infrastructure Is Different](#1-why-ai-infrastructure-is-different)
2. [CPU vs GPU](#2-cpu-vs-gpu)
3. [GPU Memory](#3-gpu-memory)
4. [Quantization](#4-quantization)
5. [Model Serving](#5-model-serving)
6. [vLLM](#6-vllm)
7. [Continuous Batching](#7-continuous-batching)
8. [Time to First Token vs Total Latency](#8-time-to-first-token-vs-total-latency)
9. [Docker and AI Workloads](#9-docker-and-ai-workloads)
10. [Kubernetes + GPUs](#10-kubernetes--gpus)
11. [GPU Scheduling](#11-gpu-scheduling)
12. [Kubernetes Is Not the AI Architecture](#12-kubernetes-is-not-the-ai-architecture)
13. [KServe](#13-kserve)
14. [Autoscaling AI Workloads](#14-autoscaling-ai-workloads)
15. [Scale-to-Zero](#15-scale-to-zero)
16. [Multi-Model Infrastructure](#16-multi-model-infrastructure)
17. [Managed vs Self-Hosted AI Infrastructure](#17-managed-vs-self-hosted-ai-infrastructure)
18. [Hybrid AI Infrastructure](#18-hybrid-ai-infrastructure)
19. [Multi-Cloud AI](#19-multi-cloud-ai)
20. [Day 04 Architecture Exercise](#20-day-04-architecture-exercise)
21. [Day 04 Hands-On Labs](#21-day-04-hands-on-labs)
22. [Day 04 Deliverables](#22-day-04-deliverables)
23. [Key Takeaways](#23-key-takeaways)

> **Sample App**: The Enterprise AI Knowledge Assistant from Day 01-03 now needs production infrastructure.

## The Goal of Day 04

You do not need to become a CUDA expert or memorize Kubernetes YAML.

You need to understand:

- How do we turn an AI model into a scalable, reliable, observable production service?
- Why AI infrastructure is different from traditional web infrastructure
- How GPU memory and compute affect architecture decisions
- What inference servers do and why they matter
- How to design for concurrency, latency, and throughput
- When to use managed vs self-hosted vs hybrid infrastructure

---

## Objective

Understand how to turn an AI model into a scalable, reliable, observable production service.

## Why AI Infrastructure Is Different

Traditional web applications:

```
Request → Application → Database → Response
```

AI workloads introduce additional complexity:

```
Request → Preprocessing → Model → Inference → Token Generation → Response
```

The model may require:

- Large memory
- GPU acceleration
- Specialized runtimes
- High-throughput networking
- Model loading
- Batching
- Concurrency management
- Autoscaling

Performance depends on:

- Model size
- Input tokens
- Output tokens
- Context length
- GPU memory
- Batch size
- Concurrency

AI infrastructure is a distributed-systems problem with specialized accelerators.

## CPU vs GPU

CPU: Small number of powerful, general-purpose cores.

```
┌───┐ ┌───┐ ┌───┐ ┌───┐
│ C │ │ C │ │ C │ │ C │
└───┘ └───┘ └───┘ └───┘
```

GPU: Large number of parallel processing units.

```
┌─┬─┬─┬─┬─┬─┬─┬─┐
│ │ │ │ │ │ │ │ │
├─┼─┼─┼─┼─┼─┼─┼─┤
│ │ │ │ │ │ │ │ │
├─┼─┼─┼─┼─┼─┼─┼─┤
│ │ │ │ │ │ │ │ │
└─┴─┴─┴─┴─┴─┴─┴─┘
```

LLM inference contains significant parallel computation, making GPUs extremely important.

Key insight: GPU ≠ automatically faster AI. The architecture around the GPU matters.

## GPU Memory

One of the most important concepts: Can the model fit in GPU memory?

```
GPU
┌──────────────────────────┐
│ Model Weights             │
│ KV Cache                  │
│ Activations               │
│ Runtime Overhead          │
└──────────────────────────┘
```

Memory requirements increase with concurrency and context length.

Architectural decisions around memory:

- Quantization
- Model size
- Batching
- GPU type
- Number of GPUs
- Model parallelism
- Concurrency

## Quantization

Higher precision → More memory → Higher infrastructure cost

Quantization → Lower memory → Potentially lower cost

But there can be quality and performance trade-offs.

The architect's question: "What is the acceptable quality/performance trade-off for this workload?"

## Model Serving

```
Client → Load Balancer → Inference API → Model Server → GPU
```

A model-serving system handles:

- Requests
- Concurrency
- Batching
- Streaming
- Health checks
- Metrics
- Model loading
- Failures
- Scaling

## vLLM

An inference engine designed to efficiently serve LLM workloads.

Naive architecture:

```
Request → Python Application → Model → GPU
```

Production-oriented serving:

```
Requests → Inference Server → Scheduling / Batching → Optimized Model Execution → GPU
```

The inference layer manages model execution efficiently.

## Continuous Batching

100 users send requests. An inference engine batches work dynamically:

```
Request 1 ─┐
Request 2 ─┤
Request 3 ─┼──→ Scheduler → GPU
Request 4 ─┤
Request 5 ─┘
```

Improves GPU utilization and throughput, but introduces trade-offs around latency.

Throughput ↕ Latency is a fundamental architectural trade-off.

## Time to First Token vs Total Latency

```
User Request
     │
     ├───────────────┐
     │               │
     ▼               ▼
Time to First      Total
Token              Response
```

- **Time to First Token (TTFT):** How quickly does the model start responding?
- **Total Latency:** How long until the complete response is generated?

For interactive applications, TTFT significantly affects perceived responsiveness.

For batch workloads, total throughput may matter more.

Architecture depends on the workload.

## Docker and AI Workloads

Containers provide:

- Reproducibility
- Isolation
- Dependency management
- Deployment consistency

```
┌───────────────────────────────┐
│ AI Container                  │
│                               │
│ Application                   │
│ Inference Runtime             │
│ Model Dependencies            │
│ CUDA / GPU Libraries          │
└──────────────┬────────────────┘
               │
               ▼
              GPU
```

GPU workloads introduce additional requirements. The container runtime and orchestration platform need mechanisms to expose GPU resources.

## Kubernetes + GPUs

```
                 Kubernetes Cluster
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
     CPU Node        GPU Node        GPU Node
                        │               │
                   ┌────┴────┐     ┌────┴────┐
                   │ Model   │     │ Model   │
                   │ Server  │     │ Server  │
                   └─────────┘     └─────────┘
```

Kubernetes can schedule workloads requiring GPU resources through device plugins.

Architect-level questions:

- Which workloads need GPUs?
- How are GPU resources allocated?
- How do we isolate workloads?
- How do we scale GPU nodes?
- What happens when GPUs are exhausted?
- How do we avoid expensive idle GPUs?

## GPU Scheduling

Example cluster with 8 GPU nodes and different workload requirements:

```
                   Scheduler
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       GPU Pool 1   GPU Pool 2   CPU Pool
          │            │            │
       Inference    Inference     RAG/API
```

Introduces:

- Resource fragmentation
- GPU utilization
- Workload priority
- Capacity planning
- Scheduling constraints

## Kubernetes Is Not the AI Architecture

Kubernetes is an infrastructure platform. Your AI architecture still needs:

```
Application
    ↓
API Gateway
    ↓
AI Gateway
    ↓
Model Gateway
    ↓
Inference Platform
    ↓
GPU
```

Alongside:

- Data
- Security
- Observability
- Governance
- FinOps

Kubernetes is one layer, not the entire architecture.

## KServe

Kubernetes-native model serving capabilities:

```
                    Kubernetes
                         │
                         ▼
                    KServe
                         │
                ┌────────┴────────┐
                ▼                 ▼
          Model Service       Model Service
                │                 │
                ▼                 ▼
              GPU               GPU
```

Separate model serving concerns from application logic.

## Autoscaling AI Workloads

Traditional autoscaling signals: CPU, memory, request count.

AI workloads may need additional signals:

- GPU utilization
- Queue depth
- Active requests
- Token throughput
- Inference latency
- Model-specific workload

```
              Incoming Requests
                      │
                      ▼
                  Queue Depth
                      │
                      ▼
                  Autoscaler
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
      Scale Up                 Scale Down
          │                       │
          ▼                       ▼
       GPU Pods                GPU Pods
```

GPU autoscaling is expensive. Starting another GPU node isn't equivalent to starting another small web container.

## Scale-to-Zero

```
No Traffic → No Model Instances

Traffic → Start Model → Serve Requests
```

Trade-offs:

- Cost
- Cold Start
- Availability

Large models may have long startup times because the model has to be loaded into memory.

## Multi-Model Infrastructure

Organization with multiple models:

```
Model A → Customer Support
Model B → Code Generation
Model C → Document Classification
Model D → Internal Search
```

Architecture considerations:

- GPU partitioning
- Resource isolation
- Model loading
- Scheduling
- Priority
- Noisy neighbors
- Capacity planning

This becomes an AI platform, not simply an AI application.

## Managed vs Self-Hosted AI Infrastructure

### Managed

```
Your Application → Cloud AI Service → Provider Infrastructure → GPU
```

Advantages:

- Faster implementation
- Less infrastructure management
- Elastic capacity
- Reduced operational burden

Trade-offs:

- Ongoing API cost
- Provider dependency
- Limited infrastructure control
- Data/privacy considerations

### Self-Hosted

```
Application → AI Gateway → Kubernetes → Inference Server → GPU Cluster → Model
```

Advantages:

- Greater control
- Model choice
- Data locality
- Infrastructure customization
- Potential economics at high utilization

Trade-offs:

- GPU capital/operating cost
- Platform engineering
- Maintenance
- Upgrades
- Reliability
- Security

The correct answer is workload-dependent.

## Hybrid AI Infrastructure

Often the answer isn't either/or:

```
                    AI Gateway
                        │
             ┌──────────┼──────────┐
             ▼          ▼          ▼
          Cloud      Self-hosted   Cloud
          Model        Model       Model
```

Example workloads:

- Sensitive workloads → Self-hosted
- General workloads → Managed
- High-volume workloads → Optimized self-hosted inference
- Complex reasoning → Premium managed model

## Multi-Cloud AI

Potential environments:

- AWS
- Azure
- Google Cloud
- OCI
- Alibaba Cloud
- Private cloud
- On-premises
- Edge

Questions to ask before multi-cloud:

- Is there a regulatory requirement?
- Is there a pricing advantage?
- Is there a regional availability requirement?
- Do we need provider redundancy?
- Can the team operate multiple platforms?
- Does the workload justify the complexity?

Multi-cloud is an architectural decision, not a checkbox.

---

## Day 04 Architecture Exercise

Let's evolve our Enterprise AI Knowledge Assistant.

Yesterday it looked like:

```
User
    ↓
API Gateway
    ↓
AI Gateway
    ↓
RAG / Agents
    ↓
Model Gateway
    ↓
Models
```

Today, design the infrastructure underneath the model layer.

### Requirements

Assume:

- 10,000 users
- 500 concurrent users at peak
- Multiple LLM workloads
- High availability
- GPU-based self-hosted inference
- Managed model fallback
- Kubernetes
- Observability
- Cost monitoring

### Architecture to Design

```
Internet / Internal Network
          ↓
      API Gateway
          ↓
       AI Gateway
          ↓
      Model Gateway
          ↓
    ┌─────┴─────┐
    ↓           ↓
Managed      Kubernetes
Models          │
                ↓
            GPU Nodes
                │
          ┌─────┴─────┐
          ↓           ↓
        vLLM        KServe
          │           │
          └─────┬─────┘
                ↓
             Models
```

---

## Day 04 Hands-On Labs

You don't need to build a huge GPU cluster today. Run smaller experiments.

### Experiment 1 — Model Serving

Deploy an open-weight model using an inference server.

**Measure:**

- Startup time
- Memory usage
- Latency
- Throughput

### Experiment 2 — Concurrency

Send increasing numbers of requests:

- 1, 5, 10, 25, 50, 100

**Observe:**

- Latency
- Throughput
- Resource utilization
- Failures

### Experiment 3 — Model Size

Compare two model sizes.

**Observe:**

- Memory
- Latency
- Throughput
- Quality
- Infrastructure requirements

### Experiment 4 — Managed vs Self-Hosted

Compare your self-hosted setup with a managed model API.

**Document:**

- Operational complexity
- Performance
- Cost
- Scalability
- Control

---

## Day 04 Architect Questions

Answer these before moving on:

1. Why do LLMs often need GPUs?
2. Why does GPU memory matter?
3. Why does model size affect infrastructure?
4. What is quantization?
5. What does an inference server do?
6. Why is batching important?
7. What is the difference between TTFT and total latency?
8. Why use Kubernetes for AI workloads?
9. How are GPUs exposed to Kubernetes workloads?
10. What should trigger AI autoscaling?
11. Why can GPU autoscaling be expensive?
12. When does self-hosted inference make sense?
13. When is managed inference better?
14. Why might a hybrid architecture be preferable?
15. What happens if your GPU cluster reaches capacity?
16. What happens if your primary inference service fails?
17. How would you design for 10x traffic?
18. How would you prevent one workload from consuming all GPU capacity?

---

## Day 04 Deliverables

By the end of today, create:

### 1. AI Infrastructure Diagram

Show:

- API Gateway
- AI Gateway
- Model Gateway
- Kubernetes
- GPU nodes
- Inference servers
- Models
- Managed fallback

### 2. Capacity Plan

Document:

- Expected traffic
- Concurrent users
- GPU requirements
- Model size
- Latency target
- Scaling strategy

### 3. Infrastructure Decision Record

Answer:

- Why did you choose managed, self-hosted, or hybrid inference?

### 4. Performance Test

Record:

- Concurrency
- Latency
- Throughput
- GPU Utilization
- Memory
- Errors

---

## What You Should Understand After Day 04

You should now be able to see the entire stack:

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

With cross-cutting layers:

- Security
- Observability
- Reliability
- Governance
- FinOps

**This is the key transition:**

You're no longer designing an AI application. You're designing the platform that runs AI applications.

---

## 23. Key Takeaways

```
┌─────────────────────────────────────────────────────────────────┐
│                     DAY 04 KEY TAKEAWAYS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. AI infrastructure ≠ traditional web infrastructure          │
│                                                                 │
│  2. GPU memory is often the binding constraint                  │
│                                                                 │
│  3. Quantization trades quality for cost — find your threshold  │
│                                                                 │
│  4. Inference servers (vLLM, KServe) optimize GPU utilization   │
│                                                                 │
│  5. Batching improves throughput but affects latency             │
│                                                                 │
│  6. TTFT vs total latency — different workloads, different goals│
│                                                                 │
│  7. Kubernetes is one layer, not the entire AI architecture     │
│                                                                 │
│  8. GPU autoscaling is expensive — design for cost              │
│                                                                 │
│  9. Hybrid architectures balance control, cost, and capability  │
│                                                                 │
│ 10. Architecture = minimum reliable infrastructure for required │
│     AI capability at required quality, latency, and cost        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

> **Next**: See Day 05 (`05-data-architecture/`) to understand data architecture for AI systems.
