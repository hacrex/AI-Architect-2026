# Capstone — Cost Model

## Monthly Cost Breakdown

| Component | Unit Cost | Volume | Monthly Cost |
|-----------|-----------|--------|--------------|
| LLM API — GPT-4o (primary) | $2.50/1M input, $10/1M output | 50M input, 10M output | $225,000 |
| LLM API — Claude (fallback) | $3/1M input, $15/1M output | 10M input, 2M output | $60,000 |
| Embedding API | $0.13/1M tokens | 100M tokens | $13,000 |
| GPU — Self-hosted (Llama 70B) | $3.50/hr × 24hr × 30 days | 2 × A100 | $5,040 |
| Vector DB (Qdrant) | Self-hosted on Kubernetes | - | $2,000 |
| PostgreSQL (RDS) | db.r6g.xlarge, Multi-AZ | - | $3,500 |
| Redis (ElastiCache) | cache.r6g.large, cluster | - | $2,400 |
| Kubernetes (EKS) | 8 nodes (m6i.xlarge) | - | $8,000 |
| Application compute | FastAPI, workers | - | $4,000 |
| S3 storage | 500GB documents | - | $12 |
| Monitoring (Prometheus + Grafana) | Self-hosted | - | $1,500 |
| Observability (OpenTelemetry) | Collector + storage | - | $2,000 |
| Security (Vault, cert-manager) | Self-hosted | - | $1,000 |
| **Total** | | | **$327,552** |

## Cost Per Request

| Metric | Value |
|--------|-------|
| Average input tokens per request | 800 |
| Average output tokens per request | 300 |
| Average cost per request (managed) | $0.005 |
| Average cost per request (self-hosted) | $0.001 |
| Weighted average (80% managed, 20% self-hosted) | $0.0042 |
| Requests per day | 50,000 |
| Daily cost | $210 |
| Monthly cost (model only) | $6,300 |

*Note: Total monthly cost includes infrastructure, engineering, operations. Model cost is ~40% of total.*

## Cost Optimization

| Lever | Implementation | Expected Savings |
|-------|---------------|------------------|
| Semantic caching | Redis embedding similarity | 30-40% on model costs |
| Model routing | Simple → self-hosted, complex → managed | 20-25% on model costs |
| Prompt optimization | Reduce context window usage | 10-15% on model costs |
| Batch processing | Off-peak inference for non-urgent | 5-10% on GPU costs |

### Optimized Cost After Savings

| Lever | Savings |
|-------|---------|
| Semantic cache (35% hit rate) | -$78,750 |
| Model routing (20% to self-hosted) | -$37,500 |
| Prompt optimization | -$18,750 |
| **Optimized monthly total** | **$192,552** |

## Scaling Projection

| Growth | Users | Requests/day | Monthly Cost | Cost/User |
|--------|-------|--------------|--------------|-----------|
| Current | 10,000 | 50,000 | $192,552 | $19.26 |
| 2x | 20,000 | 100,000 | $310,000 | $15.50 |
| 5x | 50,000 | 250,000 | $650,000 | $13.00 |
| 10x | 100,000 | 500,000 | $1,100,000 | $11.00 |

*Note: Cost per user decreases with scale due to fixed costs being spread across more users.*

## Break-Even Analysis

| Approach | Fixed Cost/mo | Variable Cost/request | Break-Even (requests/mo) |
|----------|--------------|----------------------|--------------------------|
| All managed | $0 | $0.005 | N/A |
| All self-hosted | $15,000 | $0.001 | 3,750,000 |
| Hybrid (recommended) | $7,500 | $0.003 | 1,250,000 |

Current volume: 1,500,000 requests/month → Hybrid is optimal.

## Annual Budget Summary

| Category | Annual Cost | % of Total |
|----------|-------------|------------|
| Model inference | $225,000 | 31% |
| Infrastructure | $195,000 | 27% |
| Engineering team | $200,000 | 27% |
| Operations | $60,000 | 8% |
| Security & compliance | $30,000 | 4% |
| Observability | $15,000 | 2% |
| **Total** | **$725,000** | **100%** |
