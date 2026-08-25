"""Script to simulate traffic and test scaling behavior."""
import sys
sys.path.insert(0, ".")

from pipelines.scale_pipeline import ScalePipeline


def main():
    pipeline = ScalePipeline()

    print("=== Traffic Simulation ===\n")

    queries = [
        "How do I deploy Kubernetes?",
        "What are the steps to deploy a Kubernetes cluster?",
        "Explain Kubernetes deployment process",
        "How to set up a K8s cluster?",
        "What is the best way to deploy containers?",
        "How do I configure a load balancer?",
        "What are Kubernetes services?",
        "Explain pod networking in Kubernetes",
    ]

    scenarios = [
        ("Normal Traffic (50 requests)", 50),
        ("Spike Traffic (200 requests)", 200),
        ("Load Test (500 requests)", 500),
    ]

    for name, count in scenarios:
        print(f"--- {name} ---")
        result = pipeline.simulate_traffic(count, queries)
        print(f"  Total Requests: {count}")
        print(f"  Cache Hits: {result['cache_hits']} ({result['cache_hit_rate']}%)")
        print(f"  Cache Misses: {result['cache_misses']}")
        print(f"  Rate Limited: {result['rate_limited']}")
        print(f"  Successful: {result['success']}")
        print(f"  Failed: {result['failed']}")
        print(f"  Total Cost: ${result['total_cost']}")
        print()

    print("=== Semantic Cache Demo ===\n")
    pipeline2 = ScalePipeline()

    test_queries = [
        "How do I deploy Kubernetes?",
        "What are the steps to deploy a Kubernetes cluster?",
        "How to set up a Kubernetes deployment?",
    ]

    for q in test_queries:
        result = pipeline2.process_request(q, "demo-user")
        print(f"Query: {q}")
        print(f"  Status: {result['status']}")
        print(f"  Provider: {result.get('provider', 'N/A')}")
        print()

    cache_stats = pipeline2.cache.get_stats()
    print(f"Final Cache Stats:")
    print(f"  Entries: {cache_stats.total_entries}")
    print(f"  Hit Rate: {cache_stats.hit_rate_pct}%")
    print(f"  Tokens Saved: {cache_stats.tokens_saved}")


if __name__ == "__main__":
    main()
