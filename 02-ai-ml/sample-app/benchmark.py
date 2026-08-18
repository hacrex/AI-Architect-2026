"""Benchmark script for comparing model performance."""

import asyncio
import httpx
import json
import time
from typing import List, Dict
from app.model_comparator import comparator
from app.model_gateway import model_gateway
from config.settings import settings

BASE_URL = "http://localhost:8001"


async def run_benchmark(
    models: List[str] = None,
    category: str = "all",
    iterations: int = 3,
):
    """Run benchmark suite."""
    if models is None:
        models = ["gpt-3.5-turbo", "gpt-4"]

    print(f"Running benchmark for: {', '.join(models)}")
    print(f"Category: {category}")
    print(f"Iterations: {iterations}")
    print("=" * 60)

    results = await comparator.run_benchmark(
        models=models,
        category=category,
        iterations=iterations,
    )

    # Print results
    print("\nBenchmark Results:")
    print("-" * 60)

    for model in models:
        summary = comparator.calculate_benchmark_summary(results, model)
        print(f"\n{model}:")
        print(f"  Total Prompts: {summary.total_prompts}")
        print(f"  Avg Latency: {summary.avg_latency_ms:.0f}ms")
        print(f"  Total Input Tokens: {summary.total_input_tokens}")
        print(f"  Total Output Tokens: {summary.total_output_tokens}")
        print(f"  Total Cost: ${summary.total_cost:.4f}")

    # Compare models
    if len(models) > 1:
        print("\n" + "=" * 60)
        print("Model Comparison:")
        print("-" * 60)

        summaries = {}
        for model in models:
            summaries[model] = comparator.calculate_benchmark_summary(
                results, model
            )

        # Find best model for each metric
        fastest = min(summaries.values(), key=lambda s: s.avg_latency_ms)
        cheapest = min(summaries.values(), key=lambda s: s.total_cost)

        print(f"\nFastest: {fastest.model} ({fastest.avg_latency_ms:.0f}ms avg)")
        print(f"Cheapest: {cheapest.model} (${cheapest.total_cost:.4f} total)")

    return results


def calculate_cost_estimate(
    requests_per_month: int,
    distribution: Dict[str, float],
    avg_tokens: Dict[str, Dict[str, int]],
):
    """Calculate monthly cost estimate."""
    print("\n" + "=" * 60)
    print("Monthly Cost Estimate:")
    print("-" * 60)

    total_cost = 0

    for category, percentage in distribution.items():
        requests = int(requests_per_month * percentage)
        input_tokens = avg_tokens[category]["input"]
        output_tokens = avg_tokens[category]["output"]

        # Use GPT-4 pricing as example
        model_info = settings.model_info.get("gpt-4", {})
        input_cost = model_info.get("input_cost", 0.03)
        output_cost = model_info.get("output_cost", 0.06)

        cost = (requests * input_tokens * input_cost / 1000) + (
            requests * output_tokens * output_cost / 1000
        )
        total_cost += cost

        print(
            f"  {category}: {requests} requests = ${cost:.2f}"
        )

    print(f"\n  Total Monthly Cost: ${total_cost:.2f}")
    return total_cost


async def main():
    """Run full benchmark suite."""
    print("Day 02 - Model Benchmark Suite")
    print("=" * 60)
    print()

    # Run benchmark
    results = await run_benchmark(
        models=["gpt-3.5-turbo", "gpt-4"],
        category="all",
        iterations=3,
    )

    # Calculate cost estimate
    print("\n" + "=" * 60)
    print("Cost Analysis")
    print("=" * 60)

    distribution = {
        "simple": 0.5,
        "normal": 0.35,
        "complex": 0.15,
    }

    avg_tokens = {
        "simple": {"input": 200, "output": 100},
        "normal": {"input": 500, "output": 300},
        "complex": {"input": 1500, "output": 800},
    }

    # Single model approach (GPT-4 only)
    print("\nSingle Model Approach (GPT-4 only):")
    single_cost = calculate_cost_estimate(
        requests_per_month=10000,
        distribution={"all": 1.0},
        avg_tokens={"all": {"input": 600, "output": 350}},
    )

    # Routed approach
    print("\nRouted Approach (GPT-3.5 + GPT-4):")
    routed_cost = calculate_cost_estimate(
        requests_per_month=10000,
        distribution=distribution,
        avg_tokens=avg_tokens,
    )

    # Savings
    savings = single_cost - routed_cost
    savings_percentage = (savings / single_cost) * 100

    print("\n" + "=" * 60)
    print("Cost Savings Summary:")
    print("-" * 60)
    print(f"  Single Model Cost: ${single_cost:.2f}/month")
    print(f"  Routed Cost: ${routed_cost:.2f}/month")
    print(f"  Savings: ${savings:.2f}/month ({savings_percentage:.1f}%)")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
