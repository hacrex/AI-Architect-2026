# ADR-001: Model Hosting Strategy

## Title

LLM Hosting Strategy for Enterprise AI Knowledge Platform

## Context

The Enterprise AI Knowledge Assistant requires an inference strategy that balances cost, latency, privacy, and operational burden.

### Requirements

- **Users**: 10,000 employees
- **Data**: Sensitive enterprise documents (HR, legal, financial, engineering)
- **Traffic**: Predictable production traffic with peak periods
- **Availability**: High (99.9%)
- **Workloads**: Multiple AI workloads with different quality and latency requirements
- **Infrastructure**: Cloud + Kubernetes
- **Security**: Enterprise IAM, data cannot leave environment for sensitive workloads

### Hard Constraints

1. Sensitive data (legal, financial, HR) must remain within our environment
2. Must support enterprise IAM integration
3. Must be operable by current team (3 platform engineers, 0 dedicated GPU engineers)

---

## Options

### Option A: Managed Proprietary Model (OpenAI, Anthropic, etc.)

**Pros:**
- Rapid adoption, minimal infrastructure
- Strong capabilities, continuous updates
- No GPU management required
- Access to latest models immediately

**Cons:**
- Per-token pricing at scale ($0.03-$0.06/1K tokens for GPT-4 class)
- Provider dependency and lock-in
- API rate limits and availability dependent on provider
- Data leaves our infrastructure
- Provider-specific APIs and limits

### Option B: Self-Hosted Open-Weight Model (Llama, Mistral, etc.)

**Pros:**
- Full control over model and data
- Data locality and privacy
- Customization (fine-tuning, quantization)
- Predictable economics at sufficient scale
- Reduced vendor lock-in

**Cons:**
- GPU costs (hardware + cloud: $2,000-$10,000/month per node)
- Operations burden (upgrades, reliability, monitoring)
- Security responsibility (model, infrastructure, data)
- Platform engineering required
- Team lacks GPU expertise

### Option C: Hybrid Strategy

**Pros:**
- Route by data sensitivity
- Fallback capability
- Cost optimization per use case
- Best of both worlds where appropriate

**Cons:**
- Increased complexity
- Multiple vendor relationships
- Routing logic overhead
- Need to evaluate models across providers

---

## Decision

**Use a hybrid model architecture.**

```
                 Model Gateway
                      │
          ┌───────────┴───────────┐
          ↓                       ↓
     Managed Models        Self-Hosted Models
          │                       │
     Complex Tasks          Sensitive Tasks
  (general Q&A,          (legal, financial,
   research, coding)       HR documents)
```

### Routing Rules

| Workload Type | Route To | Rationale |
|--------------|----------|-----------|
| General Q&A | Managed (GPT-4/Claude) | Best capability, acceptable data exposure |
| Engineering docs | Managed (GPT-4) | Low sensitivity, high quality needed |
| Legal documents | Self-hosted (Llama 3 70B) | Data cannot leave environment |
| Financial data | Self-hosted (Llama 3 70B) | Compliance requirement |
| HR sensitive | Self-hosted (Llama 3 70B) | Privacy requirement |
| Fallback | Self-hosted (Llama 3 70B) | Provider outage resilience |

---

## Rationale

This allows:
- Provider flexibility and reduced single-provider dependency
- Data-sensitive workloads to remain controlled within our environment
- Fallback options when providers experience outages
- Workload-specific model selection based on requirements
- Cost optimization across different volume tiers

---

## Consequences

### Positive

- Flexibility to route by sensitivity and requirement
- Reduced single-provider dependency
- Workload-specific optimization
- Compliance with data residency for sensitive workloads
- Fallback capability during provider outages

### Negative

- More platform complexity (model gateway, routing logic)
- Multiple evaluation paths (must benchmark models across providers)
- Additional operational overhead (managed + self-hosted)
- Team needs to develop self-hosting expertise
- Integration complexity with multiple APIs

---

## Revisit Conditions

Revisit this decision when:

1. **Traffic changes significantly** — If self-hosted utilization is too low, costs become inefficient
2. **Pricing changes** — If managed API costs drop 50%+, self-hosted may become unnecessary
3. **Privacy requirements change** — If regulations require all data on-premise, eliminate managed
4. **Self-hosted utilization becomes uneconomical** — If GPU costs exceed managed API costs at our volume
5. **Model capabilities change substantially** — If open-weight models match proprietary quality, go fully self-hosted
6. **Team capability changes** — If we hire GPU/ML engineers, self-hosted becomes more viable
7. **Provider lock-in concerns materialize** — If a provider changes terms or deprecates models

---

## Metrics to Track

| Metric | Target | Current |
|--------|--------|---------|
| Managed API cost/month | < $2,000 | TBD |
| Self-hosted GPU cost/month | < $5,000 | TBD |
| Sensitive workload routing % | 100% self-hosted | TBD |
| Fallback activation frequency | Track | TBD |
| Model evaluation frequency | Monthly | TBD |
