"""Tests for the Scale, Reliability & AI FinOps sample app."""
import sys
sys.path.insert(0, ".")

from app.semantic_cache import SemanticCache
from app.fallback_router import FallbackRouter
from app.circuit_breaker import CircuitBreaker
from app.rate_limiter import RateLimiter
from app.cost_tracker import CostTracker
from app.capacity_planner import CapacityPlanner
from app.models import ModelProvider, FallbackRoute, CircuitState
from pipelines.scale_pipeline import ScalePipeline


def test_semantic_cache():
    print("=== Testing Semantic Cache ===")
    cache = SemanticCache(similarity_threshold=0.8, max_entries=100)

    entry1 = cache.put("How do I deploy Kubernetes?", "Deploy with kubectl apply", 500)
    assert entry1.key is not None
    print(f"  Stored entry: {entry1.key}")

    hit = cache.get("How do I deploy Kubernetes?")
    assert hit is not None
    print(f"  Exact match hit: {hit[:40]}")

    hit2 = cache.get("What are the steps to deploy a Kubernetes cluster?")
    print(f"  Similar query hit: {hit2 is not None}")

    stats = cache.get_stats()
    print(f"  Entries: {stats.total_entries}")
    print(f"  Hit Rate: {stats.hit_rate_pct}%")

    cache.invalidate(entry1.key)
    assert cache.get_stats().total_entries == 0
    print("  Invalidation: OK")

    print("PASSED\n")


def test_fallback_router():
    print("=== Testing Fallback Router ===")
    router = FallbackRouter(timeout_seconds=5.0)

    routes = [
        FallbackRoute(id="r1", name="Primary", provider=ModelProvider.OPENAI,
                      model="gpt-4o", priority=0, timeout_seconds=1.0),
        FallbackRoute(id="r2", name="Secondary", provider=ModelProvider.ANTHROPIC,
                      model="claude-3", priority=1, timeout_seconds=1.0),
        FallbackRoute(id="r3", name="Fallback", provider=ModelProvider.SELF_HOSTED,
                      model="llama-3", priority=2, timeout_seconds=1.0),
    ]
    for r in routes:
        router.add_route(r)

    print(f"  Routes: {len(router.list_routes())}")
    assert len(router.list_routes()) == 3

    result = router.route_request("test query")
    print(f"  Routed to: {result['provider']}/{result['model']}")
    assert result["provider"] is not None

    router.disable_route("r1")
    result2 = router.route_request("test query")
    print(f"  After disabling r1: {result2['provider']}/{result2['model']}")
    assert result2["provider"] != "openai" or result2["fallback_chain_position"] > 0

    stats = router.get_stats()
    print(f"  Stats entries: {len(stats)}")

    print("PASSED\n")


def test_circuit_breaker():
    print("=== Testing Circuit Breaker ===")
    cb = CircuitBreaker("test", failure_threshold=3, recovery_timeout=1, half_open_max_calls=2)

    assert cb.state.state == CircuitState.CLOSED
    print(f"  Initial state: {cb.state.state.value}")

    for _ in range(3):
        cb.record_failure()
    assert cb.state.state == CircuitState.OPEN
    print(f"  After 3 failures: {cb.state.state.value}")

    assert not cb.can_execute()
    print(f"  Can execute (open): {cb.can_execute()}")

    import time
    time.sleep(1.1)
    assert cb.can_execute()
    print(f"  After recovery timeout: {cb.state.state.value}")

    cb.record_success()
    cb.record_success()
    assert cb.state.state == CircuitState.CLOSED
    print(f"  After 2 successes in half-open: {cb.state.state.value}")

    status = cb.get_status()
    print(f"  Status: {status['state']}, failures: {status['failure_count']}")

    print("PASSED\n")


def test_rate_limiter():
    print("=== Testing Rate Limiter ===")
    limiter = RateLimiter(capacity=5, refill_rate=0.0)

    results = []
    for _ in range(7):
        results.append(limiter.allow("test-user"))

    allowed = sum(1 for r in results if r["allowed"])
    denied = sum(1 for r in results if not r["allowed"])
    print(f"  7 requests: {allowed} allowed, {denied} denied")
    assert allowed == 5
    assert denied == 2

    status = limiter.get_status("test-user")
    print(f"  Remaining tokens: {status['tokens']}")

    limiter.reset("test-user")
    status2 = limiter.get_status("test-user")
    print(f"  After reset: {status2['tokens']} tokens")

    print("PASSED\n")


