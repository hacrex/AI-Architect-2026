# Day 10 — AI Observability Architecture

## Observability Layers

```
┌──────────────────────────────┐
│       Business Outcome       │  Revenue, user retention, task completion
├──────────────────────────────┤
│        AI Quality            │  Groundedness, relevance, evaluation scores
├──────────────────────────────┤
│       Model Behavior         │  Token usage, TTFT, latency, provider health
├──────────────────────────────┤
│     AI Workflow / Trace      │  RAG chain, agent steps, tool calls
├──────────────────────────────┤
│      Application Layer       │  Requests, errors, HTTP status, queue depth
├──────────────────────────────┤
│    Infrastructure Layer      │  CPU, memory, GPU, network, pod health
└──────────────────────────────┘
```

You need visibility across the entire stack. Infrastructure health does not equal AI quality.

---

## Infrastructure Metrics

| Metric | Source | Alert Threshold | Why It Matters |
|--------|--------|-----------------|----------------|
| GPU utilization | Prometheus | > 90% for 5min | Inference bottleneck |
| GPU memory usage | Prometheus | > 85% | OOM risk for model loading |
| GPU temperature | DCGM exporter | > 85C | Thermal throttling |
| CPU utilization | Prometheus | > 80% | Application bottleneck |
| Memory utilization | Prometheus | > 85% | OOM risk |
| Request queue depth | Custom | > 100 | Backpressure building |
| API latency (p95) | OpenTelemetry | > 2s | User experience degrading |
| Error rate | OpenTelemetry | > 1% | System instability |
| Container restarts | Kubernetes | > 3 in 10min | Crash loop |
| Network throughput | Prometheus | Baseline deviation > 50% | Connectivity issues |

---

## Application Metrics

| Metric | Source | Alert Threshold | Why It Matters |
|--------|--------|-----------------|----------------|
| Requests/sec | OpenTelemetry | Baseline deviation > 50% | Traffic anomaly |
| Success rate | OpenTelemetry | < 99% | Core reliability |
| P50 latency | OpenTelemetry | > 1s | Average user experience |
| P95 latency | OpenTelemetry | > 5s | Tail user experience |
| P99 latency | OpenTelemetry | > 10s | Worst-case experience |
| Timeout rate | OpenTelemetry | > 2% | Provider or network issues |
| Retry rate | OpenTelemetry | > 5% | Cascading failures |
| Queue wait time | Custom | > 2s | Processing bottleneck |

---

## AI-Specific Metrics

| Metric | Source | Alert Threshold | Why It Matters |
|--------|--------|-----------------|----------------|
| Input tokens / request | LLM provider | Baseline deviation > 30% | Context bloat or prompt change |
| Output tokens / request | LLM provider | Baseline deviation > 30% | Response behavior change |
| Total tokens / day | LLM provider | > budget + 20% | Cost overrun |
| Time to first token (TTFT) | LLM provider | > 2s | User perception of speed |
| Tokens / second | LLM provider | < 20 | Throughput degradation |
| Model latency | LLM provider | > 10s | Inference bottleneck |
| Model error rate | LLM provider | > 1% | Provider instability |
| Model provider | Gateway | — | Which provider is serving |
| Model version | Gateway | — | Version tracking for correlation |

---

## Token Observability

Tokens affect cost, latency, context size, and throughput.

Dashboard should show:

| Dimension | Example |
|-----------|---------|
| Tokens / Request | 2,500 avg |
| Tokens / User | 12,000 / day |
| Tokens / Application | 2.5M / day |
| Tokens / Model | GPT-4o: 1.8M, Claude: 0.7M |
| Tokens / Tenant | Acme: 500K, Beta: 200K |
| Tokens / Day | Trend over 30 days |

This connects directly to the FinOps architecture from Day 09.

---

## RAG Observability

A RAG request should expose:

```
User Query
    ↓
Query Transformation
    ↓
Embedding
    ↓
Retrieval
    ↓
Retrieved Documents
    ↓
Filtering
    ↓
Reranking
    ↓
Context
    ↓
LLM
```

