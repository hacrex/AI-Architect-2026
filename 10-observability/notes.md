# Day 10 → AI Observability

## The Final Three Days

We are now entering the final three days of the 12-day journey.

So far, we've built the architecture layer by layer:

- Day 01 → Architecture Foundations
- Day 02 → AI/ML & LLM Fundamentals
- Day 03 → LLM Engineering
- Day 04 → AI Infrastructure
- Day 05 → Data Architecture
- Day 06 → MLOps & AI Platform Engineering
- Day 07 → AI System Architecture
- Day 08 → Technology Decisions
- Day 09 → Scale, Reliability & AI FinOps

Today we answer a different question:

**How do you know what your AI system is actually doing in production?**

A traditional application might be observable through:

- Metrics
- Logs
- Traces

An AI system needs those too.

But they aren't enough.

You also need visibility into:

- Model behavior
- Token consumption
- Retrieval
- Prompts
- Responses
- Tool calls
- Agent workflows
- Evaluation
- Quality
- Cost

The source material reinforces the importance of continuous model performance tracking, versioning, evaluation, and drift monitoring rather than treating AI monitoring as a one-time deployment activity.

---

## 1. What Is AI Observability?

At a high level:

> Observability is the ability to understand the internal state and behavior of a system from the information it produces.

For a traditional application:

```
Request
   ↓
Service
   ↓
Database
   ↓
Response
```

You might observe:

- Latency
- Errors
- CPU
- Memory
- Logs

For an AI application:

```
User
 ↓
Gateway
 ↓
RAG
 ↓
Retriever
 ↓
Tools
 ↓
Model
 ↓
Response
```

Now we need to understand:

- Which model?
- Which prompt?
- Which documents?
- Which chunks?
- Which tools?
- How many tokens?
- How long did inference take?
- Why did retrieval fail?
- Why did the model produce this answer?
- What did it cost?
- Was the answer actually useful?

That is AI observability.

---

## 2. The Three Traditional Pillars

Start with the fundamentals.

### Metrics

Numerical measurements over time.

Examples:

- Request Rate
- Error Rate
- Latency
- CPU
- Memory
- GPU Utilization
- Queue Depth

### Logs

Discrete events.

For example:

```
2026-08-25 17:10:22
Model request failed
provider=primary
status=429
```

Logs tell you:

**What happened?**

### Traces

A trace follows a request across multiple components.

```
Request
 │
 ├── API Gateway
 │
 ├── AI Gateway
 │
 ├── Retriever
 │
 ├── Vector DB
 │
 ├── Model Gateway
 │
 └── LLM
```

Traces tell you:

**Where did the request spend its time and where did it fail?**

---

## 3. Why Traditional Observability Isn't Enough

Imagine your application reports:

```
HTTP 200
Latency: 2.4 seconds
```

Everything looks healthy.

But the user receives:

> "I couldn't find any information."

The infrastructure is healthy.

The application is healthy.

But the AI system failed.

Why?

Possibilities:

```
Retriever returned poor documents
        ↓
Context was irrelevant
        ↓
LLM had insufficient information
        ↓
Poor answer
```

Traditional infrastructure metrics didn't necessarily tell you that.

This is the fundamental difference:

> **Infrastructure health does not equal AI quality.**

---

## 4. AI Observability Layers

Think of observability as multiple layers:

```
┌──────────────────────────────┐
│       Business Outcome       │
├──────────────────────────────┤
│        AI Quality            │
├──────────────────────────────┤
│       Model Behavior         │
├──────────────────────────────┤
│     AI Workflow / Trace      │
├──────────────────────────────┤
│      Application Layer       │
├──────────────────────────────┤
│    Infrastructure Layer      │
└──────────────────────────────┘
```

You need visibility across the entire stack.

---

## 5. Infrastructure Observability

Start with what you already know from Cloud and Platform Engineering.

Monitor:

- CPU
- Memory
- GPU
- Disk
- Network
- Pod Health
- Node Health
- Container Restarts

For AI infrastructure, GPU metrics become particularly important.

For example:

- GPU Utilization
- GPU Memory
- GPU Temperature
- GPU Power
- Inference Throughput
- Queue Depth

But remember:

> High GPU utilization doesn't necessarily mean a healthy AI system.

You could have:

```
GPU = 99%
Latency = 30 seconds
Errors = increasing
```

That's not success.

---

## 6. Application Metrics

Now move one layer up.

Track:

- Requests/sec
- Errors/sec
- Success Rate
- P50 Latency
- P95 Latency
- P99 Latency
- Timeouts
- Retries
- Queue Time

