"""Test script for Data Pipeline API."""
import requests
import json

BASE_URL = "http://localhost:8005"


def test_health():
    print("=== Health Check ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_ingest():
    print("=== Ingest Document ===")
    doc = {
        "document_id": "eng-001",
        "title": "Kubernetes Guide",
        "content": "# Kubernetes Guide\n\n## Overview\n\nKubernetes is a container orchestration platform.\n\n## Deployment\n\nUse kubectl to deploy applications.",
        "department": "engineering",
        "classification": "internal"
    }
    response = requests.post(f"{BASE_URL}/ingest", json=doc)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_query():
    print("=== Query Documents ===")
    query = {
        "query": "How do I deploy to Kubernetes?",
        "user_id": "alice@company.com",
        "top_k": 5
    }
    response = requests.post(f"{BASE_URL}/query", json=query)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_stats():
    print("=== Stats ===")
    response = requests.get(f"{BASE_URL}/stats")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


if __name__ == "__main__":
    print("Data Pipeline API Tests\n")
    test_health()
    test_ingest()
    test_query()
    test_stats()
    print("All tests completed!")
