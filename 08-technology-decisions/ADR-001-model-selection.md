# ADR-001: Model Selection

## Decision

Choose between managed proprietary model, self-hosted open-weight model, and hybrid strategy for AI inference.

## Context

We need to select an inference strategy that balances cost, latency, privacy, and operational burden. The system requires [specify requirements].

## Options

### Option A: Managed Proprietary Model (OpenAI, Anthropic, etc.)

**Pros:**
- Rapid adoption, minimal infrastructure
- Strong capabilities, continuous updates
- No GPU management required

**Cons:**
- Per-token pricing at scale
- Provider dependency and lock-in
- API rate limits
- Data leaves your infrastructure

### Option B: Self-Hosted Open-Weight Model (Llama, Mistral, etc.)

**Pros:**
- Full control over model and data
- Data locality and privacy
- Customization (fine-tuning)
- Predictable economics at sufficient scale

**Cons:**
- GPU costs (hardware + cloud)
- Operations burden (upgrades, reliability)
- Security responsibility
- Platform engineering required

### Option C: Hybrid Strategy

**Pros:**
- Route by data sensitivity
- Fallback capability
- Cost optimization per use case

**Cons:**
- Increased complexity
- Multiple vendor relationships
- Routing logic overhead

## Trade-offs

| Factor | Managed | Self-Hosted | Hybrid |
|--------|---------|-------------|--------|
| Cost (low volume) | Best | Worst | Moderate |
| Cost (high volume) | Worst | Best | Moderate |
| Privacy | Provider-dependent | Full control | Selective |
| Operations | None | Significant | Moderate |
| Latency | Network-dependent | Local | Variable |
| Lock-in | High | Low | Moderate |

## Consequences

Choose this option if:

- [ ] Cost per request is predictable and within budget
- [ ] Data sensitivity requirements are met
- [ ] Operational team can support the infrastructure
- [ ] Vendor lock-in is acceptable
