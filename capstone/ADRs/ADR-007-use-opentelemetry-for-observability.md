# ADR-007: OpenTelemetry for Observability

## Status

Accepted

## Date

2026-08-21

## Context

We need comprehensive observability across infrastructure, application, and model layers. Requirements include:

- Distributed tracing across services
- Metrics collection and alerting
- Log aggregation and search
- Cost tracking per request
- Model quality monitoring
- Vendor-neutral instrumentation

## Options

| Option | Pros | Cons |
|--------|------|------|
| CloudWatch/Stackdriver | Integrated, simple | Vendor lock-in, limited customization |
| Datadog | Feature-rich, APM | Expensive at scale, vendor lock-in |
| OpenTelemetry + Grafana | Open source, customizable, vendor-neutral | Self-hosted operations |
| ELK Stack | Good for logs | Limited metrics/tracing |

## Decision

We will use **OpenTelemetry** for instrumentation with **Prometheus + Grafana** for metrics and visualization.

## Rationale

- Vendor-neutral — no lock-in to cloud provider
- Best-in-class tracing with OpenTelemetry
- Prometheus is industry standard for metrics
- Grafana provides rich visualization and dashboards
- Self-hosted controls cost at scale
- Active CNCF ecosystem

## Architecture

```
Application → OTel SDK → OTel Collector → Backend
                                        ├── Prometheus (metrics)
                                        ├── Tempo (traces)
                                        ├── Loki (logs)
                                        └── Grafana (dashboards)
```

## Consequences

### Positive

- No vendor lock-in
- Comprehensive observability stack
- Rich ecosystem of exporters and integrations
- Cost-effective at scale

### Negative

- Self-hosted operations required
- Initial setup complexity
- Team needs to learn OTel concepts

## Review Date

2026-11-21 (3 months post-launch)
