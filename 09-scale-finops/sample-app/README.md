# Scale, Reliability & AI FinOps — Sample App

A working prototype demonstrating **horizontal scaling, reliability patterns, semantic caching, fallback routing, circuit breakers, rate limiting, AI cost tracking (FinOps), and capacity planning** from Day 09.

> **Building on Day 08**: This app takes the technology decisions and adds operational awareness — scaling, reliability, and cost optimization as architecture concerns.

## Architecture

```
                         USERS
                           │
                           ▼
                    ┌─────────────┐
                    │  FastAPI    │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ Rate Limiter│
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Semantic  │◄──── Cache Hit → Return
                    │    Cache    │
                    └──────┬──────┘
                           │ Cache Miss
                           ▼
                    ┌─────────────┐
                    │  Circuit    │──── Open → Fallback
                    │  Breaker    │
                    └──────┬──────┘
                           │ Closed
                           ▼
                    ┌─────────────┐
                    │  Fallback   │
                    │   Router    │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
           Primary     Secondary    Fallback
           (OpenAI)   (Anthropic)  (Self-Hosted)
                           │
                           ▼
                    ┌─────────────┐
                    │    Cost     │
                    │   Tracker   │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  Capacity   │
                    │   Planner   │
                    └─────────────┘
```

## Project Structure

```
sample-app/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application
│   ├── models.py                  # Pydantic models
│   ├── semantic_cache.py          # Meaning-based response caching
│   ├── fallback_router.py         # Multi-provider failover chain
│   ├── circuit_breaker.py         # Cascading failure protection
│   ├── rate_limiter.py            # Token bucket rate limiting
│   ├── cost_tracker.py            # AI FinOps cost monitoring
│   └── capacity_planner.py        # Infrastructure capacity estimation
├── config/
│   ├── settings.py                # Configuration
│   └── .env.example               # Environment template
├── pipelines/
│   ├── __init__.py
│   └── scale_pipeline.py          # End-to-end scaling workflow
├── scripts/
│   ├── status.py                  # View full system status
│   ├── simulate.py                # Traffic simulation
│   └── cost_report.py             # Cost analysis report
├── requirements.txt
└── test_system.py                 # Test all components
```

## Quick Start

```bash
# 1. Navigate to sample-app
cd 09-scale-finops/sample-app

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the API
uvicorn app.main:app --reload --port 8090

# 5. Open API docs
# http://localhost:8090/docs
```

## Core Components

### 1. Semantic Cache

Meaning-based response reuse — queries are matched by semantic similarity, not exact string match:

```python
from app.semantic_cache import SemanticCache

cache = SemanticCache(similarity_threshold=0.92)
cache.put("How do I deploy Kubernetes?", "Deploy with kubectl", 500)

# Exact match
result = cache.get("How do I deploy Kubernetes?")

# Similar meaning — still hits!
result = cache.get("What are the steps to deploy a Kubernetes cluster?")
```

### 2. Fallback Router

Multi-provider failover with timeout-based routing:

```python
from app.fallback_router import FallbackRouter
from app.models import FallbackRoute, ModelProvider

router = FallbackRouter(timeout_seconds=5.0)
router.add_route(FallbackRoute(
    id="r1", name="Primary", provider=ModelProvider.OPENAI,
    model="gpt-4o", priority=0
))
router.add_route(FallbackRoute(
    id="r2", name="Fallback", provider=ModelProvider.ANTHROPIC,
    model="claude-3-sonnet", priority=1
))

result = router.route_request("user query")
```

### 3. Circuit Breaker

Prevent cascading failures with state-based protection:

```python
from app.circuit_breaker import CircuitBreaker

cb = CircuitBreaker("openai", failure_threshold=5, recovery_timeout=30)

result = cb.execute(some_function, arg1, arg2)
if result["fallback_needed"]:
    # Use fallback provider
    pass
```

### 4. Cost Tracker (FinOps)

AI-specific cost monitoring:

```python
from app.cost_tracker import CostTracker
from app.models import ModelProvider

tracker = CostTracker()
tracker.record_request(
    provider=ModelProvider.OPENAI, model="gpt-4o",
    input_tokens=2000, output_tokens=500
)

summary = tracker.get_summary("month")
budget = tracker.check_budget()
```

### 5. Capacity Planner

Infrastructure capacity estimation and bottleneck detection:

