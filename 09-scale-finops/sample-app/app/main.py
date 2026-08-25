"""FastAPI application for Scale, Reliability & AI FinOps."""
from datetime import datetime
from fastapi import FastAPI, HTTPException
from typing import Optional
from app.models import ModelProvider, FallbackRoute, CircuitState
from app.semantic_cache import SemanticCache
from app.fallback_router import FallbackRouter
from app.circuit_breaker import CircuitBreaker
from app.rate_limiter import RateLimiter
from app.cost_tracker import CostTracker
from app.capacity_planner import CapacityPlanner
import config.settings as settings

app = FastAPI(
    title="Scale, Reliability & AI FinOps API",
    description="Scaling, reliability patterns, and cost optimization for AI systems",
    version="0.1.0"
)

cache = SemanticCache(
    similarity_threshold=settings.CACHE_SIMILARITY_THRESHOLD,
    max_entries=settings.CACHE_MAX_ENTRIES,
    default_ttl=settings.CACHE_DEFAULT_TTL_SECONDS
)

router = FallbackRouter(
    timeout_seconds=settings.FALLBACK_TIMEOUT_SECONDS,
    max_retries=settings.FALLBACK_MAX_RETRIES
)

circuit_breakers: dict[str, CircuitBreaker] = {}

rate_limiter = RateLimiter(
    capacity=settings.RATE_LIMIT_REQUESTS_PER_MINUTE,
    refill_rate=settings.RATE_LIMIT_REQUESTS_PER_MINUTE / 60
)

cost_tracker = CostTracker()
capacity_planner = CapacityPlanner()


def _seed_fallback_routes():
    routes = [
        FallbackRoute(id="route-001", name="Primary OpenAI", provider=ModelProvider.OPENAI,
                      model="gpt-4o", priority=0, timeout_seconds=5.0),
        FallbackRoute(id="route-002", name="Secondary Anthropic", provider=ModelProvider.ANTHROPIC,
                      model="claude-3-sonnet", priority=1, timeout_seconds=5.0),
        FallbackRoute(id="route-003", name="Fallback Azure OpenAI", provider=ModelProvider.AZURE,
                      model="gpt-4o-mini", priority=2, timeout_seconds=8.0),
        FallbackRoute(id="route-004", name="Self-Hosted Llama", provider=ModelProvider.SELF_HOSTED,
                      model="llama-3-8b", priority=3, timeout_seconds=10.0),
    ]
    for r in routes:
        router.add_route(r)

    circuit_breakers["openai"] = CircuitBreaker("openai", failure_threshold=5, recovery_timeout=30)
    circuit_breakers["anthropic"] = CircuitBreaker("anthropic", failure_threshold=5, recovery_timeout=30)
    circuit_breakers["azure"] = CircuitBreaker("azure", failure_threshold=3, recovery_timeout=60)
    circuit_breakers["self_hosted"] = CircuitBreaker("self_hosted", failure_threshold=10, recovery_timeout=15)


_seed_fallback_routes()


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "semantic_cache": "ok",
            "fallback_router": "ok",
            "circuit_breakers": "ok",
            "rate_limiter": "ok",
            "cost_tracker": "ok",
            "capacity_planner": "ok"
        }
    }


@app.get("/cache/stats")
def cache_stats():
    return cache.get_stats().model_dump()


@app.get("/cache/entries")
def cache_entries():
    return cache.list_entries()


@app.post("/cache/put")
def cache_put(query: str, response: str, tokens_saved: int = 0):
    entry = cache.put(query, response, tokens_saved)
    return {"key": entry.key, "stored": True}


@app.post("/cache/invalidate")
def cache_invalidate(pattern: str = ""):
    if pattern:
        count = cache.invalidate_by_pattern(pattern)
    else:
        count = cache.clear()
    return {"invalidated": count}


@app.get("/fallback/routes")
def fallback_routes():
    return router.list_routes()


@app.get("/fallback/stats")
def fallback_stats():
    return router.get_stats()


@app.post("/fallback/route")
def fallback_route_request(query: str):
    return router.route_request(query)


@app.post("/fallback/disable/{route_id}")
def disable_route(route_id: str):
    if router.disable_route(route_id):
        return {"disabled": route_id}
    raise HTTPException(status_code=404, detail=f"Route {route_id} not found")


@app.post("/fallback/enable/{route_id}")
def enable_route(route_id: str):
    if router.enable_route(route_id):
        return {"enabled": route_id}
    raise HTTPException(status_code=404, detail=f"Route {route_id} not found")


