# Day 03 — LLM Engineering

## Objective

Learn the architecture patterns behind production LLM applications.

## Core topics

### RAG

Understand the pipeline:

User → Query Processing → Retrieval → Context Assembly → Model → Validation → Response

Study:

- chunking
- embeddings
- retrieval
- reranking
- metadata filtering
- citations
- evaluation

### Tool use

Learn:

- function calling
- structured outputs
- API tools
- permissions
- tool failure handling

### Agents

Understand:

- single-agent systems
- multi-agent systems
- orchestration
- planning
- delegation
- memory
- state

### Model routing

Route requests based on:

- cost
- capability
- latency
- availability
- data sensitivity

### Context engineering

Consider:

- context windows
- memory
- prompt construction
- context compression
- retrieval quality

## Exercise

Design a multi-agent customer-support system.

Include:

- user interface
- API gateway
- agent orchestrator
- specialized agents
- knowledge base
- vector database
- model gateway
- state store
- observability
- human escalation

Document what happens when one agent fails.

## Deliverable

Architecture diagram + failure-flow diagram.
