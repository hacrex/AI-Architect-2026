"""Test script to demonstrate the AI Knowledge Assistant."""

import httpx
import json

BASE_URL = "http://localhost:8000"


def test_health():
    response = httpx.get(f"{BASE_URL}/health")
    print("Health Check:")
    print(json.dumps(response.json(), indent=2))
    print()


def test_queries():
    headers = {"Authorization": "Bearer user-001"}

    queries = [
        "What is the leave policy?",
        "How do I request AWS access?",
        "What is the security policy?",
        "How many sick days do I get?",
        "Can I work remotely?",
    ]

    for query in queries:
        print(f"Query: {query}")
        response = httpx.post(
            f"{BASE_URL}/query",
            json={"query": query, "top_k": 3},
            headers=headers,
        )

        if response.status_code == 200:
            result = response.json()
            print(f"Answer: {result['answer'][:200]}...")
            print(f"Sources: {result['sources']}")
            print(f"Latency: {result['latency_ms']}ms")
        else:
            print(f"Error: {response.status_code} - {response.text}")
        print()


def test_access_control():
    print("Testing Access Control:")

    limited_headers = {"Authorization": "Bearer user-003"}
    query = "What is the expense policy?"

    response = httpx.post(
        f"{BASE_URL}/query",
        json={"query": query, "top_k": 3},
        headers=limited_headers,
    )

    print(f"Query (limited user): {query}")
    print(f"Response: {response.json().get('answer', 'No access')[:200]}")
    print()


if __name__ == "__main__":
    print("=== AI Knowledge Assistant Test ===\n")
    test_health()
    test_queries()
    test_access_control()
