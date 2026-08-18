"""Test script for Day 02 Model Comparison & Routing Sample App."""

import httpx
import json
import time

BASE_URL = "http://localhost:8001"


def test_health():
    """Test health endpoint."""
    print("=== Testing Health Endpoint ===")
    response = httpx.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_models():
    """Test models endpoint."""
    print("=== Testing Models Endpoint ===")
    response = httpx.get(f"{BASE_URL}/models")
    print(f"Status: {response.status_code}")
    models = response.json()
    for model in models:
        print(
            f"  {model['id']}: {model['name']} ({model['tier']}) - ${model['input_cost_per_1k']}/1K input"
        )
    print()


def test_single_model():
    """Test single model query."""
    print("=== Testing Single Model Query ===")
    response = httpx.post(
        f"{BASE_URL}/query",
        json={"query": "What is 2 + 2?", "model": "gpt-3.5-turbo"},
    )
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Model: {result['model_used']}")
    print(f"Routing: {result['routing_decision']}")
    print(f"Latency: {result['latency_ms']:.0f}ms")
    print(f"Tokens: {result['tokens_used']}")
    print(f"Cost: ${result['cost_estimate']:.4f}")
    print(f"Answer: {result['answer'][:100]}...")
    print()


def test_auto_routing():
    """Test auto-routing with different complexity levels."""
    print("=== Testing Auto-Routing ===")

    test_queries = [
        ("Simple", "What is 2 + 2?"),
        ("Normal", "Explain the difference between REST and GraphQL."),
        (
            "Complex",
            "Compare horizontal vs vertical scaling for a cloud-native application handling 10,000 requests per second.",
        ),
    ]

    for expected, query in test_queries:
        print(f"\n{expected} Query: {query[:50]}...")
        response = httpx.post(
            f"{BASE_URL}/query/auto", json={"query": query}
        )
        result = response.json()
        print(f"  Routing: {result['routing_decision']}")
        print(f"  Model: {result['model_used']}")
        print(f"  Latency: {result['latency_ms']:.0f}ms")
        print(f"  Cost: ${result['cost_estimate']:.4f}")
    print()


def test_classification():
    """Test query classification endpoint."""
    print("=== Testing Query Classification ===")

    test_queries = [
        "What is 2 + 2?",
        "Explain the difference between REST and GraphQL.",
        "Compare horizontal vs vertical scaling for a cloud-native application.",
    ]

    for query in test_queries:
        response = httpx.get(f"{BASE_URL}/classify", params={"query": query})
        result = response.json()
        print(f"Query: {query[:50]}...")
        print(f"  Complexity: {result['complexity']}")
        print(f"  Model: {result['selected_model']}")
        print(f"  Reason: {result['reason']}")
    print()


def test_comparison():
    """Test model comparison."""
    print("=== Testing Model Comparison ===")
    response = httpx.post(
        f"{BASE_URL}/compare",
        json={
            "query": "Explain the CAP theorem in distributed systems.",
            "models": ["gpt-3.5-turbo", "gpt-4"],
        },
    )
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Query: {result['query']}")
    print(f"Routing Decision: {result['routing_decision']}")
    print(f"Recommendation: {result['recommendation']}")
    print("\nModel Comparison:")
    for r in result["results"]:
        print(f"  {r['model_used']}:")
        print(f"    Latency: {r['latency_ms']:.0f}ms")
        print(f"    Tokens: {r['tokens_used']}")
        print(f"    Cost: ${r['cost_estimate']:.4f}")
        print(f"    Response: {r['content'][:100]}...")
    print()


if __name__ == "__main__":
    print("Day 02 - Model Comparison & Routing Tests")
    print("=" * 50)
    print()

    try:
        test_health()
        test_models()
        test_single_model()
        test_auto_routing()
        test_classification()
        test_comparison()

        print("=" * 50)
        print("All tests completed!")
        print()
        print("Next steps:")
        print("1. Review the results above")
        print("2. Fill out comparison tables in exercise.md")
        print("3. Design your own model routing strategy")
        print("4. Estimate costs for your specific use case")

    except httpx.ConnectError:
        print("ERROR: Could not connect to server")
        print("Make sure the server is running: uvicorn app.main:app --reload --port 8001")