For example:

```
P50 = 1.2 sec
P95 = 4.8 sec
P99 = 11.2 sec
```

The average latency might look acceptable while a meaningful percentage of users are experiencing very slow responses.

This is why percentile-based metrics matter.

---

## 7. AI-Specific Metrics

Now the interesting part.

Track:

- Input Tokens
- Output Tokens
- Total Tokens
- Time to First Token
- Tokens/sec
- Model Latency
- Model Errors
- Model Provider
- Model Version

A request might look like:

```
Model:
Model-A

Input:
4,210 tokens

Output:
812 tokens

TTFT:
0.9 sec

Total:
3.4 sec

Cost:
$0.XX
```

Now you can connect:

```
Performance
+
Usage
+
Cost
```

---

## 8. Token Observability

Tokens aren't just a billing metric.

They affect:

- Cost
- Latency
- Context Size
- Throughput

Consider:

```
Request A
Input: 1,000 tokens

Request B
Input: 20,000 tokens
```

The second request may consume significantly more resources.

Therefore dashboards should allow you to see:

- Tokens / Request
- Tokens / User
- Tokens / Application
- Tokens / Model
- Tokens / Tenant
- Tokens / Day

This connects directly to the FinOps architecture from Day 09.

---

## 9. LLM Tracing

Now imagine one request:

> "Explain our production incident and tell me what action I should take."

The system might execute:

```
Request
  ↓
Authentication
  ↓
Intent Detection
  ↓
Vector Search
  ↓
Metadata Filtering
  ↓
Reranking
  ↓
Context Assembly
  ↓
LLM
  ↓
Tool Call
  ↓
LLM
  ↓
Response
```

A normal application trace may show:

```
HTTP 200
2.7 sec
```

An AI trace should show the entire chain.

```
Trace #84291
│
├── Retrieval: 320 ms
├── Reranking: 180 ms
├── Model Call #1: 1.1 sec
├── Tool Call: 540 ms
└── Model Call #2: 610 ms
```

Now debugging becomes much easier.

---

## 10. RAG Observability

This is particularly important for the system we've been building.

A RAG request should expose:

```
User Query
    ↓
Query Transformation
    ↓
Embedding
    ↓
Retrieval
    ↓
Retrieved Documents
    ↓
Filtering
    ↓
Reranking
    ↓
Context
    ↓
LLM
```

You want to answer:

- Did retrieval happen?
- How many documents were retrieved?
- Which documents were retrieved?
- Were they authorized?
- How relevant were they?
- How much context reached the model?
- Did the model actually use the retrieved information?

---

## 11. Retrieval Quality

Suppose users complain:

> "The AI keeps giving bad answers."

Don't immediately blame the LLM.

Check:

```
Question
 ↓
Retrieved Documents
```

Maybe the actual problem is:

```
Relevant Document:
Rank 42

while the system only retrieves:

Top 5
```

The model never received the correct information.

Therefore:

> **A bad AI answer can be a retrieval problem rather than a model problem.**

This is why RAG evaluation and continuous monitoring matter. The source material explicitly identifies performance tracking and drift monitoring as part of ongoing model management.

---

## 12. Agent Observability

Agents make observability considerably harder.

Imagine:

```
User
 ↓
Agent
 ├── Search Tool
 ├── Database Tool
 ├── API Tool
 ├── Calculator
 └── Another Model
```

The agent may take multiple steps.

You need to see:

```
Agent Run #9281

Step 1
Reason / Decision
 ↓
Search Tool

Step 2
Tool Result
 ↓
Database Query

Step 3
Decision
 ↓
Model Call

Step 4
Final Response
```

Now ask:

> Why did the agent take seven steps when three were enough?

That is an observability problem.

---

## 13. Agent Failure Modes

Agents can fail in ways traditional APIs don't.

For example:

```
Agent
 ↓
Tool A
 ↓
Tool B
 ↓
Tool A again
 ↓
Tool B again
 ↓
Loop
```

Without proper tracing:

> "The request is slow."

With tracing:

```
Agent Loop Detected
12 tool calls
Same operation repeated 6 times
```

Now you have something actionable.

---

## 14. Model Behavior Observability

Infrastructure metrics don't tell you whether model behavior changed.

Imagine:

```
Model v1
Answer Quality = 91%

Model v2
Answer Quality = 82%
```

Everything else looks healthy.

```
CPU ✓
GPU ✓
Latency ✓
Errors ✓
Availability ✓
```

Yet the AI became worse.

