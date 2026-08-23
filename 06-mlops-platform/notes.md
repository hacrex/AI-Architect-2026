# Day 06 — MLOps & AI Platform Engineering

> **Building on Day 05**: Yesterday we designed the data architecture that makes AI systems trustworthy — ingestion, chunking, vector databases, and governance. Today we connect all the layers we've built into an operational platform.

We've now built the major layers of our AI system:

- Day 01 → Architecture Foundations
- Day 02 → AI/ML & LLM Fundamentals
- Day 03 → LLM Engineering
- Day 04 → AI Infrastructure
- Day 05 → Data Architecture

Today we connect them.

The question changes from:

**"Can we build an AI system?"**

to:

**"Can an organization reliably build, deploy, operate, evaluate, and continuously improve hundreds of AI systems?"**

That is where MLOps and AI Platform Engineering enter the picture.

---

## Table of Contents

1. [What Is MLOps?](#1-what-is-mlops)
2. [MLOps vs LLMOps vs GenAIOps](#2-mlops-vs-llmops-vs-genaiops)
3. [Why AI Needs a Platform](#3-why-ai-needs-a-platform)
4. [AI Platform ≠ Kubernetes Cluster](#4-ai-platform--kubernetes-cluster)
5. [The AI Platform Layers](#5-the-ai-platform-layers)
6. [Experiment Tracking](#6-experiment-tracking)
7. [Model Registry](#7-model-registry)
8. [Model Promotion](#8-model-promotion)
9. [Evaluation Is the CI/CD of AI Quality](#9-evaluation-is-the-cicd-of-ai-quality)
10. [Evaluation Before Deployment](#10-evaluation-before-deployment)
11. [CI/CD for AI](#11-cicd-for-ai)
12. [GitOps for AI Platforms](#12-gitops-for-ai-platforms)
13. [Model Deployment Strategies](#13-model-deployment-strategies)
14. [Drift](#14-drift)
15. [LLM Evaluation Is Continuous](#15-llm-evaluation-is-continuous)
16. [Observability for AI Platforms](#16-observability-for-ai-platforms)
17. [Feature Stores and ML Platforms](#17-feature-stores-and-ml-platforms)
18. [Self-Service AI Platform](#18-self-service-ai-platform)
19. [Internal Developer Platform for AI](#19-internal-developer-platform-for-ai)
20. [AI Platform Control Plane vs Data Plane](#20-ai-platform-control-plane-vs-data-plane)
21. [Our Enterprise AI Platform](#21-our-enterprise-ai-platform)
22. [Day 06 Hands-On Lab](#22-day-06-hands-on-lab)
23. [Day 06 Exercise](#23-day-06-exercise)
24. [Build an AI CI/CD Pipeline](#24-build-an-ai-cicd-pipeline)
25. [Day 06 Architect Questions](#25-day-06-architect-questions)
26. [Day 06 Deliverables](#26-day-06-deliverables)
27. [The Architect's Takeaway](#27-the-architects-takeaway)

## The Goal of Day 06

You do not need to become an MLOps engineer.

You need to understand:

- What MLOps is and why it exists
- How MLOps extends beyond traditional DevOps
- Why organizations need an AI platform
- How model registry, experiment tracking, and evaluation connect
- How CI/CD changes when AI enters the pipeline
- How to design deployment strategies for models
- How AI systems degrade without code changes
- How to architect a self-service AI platform

---

## Objective

Design the platform that manages AI workloads throughout their lifecycle.

---

## 1. What Is MLOps?

Traditional software engineering has:

```
Code
  ↓
Build
  ↓
Test
  ↓
Deploy
  ↓
Monitor
  ↓
Improve
```

Machine learning adds another dimension:

```
Data
  ↓
Experiment
  ↓
Training
  ↓
Evaluation
  ↓
Model
  ↓
Deployment
  ↓
Monitoring
  ↓
Retraining
```

MLOps brings these processes together.

A simplified lifecycle:

```
              ┌──────────────┐
              │     Data     │
              └──────┬───────┘
                     ↓
              ┌──────────────┐
              │ Experiment   │
              └──────┬───────┘
                     ↓
              ┌──────────────┐
              │   Training   │
              └──────┬───────┘
                     ↓
              ┌──────────────┐
              │ Evaluation   │
              └──────┬───────┘
                     ↓
              ┌──────────────┐
              │Model Registry│
              └──────┬───────┘
                     ↓
              ┌──────────────┐
              │  Deployment  │
              └──────┬───────┘
                     ↓
              ┌──────────────┐
              │  Monitoring  │
              └──────┬───────┘
                     ↓
                 Feedback
                     │
                     └──────────→ Improvement
```

For LLM applications, this lifecycle becomes even broader.

---

## 2. MLOps vs LLMOps vs GenAIOps

These terms overlap, but understand the distinction.

### MLOps

Focuses on:

- datasets
- experiments
- training
- models
- deployment
- monitoring
- retraining

### LLMOps

Adds concerns such as:

- prompts
- LLM versions
- token usage
- evaluation
- RAG
- embeddings
- traces
- model routing

### GenAIOps

Expands further into:

- agents
- tools
- workflows
- guardrails
- human-in-the-loop
- agent evaluation
- model/provider management
- AI governance

Conceptually:

```
MLOps
  │
  └── LLMOps
        │
        └── GenAIOps
```

Don't get trapped by the terminology.

The architectural principle is:

**AI systems need a repeatable operational lifecycle just like software systems do.**

---

## 3. Why AI Needs a Platform

Imagine one team builds an AI chatbot.

Then another team builds:

- document classification
- customer support
- code assistant
- fraud detection
- incident analysis
- recommendation system

If every team independently creates:

- Model deployment
- Vector DB
- Evaluation
- Monitoring
- Secrets
- CI/CD
- GPU infrastructure
- Logging
- Tracing

you eventually get:

```
Team A → Platform A
Team B → Platform B
Team C → Platform C
Team D → Platform D
```

That creates enormous duplication.

An AI Platform attempts to provide common capabilities.

```
                   AI Teams
        ┌────────────┼────────────┐
        ↓            ↓            ↓
     Team A        Team B        Team C
        └────────────┼────────────┘
                     ↓
             AI Platform
                     │
      ┌──────────────┼──────────────┐
      ↓              ↓              ↓
  Model Ops       Data Ops      Evaluation
      ↓              ↓              ↓
 Deployment      Pipelines      Monitoring
      ↓              ↓              ↓
 Infrastructure  Security       Governance
```

This is where Platform Engineering meets AI.

---

## 4. AI Platform ≠ Kubernetes Cluster

This distinction is extremely important for someone coming from Platform Engineering.

You could have:

- Kubernetes
- GPUs
- vLLM

and still not have an AI platform.

A platform should provide self-service capabilities.

For example:

"I want to deploy this model."

The platform should handle:

- infrastructure
- deployment
- configuration
- secrets
- observability
- scaling
- evaluation
- rollback

The developer shouldn't need to understand every GPU node or Kubernetes implementation detail.

---

## 5. The AI Platform Layers

Think about the platform as:

```
┌──────────────────────────────────────┐
│             AI PRODUCTS              │
│ Chatbots • Agents • ML Applications  │
├──────────────────────────────────────┤
│          AI DEVELOPMENT              │
│ SDKs • APIs • Templates • Workflows  │
├──────────────────────────────────────┤
│          AI OPERATIONS               │
│ Eval • Registry • Deployment • Trace │
├──────────────────────────────────────┤
│             DATA                     │
│ Lake • Warehouse • Vector • Feature  │
├──────────────────────────────────────┤
│          AI INFRASTRUCTURE            │
│ GPU • K8s • Network • Storage        │
├──────────────────────────────────────┤
│      SECURITY / GOVERNANCE            │
│ IAM • Policy • Audit • Compliance    │
└──────────────────────────────────────┘
```

The platform hides unnecessary complexity while exposing useful capabilities.

---

## 6. Experiment Tracking

AI development is experimental.

A developer might test:

- Model A
- Prompt v1
- Temperature 0.2

Then:

- Model B
- Prompt v2
- Temperature 0.5

Then:

- Model A
- Prompt v3
- RAG enabled

Without tracking, nobody knows which version produced which result.

You need:

```
Experiment
 ├── Model
 ├── Prompt
 ├── Dataset
 ├── Parameters
 ├── Evaluation
 └── Results
```

This is why experiment tracking becomes an important platform capability.

---

## 7. Model Registry

Once you have models worth deploying, you need to manage them.

Think:

```
Model Registry
│
├── Model A
│   ├── v1
│   ├── v2
│   └── v3
│
├── Model B
│   ├── v1
│   └── v2
│
└── Model C
    └── v1
```

But for modern AI systems, you may also need to track:

- model version
- source
- training dataset
- evaluation results
- deployment status
- approval state
- security status
- cost profile

The registry becomes part of your AI supply chain.

---

## 8. Model Promotion

Don't automatically send every model from experiment to production.

Think:

```
Experiment
    ↓
Evaluation
    ↓
Development
    ↓
Staging
    ↓
Approval
    ↓
Production
```

A model could fail evaluation because:

- accuracy decreased
- hallucinations increased
- latency increased
- cost increased
- safety score decreased

Therefore:

**A model should earn its way into production.**

---

## 9. Evaluation Is the CI/CD of AI Quality

Traditional software might have:

- Unit Tests
- Integration Tests
- End-to-End Tests

AI systems need additional evaluation.

For example:

```
             AI Evaluation
                  │
      ┌───────────┼────────────┐
      ↓           ↓            ↓
   Quality     Safety        Cost
      │           │            │
      ↓           ↓            ↓
 Accuracy     Toxicity      Tokens
 Grounding    Leakage       Latency
 Relevance    Injection     Spend
```

For a RAG application, you may evaluate:

- retrieval relevance
- context relevance
- groundedness
- answer relevance

For an agent:

- task completion
- tool selection
- tool correctness
- number of steps
- failure rate
- safety

---

## 10. Evaluation Before Deployment

Imagine you changed the prompt.

The application still works.

But answer quality dropped from:

**91%**

to:

**82%**

A traditional deployment pipeline may not notice.

An AI-aware pipeline can.

```
Code / Prompt Change
        ↓
Build
        ↓
Test
        ↓
AI Evaluation
        ↓
Quality Threshold
        │
     ┌──┴──┐
     ↓     ↓
   Pass   Fail
     ↓     ↓
 Deploy   Stop
```

This is one of the biggest mindset changes from conventional CI/CD.

---

## 11. CI/CD for AI

### Traditional

```
Git Push
  ↓
Build
  ↓
Test
  ↓
Deploy
```

### AI Platform

```
Git Push
  ↓
Build
  ↓
Unit Tests
  ↓
Integration Tests
  ↓
AI Evaluation
  ↓
Security Checks
  ↓
Cost / Performance Checks
  ↓
Deploy
```

And potentially:

```
                     Deployment
                         ↓
                     Canary
                    /       \
                   ↓         ↓
              Small %      Existing
                   │
                   ↓
              Evaluation
                   │
              ┌────┴────┐
              ↓         ↓
           Healthy    Degraded
              ↓         ↓
           Expand     Rollback
```

---

## 12. GitOps for AI Platforms

You've already seen GitOps in Kubernetes.

Apply the same principle here.

Instead of manually changing production:

```
Engineer
   ↓
kubectl
   ↓
Production
```

Use:

```
Git
  ↓
CI
  ↓
Artifact / Model
  ↓
GitOps Controller
  ↓
Kubernetes
  ↓
Production
```

The desired state becomes version-controlled.

This gives you:

- auditability
- reproducibility
- rollback
- consistency
- controlled change

---

## 13. Model Deployment Strategies

You don't always replace the existing model immediately.

Several deployment patterns are useful.

### Blue-Green

```
Production
    │
 ┌──┴───┐
 ↓      ↓
Blue   Green
```

Switch traffic when the new version is ready.

### Canary

```
Users
 │
 ├── 95% → Model v1
 │
 └── 5%  → Model v2
```

Observe.

If healthy:

```
5%
  ↓
25%
  ↓
50%
  ↓
100%
```

### Shadow

Send production traffic to the new model without using its responses for users.

```
User
  ↓
Model v1 → User Response

        ↘
          Model v2
          Shadow
```

Useful for evaluating new models against real traffic.

---

## 14. Drift

Traditional ML systems can suffer from data drift.

For example:

```
Training Data
     ↓
Production Data
     ↓
Distribution Changes
     ↓
Model Performance Drops
```

There can also be:

- **Data drift** — Input distribution changes.
- **Concept drift** — Relationship between inputs and outcomes changes.
- **Model drift** — Model behavior or performance changes.

For LLM applications, we also need to think about:

- changing user behavior
- changing document corpus
- changing retrieval quality
- changing model providers
- changing prompts
- changing tool behavior

---

## 15. LLM Evaluation Is Continuous

An LLM application can degrade without any code deployment.

For example:

```
Company Documents
      ↓
Documents Updated
      ↓
Retrieval Changes
      ↓
Answer Quality Changes
```

Or:

```
Model Provider
      ↓
Model Version Changes
      ↓
Output Behavior Changes
```

Therefore:

**AI systems need continuous evaluation, not just deployment-time testing.**

---

## 16. Observability for AI Platforms

We covered observability later in the original roadmap, but it needs to be considered here too.

A platform should expose:

### Infrastructure

- CPU
- memory
- GPU
- network
- storage

### Application

- requests
- errors
- latency

### AI

- tokens
- model
- prompt size
- output size
- retrieval
- tool calls
- agent steps

### Business

- successful tasks
- user feedback
- conversion
- cost per task

Think:

```
Infrastructure
      ↓
Application
      ↓
AI System
      ↓
Business Outcome
```

---

## 17. Feature Stores and ML Platforms

Not every AI workload is an LLM.

Traditional ML applications may need:

```
Data
  ↓
Feature Engineering
  ↓
Feature Store
  ↓
Training
  ↓
Model
  ↓
Inference
```

For example, fraud detection could use features such as:

- transaction frequency
- transaction amount
- account age
- geographic distance

The AI platform should support both:

- Traditional ML
- Generative AI
- Agentic AI

rather than becoming an LLM-only platform.

---

## 18. Self-Service AI Platform

Now imagine you're the architect of an enterprise AI platform.

A developer opens a portal.

They select:

```
Application Type:
[RAG Application]

Model:
[Model X]

Environment:
[Production]

Expected Traffic:
[10 req/sec]

Data:
[Knowledge Base]

Security:
[Enterprise Policy]
```

The platform generates:

- Infrastructure
- Deployment
- Secrets
- Observability
- Evaluation
- Scaling
- Governance

This is the platform engineering vision.

---

## 19. Internal Developer Platform for AI

Conceptually:

```
                Developer
                    │
                    ▼
             AI Developer Portal
                    │
          ┌─────────┼─────────┐
          ↓         ↓         ↓
       Templates  APIs      CLI/SDK
          │         │         │
          └─────────┼─────────┘
                    ↓
               AI Platform
                    │
       ┌────────────┼────────────┐
       ↓            ↓            ↓
     Models        Data       Runtime
       ↓            ↓            ↓
   Registry      Pipelines    K8s/GPU
       │            │            │
       └────────────┼────────────┘
                    ↓
               Production
```

This is where your existing platform-engineering mindset becomes extremely valuable.

---

## 20. AI Platform Control Plane vs Data Plane

This is an important architecture concept.

### Control Plane

Manages:

- models
- deployments
- policies
- configurations
- environments
- evaluations
- users
- access
- governance

### Data Plane

Actually processes:

- user requests
- inference
- retrieval
- tool calls
- model execution

Conceptually:

```
                 AI CONTROL PLANE
     ┌─────────────────────────────────┐
     │ Registry • Policy • Deployment  │
     │ Evaluation • Governance         │
     └───────────────┬─────────────────┘
                     │
                     ▼
                 AI DATA PLANE
     ┌─────────────────────────────────┐
     │ APIs • RAG • Agents • Inference │
     │ Tools • Models • Data           │
     └─────────────────────────────────┘
```

Separating these concerns can make large AI platforms easier to operate.

---

## 21. Our Enterprise AI Platform

Let's evolve our project.

### Previous Architecture

```
Data
  ↓
RAG
  ↓
AI Gateway
  ↓
Model Gateway
  ↓
Inference
  ↓
GPU
```

### Now Introduce the Platform Layer

```
                         Developers
                             │
                             ▼
                    AI Developer Platform
                             │
              ┌──────────────┼──────────────┐
              ↓              ↓              ↓
          Templates        APIs           Portal
              │              │              │
              └──────────────┼──────────────┘
                             ↓
                     AI Control Plane
                             │
       ┌─────────────────────┼─────────────────────┐
       ↓                     ↓                     ↓
 Model Registry        Evaluation Platform    Governance
       │                     │                     │
       └─────────────────────┼─────────────────────┘
                             ↓
                      AI Data Plane
                             │
          ┌──────────────────┼──────────────────┐
          ↓                  ↓                  ↓
         RAG               Agents           Inference
          │                  │                  │
          └──────────────────┼──────────────────┘
                             ↓
                       AI Infrastructure
                             │
                     Kubernetes + GPU
```

Now we're not just building an AI application.

We're designing an AI platform.

---

## 22. Day 06 Hands-On Lab

Today, design the lifecycle of a model or AI application.

Start with:

```
Developer
    ↓
Git Repository
    ↓
CI Pipeline
    ↓
Evaluation
    ↓
Registry
    ↓
Staging
    ↓
Canary
    ↓
Production
    ↓
Monitoring
    ↓
Feedback
```

Then connect it to the infrastructure we designed on Day 04.

---

## 23. Day 06 Exercise

Create a simple AI platform for the Enterprise AI Knowledge Assistant.

It should support:

### Development

```
Git
  ↓
Developer
  ↓
Experiment
Evaluation
Dataset
  ↓
Evaluation
  ↓
Quality Threshold
```

### Registry

```
Model / Prompt / Application
  ↓
Version
  ↓
Approval
```

### Deployment

```
Staging
  ↓
Canary
  ↓
Production
```

### Operations

```
Production
  ↓
Observability
  ↓
Evaluation
  ↓
Feedback
```

---

## 24. Build an AI CI/CD Pipeline

Create a conceptual pipeline:

```
                 Git Push
                    │
                    ▼
               Build/Test
                    │
                    ▼
              Security Scan
                    │
                    ▼
              AI Evaluation
                    │
             ┌──────┴──────┐
             ↓             ↓
           PASS           FAIL
             ↓             ↓
          Registry        Stop
             ↓
           Staging
             ↓
          Canary
             ↓
        Production
```

Add gates for:

- quality
- security
- latency
- cost
- safety

---

## 25. Day 06 Architect Questions

Answer these before moving on:

1. What problem does MLOps solve?
2. How does MLOps differ from traditional DevOps?
3. What additional concerns appear with LLM applications?
4. Why do organizations need an AI platform?
5. What belongs in a model registry?
6. Why is evaluation part of deployment?
7. How can an AI system degrade without code changes?
8. What is model drift?
9. What is data drift?
10. Why use canary deployment for models?
11. What is shadow deployment?
12. What should an AI CI/CD pipeline validate?
13. What is the difference between an AI control plane and data plane?
14. What should developers manage themselves?
15. What should the platform abstract away?
16. How would you support both traditional ML and GenAI?
17. How would you roll back a bad model?
18. How would you know a model is becoming worse in production?

---

## 26. Day 06 Deliverables

Create these artifacts:

### 1. AI Platform Architecture

Show:

- developer experience
- control plane
- data plane
- model registry
- evaluation
- deployment
- infrastructure

### 2. AI CI/CD Pipeline

Document:

```
Code
  → Build
  → Test
  → Evaluate
  → Security
  → Registry
  → Staging
  → Canary
  → Production
```

### 3. Model Lifecycle

Create:

```
Experiment
  → Evaluate
  → Register
  → Approve
  → Deploy
  → Monitor
  → Improve
```

### 4. Platform API

Define conceptually what an internal platform might expose:

```
POST /applications
POST /deployments
POST /evaluations
GET  /models
GET  /deployments/{id}
POST /rollback
```

You don't need to build the complete platform today.

The goal is to think about platform interfaces.

---

## 27. The Architect's Takeaway

The biggest lesson today is:

**AI Platform Engineering is about turning AI infrastructure and operational complexity into reusable capabilities for engineering teams.**

A mature platform should allow developers to focus on:

```
Business Problem
      ↓
AI Application
      ↓
Model / Workflow
```

while the platform handles:

- Infrastructure
- Deployment
- Security
- Evaluation
- Observability
- Scaling
- Governance
- Cost

That is the platform-engineering mindset applied to AI.

---

## Your Progress

We've now moved through the first half of the roadmap:

```
Day 01
Architecture Foundations
        ↓
Day 02
AI/ML & LLM Fundamentals
        ↓
Day 03
LLM Engineering
        ↓
Day 04
AI Infrastructure
        ↓
Day 05
Data Architecture
        ↓
Day 06
MLOps & AI Platform Engineering
```

The next six days shift increasingly toward architecture decisions and production ownership:

- Day 07 → AI System Architecture
- Day 08 → Technology Decisions
- Day 09 → Scale, Reliability & FinOps
- Day 10 → AI Observability
- Day 11 → Security & Governance
- Day 12 → Business Alignment & Portfolio

### The question for tomorrow

So far, we've learned the individual layers.

Now we need to answer:

**How do all these layers become one coherent AI system architecture?**

That's Day 07 → AI System Architecture.
