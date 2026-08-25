# Day 08 — Technology Decisions, Build vs Buy & Architecture Trade-offs — Exercises

> Building on Day 07: We designed the complete system. Today we make defensible decisions about what to build, buy, and adopt.

---

## Exercise 1: Technology Decision Matrix

Create a decision matrix for three major technology decisions.

### Decision 1: Model Hosting Strategy

| Criteria | Weight | Managed (OpenAI/Anthropic) | Self-Hosted (Llama/Mistral) | Hybrid |
|----------|--------|---------------------------|---------------------------|--------|
| Capability | 20% | | | |
| Cost at projected scale | 20% | | | |
| Data privacy | 20% | | | |
| Latency | 10% | | | |
| Team capability | 10% | | | |
| Vendor independence | 10% | | | |
| Maintenance burden | 10% | | | |

Calculate weighted scores.

### Decision 2: Vector Storage Strategy

| Criteria | Weight | PostgreSQL + pgvector | Dedicated Vector DB (Pinecone) | Managed Vector Service |
|----------|--------|----------------------|-------------------------------|----------------------|
| Capability | 20% | | | |
| Cost at scale | 20% | | | |
| Operational burden | 20% | | | |
| Scalability | 15% | | | |
| Team capability | 15% | | | |
| Vendor lock-in | 10% | | | |

### Decision 3: Inference Platform Strategy

| Criteria | Weight | Managed API | vLLM on Kubernetes | KServe | Hybrid |
|----------|--------|------------|-------------------|--------|--------|
| Capability | 20% | | | | |
| Cost at scale | 20% | | | | |
| Latency | 15% | | | | |
| Scalability | 15% | | | | |
| Team capability | 15% | | | | |
| Maintenance | 15% | | | | |

---

## Exercise 2: Hard Constraints

Document requirements that automatically eliminate options.

For each constraint below, identify which technology options are disqualified:

1. **Data cannot leave our VPC**
2. **Must support < 200ms p95 latency**
3. **Must be SOC 2 compliant**
4. **Team has 0 GPU engineers**
5. **Budget is $5,000/month maximum**
6. **Must support 10,000 concurrent users**
7. **No single-provider dependency**

---

## Exercise 3: Build vs Buy Analysis

For each component, make a Build vs Buy recommendation:

### Component 1: Vector Search
- Build: Custom vector retrieval
- Buy: Managed vector database
- Use: PostgreSQL + pgvector

### Component 2: Model Gateway
- Build: Custom routing layer
- Buy: Managed API gateway
- Use: Open-source gateway

### Component 3: Observability
- Build: Custom tracing system
- Buy: Managed observability platform
- Use: Open-source stack (Prometheus + Grafana)

### Component 4: Authentication
- Build: Custom auth system
- Buy: Managed identity provider
- Use: Enterprise SSO integration

For each, answer:
- Is this our competitive advantage?
- What is the full build cost (5-year)?
- What is the full buy cost (5-year)?
- What is the migration cost if we need to change?

---

## Exercise 4: ADR — Model Hosting

Create an ADR using this template:

### ADR-XXX: Model Hosting Strategy

**Title**: What decision are we making?

**Context**: Why do we need to make it?
- Users:
- Data sensitivity:
- Traffic:
- Requirements:

**Options**:
- Option A:
- Option B:
- Option C:

**Decision**: What did we choose?

**Rationale**: Why?

**Consequences**:
- Positive:
- Negative:

**Revisit Conditions**:
- When should we reconsider?

---

## Exercise 5: ADR — Vector Storage

Create an ADR for vector storage decisions.

---

## Exercise 6: ADR — Inference Platform

Create an ADR for inference platform decisions.

---

## Exercise 7: Challenge Your Own Decision

After completing Exercises 4-6, deliberately argue against each of your decisions:

1. For each ADR you wrote, write a "Devil's Advocate" section arguing the opposite position
2. Identify the strongest argument against your chosen architecture
3. Identify what would have to change for the rejected options to become preferable

---

## Exercise 8: Workload-to-Technology Mapping

Match each workload to the most appropriate technology strategy:

| Workload | Users | Sensitivity | Traffic | Team Size | Recommended Strategy |
|----------|-------|-------------|---------|-----------|---------------------|
| Internal prototype | 100 | Low | Low | 2 | |
| Enterprise assistant | 10,000 | High | High | 10 | |
| Research experiment | 10 | Low | Low | 3 | |
| Customer-facing product | 100,000 | High | High | 20 | |

---

## Exercise 9: Hidden Cost Calculator

For a self-hosted LLM inference platform, calculate:

1. GPU costs (cloud or hardware)
2. Engineering time for setup
3. Ongoing maintenance (hours/month)
4. Monitoring and alerting
5. Security patching
6. Model updates
7. Scaling costs
8. On-call costs

Total: What is the 3-year total cost of ownership?

---

## Exercise 10: Revisit Conditions

For each of your ADRs, define specific triggers that would cause you to reconsider:

1. What traffic volume would make self-hosted uneconomical?
2. What pricing change from a provider would shift the decision?
3. What team growth would make self-hosted feasible?
4. What privacy regulation change would eliminate managed options?

---

## Day 08 Deliverables

Submit:

1. **Technology Decision Matrix** (Exercise 1)
2. **Hard Constraints Document** (Exercise 2)
3. **Build vs Buy Analysis** (Exercise 3)
4. **Three ADRs** (Exercises 4-6)
5. **Devil's Advocate Analysis** (Exercise 7)
6. **Workload Mapping** (Exercise 8)
7. **Hidden Cost Calculator** (Exercise 9)
8. **Revisit Conditions** (Exercise 10)