```python
from app.capacity_planner import CapacityPlanner

planner = CapacityPlanner()
layers = planner.estimate_capacity(scale_factor=10.0)
bottleneck = planner.find_bottleneck(scale_factor=10.0)
plan = planner.create_scale_plan("10x Growth", 10.0)
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | System health check |
| GET | /cache/stats | Cache hit rate and savings |
| GET | /cache/entries | List cached entries |
| POST | /cache/put | Store a cache entry |
| POST | /cache/invalidate | Invalidate cache entries |
| GET | /fallback/routes | List fallback routes |
| GET | /fallback/stats | Fallback routing statistics |
| POST | /fallback/route | Route a request through fallback chain |
| POST | /fallback/disable/{id} | Disable a fallback route |
| POST | /fallback/enable/{id} | Enable a fallback route |
| GET | /circuit-breakers | Circuit breaker states |
| POST | /circuit-breakers/{name}/reset | Reset a circuit breaker |
| GET | /rate-limiter/status | Rate limiter status |
| GET | /rate-limiter/buckets | All rate limit buckets |
| POST | /rate-limiter/check | Check rate limit |
| GET | /cost/summary | Cost summary by period |
| GET | /cost/by-provider | Cost breakdown by provider |
| GET | /cost/by-model | Cost breakdown by model |
| GET | /cost/budget | Budget check |
| POST | /cost/record | Record a cost event |
| GET | /capacity/estimate | Capacity estimation |
| GET | /capacity/bottleneck | Find first bottleneck |
| GET | /capacity/plan | Create a scale plan |
| GET | /capacity/compare | Compare scale plans |
| GET | /capacity/cost-per-request | Cost per request estimate |
| GET | /architecture/overview | Full architecture overview |

## Running the Tests

```bash
# Run all tests
python test_system.py

# View full system status
python scripts/status.py

# Simulate traffic patterns
python scripts/simulate.py

# Generate cost reports
python scripts/cost_report.py
```

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
# Semantic Cache
CACHE_SIMILARITY_THRESHOLD=0.92
CACHE_MAX_ENTRIES=10000
CACHE_DEFAULT_TTL_SECONDS=3600

# Fallback
FALLBACK_TIMEOUT_SECONDS=5.0
FALLBACK_MAX_RETRIES=2

# Circuit Breaker
CB_FAILURE_THRESHOLD=5
CB_RECOVERY_TIMEOUT_SECONDS=30

# Rate Limiting
RATE_LIMIT_REQUESTS_PER_MINUTE=60
RATE_LIMIT_BURST_SIZE=10

# Cost Tracking
COST_PER_1M_INPUT_TOKENS=3.0
COST_PER_1M_OUTPUT_TOKENS=15.0
GPU_COST_PER_HOUR=2.50
MONTHLY_BUDGET_LIMIT_USD=15000.0

# Capacity Planning
BASELINE_REQUESTS_PER_SEC=10
PEAK_MULTIPLIER=10.0
```

## Key Concepts Demonstrated

| Concept | Implementation |
|---------|----------------|
| Semantic Caching | Cosine similarity matching with TTL and eviction |
| Fallback Routing | Priority-based multi-provider failover chain |
| Circuit Breaker | Closed → Open → Half-Open state machine |
| Rate Limiting | Token bucket algorithm with per-user limits |
| AI FinOps | Cost tracking by provider, model, and request |
| Capacity Planning | Layer-by-layer capacity estimation and bottleneck detection |
| Graceful Degradation | Reduced functionality during provider failures |
| Backpressure | Rate limiting when demand exceeds capacity |

## Pre-seeded Configuration

The sample app comes pre-configured with:

### Fallback Routes
1. **Primary**: OpenAI GPT-4o (priority 0)
2. **Secondary**: Anthropic Claude 3 Sonnet (priority 1)
3. **Fallback**: Azure OpenAI GPT-4o-mini (priority 2)
4. **Self-Hosted**: Llama 3 8B (priority 3)

### Circuit Breakers
- OpenAI (5 failures → open, 30s recovery)
- Anthropic (5 failures → open, 30s recovery)
- Azure (3 failures → open, 60s recovery)
- Self-Hosted (10 failures → open, 15s recovery)

### Cost Tracking
- Input tokens: $3.00/1M
- Output tokens: $15.00/1M
- GPU: $2.50/hour
- Monthly budget: $15,000

## Next Steps

After running this sample app, you should understand:

1. How semantic caching reduces latency and cost at scale
2. How fallback routing provides resilience against provider failures
3. How circuit breakers prevent cascading failures
4. How rate limiting implements backpressure
5. How AI cost tracking enables FinOps
6. How capacity planning identifies bottlenecks before they occur
7. How to balance reliability, scale, and cost

Move to **Day 10 → AI Observability** to learn about connecting every layer through observability.
