# Business Architecture — Success Metrics & Templates

## Business-value scorecard

| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| Cost per successful task | $____ | $____ | Token cost + compute |
| Resolution rate | ____% | ____% | Tasks completed without human |
| Response latency (p95) | ____s | ____s | End-to-end timing |
| Automation percentage | ____% | ____% | Human-free completions |
| User satisfaction | ____/5 | ____/5 | Post-interaction survey |
| Human escalation rate | ____% | ____% | Transfers to human agent |
| Error rate | ____% | ____% | Failed requests |
| Revenue impact | $____ | $____ | Attributed revenue |
| Operational savings | $____ | $____ | Cost avoidance |

---

## ROI Template

```
ROI = (Business Value - AI Operating Cost - Implementation Cost) / (AI Operating Cost + Implementation Cost)
```

### Productivity Value Calculation

| Factor | Value |
|--------|-------|
| Employees affected | ______ |
| Time saved per day (min) | ______ |
| Working days per year | 220 |
| Average hourly rate | $____ |
| **Annual value** | **$____** |

### Cost Comparison

| Category | Annual Cost |
|----------|-------------|
| Model inference | $____ |
| Infrastructure | $____ |
| Engineering team | $____ |
| Platform operations | $____ |
| Security & compliance | $____ |
| Observability | $____ |
| Maintenance | $____ |
| **Total** | **$____** |

---

## Architecture summary template

### What we built

[One paragraph describing the system]

### Key decisions

1. [Decision 1] — [Rationale]
2. [Decision 2] — [Rationale]
3. [Decision 3] — [Rationale]

### Alternatives considered

- [Alternative 1] — Why rejected
- [Alternative 2] — Why rejected

### Risks

- [Risk 1] — Mitigation
- [Risk 2] — Mitigation

### Cost

- Monthly infrastructure: $____
- Monthly model spend: $____
- Total monthly: $____

### Success criteria

- [Metric 1]: Target
- [Metric 2]: Target

---

## One-Page Architecture Brief Template

```
# [System Name] — Architecture Brief

## Problem
What problem are we solving?

## Users
Who benefits?

## Outcome
What changes if we succeed?

## Requirements
What must the system achieve?

## Architecture
What are the major components?

## Decisions
What are the three most important choices?

## Risks
What could go wrong?

## Governance
What controls are required?

## Cost
What is the expected operating model?

## Success Metrics
How will we know it worked?
```

---

## Architecture Review Structure (45 minutes)

| Section | Time | Content |
|---------|------|---------|
| Business problem | 5 min | What problem are we solving? |
| Desired outcome | 3 min | What changes if we succeed? |
| Requirements | 5 min | What must the system achieve? |
| Proposed architecture | 10 min | Major components |
| Major decisions | 5 min | Top 3 choices |
| Risks | 5 min | What could go wrong? |
| Cost | 5 min | Expected operating model |
| Expected value | 5 min | ROI and business impact |
| Open decisions | 7 min | What needs input? |

---

## ADR Template

```markdown
# ADR-XXX: [Decision Title]

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
[What is the situation?]

## Options
### Option 1: [Name]
- Pros: ...
- Cons: ...

### Option 2: [Name]
- Pros: ...
- Cons: ...

### Option 3: [Name]
- Pros: ...
- Cons: ...

## Decision
[What did we choose?]

## Rationale
[Why this option?]

## Consequences
[What are the trade-offs?]

## Revisit Conditions
[When should we reconsider?]
```

---

## Cost Architecture Comparison

| Approach | Fixed Cost | Variable Cost | Break-Even | Best For |
|----------|-----------|---------------|------------|----------|
| Managed Model | $0 | High per-token | N/A | Development, low volume |
| Self-Hosted | High (GPU) | Low per-token | High volume | Production scale |
| Hybrid | Medium | Mixed | Medium volume | Balanced approach |

---

## AI Metrics → Business Metrics Chain

```
AI Metric: Task Success ↑
    ↓
Business Metric: Resolution Time ↓
    ↓
Business Outcome: Support Cost ↓
```

### Failure Modes

| Mode | Description |
|------|-------------|
| Good AI, Bad Adoption | 95% model quality, 4% adoption |
| Wrong Optimization | 30% cost reduction, 40% task success drop |

**Rule:** Optimize for business outcomes, not isolated technical metrics.