@app.get("/circuit-breakers")
def circuit_breakers_status():
    return {name: cb.get_status() for name, cb in circuit_breakers.items()}


@app.post("/circuit-breakers/{name}/reset")
def reset_circuit_breaker(name: str):
    if name in circuit_breakers:
        circuit_breakers[name].reset()
        return {"reset": name}
    raise HTTPException(status_code=404, detail=f"Circuit breaker {name} not found")


@app.get("/rate-limiter/status")
def rate_limiter_status(name: str = "global"):
    return rate_limiter.get_status(name)


@app.get("/rate-limiter/buckets")
def rate_limiter_buckets():
    return rate_limiter.list_buckets()


@app.post("/rate-limiter/check")
def rate_limiter_check(name: str = "global", tokens: int = 1):
    return rate_limiter.allow(name, tokens)


@app.get("/cost/summary")
def cost_summary(period: str = "all"):
    return cost_tracker.get_summary(period).model_dump()


@app.get("/cost/by-provider")
def cost_by_provider():
    return cost_tracker.get_cost_by_provider()


@app.get("/cost/by-model")
def cost_by_model():
    return cost_tracker.get_cost_by_model()


@app.get("/cost/budget")
def cost_budget():
    return cost_tracker.check_budget()


@app.get("/cost/records")
def cost_records(limit: int = 50):
    return cost_tracker.list_records(limit)


@app.post("/cost/record")
def record_cost(provider: str, model: str, input_tokens: int,
                output_tokens: int, embedding_tokens: int = 0,
                vector_searches: int = 0, gpu_seconds: float = 0.0,
                cached: bool = False):
    try:
        p = ModelProvider(provider)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid provider: {provider}")

    record = cost_tracker.record_request(
        provider=p, model=model, input_tokens=input_tokens,
        output_tokens=output_tokens, embedding_tokens=embedding_tokens,
        vector_searches=vector_searches, gpu_seconds=gpu_seconds, cached=cached
    )
    return {"id": record.id, "cost_usd": record.total_cost_usd}


@app.get("/capacity/estimate")
def capacity_estimate(scale_factor: float = 1.0):
    return [l.model_dump() for l in capacity_planner.estimate_capacity(scale_factor)]


@app.get("/capacity/bottleneck")
def capacity_bottleneck(scale_factor: float = 1.0):
    return capacity_planner.find_bottleneck(scale_factor).model_dump()


@app.get("/capacity/plan")
def capacity_plan(name: str = "Default", scale_factor: float = 1.0):
    plan = capacity_planner.create_scale_plan(name, scale_factor)
    return plan.model_dump()


@app.get("/capacity/compare")
def capacity_compare(factors: str = "1,3,5,10"):
    try:
        factor_list = [float(f.strip()) for f in factors.split(",")]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid factors format")
    return capacity_planner.compare_plans(factor_list)


@app.get("/capacity/cost-per-request")
def cost_per_request(scale_factor: float = 1.0):
    return capacity_planner.estimate_cost_per_request(scale_factor)


@app.get("/architecture/overview")
def architecture_overview():
    return {
        "components": {
            "semantic_cache": {
                "description": "Meaning-based response reuse",
                "threshold": settings.CACHE_SIMILARITY_THRESHOLD,
                "max_entries": settings.CACHE_MAX_ENTRIES
            },
            "fallback_router": {
                "description": "Multi-provider failover chain",
                "routes": len(router.list_routes()),
                "timeout": settings.FALLBACK_TIMEOUT_SECONDS
            },
            "circuit_breakers": {
                "description": "Cascading failure protection",
                "count": len(circuit_breakers),
                "threshold": settings.CB_FAILURE_THRESHOLD
            },
            "rate_limiter": {
                "description": "Token bucket request throttling",
                "capacity": settings.RATE_LIMIT_REQUESTS_PER_MINUTE
            },
            "cost_tracker": {
                "description": "AI FinOps cost monitoring",
                "budget_monthly": settings.MONTHLY_BUDGET_LIMIT_USD
            },
            "capacity_planner": {
                "description": "Infrastructure capacity estimation",
                "baseline_rps": settings.BASELINE_REQUESTS_PER_SEC,
                "peak_multiplier": settings.PEAK_MULTIPLIER
            }
        },
        "architecture_flow": [
            "User Request → Rate Limiter",
            "Rate Limiter → Semantic Cache",
            "Cache Hit → Return Cached Response",
            "Cache Miss → Circuit Breaker Check",
            "Circuit Breaker Open → Fallback Route",
            "Circuit Breaker Closed → Primary Provider",
            "Response → Cache Store",
            "Cost Record → Cost Tracker"
        ]
    }
