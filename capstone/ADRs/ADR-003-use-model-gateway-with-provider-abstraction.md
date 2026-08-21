# ADR-003: Use Model Gateway with Provider Abstraction

## Status

Accepted

## Date

2026-08-21

## Context

The Enterprise AI Knowledge Assistant requires LLM inference for:

- Answer generation
- Query classification
- Embedding generation
- Document summarization
- Tool call reasoning

We need to decide how to integrate with LLM providers while avoiding:

- Tight coupling to a single provider
- Vendor lock-in
- Single point of failure
- Cost opacity
- Inability to optimize for different workloads

Options:

1. **Direct API calls** — Call provider APIs directly in application code
2. **Model Gateway** — Abstract layer that routes requests to multiple providers
3. **Provider SDK** — Use each provider's SDK independently
4. **Open-source framework** — Use LangChain, LiteLLM, or similar

## Decision

We will implement a **custom Model Gateway** with provider abstraction, supporting multiple LLM providers with automatic routing, fallback, and cost tracking.

## Architecture

```
Application
     │
     ▼
┌─────────────┐
│Model Gateway│
│             │
│ - Router    │
│ - Fallback  │
│ - Tracker   │
│ - Cache     │
└──────┬──────┘
       │
  ┌────┼─────────┐
  ↓    ↓         ↓
OpenAI Anthropic Self-hosted
  ↓    ↓         ↓
GPT-4 Claude    vLLM
     Sonnet      │
                GPU
```

## Rationale

### Why Not Direct API Calls?

| Problem | Impact |
|---------|--------|
| Provider lock-in | Cannot switch without code changes |
| No fallback | Provider outage = system down |
| No cost visibility | Surprises on monthly bill |
| No routing | Same model for all requests |
| Code duplication | Same retry/error logic everywhere |

### Why Not Provider SDK?

- Still couples to specific provider
- Different SDKs for different providers
- No unified interface
- Difficult to add new providers

### Why Not Open-Source Framework?

- LangChain adds significant abstraction overhead
- Limited control over routing logic
- Framework updates may break application
- Adds dependency risk

### Why Custom Model Gateway?

| Benefit | Description |
|---------|------------|
| Provider abstraction | Uniform interface across all providers |
| Automatic fallback | Provider down → automatic failover |
| Cost tracking | Real-time token usage and cost monitoring |
| Intelligent routing | Route based on complexity, cost, latency |
| Cache layer | Avoid redundant API calls |
| Policy enforcement | Rate limits, budget caps, content filtering |

## Provider Strategy

### Primary: OpenAI (GPT-4)

- Best for complex reasoning
- Strong instruction following
- Good citation support
- Cost: $0.03/1K input, $0.06/1K output

### Secondary: Anthropic (Claude)

- Strong for analysis and summarization
- Good safety characteristics
- Alternative if OpenAI unavailable
- Cost: $0.015/1K input, $0.075/1K output

### Tertiary: Self-hosted (vLLM)

- Cost-effective for high-volume simple queries
- Data stays on-premises
- No API dependency
- Cost: Infrastructure only

## Routing Logic

```
Request → Complexity Classifier
              │
    ┌─────────┼─────────┐
    ↓         ↓         ↓
 Simple    Normal    Complex
    │         │         │
    ↓         ↓         ↓
Self-hosted  Claude    GPT-4
    │         │         │
    └─────────┼─────────┘
              │
         Fallback?
              │
    ┌─────────┼─────────┐
    ↓         ↓         ↓
Claude    GPT-4    Self-hosted
```

## Fallback Strategy

| Scenario | Primary | Fallback | Last Resort |
|----------|---------|----------|-------------|
| Provider timeout | Retry 2x | Switch provider | Cached response |
| Provider error | Retry 2x | Switch provider | Error message |
| Provider outage | Switch provider | Self-hosted | Queue for retry |
| Rate limit | Switch provider | Self-hosted | Queue |
| Budget exceeded | Switch to cheaper | Self-hosted | Pause requests |

## Cost Tracking

### Per-Request Tracking

```json
{
  "request_id": "req-123",
  "model": "gpt-4",
  "provider": "openai",
  "input_tokens": 500,
  "output_tokens": 200,
  "latency_ms": 1200,
  "cost_usd": 0.027,
  "cached": false
}
```

### Budget Controls

| Control | Limit | Action |
|---------|-------|--------|
| Per-user daily | $5 | Throttle requests |
| Per-department monthly | $1,000 | Alert + review |
| Total monthly | $5,000 | Alert + approval required |
| Per-request max | $0.50 | Reject request |

## Consequences

### Positive

- No provider lock-in
- Automatic failover
- Cost visibility and control
- Ability to optimize routing
- Clean application code

### Negative

- Additional infrastructure component
- Gateway itself is a potential SPOF
- More complex debugging
- Gateway updates require testing

### Risks

| Risk | Mitigation |
|------|-----------|
| Gateway outage | Deploy as HA pair, circuit breaker |
| Routing errors | A/B testing, gradual rollout |
| Cost overrun | Real-time budget alerts |
| Provider deprecation | Adapter pattern, easy provider swap |

## Performance Targets

| Metric | Target |
|--------|--------|
| Gateway overhead | < 10ms |
| Fallback time | < 5s |
| Cache hit rate | > 30% |
| Availability | 99.95% |

## Review Date

2026-11-21 (3 months post-launch)
