"""Scale Pipeline — end-to-end scaling, reliability, and cost workflow."""
from app.semantic_cache import SemanticCache
from app.fallback_router import FallbackRouter
from app.circuit_breaker import CircuitBreaker
from app.rate_limiter import RateLimiter
from app.cost_tracker import CostTracker
from app.capacity_planner import CapacityPlanner
from app.models import FallbackRoute, ModelProvider
import config.settings as settings


class ScalePipeline:
    """Complete scale, reliability, and FinOps pipeline."""

    def __init__(self):
        self.cache = SemanticCache(
            similarity_threshold=settings.CACHE_SIMILARITY_THRESHOLD,
            max_entries=settings.CACHE_MAX_ENTRIES
        )
        self.router = FallbackRouter(
            timeout_seconds=settings.FALLBACK_TIMEOUT_SECONDS
        )
        self.circuit_breakers = {
            "openai": CircuitBreaker("openai", failure_threshold=5, recovery_timeout=30),
            "anthropic": CircuitBreaker("anthropic", failure_threshold=5, recovery_timeout=30),
        }
        self.rate_limiter = RateLimiter(capacity=60, refill_rate=1.0)
        self.cost_tracker = CostTracker()
        self.capacity_planner = CapacityPlanner()
        self._seed_routes()

    def _seed_routes(self):
        routes = [
            FallbackRoute(id="route-001", name="Primary", provider=ModelProvider.OPENAI,
                          model="gpt-4o", priority=0),
            FallbackRoute(id="route-002", name="Secondary", provider=ModelProvider.ANTHROPIC,
                          model="claude-3-sonnet", priority=1),
            FallbackRoute(id="route-003", name="Fallback", provider=ModelProvider.SELF_HOSTED,
                          model="llama-3-8b", priority=2),
        ]
        for r in routes:
            self.router.add_route(r)

    def process_request(self, query: str, user_id: str = "anonymous") -> dict:
        rate_check = self.rate_limiter.allow(user_id)
        if not rate_check["allowed"]:
            return {
                "status": "rate_limited",
                "retry_after_seconds": rate_check["retry_after_seconds"],
                "remaining": rate_check["remaining"]
            }

        cached = self.cache.get(query)
        if cached:
            self.cost_tracker.record_request(
                provider=ModelProvider.OPENAI, model="cache",
                input_tokens=0, output_tokens=0, cached=True
            )
            return {
                "status": "cache_hit",
                "response": cached,
                "provider": "cache",
                "cost_usd": 0
            }

        route_result = self.router.route_request(query)

        if route_result["provider"]:
            tokens_in = len(query.split()) * 2
            tokens_out = len(route_result["response"].split()) * 2
            self.cost_tracker.record_request(
                provider=ModelProvider(route_result["provider"]),
                model=route_result["model"],
                input_tokens=tokens_in,
                output_tokens=tokens_out
            )
            self.cache.put(query, route_result["response"], tokens_saved=tokens_in + tokens_out)

        return {
            "status": "success" if route_result["provider"] else "all_providers_failed",
            "response": route_result.get("response"),
            "provider": route_result.get("provider"),
            "model": route_result.get("model"),
            "latency_ms": route_result.get("latency_ms", 0),
            "fallback_chain_position": route_result.get("fallback_chain_position", 0)
        }

    def simulate_traffic(self, num_requests: int, query_pool: list[str]) -> dict:
        results = {"cache_hits": 0, "cache_misses": 0, "rate_limited": 0,
                    "success": 0, "failed": 0, "total_cost": 0}

        for i in range(num_requests):
            query = query_pool[i % len(query_pool)]
            result = self.process_request(query, f"user-{i % 10}")

            if result["status"] == "cache_hit":
                results["cache_hits"] += 1
            elif result["status"] == "rate_limited":
                results["rate_limited"] += 1
            elif result["status"] == "success":
                results["success"] += 1
                results["total_cost"] += result.get("cost_usd", 0)
            else:
                results["failed"] += 1

        results["total_cost"] = round(results["total_cost"], 6)
        results["cache_hit_rate"] = round(
            results["cache_hits"] / num_requests * 100, 1
        ) if num_requests > 0 else 0

        return results

    def get_full_status(self) -> dict:
        return {
            "cache": self.cache.get_stats().model_dump(),
            "fallback_routes": self.router.list_routes(),
            "fallback_stats": self.router.get_stats(),
            "circuit_breakers": {
                name: cb.get_status() for name, cb in self.circuit_breakers.items()
            },
            "rate_limiter": self.rate_limiter.list_buckets(),
            "cost_summary": self.cost_tracker.get_summary().model_dump(),
            "budget_check": self.cost_tracker.check_budget(),
            "capacity_1x": [l.model_dump() for l in self.capacity_planner.estimate_capacity(1.0)],
            "capacity_10x": [l.model_dump() for l in self.capacity_planner.estimate_capacity(10.0)],
            "cost_comparison": self.capacity_planner.compare_plans([1, 3, 5, 10])
        }
