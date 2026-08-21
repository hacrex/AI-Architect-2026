# ADR-002: Use Multi-Agent Orchestration for Complex Queries

## Status

Accepted

## Date

2026-08-21

## Context

The Enterprise AI Knowledge Assistant needs to handle different types of queries:

- **Simple**: "What is our vacation policy?" → Direct RAG retrieval
- **Normal**: "How do I request AWS access?" → RAG + step-by-step synthesis
- **Complex**: "Compare our cloud costs this quarter with last quarter and recommend optimizations" → Multiple data sources, analysis, recommendations

We need to decide how to handle complex queries that require:

- Multiple retrieval passes
- Tool invocations (database lookups, API calls)
- Multi-step reasoning
- Cross-domain knowledge synthesis

Options:

1. **Single agent with tools** — One agent handles everything
2. **Multi-agent orchestration** — Specialized agents for different domains
3. **Deterministic pipeline** — Fixed workflow for each query type
4. **Hybrid** — Simple queries skip agents, complex queries use orchestration

## Decision

We will use **hybrid multi-agent orchestration** — simple queries bypass agents entirely, complex queries are routed to a orchestrator that delegates to specialized agents.

## Architecture

```
Query → Complexity Classifier
              │
    ┌─────────┴─────────┐
    ↓                   ↓
 Simple             Complex
    │                   │
    ▼                   ▼
  RAG            Orchestrator
    │              /    |    \
    ▼             ↓     ↓     ↓
  Answer     Research Database Security
               Agent    Agent    Agent
```

## Rationale

### Why Not Single Agent?

- Single agent becomes a bottleneck for complex queries
- No separation of concerns
- Tool authorization harder to manage
- Difficult to optimize individual capabilities

### Why Not Deterministic Pipeline?

- Query patterns change over time
- New tools and data sources added frequently
- Rigid workflows break on edge cases
- No learning from past interactions

### Why Multi-Agent?

| Benefit | Description |
|---------|------------|
| Separation of concerns | Each agent specializes in one domain |
| Independent scaling | Scale research agent separately from database agent |
| Tool isolation | Each agent has minimal required permissions |
| Fault isolation | One agent failure doesn't break the system |
| Testability | Test each agent independently |

### Why Hybrid?

- 80% of queries are simple — agents add unnecessary latency
- Agent orchestration has overhead (500-1000ms)
- Simple queries don't need tool access
- Cost optimization — simple queries use fewer tokens

## Agent Design

### Orchestrator

- Classifies query complexity
- Plans multi-step approach
- Delegates to specialized agents
- Synthesizes results
- Manages shared state

### Research Agent

- Searches internal documentation
- Retrieves relevant policies
- Provides citations
- Tools: `search_docs()`, `get_policy()`

### Database Agent

- Queries order/inventory data
- Calculates metrics
- Generates reports
- Tools: `lookup_order()`, `get_metrics()`, `run_query()`

### Security Agent

- Validates access permissions
- Checks data classification
- Enforces compliance rules
- Tools: `check_permissions()`, `audit_access()`

## Consequences

### Positive

- Clear domain boundaries
- Independent deployment and scaling
- Fine-grained access control per agent
- Easier debugging and monitoring
- Extensible — add new agents without changing existing ones

### Negative

- Increased system complexity
- Agent coordination overhead
- State management across agents
- More failure points
- Harder to test end-to-end

### Risks

| Risk | Mitigation |
|------|-----------|
| Agent timeout | Fallback to single-agent mode |
| Agent error | Retry with exponential backoff |
| State inconsistency | Centralized state store with transactions |
| Orchestrator bottleneck | Horizontal scaling, async processing |

## Performance Targets

| Metric | Simple Query | Complex Query |
|--------|-------------|---------------|
| Latency (p50) | < 1s | < 5s |
| Latency (p99) | < 2s | < 10s |
| Accuracy | > 90% | > 85% |
| Tool invocations | 0 | 2-5 |

## Review Date

2026-11-21 (3 months post-launch)
