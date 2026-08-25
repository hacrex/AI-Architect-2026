# Day 12 — Business Architecture Exercises

## Exercise 1: Use Case Prioritization (20 min)

### Task

Create a prioritization matrix for 5 AI use cases in your organization.

### Template

| Use Case | Business Value (1-5) | Feasibility (1-5) | Data Readiness (1-5) | Risk (1-5) | Cost (1-5) | Time to Value (1-5) | Weighted Score |
|----------|---------------------|-------------------|---------------------|-----------|-----------|-------------------|---------------|
| | | | | | | | |

### Scoring Guide

- **Business Value**: Revenue impact, cost savings, productivity gain
- **Feasibility**: Technical readiness, team skills, infrastructure
- **Data Readiness**: Quality, availability, compliance
- **Risk**: Lower is better (1=low risk, 5=high risk)
- **Cost**: Lower is better (1=low cost, 5=high cost)
- **Time to Value**: Lower is better (1=fast, 5=slow)

### Deliverable

A ranked list with your top 3 recommended use cases and justification.

---

## Exercise 2: Business Language Translation (15 min)

### Task

Translate the following technical descriptions into business language.

### Scenario 1

**Technical:** "We're implementing a model gateway with semantic caching and fallback routing across three providers."

**Business:** _______________________________________________

### Scenario 2

**Technical:** "The RAG pipeline uses chunked embedding with hybrid search and re-ranking to improve retrieval precision."

**Business:** _______________________________________________

### Scenario 3

**Technical:** "We're deploying agent tool authorization with policy-based access control and audit logging."

**Business:** _______________________________________________

---

## Exercise 3: ROI Calculation (25 min)

### Task

Calculate the ROI for an AI Knowledge Assistant.

### Given

| Factor | Value |
|--------|-------|
| Employees | 5,000 |
| Current time searching for information | 45 min/day |
| Expected time saved with AI | 20 min/day |
| Working days per year | 220 |
| Average hourly rate | $60 |
| Annual AI platform cost | $800,000 |

### Calculate

1. Annual productivity value
2. Net value (productivity - cost)
3. ROI percentage
4. Payback period in months

---

## Exercise 4: One-Page Architecture Brief (30 min)

### Task

Create a one-page architecture brief for an AI system you would build.

### Template

```
# [System Name] — Architecture Brief

## Problem
[What problem are we solving?]

## Users
[Who benefits?]

## Outcome
[What changes if we succeed?]

## Requirements
[What must the system achieve?]

## Architecture
[What are the major components?]

## Decisions
[What are the three most important choices?]

## Risks
[What could go wrong?]

## Governance
[What controls are required?]

## Cost
[What is the expected operating model?]

## Success Metrics
[How will we know it worked?]
```

---

## Exercise 5: ADR Writing (25 min)

### Task

Write an Architecture Decision Record for one of the following:

1. Managed vs Self-Hosted Models
2. Vector Database Selection
3. Model Gateway vs Direct API Calls

### ADR Template

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

## Exercise 6: Architecture Review Presentation (30 min)

### Task

Prepare a 15-minute architecture review presentation.

### Structure

| Slide | Content | Time |
|-------|---------|------|
| 1 | Business Problem | 1 min |
| 2 | Desired Outcome | 1 min |
| 3 | Requirements | 2 min |
| 4 | Architecture Overview | 3 min |
| 5 | Major Decisions | 2 min |
| 6 | Risks | 2 min |
| 7 | Cost Model | 2 min |
| 8 | Success Metrics | 2 min |

### Deliverable

Slides or written outline with all 8 sections.

---

## Exercise 7: Portfolio Structure (20 min)

### Task

Plan your AI Architecture Portfolio with 3-5 projects.

### Template

```
Portfolio Plan

Project 1: [Name]
- Business Context: ...
- Architecture: ...
- Key Decisions: ...
- Demonstrates: ...

Project 2: [Name]
- Business Context: ...
- Architecture: ...
- Key Decisions: ...
- Demonstrates: ...

Project 3: [Name]
- Business Context: ...
- Architecture: ...
- Key Decisions: ...
- Demonstrates: ...

Project 4: [Name]
- Business Context: ...
- Architecture: ...
- Key Decisions: ...
- Demonstrates: ...

Project 5: [Name]
- Business Context: ...
- Architecture: ...
- Key Decisions: ...
- Demonstrates: ...
```

---

## Exercise 8: Final Architecture Review (30 min)

### Task

Answer all 14 architecture review questions for your system.

### Questions

1. **Business Problem:** What problem are we solving?
2. **Users:** Who benefits?
3. **Value:** How will we measure success?
4. **Data:** Where does the information come from?
5. **AI:** Why does AI need to be involved?
6. **Architecture:** Why are these components necessary?
7. **Technology:** Why these technologies?
8. **Scale:** What happens at 10x traffic?
9. **Reliability:** What happens when dependencies fail?
10. **Security:** What can users and agents access?
11. **Governance:** Who owns the system?
12. **Cost:** What will it cost to operate?
13. **Observability:** How will we know when it is failing?
14. **Change:** What happens when models and requirements change?

### Deliverable

Written answers to all 14 questions.
