# Day 10 — AI Observability

## Objective

Build observability around infrastructure, applications, models, retrieval, agents, quality, and cost.

## Traditional signals

- CPU
- memory
- storage
- network
- availability
- latency

## AI signals

Track:

- token usage
- cost per request
- model latency
- time to first token
- retrieval quality
- hallucination signals
- user feedback
- prompt quality
- agent success rate
- tool failures
- model drift

## Tools

Explore:

- OpenTelemetry
- Prometheus
- Grafana
- Langfuse
- LangSmith

## Architecture

Design an observability pipeline:

Application → Telemetry → Collection → Storage → Dashboards → Alerts → Feedback

## Exercise

Create an AI production dashboard specification.

Include at least:

- 5 infrastructure metrics
- 5 AI quality metrics
- 3 cost metrics
- 3 alert conditions

## Deliverable

Dashboard specification + alerting matrix.
