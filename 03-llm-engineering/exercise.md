# Day 03 — LLM Engineering: Exercise

**Estimated Time**: 3-4 hours total

| Exercise | Task | Time |
|----------|------|------|
| A | Build a RAG pipeline | 60 min |
| B | Add tool calling | 45 min |
| C | Model Gateway abstraction | 40 min |
| D | RAG decision document | 30 min |
| - | Run sample app | 20 min |

## Overview

Today's exercises focus on **RAG implementation**, **tool calling**, and **model gateway abstraction**. You'll build the core components of an LLM application.

---

## Exercise A: Build a RAG Pipeline

### Objective

Implement a working RAG pipeline that retrieves relevant documents and generates answers.

### Architecture

```
Documents → Chunking → Embeddings → Vector DB → Retriever
         → Context → LLM → Answer
```

### Steps

1. **Collect documents** — Gather 5-10 documents (PDFs, markdown, or text files)
2. **Implement chunking** — Split documents into chunks (200-500 tokens each)
3. **Generate embeddings** — Use an embedding model to vectorize chunks
4. **Store in vector DB** — Use ChromaDB, FAISS, or a managed service
5. **Build retrieval** — Implement semantic search with metadata filtering
6. **Assemble context** — Combine retrieved chunks with the user query
7. **Generate answers** — Pass context to LLM and return response

### Measurement Template

For each test query, record:

| Metric | Value |
|--------|-------|
| Query | |
| Retrieved documents | |
| Context size (tokens) | |
| Response quality (1-5) | |
| Latency (ms) | |
| Relevant docs retrieved? | |

### Deliverable

Working RAG prototype with 3 test queries demonstrating retrieval and answer generation.

---

## Exercise B: Add Tool Calling

### Objective

Create one tool the AI can call and demonstrate tool invocation.

### Step 1: Choose a Tool

Pick one:

| Tool | Description | API Required |
|------|-------------|--------------|
| `get_server_status()` | Returns mock server health | None (mock) |
| `search_internal_docs()` | Queries your RAG pipeline | Your RAG system |
| `get_weather()` | Calls a weather API | OpenWeatherMap or similar |
| `lookup_order(order_id)` | Returns order details | Mock database |
| `create_jira_ticket()` | Creates a Jira ticket | Jira API |

### Step 2: Implement the Tool

Your tool must include:

- [ ] Authentication (API key or token)
- [ ] Input validation
- [ ] Error handling
- [ ] Audit logging
- [ ] Rate limiting

### Step 3: Test Tool Invocation

Test with these prompts:

```
1. "What's the status of server web-01?"
2. "Search for our API rate limiting policy"
3. "What's the weather in New York?"
```

### Measurement Template

| Metric | Value |
|--------|-------|
| Tool called | |
| Input parameters | |
| Execution time (ms) | |
| Response correct? | |
| Error handled? | |
| Audit logged? | |

### Deliverable

One working tool with authentication, validation, error handling, and audit logging.

---

## Exercise C: Model Gateway Abstraction

### Objective

Create a simple abstraction that routes requests to different model providers.

### Interface

```python
def generate(prompt: str, model_preference: str = "auto") -> str:
    """
    Generate a response using the appropriate model.
    
    Args:
        prompt: The user prompt
        model_preference: "auto", "fast", "balanced", "powerful"
    
    Returns:
        Generated response string
    """
```

### Steps

1. **Define routing logic:**

```
Request Complexity → Model Selection

Simple (factual, short) → Fast model (GPT-3.5, Claude Haiku)
Normal (analytical) → Balanced model (GPT-4, Claude Sonnet)
Complex (reasoning, code) → Powerful model (GPT-4, Claude Opus)
```

2. **Implement fallback:**

```
Primary provider fails → Try secondary → Try tertiary → Return cached/error
```

3. **Track token usage:**

```python
{
    "model": "gpt-4",
    "input_tokens": 500,
    "output_tokens": 200,
    "latency_ms": 1200,
    "cost_usd": 0.021
}
```

### Measurement Template

| Metric | Value |
|--------|-------|
| Requests routed | |
| Model distribution | |
| Fallback triggered | |
| Average latency | |
| Total tokens used | |
| Total cost | |

### Deliverable

Model Gateway with routing logic, fallback handling, and token tracking.

---

## Exercise D: RAG Decision Document

### Objective

Write a short decision document explaining your RAG architecture choices.

### Template

```
## Why RAG?

[Explain why RAG is appropriate for your use case]

## Architecture Choices

### Chunking Strategy
- Size: [tokens]
- Overlap: [tokens]
- Why: [reasoning]

### Embedding Model
- Model: [name]
- Dimensions: [number]
- Why: [reasoning]

### Vector DB
- Database: [name]
- Index type: [type]
- Why: [reasoning]

### Retrieval Strategy
- Search type: [semantic/hybrid/keyword]
- Top-K: [number]
- Reranking: [yes/no]
- Why: [reasoning]

## What Would Make Me Replace RAG?

- [ ] Fine-tuning (if: behavior needs to change, not knowledge)
- [ ] Direct API (if: data is small and static)
- [ ] Hybrid approach (if: both knowledge and behavior need customization)

## Cost Estimate

- Monthly embedding cost: $[amount]
- Monthly retrieval cost: $[amount]
- Monthly LLM cost: $[amount]
- Total: $[amount]
```

### Deliverable

Completed RAG decision document with your architecture choices justified.

---

## Day 03 Final Deliverables

By the end of Day 03, you should have:

1. **Working RAG Pipeline** (Exercise A)
2. **Tool-Enabled AI Workflow** (Exercise B)
3. **Model Gateway Abstraction** (Exercise C)
4. **RAG Decision Document** (Exercise D)
5. **Sample App Running** (see sample-app/README.md)

### Self-Assessment Questions

Answer these before moving to Day 04:

### RAG
1. When should you use RAG vs fine-tuning?
2. Why is retrieval quality critical for answer quality?
3. Why must RAG respect user permissions?
4. What happens when the vector database is unavailable?

### Context and Tools
5. What is context engineering and why does it matter?
6. Why are tools considered a security boundary?
7. What controls should every tool have?

### Agents
8. When does an application actually need an agent?
9. When does multi-agent architecture add value vs complexity?
10. What is the difference between context and memory?

### Architecture
11. Why do we need an AI Gateway?
12. Why should applications avoid tight coupling to one model provider?
13. What happens if your primary model provider becomes unavailable?
14. When should AI processing be asynchronous?
