# Day 04 — AI Infrastructure: Exercise

**Estimated Time**: 4-5 hours total

| Exercise | Task | Time |
|----------|------|------|
| 1 | Model serving experiment | 60 min |
| 2 | Concurrency testing | 45 min |
| 3 | Model size comparison | 45 min |
| 4 | Managed vs self-hosted | 60 min |
| - | Architect questions | 30-45 min |
| - | Capacity planning | 30 min |

## Overview

Today's exercises focus on **infrastructure**, **inference serving**, and **deployment patterns**. You'll experiment with model serving, measure performance, and design production infrastructure.

> **Prerequisite**: Complete Days 01-03 exercises to understand the AI application architecture we're now building infrastructure for.

---

## Day 04 Hands-On Labs

### Experiment 1 — Model Serving

Deploy an open-weight model using an inference server.

**Measure:**

- Startup time
- Memory usage
- Latency
- Throughput

**Steps:**

1. Deploy a model using vLLM or similar inference server
2. Record time from container start to ready state
3. Monitor GPU memory consumption
4. Send test requests and measure response times
5. Calculate requests per second

### Experiment 2 — Concurrency

Send increasing numbers of requests and observe system behavior.

**Concurrency Levels:**

- 1 request
- 5 requests
- 10 requests
- 25 requests
- 50 requests
- 100 requests

**Observe:**

- Latency at each level
- Throughput at each level
- Resource utilization
- Failure rates

### Experiment 3 — Model Size

Compare two different model sizes.

**Compare:**

- Memory requirements
- Latency differences
- Throughput differences
- Quality of outputs
- Infrastructure requirements

### Experiment 4 — Managed vs Self-Hosted

Compare your self-hosted setup with a managed model API.

**Document:**

- Operational complexity
- Performance characteristics
- Cost analysis
- Scalability options
- Control level

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

## Day 04 Deliverables

### 1. AI Infrastructure Diagram

Create a diagram showing:

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

- Concurrency levels tested
- Latency at each level
- Throughput at each level
- GPU utilization
- Memory consumption
- Error rates

## Performance Test Template

| Concurrency | Latency (ms) | Throughput (req/s) | GPU Utilization | Memory (GB) | Errors |
|-------------|--------------|-------------------|-----------------|-------------|--------|
| 1 | | | | | |
| 5 | | | | | |
| 10 | | | | | |
| 25 | | | | | |
| 50 | | | | | |
| 100 | | | | | |

## Expected Outcomes

After completing Day 04, you should be able to:

- Design a production AI infrastructure stack
- Understand GPU memory and compute requirements
- Choose appropriate inference serving solutions
- Plan capacity for AI workloads
- Make informed decisions about managed vs self-hosted inference
- Design for scalability and reliability
- Understand the cost implications of AI infrastructure
