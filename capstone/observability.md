# Capstone — Observability Plan

## Monitoring Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| Infrastructure | Prometheus + Grafana | CPU, memory, GPU, network, disk |
| Application | OpenTelemetry | Request tracing, latency, errors |
| Model | Custom + Langfuse | Token usage, quality, cost per request |
| Business | Custom dashboard | ROI, adoption, resolution time |
| Audit | Elasticsearch | Security events, access logs |
| Alerting | PagerDuty / Slack | Incident response |

## Key Dashboards

### 1. System Health Dashboard

| Metric | Alert Threshold | Panel |
|--------|----------------|-------|
| Request rate | - | Requests/sec (by endpoint) |
| Error rate | > 1% for 5min | 4xx/5xx percentage |
| Latency p50/p95/p99 | p99 > 3s | Response time distribution |
| GPU utilization | > 90% for 10min | GPU usage per node |
| Queue depth | > 500 for 10min | Request queue backlog |
| Pod count | - | Running pods per service |

### 2. AI Quality Dashboard

| Metric | Alert Threshold | Panel |
|--------|----------------|-------|
| Task success rate | < 80% | Successful tasks / total |
| Hallucination rate | > 5% | Flagged responses / total |
| Retrieval relevance | < 70% | Relevant docs / retrieved docs |
| Citation accuracy | < 85% | Correct citations / total |
| User satisfaction | < 3.5/5 | Average rating |
| Human escalation rate | > 40% | Escalations / total queries |

### 3. Cost Dashboard

| Metric | Alert Threshold | Panel |
|--------|----------------|-------|
| Daily token spend | > 120% budget | Token cost trend |
| Cost per request | > $0.01 | Average cost trend |
| Cache hit rate | < 20% | Cache hits / total requests |
| Budget vs actual | > 90% used | Monthly budget progress |
| Cost by department | - | Breakdown by team |
| Cost by model | - | Breakdown by provider |

### 4. RAG Dashboard

| Metric | Alert Threshold | Panel |
|--------|----------------|-------|
| Retrieval latency | > 500ms p95 | Vector search timing |
| Embedding latency | > 200ms p95 | Embedding generation timing |
| Documents indexed | - | Total documents count |
| Index freshness | > 24 hours | Last ingestion timestamp |
| Chunk quality | - | Average chunk relevance score |

### 5. Security Dashboard

| Metric | Alert Threshold | Panel |
|--------|----------------|-------|
| Failed auth attempts | > 10/min | Authentication failures |
| Prompt injection blocks | - | Blocked requests count |
| PII detections | - | Detected and redacted PII |
| Unauthorized access attempts | - | Denied authorization checks |
| Audit log entries | - | Events per hour |

## Alerting Rules

| Alert | Condition | Severity | Channel | Action |
|-------|-----------|----------|---------|--------|
| Model provider down | 5xx > 1% for 5min | Critical | Page | Auto-fallback to secondary |
| Latency spike | p95 > 3s for 5min | Warning | Slack | Investigate root cause |
| Cost anomaly | Daily spend > 120% budget | Warning | Slack | Review routing rules |
| Quality degradation | Success rate < 80% for 1hr | Warning | Slack | Check model, retrieval |
| Queue backlog | Depth > 500 for 10min | Warning | Slack | Scale workers |
| GPU exhaustion | Utilization > 95% for 15min | Warning | Slack | Scale GPU nodes |
| Auth brute force | > 20 failed attempts/min | Critical | Page | Block IP, alert security |
| Prompt injection spike | > 10 blocked/hour | High | Slack | Review patterns |
| Data breach indicator | Restricted data in response | Critical | Page | Isolate, investigate |
| SLO breach | Availability < 99.9% | High | Page | Incident response |

## SLOs

| SLO | Target | Measurement |
|-----|--------|-------------|
| Availability | 99.9% | Uptime / total time |
| Latency (p95) | < 2s | Response time distribution |
| Task success rate | > 85% | Successful completions |
| Error rate | < 1% | Errors / total requests |
| Data freshness | < 24 hours | Time since last ingestion |

## Feedback Loops

| Loop | Data Source | Action |
|------|------------|--------|
| User feedback | Thumbs up/down on responses | Retrain, adjust routing |
| Human escalation tracking | Escalation events | Improve agent capabilities |
| Model A/B comparison | Parallel model runs | Optimize model selection |
| Retrieval quality sampling | Human review of retrieved docs | Improve embedding, chunking |
| Cost feedback | Token spend vs budget | Adjust caching, routing |

## Incident Response

| Severity | Response Time | Escalation | Action |
|----------|--------------|------------|--------|
| Critical (data breach, system down) | < 15 min | Security + engineering lead | Isolate, assess, communicate |
| High (model outage, quality drop) | < 1 hour | Engineering lead | Fallback, investigate |
| Medium (latency spike, cost anomaly) | < 4 hours | On-call engineer | Monitor, adjust |
| Low (minor degradation) | < 24 hours | Team | Fix in next sprint |