| Metric | Source | Alert Threshold | Why It Matters |
|--------|--------|-----------------|----------------|
| Retrieval latency | Custom | > 500ms | RAG bottleneck |
| Documents retrieved | Custom | < 3 | Insufficient context |
| Retrieval relevance (top) | Custom | < 0.7 | Poor matching |
| Retrieval relevance (avg) | Custom | < 0.5 | Broad failure |
| Context tokens | Custom | > 80% of model limit | Truncation risk |
| Authorization filter rate | Custom | > 20% filtered | Permission mismatch |
| Reranking latency | Custom | > 200ms | Reranking bottleneck |

Key insight: **A bad AI answer can be a retrieval problem rather than a model problem.**

---

## Agent Observability

| Metric | Source | Alert Threshold | Why It Matters |
|--------|--------|-----------------|----------------|
| Agent steps / run | Custom | > 10 | Inefficiency or loop |
| Agent loop detected | Custom | > 0 | Infinite loop risk |
| Tool calls / run | Custom | > 8 | Excessive tool usage |
| Tool error rate | Custom | > 10% | Tool reliability |
| Agent success rate | Custom | < 85% | Task completion |
| Agent total tokens | Custom | > 50K | Cost per run |
| Agent total latency | Custom | > 30s | User timeout risk |

---

## LLM Tracing

A normal application trace:

```
HTTP 200
2.7 sec
```

An AI trace should show the entire chain:

```
Trace #84291
│
├── Authentication: 12 ms
├── Query Processing: 45 ms
├── Embedding: 80 ms
├── Vector Search: 150 ms
├── Metadata Filtering: 30 ms
├── Reranking: 120 ms
├── Context Assembly: 15 ms
├── Model Call #1: 1,100 ms (2,100 input + 450 output tokens)
├── Tool Call: 540 ms
├── Model Call #2: 610 ms (1,800 input + 320 output tokens)
└── Response: 5 ms

Total: 2,707 ms
Cost: $0.023
```

---

## Quality Metrics

| Metric | Source | Alert Threshold | Why It Matters |
|--------|--------|-----------------|----------------|
| Groundedness score | Evaluation | < 95% | Hallucination risk |
| Relevance score | Evaluation | < 80% | Answer quality |
| Task success rate | Feedback + eval | < 90% | User satisfaction |
| User satisfaction | Feedback loop | < 3.5 / 5 | Subjective quality |
| Evaluation score | Automated eval | Baseline - 10% | Regression detection |
| Hallucination rate | Evaluation | > 5% | Trust erosion |

---

## Cost Metrics

| Metric | Source | Alert Threshold | Why It Matters |
|--------|--------|-----------------|----------------|
| Cost per request | Custom | > $0.05 | Unit economics |
| Cost per successful task | Custom | > $0.50 | Business value |
| Daily token spend | Provider API | > budget + 20% | Budget overrun |
| Monthly total cost | Aggregated | > monthly budget | Financial sustainability |
| Cache hit rate | Custom | < 40% | Missed optimization |
| Cost by model | Custom | — | Model routing efficiency |
| Cost by tenant | Custom | — | Per-customer profitability |

---

## SLI / SLO / SLA

### SLI (Service Level Indicator)

What you measure.

| SLI | Measurement |
|-----|-------------|
| Availability | Successful requests / total requests |
| Latency | P95 response time |
| Task Success | Correct answers / total queries |
| Groundedness | Grounded responses / total responses |
| Retrieval Quality | Relevant docs retrieved / total retrievals |

### SLO (Service Level Objective)

What you target.

| SLO | Target | Window |
|-----|--------|--------|
| Availability | 99.9% | 30 days |
| P95 Latency | < 5 sec | 1 hour |
| Task Success | > 90% | 7 days |
| Groundedness | > 95% | 7 days |
| Retrieval Relevance | > 80% | 7 days |

### SLA (Service Level Agreement)

What you formally promise to customers.

| SLA | Commitment |
|-----|------------|
| Availability | 99.9% uptime |
| Support Response | < 4 hours for critical |
| Data Retention | 90 days |

---

## Alert Design

### Bad alerts (alert on everything)

```
GPU utilization > 80%        → Might be normal
Latency > 1s                 → Might be acceptable
Error rate > 0.1%            → Might be transient
```

### Good alerts (correlated conditions)

```
GPU utilization > 90%
AND P95 latency increasing
AND queue depth increasing
→ Meaningful system condition

Retrieval relevance ↓
AND answer quality ↓
AND user complaints ↑
→ Data or retrieval problem

Model deployed
AND quality score ↓ 10%
AND cost ↑ 20%
→ Regression from deployment
```

