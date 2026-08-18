# Observability — Dashboard Specification

## Infrastructure metrics

| Metric | Source | Alert Threshold |
|--------|--------|-----------------|
| GPU utilization | Prometheus | > 90% for 5min |
| GPU memory usage | Prometheus | > 85% |
| Request queue depth | Custom | > 100 |
| API latency (p95) | OpenTelemetry | > 2s |
| Error rate | OpenTelemetry | > 1% |

## AI quality metrics

| Metric | Source | Alert Threshold |
|--------|--------|-----------------|
| Hallucination rate | Langfuse | > 5% |
| Retrieval relevance | Custom | < 70% |
| User satisfaction | Feedback | < 3.5/5 |
| Agent success rate | Custom | < 85% |
| Tool failure rate | Custom | > 10% |

## Cost metrics

| Metric | Source | Alert Threshold |
|--------|--------|-----------------|
| Cost per request | Custom | > $0.05 |
| Daily token spend | Provider API | > budget + 20% |
| Cache hit rate | Custom | < 40% |

## Alert conditions

| Severity | Condition | Action |
|----------|-----------|--------|
| Critical | Model provider down | Page on-call |
| Warning | Latency p95 > 2s | Slack alert |
| Info | Cost variance > 20% | Daily digest |
