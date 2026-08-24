# Day 07 — AI System Architecture

> **Building on Day 06**: Yesterday we connected the layers into an operational platform — model registry, evaluation, CI/CD, and monitoring. Today we design the complete AI system where every layer works together as one coherent architecture.

We've spent six days learning components.

Today, we stop looking at them separately.

The question changes from:

**"Can we build individual AI components?"**

to:

**"Can we design a complete, production-grade AI system with the right boundaries, relationships, and trade-offs?"**

That is where AI System Architecture begins.

---

## Table of Contents

1. [What Is AI System Architecture?](#1-what-is-ai-system-architecture)
2. [Start With the Business Problem](#2-start-with-the-business-problem)
3. [Functional vs Non-Functional Requirements](#3-functional-vs-non-functional-requirements)
4. [Define the Architecture Boundaries](#4-define-the-architecture-boundaries)
5. [Think in Architecture Layers](#5-think-in-architecture-layers)
6. [Architecture Is About Relationships](#6-architecture-is-about-relationships)
7. [The AI Gateway](#7-the-ai-gateway)
8. [RAG as a Subsystem](#8-rag-as-a-subsystem)
9. [Agents as Another Subsystem](#9-agents-as-another-subsystem)
10. [Synchronous vs Asynchronous Architecture](#10-synchronous-vs-asynchronous-architecture)
11. [Event-Driven AI Architecture](#11-event-driven-ai-architecture)
12. [Real-Time + Batch Architecture](#12-real-time--batch-architecture)
13. [Reliability Architecture](#13-reliability-architecture)
14. [Failure Domains](#14-failure-domains)
15. [Security Architecture](#15-security-architecture)
16. [Agent Security](#16-agent-security)
17. [Observability Architecture](#17-observability-architecture)
18. [Cost Architecture](#18-cost-architecture)
19. [Architecture Decision Records](#19-architecture-decision-records)
20. [Our Complete Enterprise AI Architecture](#20-our-complete-enterprise-ai-architecture)
21. [Day 07 Hands-On Lab](#21-day-07-hands-on-lab)
22. [Day 07 Exercise](#22-day-07-exercise)
23. [Day 07 Architecture Review](#23-day-07-architecture-review)
24. [Day 07 Deliverables](#24-day-07-deliverables)
25. [The Architect's Takeaway](#25-the-architects-takeaway)

---

## The Goal of Day 07

You do not need to implement every component today.

You need to understand:

- How individual layers combine into a complete system
- Why architecture is about relationships, not just components
- How to define boundaries, interfaces, and controls
- How to design reliability, security, and observability into the architecture
- How to document architecture decisions with ADRs
- How to perform a complete architecture review

---

## Objective

Design the complete AI system — from users to infrastructure — with deliberate relationships and decisions.

---

## 1. What Is AI System Architecture?

An AI system is not:

```
Application
    ↓
    LLM
```

And it isn't simply:

```
Application
    ↓
   RAG
    ↓
Vector DB
    ↓
   LLM
```

A production AI system may look more like:

```
                         USERS
                           │
                           ▼
                    ┌─────────────┐
                    │ API Gateway │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ AI Gateway  │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
             RAG         Agents       Routing
              │            │            │
              ▼            ▼            ▼
           Retrieval      Tools        Models
              │            │            │
              └────────────┼────────────┘
                           ▼
                    Context Assembly
                           │
                           ▼
                    Model Gateway
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
          Managed       Self-hosted   Fallback
           Models          Models
                            │
                       Kubernetes
                            │
                         GPU Pool
```

And underneath:

```
Data
Infrastructure
MLOps
Observability
Security
Governance
FinOps
```

That is the system we're learning to design.

---

## 2. Start With the Business Problem

Before drawing boxes, define the problem.

Suppose the business requirement is:

> Build an enterprise AI assistant that helps 10,000 employees find and understand internal company information.

Don't immediately choose:

- OpenAI
- Gemini
- Claude
- Kubernetes
- Pinecone
- LangGraph

First define:

### Users

10,000 employees.

### Workload

Internal knowledge search and assistance.

### Data

- policies
- documentation
- technical knowledge
- HR information
- security documentation

### Requirements

- secure access
- reliable answers
- source attribution
- low latency
- high availability
- cost control

### Constraints

- sensitive data
- multiple model providers
- changing documentation
- operational requirements

Now architecture has a reason to exist.

---

## 3. Functional vs Non-Functional Requirements

This distinction is fundamental.

### Functional

What should the system do?

```
User asks question
        ↓
System searches authorized knowledge
        ↓
System generates answer
        ↓
System provides sources
```

### Non-functional

How well should it do it?

```
Availability → 99.9%
Latency → Target defined
Security → Enterprise IAM
Scale → 10,000 users
Auditability → Required
Cost → Controlled
```

A system can satisfy every functional requirement and still fail because of non-functional requirements.

---

## 4. Define the Architecture Boundaries

Before choosing technologies, decide what's inside and outside the system.

```
┌─────────────────────────────────────────┐
│             Enterprise AI System        │
│                                         │
│  API Gateway                            │
│       ↓                                 │
│  AI Application                         │
│       ↓                                 │
│  RAG / Agents                           │
│       ↓                                 │
│  Model Gateway                          │
│       ↓                                 │
│  Inference                              │
│                                         │
└─────────────────────────────────────────┘

        External Systems
        ────────────────
        Identity Provider
        Enterprise DB
        Document Systems
        Model Providers
```

The boundary tells you:

- what you control
- what you depend on
- where security controls apply
- where failure can occur

---

## 5. Think in Architecture Layers

Our complete AI architecture can now be organized into layers.

```
┌─────────────────────────────────────────┐
│             Business Layer              │
│ Goals • KPIs • ROI • Compliance         │
├─────────────────────────────────────────┤
│            Application Layer             │
│ Web • API • Workflow • Experience       │
├─────────────────────────────────────────┤
│              AI Layer                    │
│ RAG • Agents • Tools • Context          │
├─────────────────────────────────────────┤
│             Model Layer                  │
│ LLM • Embeddings • Classifiers          │
├─────────────────────────────────────────┤
│              Data Layer                  │
│ DB • Vector • Object Storage • Streams  │
├─────────────────────────────────────────┤
│           Platform Layer                 │
│ MLOps • Evaluation • Registry           │
├─────────────────────────────────────────┤
│        Infrastructure Layer              │
│ K8s • GPU • Network • Storage            │
├─────────────────────────────────────────┤
│       Cross-Cutting Concerns             │
│ Security • Observability • FinOps        │
│ Governance • Reliability                 │
└─────────────────────────────────────────┘
```

An architect needs to understand how every layer affects the others.

---

## 6. Architecture Is About Relationships

Don't just document components.

Document how they interact.

```
User
  ↓
Identity
  ↓
API Gateway
  ↓
AI Application
  ↓
Retriever
  ↓
Vector Database
  ↓
Context
  ↓
Model
  ↓
Response
```

Now ask:

- **Who authenticates?** Identity layer.
- **Who authorizes?** Gateway / application / data layer.
- **Who retrieves?** Retrieval service.
- **Who decides which model?** Model gateway.
- **Who records the request?** Observability platform.
- **Who controls cost?** AI gateway / platform / FinOps.

Architecture is about relationships and responsibilities.

---

## 7. The AI Gateway

We've introduced this concept several times.

Now make it an architectural boundary.

```
                       AI Gateway
                           │
       ┌───────────────────┼───────────────────┐
       ↓                   ↓                   ↓
 Authentication       Rate Limiting       Policy
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                    Model Routing
                           │
              ┌────────────┼────────────┐
              ↓            ↓            ↓
          Model A       Model B       Model C
```

It can provide a central location for:

- authentication
- authorization
- rate limiting
- model routing
- token tracking
- provider abstraction
- fallback
- policy enforcement
- audit logging

This prevents every application from implementing these capabilities independently.

---

## 8. RAG as a Subsystem

RAG should not become your entire architecture.

Treat it as one subsystem.

```
                    AI Application
                          │
                          ▼
                         RAG
                          │
             ┌────────────┼────────────┐
             ↓            ↓            ↓
         Retriever     Metadata      Filters
             │
             ↓
        Vector Store
             │
             ↓
       Context Builder
```

Now RAG can evolve independently.

For example, you could change:

- Vector DB

without rewriting:

- AI Application

That's loose coupling.

---

## 9. Agents as Another Subsystem

Similarly:

```
                     AI Application
                           │
                           ▼
                         Agent
                           │
             ┌─────────────┼─────────────┐
             ↓             ↓             ↓
          Search         Database       API
           Tool            Tool         Tool
```

The agent shouldn't own the entire infrastructure.

It should interact with well-defined tools.

That gives us a useful principle:

**Keep capabilities modular and expose them through controlled interfaces.**

---

## 10. Synchronous vs Asynchronous Architecture

Not every AI operation should happen inside the user's request.

### Synchronous

```
User
  ↓
 API
  ↓
 LLM
  ↓
Response
```

Use when the user expects an immediate answer.

### Asynchronous

```
User
  ↓
 API
  ↓
Queue
  ↓
Worker
  ↓
AI Processing
  ↓
Result
```

Use for workloads such as:

- document processing
- large-scale summarization
- batch classification
- embedding generation
- report generation
- offline evaluation

---

## 11. Event-Driven AI Architecture

Now combine Day 5 data architecture with Day 7 system architecture.

Suppose a document changes.

```
Document Updated
       ↓
     Event
       ↓
    Queue
       ↓
Processing Worker
       ↓
Embedding
       ↓
Vector Store
```

The user-facing AI application doesn't need to know how the document was processed.

This reduces coupling.

---

## 12. Real-Time + Batch Architecture

A production AI platform can contain both.

```
                         AI Platform
                              │
                 ┌────────────┴────────────┐
                 ↓                         ↓
            Real-Time                  Batch
                 │                         │
                 ↓                         ↓
             API/LLM                   Queue
                 │                         │
                 ↓                         ↓
              Response                 Workers
```

For example:

**Real-time**: Employee asks: "What is our remote work policy?"

**Batch**: Every night: Process newly uploaded documents and update embeddings.

Different workloads deserve different architectures.

---

## 13. Reliability Architecture

Now think beyond the happy path.

### Model Provider Fails

```
Application
    ↓
Model Gateway
    ↓
Primary Model
    X
    ↓
Fallback Model
    ↓
Response
```

### Vector Database Fails

Possible strategies:

- fallback search
- cached knowledge
- graceful degradation
- temporary unavailability

### Queue Grows Rapidly

Use:

- backpressure
- scaling
- prioritization
- rate limiting

Architecture should define these behaviors before the incident happens.

---

## 14. Failure Domains

Map your dependencies.

```
                    AI Application
                         │
        ┌────────────────┼────────────────┐
        ↓                ↓                ↓
     Model            Vector DB          API
        │                │                │
     Provider          Storage          External
        │                │                │
       FAIL             FAIL             FAIL
```

Now document:

| Component | Failure | Impact | Response |
|-----------|---------|--------|----------|
| Model | Provider outage | No generation | Fallback |
| Vector DB | Unavailable | No retrieval | Graceful degradation |
| Queue | Backlog | Delayed jobs | Scale workers |
| GPU | Capacity exhausted | High latency | Autoscale |
| External API | Timeout | Tool unavailable | Retry/fallback |

This is the beginning of a proper reliability architecture.

---

## 15. Security Architecture

Security shouldn't be an isolated diagram created at the end.

It should follow the entire request.

```
User
  ↓
Identity
  ↓
Authorization
  ↓
API Gateway
  ↓
AI Gateway
  ↓
RAG / Agent
  ↓
Tool / Data
  ↓
Model
```

At every boundary ask:

- Who is calling?
- What can they access?
- What data can cross the boundary?
- What action can be performed?
- What should be logged?

---

## 16. Agent Security

Agentic systems make this even more important.

Imagine:

```
Agent
 ├── Search
 ├── Database
 ├── Email
 ├── Jira
 └── Production Deployment
```

Don't give the agent unrestricted access.

Use:

```
Agent
  ↓
Policy Engine
  ↓
Tool Authorization
  ↓
Tool
```

For sensitive actions:

```
Agent
  ↓
Proposed Action
  ↓
Human Approval
  ↓
Execution
```

This creates a controlled boundary around agent autonomy.

---

## 17. Observability Architecture

By now we know traditional infrastructure monitoring isn't enough.

A complete AI architecture needs visibility into:

```
Infrastructure
  ↓
Application
  ↓
AI Workflow
  ↓
Model
  ↓
Data / Retrieval
  ↓
User Outcome
```

For example:

```
Request
  ↓
Trace
 ├── Retrieval
 ├── Tool Call
 ├── Model Call
 ├── Tokens
 ├── Latency
 └── Cost
```

Observability is a system architecture concern, not merely a monitoring dashboard.

---

## 18. Cost Architecture

We also need cost visibility.

A simple AI request might involve:

```
User Request
     │
     ├── Embedding
     ├── Vector Search
     ├── LLM Input Tokens
     ├── LLM Output Tokens
     ├── Tool Calls
     ├── Storage
     └── Observability
```

Therefore:

**AI cost is a system property, not just an LLM API bill.**

---

## 19. Architecture Decision Records

You should never just draw an architecture and say:

> "This is our architecture."

Document the important decisions.

### Example: ADR-001 — Model Strategy

**Context**: We need multiple AI workloads with different quality and latency requirements.

**Options**:
- one model
- multiple models
- managed models
- self-hosted models

**Decision**: Use a model gateway with multiple providers.

**Consequences**:

Benefits:
- routing flexibility
- fallback
- reduced coupling

Costs:
- additional platform complexity
- provider integration work

This is what makes architecture defensible.

---

## 20. Our Complete Enterprise AI Architecture

Now bring Days 1-7 together.

```
                              USERS
                                │
                                ▼
                         ┌─────────────┐
                         │ API Gateway │
                         └──────┬──────┘
                                │
                         Authentication
                                │
                                ▼
                         ┌─────────────┐
                         │ AI Gateway  │
                         └──────┬──────┘
                                │
               ┌────────────────┼────────────────┐
               ↓                ↓                ↓
              RAG             Agents          Routing
               │                │                │
               ↓                ↓                ↓
          Retrieval           Tools          Models
               │                │                │
               ▼                ▼                │
          Vector DB        External APIs          │
               │                │                 │
               └────────────────┼─────────────────┘
                                ↓
                         Context Assembly
                                │
                                ▼
                         ┌─────────────┐
                         │Model Gateway│
                         └──────┬──────┘
                                │
                    ┌───────────┼───────────┐
                    ↓           ↓           ↓
                Managed      Self-hosted  Fallback
                 Models         Models
                                  │
                             Kubernetes
                                  │
                              GPU Pool
                                  │
                           Inference Layer
                                  │
                             Model Runtime

       ┌────────────────────────────────────────────┐
       │                 DATA LAYER                 │
       │ DB • Vector • Object Storage • Streaming   │
       └────────────────────────────────────────────┘

       ┌────────────────────────────────────────────┐
       │              AI PLATFORM                   │
       │ Registry • Evaluation • CI/CD • GitOps     │
       └────────────────────────────────────────────┘

       ┌────────────────────────────────────────────┐
       │         CROSS-CUTTING CONCERNS             │
       │ Security • Observability • Governance      │
       │ Reliability • FinOps • Audit               │
       └────────────────────────────────────────────┘
```

This is the architecture we have been building incrementally.

---

## 21. Day 07 Hands-On Lab

Today, stop building individual components.

Design the complete system.

### Your Scenario

**Enterprise AI Knowledge Platform for 10,000 employees**

### Requirements

- 10,000 users
- RAG
- agent capabilities
- multiple model providers
- role-based access
- document-level permissions
- high availability
- model fallback
- asynchronous document ingestion
- Kubernetes-based infrastructure
- GPU inference
- managed model fallback
- evaluation
- CI/CD
- observability
- cost tracking
- auditability

---

## 22. Day 07 Exercise

### Exercise 1: System Context Diagram

Who interacts with the system?

```
Users
  ↓
AI Platform
  ↓
Enterprise Systems
```

### Exercise 2: Logical Architecture

Show:

- gateway
- RAG
- agents
- model gateway
- data
- platform

### Exercise 3: Data Flow

```
Document
  ↓
Ingestion
  ↓
Processing
  ↓
Embedding
  ↓
Vector Store
  ↓
Retrieval
  ↓
Context
  ↓
LLM
```

### Exercise 4: Deployment Architecture

```
Cloud / On-Prem
      ↓
Kubernetes
      ↓
GPU Nodes
      ↓
Inference
```

### Exercise 5: Security Architecture

```
Identity
  ↓
Authorization
  ↓
Data
  ↓
Model
  ↓
Tools
```

### Exercise 6: Architecture Decision Records

Create three ADRs:

1. **ADR-001 → Model Strategy**
2. **ADR-002 → Data / Vector Strategy**
3. **ADR-003 → Managed vs Self-Hosted**

### Exercise 7: Failure Matrix

Document at least 10 failure scenarios.

---

## 23. Day 07 Architecture Review

Now perform your own architecture review.

Ask:

### Requirements

- Did I define the workload?
- Did I define scale?
- Did I define latency?
- Did I define availability?

### Data

- Where does the data originate?
- How fresh is it?
- How is it authorized?

### AI

- Why RAG?
- Why agents?
- Why these models?
- Why model routing?

### Infrastructure

- Why Kubernetes?
- Why GPUs?
- How does scaling work?

### Reliability

- What fails?
- What is the fallback?
- What is the recovery strategy?

### Security

- What can each user access?
- What can agents do?

### Platform

- How are changes deployed?
- How are models evaluated?
- How do we roll back?

### Cost

- What is expensive?
- How do we control it?

If you cannot answer these questions, the architecture isn't finished.

---

## 24. Day 07 Deliverables

Create:

### 1. System Context Diagram

Who interacts with the system?

### 2. Logical Architecture

What components exist?

### 3. Deployment Architecture

Where do those components run?

### 4. Data Flow Diagram

How does information move?

### 5. Security Architecture

Where are identity and policy enforced?

### 6. Three ADRs

At minimum:

- **ADR-001** → Model Strategy
- **ADR-002** → Data / Vector Strategy
- **ADR-003** → Managed vs Self-Hosted

### 7. Failure Matrix

Document at least 10 failure scenarios.

---

## 25. The Architect's Takeaway

We've spent six days learning components.

Today we learned the most important architectural lesson:

**A system isn't a collection of technologies. It's a set of deliberate relationships and decisions designed around requirements.**

You can have:

- the best model
- the best vector database
- the best GPU
- the best Kubernetes cluster
- the best agent framework

and still create a bad architecture.

Because architecture isn't about having the most advanced components.

It's about having the right components, boundaries, interfaces, controls, and trade-offs for the problem you're solving.

---

## Your Journey So Far

```
Day 01
Architecture Mindset
        ↓
Day 02
Understand AI & Models
        ↓
Day 03
Engineer LLM Applications
        ↓
Day 04
Build AI Infrastructure
        ↓
Day 05
Design AI Data Architecture
        ↓
Day 06
Build AI Platforms
        ↓
Day 07
Design the Complete AI System
```

Now the series changes direction.

The next three days are about architectural judgment:

- Day 08 → Technology Selection & Build vs Buy
- Day 09 → Scale, Reliability & AI FinOps
- Day 10 → AI Observability
- Day 11 → Security & Governance
- Day 12 → Business Alignment & Portfolio

### The question for tomorrow

We stop asking:

> "What technologies can we use?"

and start asking:

> "Which technology should we choose, and why?"

That's Day 08 → Technology Decisions, Build vs Buy & Architecture Trade-offs.
