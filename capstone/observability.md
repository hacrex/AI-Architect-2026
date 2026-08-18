# Capstone — Observability Plan

## Monitoring stack

| Layer | Tool | Purpose |
|-------|------|---------|
| Infrastructure | Prometheus + Grafana | CPU, memory, GPU, network |
| Application | OpenTelemetry | Request tracing, latency |
| Model | Langfuse / LangSmith | Token usage, quality, cost |
| Business | Custom dashboard | ROI, satisfaction, efficiency |

## Key dashboards

### 1. System Health Dashboard

- GPU utilization (real-time)
- Request queue depth
- Error rate (p95)
- Latency distribution

### 2. AI Quality Dashboard

- Model accuracy metrics
- Hallucination rate
- Retrieval relevance
- User satisfaction score

### 3. Cost Dashboard

- Token spend (daily/weekly/monthly)
- Cost per request trend
- Cache hit rate
- Budget vs actual

## Alerting rules

| Alert | Condition | Severity | Channel |
|-------|-----------|----------|---------|
| Model provider down | 5xx > 1% for 5min | Critical | Page |
| Latency spike | p95 > 3s for 5min | Warning | Slack |
| Cost anomaly | Daily spend > 120% budget | Warning | Slack |
| Quality degradation | Hallucination rate > 5% | Warning | Slack |
| Queue backlog | Depth > 500 for 10min | Warning | Slack |

## Feedback loops

- User feedback (thumbs up/down)
- Human escalation tracking
- Model performance comparison (A/B)
- Retrieval quality sampling