This is why AI systems need quality telemetry alongside infrastructure telemetry.

---

## 15. Continuous Evaluation

This connects Day 06 and Day 10.

Evaluation shouldn't happen only before deployment.

Think:

```
Deploy
  ↓
Monitor
  ↓
Evaluate
  ↓
Detect Change
  ↓
Investigate
  ↓
Improve
```

For example:

```
Every Day

1000 evaluation samples
        ↓
Quality Score
        ↓
Compare with baseline
        ↓
Alert if degradation
```

This turns evaluation into an operational capability.

---

## 16. Drift Monitoring

Drift can occur when the environment changes.

For example:

```
Documents Change
       ↓
Retrieval Distribution Changes
       ↓
Context Changes
       ↓
Answer Quality Changes
```

Or:

```
Model Provider
       ↓
Model Version Changes
       ↓
Behavior Changes
```

Or:

```
Users
       ↓
New Usage Patterns
       ↓
New Queries
       ↓
Previously unseen Edge Cases
```

Monitoring needs to detect meaningful changes.

The source material explicitly identifies drift monitoring as part of model management.

---

## 17. SLI, SLO and SLA

Now connect AI observability with SRE.

### SLI

**Service Level Indicator**

What you measure.

Example:

- Successful AI requests

### SLO

**Service Level Objective**

What you target.

Example:

- 99.5% successful requests

### SLA

**Service Level Agreement**

What you formally promise to customers.

Example:

- 99.9% availability

The architecture should distinguish these.

---

## 18. AI SLOs

Traditional:

- Availability
- Latency
- Error Rate

AI systems can additionally define:

- TTFT
- Completion Latency
- Task Success
- Retrieval Success
- Groundedness
- Tool Success
- Evaluation Score

For example:

```
SLO

Availability:
99.9%

P95 Latency:
< 5 sec

Task Success:
> 90%

Grounded Responses:
> 95%
```

Now the AI platform has measurable reliability and quality targets.

---

## 19. Alerts

Don't alert on everything.

A bad alert:

```
GPU utilization > 80%
```

This might be completely normal.

A better alert could be:

```
GPU utilization > 90%
AND
P95 latency increasing
AND
queue depth increasing
```

Now the alert represents a meaningful system condition.

Similarly:

```
Retrieval relevance ↓
+
Answer quality ↓
```

could indicate a data or retrieval problem.

---

## 20. Observability Correlation

One of the most powerful concepts is correlation.

Suppose:

```
Monday
Model v2 deployed

Then:

Tuesday
Token usage ↑ 25%
Latency ↑ 15%
Cost ↑ 30%
Quality ↓ 8%
```

A good observability platform lets you correlate these events.

```
Deployment
   ↓
Model Version
   ↓
Behavior Change
   ↓
Operational Impact
   ↓
Business Impact
```

Now your telemetry becomes useful for architecture decisions.

---

## 21. AI Observability Dashboard

Imagine your production dashboard.

```
Infrastructure
GPU Utilization
CPU
Memory
Network

Application
Requests
Errors
Latency
Throughput

AI
Tokens
Model Calls
TTFT
Inference Latency

Retrieval
Tool Calls

Quality
Task Success
Groundedness
Relevance
Evaluation Score

Cost
Spend
Cost / Request
Cost / Task
Cost / Model
```

The goal is not to create a dashboard with 200 graphs.

The goal is to answer:

> "Is the system healthy, and if not, where is the problem?"

---

## 22. Observability for the Enterprise AI Platform

Let's extend our architecture again.

```
                         AI Platform
                              │
                    ┌─────────┴─────────┐
                    ↓                   ↓
                AI System          Data Platform
                    │                   │
        ┌───────────┼───────────┐       │
        ↓           ↓           ↓       ↓
       RAG        Agents     Models   Storage
        │           │           │
        └───────────┼───────────┘
                    ↓
              Observability
                    │
      ┌─────────────┼─────────────┐
      ↓             ↓             ↓
   Metrics         Logs         Traces
      │             │             │
      └─────────────┼─────────────┘
                    ↓
             AI Telemetry
                    │
       ┌────────────┼─────────────┐
       ↓            ↓             ↓
    Quality        Cost        Reliability
```

This becomes the operational nervous system of the platform.

---

## 23. Day 10 Hands-On Lab

Take the Enterprise AI Knowledge Platform we've been designing.

Add observability to every major component.

```
User
 ↓
API Gateway
 ↓
AI Gateway
 ↓
RAG / Agent
 ↓
Model Gateway
 ↓
Inference
 ↓
GPU
```

