# Scale & FinOps — Cost Model

## Cost components

| Component | Unit | Cost Driver | Estimated Monthly |
|-----------|------|-------------|-------------------|
| LLM API calls | Per 1M tokens | Token volume | $____ |
| Embedding generation | Per 1M tokens | Document volume | $____ |
| Vector database | Per GB stored | Data volume | $____ |
| GPU compute | Per hour | Inference load | $____ |
| Storage | Per GB | Documents + logs | $____ |
| Networking | Per GB egress | API traffic | $____ |
| Monitoring | Per series | Metrics volume | $____ |

## Scaling cost projection

| Traffic Level | Requests/day | Token volume | Monthly cost |
|--------------|--------------|--------------|--------------|
| Baseline | 10K | 10M | $____ |
| 3x growth | 30K | 30M | $____ |
| 10x growth | 100K | 100M | $____ |

## Cost optimization levers

1. **Semantic caching** — Reduce repeat queries by 30-60%
2. **Model routing** — Use cheaper models for simple tasks
3. **Prompt optimization** — Reduce tokens per request
4. **Batch processing** — Amortize fixed costs
5. **Reserved capacity** — Commit for discounts
