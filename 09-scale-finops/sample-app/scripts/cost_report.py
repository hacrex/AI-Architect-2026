"""Script to generate and display cost reports."""
import sys
sys.path.insert(0, ".")

from app.cost_tracker import CostTracker
from app.capacity_planner import CapacityPlanner
from app.models import ModelProvider


def main():
    tracker = CostTracker()
    planner = CapacityPlanner()

    print("=== AI FinOps Cost Report ===\n")

    print("--- Simulating Request Costs ---\n")

    scenarios = [
        (ModelProvider.OPENAI, "gpt-4o", 2000, 500, False),
        (ModelProvider.OPENAI, "gpt-4o", 2000, 500, True),
        (ModelProvider.ANTHROPIC, "claude-3-sonnet", 3000, 800, False),
        (ModelProvider.AZURE, "gpt-4o-mini", 1000, 200, False),
        (ModelProvider.SELF_HOSTED, "llama-3-8b", 1500, 400, False),
        (ModelProvider.OPENAI, "gpt-4o", 5000, 1000, False),
        (ModelProvider.OPENAI, "gpt-4o", 1000, 300, True),
        (ModelProvider.ANTHROPIC, "claude-3-sonnet", 4000, 600, False),
    ]

    for provider, model, inp, out, cached in scenarios:
        record = tracker.record_request(
            provider=provider, model=model,
            input_tokens=inp, output_tokens=out,
            embedding_tokens=500 if not cached else 0,
            vector_searches=1 if not cached else 0,
            cached=cached
        )
        status = "CACHED" if cached else "LIVE"
        print(f"  [{status}] {provider.value}/{model}: {inp}+{out} tokens = ${record.total_cost_usd:.6f}")

    print("\n--- Cost Summary ---")
    summary = tracker.get_summary("all")
    print(f"  Total Cost: ${summary.total_cost_usd}")
    print(f"  Model Cost: ${summary.model_cost_usd}")
    print(f"  Embedding Cost: ${summary.embedding_cost_usd}")
    print(f"  Retrieval Cost: ${summary.retrieval_cost_usd}")
    print(f"  Total Requests: {summary.total_requests}")
    print(f"  Cached Requests: {summary.cached_requests}")
    print(f"  Cache Savings: ${summary.cache_savings_usd}")
    print(f"  Cost per Request: ${summary.cost_per_request:.8f}")

    print("\n--- Cost by Provider ---")
    by_provider = tracker.get_cost_by_provider()
    for provider, data in by_provider.items():
        print(f"  {provider:15s}: ${data['cost_usd']:.6f} ({data['requests']} reqs, {data['total_tokens']} tokens)")

    print("\n--- Cost by Model ---")
    by_model = tracker.get_cost_by_model()
    for model, data in by_model.items():
        print(f"  {model:20s}: ${data['cost_usd']:.6f} ({data['requests']} reqs)")

    print("\n--- Budget Check ---")
    budget = tracker.check_budget()
    print(f"  Daily Budget: ${budget['daily_budget_usd']}")
    print(f"  Today Cost: ${budget['today_cost_usd']}")
    print(f"  Remaining: ${budget['remaining_usd']}")
    print(f"  Utilization: {budget['utilization_pct']}%")

    print("\n--- Capacity Cost Comparison ---")
    comparison = planner.compare_plans([1, 3, 5, 10])
    for plan in comparison:
        print(f"  {plan['scale_factor']:3.0f}x: ${plan['monthly_cost']:,.2f}/mo | "
              f"GPUs: {plan['gpu_needed']} | RPS: {plan['baseline_rps']:.0f}")

    print("\n--- Cost per Request by Scale ---")
    for factor in [1, 5, 10]:
        cpr = planner.estimate_cost_per_request(factor)
        print(f"  {factor}x: ${cpr['cost_per_request']:.8f}/req "
              f"(token: ${cpr['token_cost_per_request']:.6f}, "
              f"infra: ${cpr['infrastructure_cost_per_request']:.8f})")


if __name__ == "__main__":
    main()