For each layer define:

- Metrics
- Logs
- Traces
- Alerts
- SLO

---

## 24. Build an AI Trace

Create one representative request:

> "Explain our incident response policy."

Trace:

```
Trace
│
├── Authentication
│
├── Query Processing
│
├── Embedding
│
├── Vector Search
│
├── Metadata Filtering
│
├── Reranking
│
├── Context Assembly
│
├── Model Request
│
└── Response
```

Record:

- Latency
- Tokens
- Retrieved Documents
- Model
- Cost
- Result

---

## 25. Day 10 Failure Investigation

Take this hypothetical incident:

Users report:

> "AI answers became worse."

Don't immediately change the model.

Investigate:

**Step 1**

Check availability.

```
Healthy
```

**Step 2**

Check latency.

```
Healthy
```

**Step 3**

Check model errors.

```
Healthy
```

**Step 4**

Check retrieval.

```
Relevance ↓
```

**Step 5**

Check document pipeline.

```
New document parser deployed
```

**Step 6**

Compare document chunks.

```
Chunk quality degraded
```

**Root cause:**

```
Data ingestion change → retrieval degradation → AI quality degradation
```

This is exactly why AI observability needs to cross system boundaries.

---

## 26. Day 10 Architect Exercise

Design an observability strategy for:

- 100,000 users
- 10,000,000 AI requests/month
- Multiple models
- RAG
- Agents
- GPU inference
- Managed model fallback

Define:

### Infrastructure telemetry

What do you measure?

### AI telemetry

What do you measure?

### Quality telemetry

What do you measure?

### Cost telemetry

What do you measure?

### Security telemetry

What do you measure?

### Alerting

What conditions require immediate action?

---

## 27. Day 10 Architect Questions

Answer these before moving on:

1. What are the three traditional pillars of observability?
2. Why aren't infrastructure metrics enough for AI?
3. What AI-specific metrics should be tracked?
4. What is TTFT?
5. Why is token usage an observability concern?
6. What should an LLM trace contain?
7. How do you observe RAG retrieval quality?
8. How do you trace an agent workflow?
9. What is drift?
10. Why is continuous evaluation important?
11. What are SLI, SLO and SLA?
12. Which AI-specific SLOs would you define?
13. What makes a good AI alert?
14. How can you correlate a model deployment with quality degradation?
15. How would you investigate an AI system whose infrastructure looks healthy but answers are getting worse?

---

## 28. Day 10 Deliverables

Create:

### 1. AI Observability Architecture

Show:

- Metrics
- Logs
- Traces
- AI Telemetry
- Evaluation
- Alerts
- Dashboards

### 2. AI Trace

Document one complete request.

### 3. SLO Definition

Define at least:

- Availability
- Latency
- Task Success
- AI Quality

### 4. Production Dashboard Design

Include:

- Infrastructure
- Application
- AI
- Quality
- Cost

### 5. Incident Runbook

Create a runbook for:

**AI response quality suddenly drops**

Include:

```
Detection
  ↓
Investigation
  ↓
Trace
  ↓
Retrieval Check
  ↓
Model Check
  ↓
Data Check
  ↓
Mitigation
  ↓
Recovery
```

---

## 29. The Architect's Takeaway

The most important lesson today is:

> **If you cannot observe an AI system, you cannot reliably operate it.**

And observability isn't simply:

```
CPU
Memory
GPU
```

A production AI architect needs visibility into:

```
Infrastructure
      ↓
Application
      ↓
AI Workflow
      ↓
Retrieval
      ↓
Model
      ↓
Quality
      ↓
Cost
      ↓
Business Outcome
```

The source material also emphasizes that AI systems require ongoing performance tracking, versioning, evaluation, and drift monitoring.

The goal is to move from:

> "The API is healthy."

to:

> "The AI system is healthy, the answers are meeting our quality targets, the system is operating within its SLOs, and we know what is driving its cost."

That's a much higher standard.

---

## Your Progress

```
Day 01 → Architecture Foundations
Day 02 → AI/ML & LLM Fundamentals
Day 03 → LLM Engineering
Day 04 → AI Infrastructure
Day 05 → Data Architecture
Day 06 → MLOps & AI Platform Engineering
Day 07 → AI System Architecture
Day 08 → Technology Decisions
Day 09 → Scale, Reliability & AI FinOps
Day 10 → AI Observability
```

Only two days remain.

- Day 11 → AI Security & Governance
- Day 12 → Business Alignment & AI Architecture Portfolio
