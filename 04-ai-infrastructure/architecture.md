# AI Infrastructure — Deployment Comparison

## Option A: Managed Model API

```
┌──────────┐    ┌──────────┐    ┌─────────────────┐
│  Client  │───▶│ Gateway  │───▶│ Provider API    │
└──────────┘    └──────────┘    │ (OpenAI/Anthropic)│
                                └─────────────────┘
```

**Pros:** Fast adoption, low ops burden, strong capabilities
**Cons:** Per-token cost, vendor dependency, API limits, data privacy concerns

## Option B: Self-Hosted Open-Weight Model

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌─────────┐
│  Client  │───▶│ Gateway  │───▶│ K8s + GPU│───▶│ Model   │
└──────────┘    └──────────┘    │ Cluster  │    │ (vLLM)  │
                                └──────────┘    └─────────┘
```

**Pros:** Full control, data locality, customization, predictable economics at scale
**Cons:** GPU costs, operations, upgrades, reliability, security, platform engineering

## Comparison matrix

| Factor | Managed API | Self-Hosted |
|--------|------------|-------------|
| Cost at low volume | Lower | Higher |
| Cost at high volume | Higher | Lower |
| Latency | Network-dependent | Local, lower |
| Privacy | Provider sees data | Full control |
| Scaling | Automatic | Manual design |
| Operations | None | Significant |
| Vendor lock-in | High | Low |
