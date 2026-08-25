# Day 10 — AI Observability Exercise

## Overview

Design a complete observability strategy for an Enterprise AI Knowledge Platform serving 100,000 users with 10,000,000 AI requests per month.

---

## Part 1: Observability Architecture

Design the full observability stack.

### Components to instrument

```
User
 ↓
API Gateway
 ↓
AI Gateway
 ↓
RAG Pipeline
 ↓
Agent Framework
 ↓
Model Gateway
 ↓
Inference (Managed + Self-hosted)
 ↓
GPU Infrastructure
```

### For each component, define:

| Component | Metrics | Logs | Traces | Alerts | SLO |
|-----------|---------|------|--------|--------|-----|
| API Gateway | | | | | |
| AI Gateway | | | | | |
| RAG Pipeline | | | | | |
| Agent Framework | | | | | |
| Model Gateway | | | | | |
| Inference | | | | | |
| GPU Infrastructure | | | | | |

---

## Part 2: AI Trace

Document one complete request:

> "Explain our incident response policy and tell me what action I should take."

### Create a trace showing:

```
Trace ID: ___________
Total Duration: _____ ms
Total Tokens: _____
Total Cost: $_____
```

| Span | Duration | Tokens | Notes |
|------|----------|--------|-------|
| Authentication | | | |
| Query Processing | | | |
| Embedding | | | |
| Vector Search | | | |
| Metadata Filtering | | | |
| Reranking | | | |
| Context Assembly | | | |
| Model Call #1 | | | |
| Tool Call (if any) | | | |
| Model Call #2 (if any) | | | |
| Response | | | |

---

## Part 3: SLO Definition

Define SLOs for the AI platform.

### Traditional SLOs

| SLO | SLI | Target | Window | Error Budget |
|-----|-----|--------|--------|--------------|
| Availability | | | | |
| Latency | | | | |
| Error Rate | | | | |

### AI-Specific SLOs

| SLO | SLI | Target | Window | Error Budget |
|-----|-----|--------|--------|--------------|
| Task Success | | | | |
| Groundedness | | | | |
| Retrieval Quality | | | | |
| TTFT | | | | |

### Calculate error budgets

For each SLO, calculate:

- Allowed downtime per month
- Allowed failed requests per day
- Budget consumption rate

---

## Part 4: Production Dashboard

Design a dashboard with 6 panels.

### Panel 1: Infrastructure Health

Draw the layout showing:
- GPU utilization gauge
- CPU/memory bars
- Queue depth
- Container health

### Panel 2: Application Performance

Draw the layout showing:
- Request rate line chart
- Error rate line chart
- Latency percentiles (P50, P95, P99)

### Panel 3: AI Metrics

Draw the layout showing:
- Token usage over time
- Model call distribution (pie chart)
- TTFT trend
- Cost per request trend

### Panel 4: RAG Quality

Draw the layout showing:
- Retrieval relevance distribution
- Documents retrieved histogram
- Context size trend
- Authorization filter rate

### Panel 5: Quality & Evaluation

Draw the layout showing:
- Task success rate gauge
- Groundedness score gauge
- User satisfaction trend
- Drift status indicators

### Panel 6: Cost

Draw the layout showing:
- Daily spend vs budget
- Cost by provider (stacked bar)
- Cost per task trend
- Cache savings

---

## Part 5: Alert Rules

Define 10 alert rules.

| # | Alert Name | Condition | Severity | Component | Response |
|---|------------|-----------|----------|-----------|----------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |
| 6 | | | | | |
| 7 | | | | | |
| 8 | | | | | |
| 9 | | | | | |
| 10 | | | | | |

### Alert design principles

- Don't alert on single metrics — use correlated conditions
- Include at least one quality alert
- Include at least one cost alert
- Include at least one retrieval alert
- Define clear response actions for each

---

## Part 6: Incident Runbook

Create a runbook for: **"AI response quality suddenly drops"**

### Fill in each step:

**Detection**
- How do we know? _______________
- Who gets notified? _______________
- What dashboard shows it? _______________

**Investigation Steps**
1. Check: _______________ → Result: _______________
2. Check: _______________ → Result: _______________
3. Check: _______________ → Result: _______________
4. Check: _______________ → Result: _______________
5. Check: _______________ → Result: _______________

**Root Cause Categories**
- [ ] Data ingestion change
- [ ] Model provider change
- [ ] Retrieval degradation
- [ ] Prompt/context change
- [ ] Traffic pattern change
- [ ] Infrastructure issue

**Mitigation Options**
- Option A: _______________
- Option B: _______________
- Option C: _______________

**Recovery Verification**
- Quality score returns to: _______________
- SLO status: _______________
- Monitoring duration: _______________

**Post-Incident**
- [ ] Update runbook
- [ ] Add missing alert
- [ ] Review deployment process
- [ ] Document lessons learned

---

## Part 7: Drift Detection

Design drift monitoring for the platform.

### Metrics to monitor for drift

| Metric | Baseline | Window | Detection Method | Alert Threshold |
|--------|----------|--------|------------------|-----------------|
| Retrieval relevance | | | | |
| Token usage per request | | | | |
| Model latency | | | | |
| Query distribution | | | | |
| Document chunk quality | | | | |

### Drift response process

```
Drift detected
    ↓
Compare with recent changes (deployments, data updates)
    ↓
Identify correlated event
    ↓
Assess impact on SLOs
    ↓
Decide: investigate / mitigate / accept
    ↓
Document and update baselines
```

---

## Deliverables

1. **Observability architecture diagram** — all layers instrumented
2. **AI trace document** — one complete request traced
3. **SLO table** — traditional + AI-specific with error budgets
4. **Dashboard mockup** — 6-panel layout
5. **Alert rules table** — 10 rules with severity and response
6. **Incident runbook** — step-by-step investigation guide
7. **Drift detection plan** — metrics, baselines, response process
