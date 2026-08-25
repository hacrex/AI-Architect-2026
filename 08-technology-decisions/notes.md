# Day 08 — Technology Decisions, Build vs Buy & Architecture Trade-offs

> **Building on Day 07**: We designed the complete AI system with all layers connected. Today, the question changes from "How can we build this system?" to "What should we actually build, buy, adopt, or avoid?"

We've reached the second half of the journey.

The first seven days were about building your technical and architectural vocabulary:

```
Day 01 → Architecture Foundations
Day 02 → AI/ML & LLM Fundamentals
Day 03 → LLM Engineering
Day 04 → AI Infrastructure
Day 05 → Data Architecture
Day 06 → MLOps & AI Platform Engineering
Day 07 → Complete AI System Architecture
```

Today, the question changes.

Until now, we've mostly asked:

**"How can we build this system?"**

Today we ask:

**"What should we actually build, buy, adopt, or avoid?"**

That is one of the defining responsibilities of an architect.

---

## Table of Contents

1. [Technology Selection Is Architecture](#1-technology-selection-is-architecture)
2. [The Architect's Decision Framework](#2-the-architects-decision-framework)
3. [Managed vs Self-Hosted Models](#3-managed-vs-self-hosted-models)
4. [Self-Hosted Open-Weight Models](#4-self-hosted-open-weight-models)
5. [Neither Is Automatically Better](#5-neither-is-automatically-better)
6. [Build vs Buy](#6-build-vs-buy)
7. [Your Competitive Advantage Matters](#7-your-competitive-advantage-matters)
8. [The Hidden Cost of Building](#8-the-hidden-cost-of-building)
9. [The Hidden Cost of Buying](#9-the-hidden-cost-of-buying)
10. [Over-Engineering](#10-over-engineering)
11. [Under-Engineering](#11-under-engineering)
12. [Technology Selection Should Follow Workload](#12-technology-selection-should-follow-workload)
13. [Single Provider vs Multi-Provider](#13-single-provider-vs-multi-provider)
14. [Open Source vs Proprietary](#14-open-source-vs-proprietary)
15. [Technology Maturity](#15-technology-maturity)
16. [Team Capability Is an Architecture Constraint](#16-team-capability-is-an-architecture-constraint)
17. [Architecture Trade-Off Matrix](#17-architecture-trade-off-matrix)
18. [Don't Use Scores Blindly](#18-dont-use-scores-blindly)
19. [Architecture Decision Records](#19-architecture-decision-records)
20. [Example ADR](#20-example-adr)
21. [Your Enterprise AI Architecture Decision](#21-your-enterprise-ai-architecture-decision)
22. [Day 08 Hands-On Exercise](#22-day-08-hands-on-exercise)
23. [Day 08 Exercise: Challenge Your Own Decisions](#23-day-08-exercise-challenge-your-own-decisions)
24. [Day 08 Deliverables](#24-day-08-deliverables)
25. [Day 08 Architect Questions](#25-day-08-architect-questions)
26. [The Most Important Lesson Today](#26-the-most-important-lesson-today)

---

## The Goal of Day 08

You do not need to become an expert in every technology.

You need to understand:

- How to evaluate technology options systematically
- The difference between building, buying, and adopting
- How to identify hard constraints vs weighted preferences
- How to document decisions with ADRs
- How to challenge your own architectural choices
- The hidden costs of both building and buying
- When team capability changes the decision

---

## Objective

Make defensible technology decisions using structured evaluation frameworks, hard constraints, and Architecture Decision Records.

---

## 1. Technology Selection Is Architecture

An engineer may ask:

> "How do I deploy this model?"

An architect asks:

> "Should we deploy this model ourselves at all?"

That distinction matters.

Consider a simple AI requirement:

> Build an enterprise support assistant.

You could choose:

**Option A**: Managed proprietary LLM

**Option B**: Self-hosted open-weight LLM

**Option C**: Hybrid

All three can work.

The architectural challenge is determining which one is appropriate for the requirements.

---

## 2. The Architect's Decision Framework

Don't begin with technology.

Begin with requirements.

```
Business Requirement
        ↓
Technical Constraints
        ↓
Architecture Options
        ↓
Trade-off Analysis
        ↓
Decision
        ↓
ADR
        ↓
Implementation
```

For AI systems, your decision criteria should include:

| Criteria | Description |
|----------|-------------|
| Capability | Does it meet functional requirements? |
| Cost | What is the total cost of ownership? |
| Latency | Does it meet performance requirements? |
| Scalability | Can it grow with the workload? |
| Data privacy | Does it meet compliance requirements? |
| Security | Does it meet security posture? |
| Availability | Does it meet uptime requirements? |
| Vendor lock-in | How hard is it to change later? |
| Team expertise | Can your team operate it? |
| Operational complexity | What is the ongoing burden? |
| Maintenance burden | What does long-term upkeep look like? |
| Long-term flexibility | Can it adapt as needs change? |

The roadmap specifically identifies projected cost, latency, privacy, vendor lock-in, team capability, and maintenance commitment as key evaluation dimensions.

---

## 3. Managed vs Self-Hosted Models

This is probably the most important technology decision in modern AI architecture.

### Managed Model

```
Your Application
       ↓
Model API
       ↓
AI Provider
       ↓
Model Infrastructure
```

You don't operate the underlying GPU infrastructure.

**Advantages:**
- Fast implementation
- Low operational overhead
- Provider-managed scaling
- Access to highly capable models
- No GPU fleet management

**Trade-offs:**
- Per-token pricing
- Provider dependency
- Potential vendor lock-in
- Data/privacy considerations
- Provider-specific APIs and limits

---

## 4. Self-Hosted Open-Weight Models

Alternative:

```
Application
     ↓
AI Gateway
     ↓
Inference Server
     ↓
Kubernetes
     ↓
GPU
     ↓
Open-Weight Model
```

Examples of open-weight model families include Llama, Mistral, and others.

The roadmap highlights the benefits of control over data, predictable cost at sufficient scale, and reduced vendor lock-in, while also emphasizing the operational burden of infrastructure, updates, and maintenance.

**Advantages:**
- Greater infrastructure control
- Data locality
- Model flexibility
- Reduced dependency on a single provider
- Potentially attractive economics at high utilization

**Trade-offs:**
- GPU infrastructure
- Operations
- Model updates
- Security
- Scaling
- Monitoring
- Maintenance
- Platform engineering effort

---

## 5. Neither Is Automatically Better

This is an important architect mindset.

Don't say: "Open source is better."
Don't say: "Managed APIs are better."

Instead: "Better for which workload?"

| Requirement | Managed | Self-Hosted |
|-------------|---------|-------------|
| Fast launch | Strong | Weaker |
| Low operations | Strong | Weaker |
| Data control | Depends | Strong |
| Custom infrastructure | Limited | Strong |
| Provider independence | Weaker | Stronger |
| High utilization economics | Depends | Potentially strong |
| Small team | Strong | Potentially difficult |
| GPU expertise | Not required | Important |

The correct answer depends on the workload and constraints.

---

## 6. Build vs Buy

The same thinking applies beyond models.

Suppose you need Vector Search. Do you:

**Build**: Custom vector retrieval system

**Buy**: Managed vector database

Or perhaps **Use**: PostgreSQL + pgvector

There are three different decisions.

The question isn't: "Can we build it?"
Almost anything can be built.

The question is: **"Should we spend our engineering capacity building it?"**

---

## 7. Your Competitive Advantage Matters

This is one of the strongest filters for Build vs Buy.

Ask: **Is this capability part of our competitive advantage?**

Suppose you're building an AI healthcare product.

Your competitive advantage may be:
- domain knowledge
- workflow
- proprietary data
- user experience
- specialized models

Your competitive advantage probably isn't:
- Custom Kubernetes scheduler

If infrastructure isn't your differentiator, buying or adopting existing capabilities may make more sense.

---

## 8. The Hidden Cost of Building

When someone says: "We can build it ourselves."

Calculate the full cost. Not just development.

```
Build Cost
   │
   ├── Initial Engineering
   ├── Infrastructure
   ├── Security
   ├── Monitoring
   ├── Documentation
   ├── On-call
   ├── Upgrades
   ├── Hiring
   ├── Maintenance
   └── Opportunity Cost
```

The initial implementation may look cheap.
The five-year operational cost may not be.

---

## 9. The Hidden Cost of Buying

Buying isn't free of trade-offs either.

```
Managed Service
     ↓
Subscription / API Cost
     +
Vendor Dependency
     +
Migration Cost
     +
Integration Cost
     +
Potential Price Changes
```

At low volume, managed infrastructure might be significantly simpler.
At very high volume, the economics may change.

Therefore: **Always model the workload over time.**

---

## 10. Over-Engineering

The roadmap identifies over-engineering as one of the major failure modes.

Imagine you have:
- 500 users
- 10 requests/minute
- Small AI workload

And you build:
- Multi-region Kubernetes
- GPU fleet
- Custom inference engine
- Multi-cloud
- Service mesh
- Custom model gateway
- Five model providers

Technically impressive. Architecturally questionable.

You may have solved problems you don't actually have.

---

## 11. Under-Engineering

The opposite failure is equally dangerous.

Suppose your organization has:
- 10 million requests/day
- Sensitive enterprise data
- Strict latency requirements
- Large engineering team

And you choose:
- One external API
- No abstraction
- No fallback
- No caching
- No evaluation
- No provider strategy

You may have optimized for speed today while creating major problems tomorrow.

This is under-resourcing.

The roadmap explicitly calls out both over-engineering and adopting self-hosted infrastructure that the team cannot realistically support as expensive failure modes.

---

## 12. Technology Selection Should Follow Workload

Let's take four hypothetical workloads.

### Workload A
- Internal prototype
- 100 users
- Low sensitivity
- Low traffic

**Likely direction:** Managed model

### Workload B
- Enterprise AI
- 100,000 users
- Sensitive data
- High volume

**Potential direction:** Hybrid

### Workload C
- Highly sensitive workload
- Strict data locality
- Large predictable volume
- Strong GPU team

**Potential direction:** Self-hosted

### Workload D
- Research prototype
- Uncertain requirements
- Small team

**Potential direction:** Managed first

The point isn't the specific answer. The point is the reasoning process.

---

## 13. Single Provider vs Multi-Provider

Another major architecture decision.

### Single Provider

```
Application
     ↓
Provider A
```

Simple. But introduces dependency.

### Multi-Provider

```
                  AI Gateway
                      │
          ┌───────────┼───────────┐
          ↓           ↓           ↓
      Provider A  Provider B  Self-hosted
```

**Potential benefits:**
- fallback
- pricing flexibility
- model diversity
- reduced provider dependency

**Potential costs:**
- integration complexity
- evaluation complexity
- different APIs
- different model behaviors
- operational complexity

Again: **Flexibility has a price.**

---

## 14. Open Source vs Proprietary

Don't reduce this to an ideological debate.

Evaluate:
- Capability
- Cost
- Control
- Security
- Privacy
- Support
- Community
- Roadmap
- Maintenance

**Proprietary** — Potentially: Fast, High capability, Low operations

**Open-weight** — Potentially: More control, More customization, More operations

The architecture decision should be based on the requirements.

---

## 15. Technology Maturity

Another useful question: **How mature is the technology?**

A technology may be:

```
Experimental
    ↓
Emerging
    ↓
Production-capable
    ↓
Mature
```

Do not automatically use the newest tool in a critical production system.

Ask:
- How stable is it?
- Who maintains it?
- What is the release cadence?
- Is there enterprise support?
- How easy is migration?
- Is the ecosystem healthy?

The latest technology isn't necessarily the best architectural choice.

---

## 16. Team Capability Is an Architecture Constraint

This is easy to overlook.

Imagine: Self-hosted GPU platform looks perfect technically.

But your team has:
- 0 GPU engineers
- 0 ML infrastructure engineers
- 1 platform engineer

That changes the decision.

**Architecture doesn't exist in isolation. Your actual organization is part of the architecture.**

The roadmap explicitly includes team capability and long-term maintenance commitment in the decision criteria.

---

## 17. Architecture Trade-Off Matrix

Today, create a decision matrix.

| Criteria | Weight | Managed | Self-Hosted |
|----------|--------|---------|-------------|
| Capability | 20% | 9 | 8 |
| Cost at projected scale | 20% | 7 | 9 |
| Data privacy | 20% | 6 | 9 |
| Latency | 10% | 8 | 9 |
| Team capability | 10% | 9 | 5 |
| Vendor independence | 10% | 5 | 9 |
| Maintenance | 10% | 9 | 5 |

Then calculate a weighted score.

**The numbers are not the answer. The reasoning behind the numbers is the answer.**

---

## 18. Don't Use Scores Blindly

A common mistake is: "Self-hosted scored 8.1, therefore self-hosted wins."

No.

Some criteria are hard constraints.

For example: **Data cannot leave our environment.**

If a managed service violates that requirement: Managed = Disqualified.

It doesn't matter that it scored highly elsewhere.

Therefore use:

```
Hard Constraints
       ↓
Eliminate Invalid Options
       ↓
Weighted Trade-Off Analysis
       ↓
Final Decision
```

This is a much stronger architecture process.

---

## 19. Architecture Decision Records

Once you make the decision, document it.

An ADR should answer:

| Section | Question |
|---------|----------|
| Title | What decision are we making? |
| Context | Why do we need to make it? |
| Options | What alternatives did we consider? |
| Decision | What did we choose? |
| Rationale | Why? |
| Consequences | What do we gain? What do we give up? |
| Revisit Conditions | When should we reconsider the decision? |

The roadmap specifically recommends documenting significant technology decisions as ADRs and preserving what was chosen, what was considered, and why.

---

## 20. Example ADR

### ADR-001: LLM Hosting Strategy

**Context**: The Enterprise AI Knowledge Assistant requires:
- 10,000 employees
- Sensitive internal documentation
- Predictable production traffic
- High availability
- Multiple AI workloads

**Options:**
- A. Managed proprietary models
- B. Self-hosted open-weight models
- C. Hybrid

**Decision**: Use a hybrid model architecture.

```
                 Model Gateway
                      │
          ┌───────────┴───────────┐
          ↓                       ↓
     Managed Models        Self-Hosted Models
          │                       │
     Complex Tasks          Sensitive Tasks
```

**Rationale**: This allows provider flexibility, data-sensitive workloads to remain controlled, fallback options, and workload-specific model selection.

**Consequences:**
- Positive: flexibility, reduced single-provider dependency, workload optimization
- Negative: more platform complexity, multiple evaluation paths, additional operational overhead

**Revisit When:**
- traffic changes significantly
- pricing changes
- privacy requirements change
- self-hosted utilization becomes uneconomical
- model capabilities change substantially

That is an architecture decision rather than a technology preference.

---

## 21. Your Enterprise AI Architecture Decision

Return to the system we've been building.

**Enterprise AI Knowledge Platform**

Requirements:
- Users: 10,000
- Data: Sensitive enterprise documents
- Traffic: Predictable + peak periods
- Availability: High
- Models: Multiple workloads
- Infrastructure: Cloud + Kubernetes
- Security: Enterprise IAM
- Future: Potential multi-provider

Now make decisions about:

| Decision | Options |
|----------|---------|
| Model hosting | Managed / Self-hosted / Hybrid? |
| Vector database | Managed / PostgreSQL + pgvector / Dedicated vector DB? |
| Inference | Managed / vLLM / KServe / Other? |
| Kubernetes | Required / Not required? |
| Model Gateway | Required / Not required? |
| Multi-provider | Required / Not required? |
| Streaming | Required / Batch / Hybrid? |

Don't choose based on popularity. Choose based on requirements.

---

## 22. Day 08 Hands-On Exercise

Create a Technology Decision Matrix.

Compare:

### Model Strategy
- Managed Proprietary
- vs Self-Hosted Open-Weight
- vs Hybrid

### Vector Strategy
- PostgreSQL + pgvector
- vs Dedicated Vector Database
- vs Managed Vector Service

### Deployment Strategy
- Managed AI Platform
- vs Kubernetes + Inference Server
- vs Hybrid

For each, evaluate:
- Capability
- Cost
- Latency
- Privacy
- Security
- Scalability
- Team capability
- Maintenance
- Vendor lock-in

---

## 23. Day 08 Exercise: Challenge Your Own Decisions

After choosing your preferred architecture, deliberately argue against it.

If you selected **Self-hosted**, ask:
> Why shouldn't we use managed models?

If you selected **Managed**, ask:
> What happens when our traffic grows 20x?

If you selected **Hybrid**, ask:
> Are we introducing unnecessary complexity?

This is a powerful architect habit:

**Try to disprove your own architecture before production does it for you.**

---

## 24. Day 08 Deliverables

Today, produce:

### 1. Technology Decision Matrix

At least three major decisions.

### 2. Three ADRs

For example:
- **ADR-001** → Model Hosting
- **ADR-002** → Vector Storage
- **ADR-003** → Inference Platform

### 3. Build vs Buy Analysis

For at least two components.

### 4. Hard Constraints

Document requirements that automatically eliminate certain options.

### 5. Revisit Conditions

For every major decision:
> "What would have to change for us to reconsider this?"

---

## 25. Day 08 Architect Questions

Answer these without looking at your notes:

1. What is the difference between technology selection and technology adoption?
2. When should you choose managed AI services?
3. When does self-hosting make sense?
4. What are the hidden costs of self-hosting?
5. What are the hidden costs of managed services?
6. What is over-engineering?
7. What is under-resourcing?
8. Why does team capability influence architecture?
9. When should you use multiple model providers?
10. When does multi-provider architecture become unnecessary complexity?
11. What is a hard constraint?
12. Why shouldn't weighted scoring be used blindly?
13. What belongs in an ADR?
14. Why should architecture decisions be revisitable?
15. What would make you change your current AI architecture?

---

## 26. The Most Important Lesson Today

The biggest shift in Day 08 is this:

> **An architect is not paid to know every technology. An architect is paid to make good decisions about technology.**

You don't need to know every:
- LLM
- vector database
- Kubernetes operator
- inference engine
- cloud service
- agent framework

You need to know:
- What it enables
- What it constrains
- What it costs
- What risks it introduces
- What alternatives exist
- When you should reconsider it

The roadmap describes this as the judgment required to choose well among options rather than defaulting to whatever tool is most discussed.

---

## Your Progress

```
Day 01 → Architecture Mindset
Day 02 → AI/ML & LLM Fundamentals
Day 03 → LLM Engineering
Day 04 → AI Infrastructure
Day 05 → Data Architecture
Day 06 → MLOps & AI Platform Engineering
Day 07 → Complete AI System Architecture
Day 08 → Technology Decisions & Trade-offs
```

Now we move into another critical architect responsibility.

The next days will cover:
- Day 09 → Scale, Reliability & AI FinOps
- Day 10 → AI Observability
- Day 11 → Security & Governance
- Day 12 → Business Alignment & Portfolio