### Alert severity matrix

| Severity | Condition | Response Time | Action |
|----------|-----------|---------------|--------|
| Critical | Model provider down | 5 min | Page on-call, activate fallback |
| Critical | SLO breached | 15 min | Page on-call, investigate |
| Warning | Latency p95 > 5s | 1 hour | Slack alert, monitor |
| Warning | Retrieval relevance < 70% | 1 hour | Slack alert, investigate |
| Warning | Cost variance > 20% | 4 hours | Slack alert, review |
| Info | Drift detected | Daily | Daily digest, review |
| Info | New error pattern | Daily | Daily digest, review |

---

## Observability Correlation

The most powerful concept: correlating events across layers.

```
Monday: Model v2 deployed
         ↓
Tuesday: Token usage ↑ 25%
         Latency ↑ 15%
         Cost ↑ 30%
         Quality ↓ 8%
         ↓
Wednesday: Investigation
           Root cause: v2 uses more tokens
           Action: Optimize prompt or rollback
```

This requires:

- Deployment events logged
- Model version tracked per request
- Quality scores computed continuously
- Cost tracked per request
- Dashboard correlating all dimensions

---

## Production Dashboard Design

### Layer 1: Infrastructure

```
┌─────────────────────────────────────────────┐
│ GPU Util: ████████░░ 78%   GPU Mem: 18/24GB │
│ CPU:      ██████░░░░ 55%   Mem:    12/32GB  │
│ Queue:    ██░░░░░░░░ 12     Restarts: 0     │
└─────────────────────────────────────────────┘
```

### Layer 2: Application

```
┌─────────────────────────────────────────────┐
│ Requests: 142/s   Errors: 0.3%  Timeout: 0.1%│
│ P50: 1.2s  P95: 3.8s  P99: 8.2s            │
│ Throughput: 142 req/s                         │
└─────────────────────────────────────────────┘
```

### Layer 3: AI

```
┌─────────────────────────────────────────────┐
│ LLM Calls: 142/s   Tokens: 356K/min         │
│ TTFT P50: 0.4s    Inference P95: 3.2s      │
│ Providers: OpenAI 85% | Anthropic 12% | Self 3%│
└─────────────────────────────────────────────┘
```

### Layer 4: RAG

```
┌─────────────────────────────────────────────┐
│ Retrievals: 142/s  Docs: 5.2 avg            │
│ Relevance Top: 0.84  Relevance Avg: 0.71   │
│ Context Tokens: 2,800 avg                   │
└─────────────────────────────────────────────┘
```

### Layer 5: Quality

```
┌─────────────────────────────────────────────┐
│ Task Success: 92.3%  Grounded: 96.1%       │
│ User Satisfaction: 4.2/5  Eval Score: 88   │
│ Drift: Normal                                │
└─────────────────────────────────────────────┘
```

### Layer 6: Cost

```
┌─────────────────────────────────────────────┐
│ Today: $127 / $500 budget (25.4%)           │
│ Cost/Request: $0.0089  Cost/Task: $0.012   │
│ Cache Hit: 34%  Savings: $42 today         │
└─────────────────────────────────────────────┘
```

---

## Incident Runbook: AI Response Quality Drop

```
Detection
│  Users report "AI answers became worse"
│  OR quality SLO breach
│  OR automated eval degradation alert
↓
Investigation
│  Step 1: Check availability → Healthy?
│  Step 2: Check latency → Healthy?
│  Step 3: Check model errors → Healthy?
│  Step 4: Check retrieval relevance → ↓ Degraded
↓
Root Cause Analysis
│  Step 5: Check data pipeline → New parser deployed 2h ago
│  Step 6: Compare document chunks → Quality degraded
│  Root cause: Data ingestion change → retrieval degradation
↓
Mitigation
│  Option A: Roll back document parser
│  Option B: Re-index affected documents
│  Option C: Switch to fallback model temporarily
↓
Recovery
│  Step 7: Deploy fix
│  Step 8: Re-index if needed
│  Step 9: Monitor quality scores
│  Step 10: Verify SLO recovery
↓
Post-Incident
   Step 11: Update runbook
   Step 12: Add alert for document quality
   Step 13: Review deployment process
```
