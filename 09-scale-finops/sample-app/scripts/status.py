"""Script to view full system status."""
import sys
sys.path.insert(0, ".")

from pipelines.scale_pipeline import ScalePipeline


def main():
    pipeline = ScalePipeline()
    status = pipeline.get_full_status()

    print("=== Scale, Reliability & AI FinOps — System Status ===\n")

    print("--- Semantic Cache ---")
    cache = status["cache"]
    print(f"  Entries: {cache['total_entries']}")
    print(f"  Hit Rate: {cache['hit_rate_pct']}%")
    print(f"  Tokens Saved: {cache['tokens_saved']}")
    print(f"  Estimated Savings: ${cache['estimated_savings_usd']}")

    print("\n--- Fallback Routes ---")
    for r in status["fallback_routes"]:
        print(f"  [{r['priority']}] {r['name']} ({r['provider']}/{r['model']}) - {'Enabled' if r['is_enabled'] else 'Disabled'}")

    print("\n--- Circuit Breakers ---")
    for name, cb in status["circuit_breakers"].items():
        print(f"  {name}: {cb['state']} (failures: {cb['failure_count']}/{cb['failure_threshold']})")

    print("\n--- Cost Summary ---")
    cost = status["cost_summary"]
    print(f"  Total Cost: ${cost['total_cost_usd']}")
    print(f"  Model Cost: ${cost['model_cost_usd']}")
    print(f"  GPU Cost: ${cost['gpu_cost_usd']}")
    print(f"  Requests: {cost['total_requests']}")
    print(f"  Cached: {cost['cached_requests']}")

    print("\n--- Budget Check ---")
    budget = status["budget_check"]
    print(f"  Daily Budget: ${budget['daily_budget_usd']}")
    print(f"  Today Cost: ${budget['today_cost_usd']}")
    print(f"  Remaining: ${budget['remaining_usd']}")
    print(f"  Over Budget: {budget['over_budget']}")

    print("\n--- Capacity (1x) ---")
    for layer in status["capacity_1x"]:
        bottleneck = " *** BOTTLENECK ***" if layer["bottleneck"] else ""
        print(f"  {layer['layer']:20s} Utilization: {layer['utilization_pct']:5.1f}%{bottleneck}")
        print(f"    {layer['recommendation']}")

    print("\n--- Capacity (10x) ---")
    for layer in status["capacity_10x"]:
        bottleneck = " *** BOTTLENECK ***" if layer["bottleneck"] else ""
        print(f"  {layer['layer']:20s} Utilization: {layer['utilization_pct']:5.1f}%{bottleneck}")
        print(f"    {layer['recommendation']}")

    print("\n--- Cost Comparison ---")
    for plan in status["cost_comparison"]:
        print(f"  {plan['scale_factor']:3.0f}x: ${plan['monthly_cost']:,.2f}/mo | "
              f"GPUs: {plan['gpu_needed']} | Bottleneck: {plan['first_bottleneck']}")


if __name__ == "__main__":
    main()
