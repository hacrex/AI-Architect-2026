# Day 02 — AI/ML & LLM Fundamentals: Exercise

**Estimated Time**: 3-4 hours total

| Exercise | Task | Time |
|----------|------|------|
| A | Model comparison lab | 45 min |
| B | Do we need an LLM? | 20 min |
| C | RAG vs fine-tuning decision | 25 min |
| D | Model routing strategy | 40 min |
| E | Model evaluation framework | 30 min |
| - | Run sample app | 20 min |

## Overview

Today's exercises focus on **model comparison**, **architecture trade-offs**, and **model routing**. You'll experiment with different models and build a model routing strategy.

---

## Exercise A: Model Comparison Lab

### Objective

Compare two LLMs across quality, latency, token usage, and cost to understand architecture trade-offs.

### Setup

You need:

- Two different LLM APIs (e.g., GPT-4 vs GPT-3.5-turbo, or Claude vs a smaller model)
- A set of test prompts representing different complexity levels
- A way to measure latency and token usage

### Test Prompts

Create three categories:

#### Simple Prompts
```
1. "What is 2 + 2?"
2. "What color is the sky?"
3. "Define 'API' in one sentence."
```

#### Normal Prompts
```
1. "Explain the difference between REST and GraphQL."
2. "What are three best practices for API design?"
3. "Summarize the concept of microservices architecture."
```

#### Complex Prompts
```
1. "Compare and contrast horizontal vs vertical scaling for a cloud-native application handling 10,000 requests per second. Consider cost, latency, and operational complexity."
2. "Design a data pipeline architecture for real-time analytics on 5TB of daily event data. Explain your technology choices and trade-offs."
3. "Analyze the security implications of using LLMs in an enterprise setting. What are the risks, mitigations, and architectural patterns to address them?"
```

### Measurement Template

For each prompt, record:

| Metric | Model A | Model B |
|--------|---------|---------|
| Model Name | | |
| Response Quality (1-5) | | |
| Latency (ms) | | |
| Input Tokens | | |
| Output Tokens | | |
| Cost (estimated) | | |
| Context Handling | | |

### Quality Rating Guide

- **5**: Excellent — accurate, complete, well-structured
- **4**: Good — mostly accurate, minor gaps
- **3**: Acceptable — core answer present, some issues
- **2**: Poor — partial answer, significant gaps
- **1**: Bad — inaccurate or irrelevant

### Deliverable

Fill out the comparison table and write a 1-paragraph recommendation:

> "For the Enterprise AI Knowledge Assistant, I recommend Model X because..."

---

## Exercise B: Do We Need an LLM?

### Objective

For each scenario below, decide:

1. Is an LLM the right choice?
2. What alternative could work?
3. What are the trade-offs?

### Scenarios

| # | Scenario | LLM Needed? | Alternative | Why? |
|---|----------|-------------|-------------|------|
| 1 | Calculate monthly salary from hours worked | | | |
| 2 | Classify support tickets into categories | | | |
| 3 | Answer questions about company policies | | | |
| 4 | Detect fraud in transaction data | | | |
| 5 | Generate personalized email responses | | | |
| 6 | Translate text between 5 languages | | | |
| 7 | Summarize 100-page legal documents | | | |
| 8 | Predict server failure from metrics | | | |
| 9 | Explain code to a junior developer | | | |
| 10 | Run SQL queries on a database | | | |

### Deliverable

Complete the table with your decisions and reasoning.

---

## Exercise C: RAG vs Fine-Tuning Decision

### Objective

For each problem statement, decide whether RAG, fine-tuning, or both is appropriate.

### Problem Statements

| # | Problem | RAG | Fine-Tuning | Both | Why? |
|---|---------|-----|-------------|------|------|
| 1 | "The model doesn't know our latest product docs" | | | | |
| 2 | "We need the model to always respond in our brand voice" | | | | |
| 3 | "Our knowledge base updates daily" | | | | |
| 4 | "The model needs to understand our proprietary data format" | | | | |
| 5 | "We need citations from internal documents" | | | | |
| 6 | "The model should follow our specific output template" | | | | |
| 7 | "Legal requirements demand data stays in our infrastructure" | | | | |
| 8 | "We need to reduce hallucinations about our products" | | | | |