def test_cost_tracker():
    print("=== Testing Cost Tracker ===")
    tracker = CostTracker()

    r1 = tracker.record_request(
        provider=ModelProvider.OPENAI, model="gpt-4o",
        input_tokens=2000, output_tokens=500
    )
    print(f"  Record 1: ${r1.total_cost_usd:.6f}")

    r2 = tracker.record_request(
        provider=ModelProvider.ANTHROPIC, model="claude-3-sonnet",
        input_tokens=3000, output_tokens=800
    )
    print(f"  Record 2: ${r2.total_cost_usd:.6f}")

    r3 = tracker.record_request(
        provider=ModelProvider.OPENAI, model="gpt-4o",
        input_tokens=1000, output_tokens=300, cached=True
    )
    print(f"  Record 3 (cached): ${r3.total_cost_usd:.6f}")

    summary = tracker.get_summary("all")
    print(f"  Total: ${summary.total_cost_usd:.6f}")
    print(f"  Requests: {summary.total_requests}")
    print(f"  Cached: {summary.cached_requests}")

    by_provider = tracker.get_cost_by_provider()
    print(f"  Providers: {list(by_provider.keys())}")

    budget = tracker.check_budget()
    print(f"  Budget remaining: ${budget['remaining_usd']:.6f}")

    assert summary.total_requests == 3
    print("PASSED\n")


def test_capacity_planner():
    print("=== Testing Capacity Planner ===")
    planner = CapacityPlanner()

    layers = planner.estimate_capacity(1.0)
    print(f"  Layers at 1x: {len(layers)}")
    for l in layers:
        bottleneck = " ***" if l.bottleneck else ""
        print(f"    {l.layer:20s} {l.utilization_pct:5.1f}%{bottleneck}")

    bottleneck = planner.find_bottleneck(1.0)
    print(f"  First bottleneck (1x): {bottleneck.layer}")

    plan = planner.create_scale_plan("Test Plan", 5.0)
    print(f"  5x Plan: ${plan.monthly_cost_estimate:,.2f}/mo")
    print(f"  First bottleneck: {plan.first_bottleneck}")

    comparison = planner.compare_plans([1, 3, 5, 10])
    print(f"  Comparison plans: {len(comparison)}")
    for p in comparison:
        print(f"    {p['scale_factor']}x: ${p['monthly_cost']:,.2f}, GPUs: {p['gpu_needed']}")

    cpr = planner.estimate_cost_per_request(1.0)
    print(f"  Cost/request (1x): ${cpr['cost_per_request']:.8f}")

    print("PASSED\n")


def test_scale_pipeline():
    print("=== Testing Scale Pipeline ===")
    pipeline = ScalePipeline()

    result = pipeline.process_request("How do I deploy Kubernetes?", "user-1")
    print(f"  First request: {result['status']}")
    assert result["status"] in ("success", "cache_hit")

    result2 = pipeline.process_request("How do I deploy Kubernetes?", "user-2")
    print(f"  Similar query: {result2['status']}")

    sim_result = pipeline.simulate_traffic(20, [
        "How do I deploy Kubernetes?",
        "What is Kubernetes?",
        "Explain containers",
    ])
    print(f"  Simulation (20 reqs):")
    print(f"    Cache Hits: {sim_result['cache_hits']}")
    print(f"    Success: {sim_result['success']}")
    print(f"    Rate Limited: {sim_result['rate_limited']}")
    print(f"    Cost: ${sim_result['total_cost']}")

    status = pipeline.get_full_status()
    print(f"  Full status keys: {list(status.keys())}")
    assert "cache" in status
    assert "fallback_routes" in status
    assert "circuit_breakers" in status
    assert "cost_summary" in status
    assert "capacity_1x" in status

    print("PASSED\n")


if __name__ == "__main__":
    print("Scale, Reliability & AI FinOps Tests\n")
    test_semantic_cache()
    test_fallback_router()
    test_circuit_breaker()
    test_rate_limiter()
    test_cost_tracker()
    test_capacity_planner()
    test_scale_pipeline()
    print("All tests passed!")
