# AI/ML — Model Selection Matrix

## Decision framework

| Criteria | Traditional Software | Small ML Model | LLM |
|----------|---------------------|----------------|-----|
| Accuracy | Deterministic | Task-specific | General, variable |
| Latency | Fastest | Fast | Slower |
| Cost | Low compute | Moderate | High (tokens/GPU) |
| Complexity | Low | Moderate | High |
| Privacy | Full control | Full control | Provider-dependent |
| Maintainability | High | Moderate | Low (model changes) |

## When to use an LLM

- Natural language understanding required
- Open-ended generation tasks
- Complex reasoning over unstructured data
- Rapid prototyping needed

## When NOT to use an LLM

- Simple rule-based logic
- Strict latency requirements (<10ms)
- Deterministic output required
- Very limited budget