### Decision Framework

Ask yourself:

1. **Is the problem about KNOWLEDGE?** → RAG
   - "The model doesn't know X"
   - "We need to reference Y"
   - "Information changes frequently"

2. **Is the problem about BEHAVIOR?** → Fine-tuning
   - "The model should always do X"
   - "We need consistent output format Y"
   - "The model should follow style Z"

3. **Is it both?** → Consider both, start with RAG

### Deliverable

Complete the table and explain your reasoning for the first 3 scenarios.

---

## Exercise D: Model Routing Strategy

### Objective

Design a model routing strategy for the Enterprise AI Knowledge Assistant.

### Step 1: Define Request Categories

Classify these user requests into Simple, Normal, or Complex:

| Request | Category | Why? |
|---------|----------|------|
| "What's the company holiday schedule?" | | |
| "Explain our data retention policy and how it applies to customer data in the EU" | | |
| "What is 15% of 2400?" | | |
| "Compare our current cloud architecture with a serverless approach, considering cost, scalability, and operational overhead" | | |
| "How do I reset my password?" | | |
| "Design a disaster recovery strategy for our multi-region deployment" | | |
| "What's the WiFi password for the office?" | | |
| "Analyze the security implications of our authentication system and recommend improvements" | | |

### Step 2: Map Categories to Models

Design your routing:

```
Simple Requests → Model: ___________
  - Latency target: ___________
  - Cost per 1K tokens: $___________

Normal Requests → Model: ___________
  - Latency target: ___________
  - Cost per 1K tokens: $___________

Complex Requests → Model: ___________
  - Latency target: ___________
  - Cost per 1K tokens: $___________
```

### Step 3: Estimate Monthly Cost

Assume:

- 10,000 requests/month
- Distribution: 50% simple, 35% normal, 15% complex
- Average input tokens: 200 (simple), 500 (normal), 1500 (complex)
- Average output tokens: 100 (simple), 300 (normal), 800 (complex)

Calculate:

| Category | Requests | Input Tokens | Output Tokens | Model Cost |
|----------|----------|--------------|---------------|------------|
| Simple | | | | |
| Normal | | | | |
| Complex | | | | |
| **Total** | | | | |

### Deliverable

Complete all three steps and compare your total cost with a single-model approach.

---

## Exercise E: Model Evaluation Framework

### Objective

Create a model evaluation framework for your organization.

### Step 1: Define Evaluation Criteria

For each criterion, rate its importance (1-5) for your use case:

| Criterion | Importance (1-5) | Notes |
|-----------|-------------------|-------|
| Response Quality | | |
| Latency | | |
| Cost | | |
| Context Window Size | | |
| Privacy/Security | | |
| Reliability/Uptime | | |
| Scalability | | |
| Vendor Support | | |
| Ease of Integration | | |

### Step 2: Create a Scoring Rubric

For your top 3 criteria, define what a score of 1, 3, and 5 looks like.

### Step 3: Evaluate Two Models

Use your framework to evaluate two different models.

| Criterion | Weight | Model A Score | Model A Weighted | Model B Score | Model B Weighted |
|-----------|--------|---------------|------------------|---------------|------------------|
| | | | | | |

### Deliverable

Your completed evaluation framework and model comparison.

---

## Day 02 Final Deliverables

By the end of Day 02, you should have:

1. **Model Comparison Table** (Exercise A)
2. **LLM Necessity Decisions** (Exercise B)
3. **RAG vs Fine-Tuning Analysis** (Exercise C)
4. **Model Routing Strategy** (Exercise D)
5. **Model Evaluation Framework** (Exercise E)
6. **Sample App Running** (see sample-app/README.md)

### Self-Assessment Questions

Answer these before moving to Day 03:

1. Why don't all AI applications need an LLM?
2. What is the difference between training and inference?
3. Why do tokens matter for cost?
4. Why does context length matter?
5. What are embeddings?
6. Why do we need vector search?
7. When would you choose RAG over fine-tuning?
8. Why might a smaller model be preferable?
9. When would you self-host an open-weight model?
10. When would you use a managed model?
11. What happens to architecture when inference traffic increases 10x?
12. Why should an enterprise consider a model gateway?
