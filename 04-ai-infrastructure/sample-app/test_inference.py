import httpx
import json
import time

BASE_URL = "http://localhost:8003"


def test_health():
    """Test health endpoint."""
    response = httpx.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    print("✓ Health check passed")
    return data


def test_model_info():
    """Test model info endpoint."""
    response = httpx.get(f"{BASE_URL}/model/info")
    assert response.status_code == 200
    data = response.json()
    print(f"✓ Model: {data['model_name']} on {data['model_device']}")
    return data


def test_single_inference():
    """Test single inference."""
    print("\n--- Test: Single Inference ---")
    response = httpx.post(
        f"{BASE_URL}/inference",
        json={
            "prompt": "What is containerization?",
            "max_tokens": 100,
        },
        timeout=30.0,
    )
    assert response.status_code == 200
    data = response.json()
    print(f"✓ Generated {data['tokens_generated']} tokens in {data['latency_ms']}ms")
    return data


def test_batch_inference():
    """Test batch inference."""
    print("\n--- Test: Batch Inference ---")
    response = httpx.post(
        f"{BASE_URL}/inference/batch",
        json={
            "prompts": [
                "What is Docker?",
                "What is Kubernetes?",
                "What is vLLM?",
            ],
            "max_tokens": 100,
        },
        timeout=60.0,
    )
    assert response.status_code == 200
    data = response.json()
    print(f"✓ Batch processed {len(data['results'])} prompts")
    print(f"  Total latency: {data['total_latency_ms']}ms")
    print(f"  Throughput: {data['throughput_per_second']} req/s")
    return data


def test_streaming():
    """Test streaming inference."""
    print("\n--- Test: Streaming Inference ---")
    response = httpx.post(
        f"{BASE_URL}/inference/stream",
        json={
            "prompt": "Write a short story about a robot",
            "max_tokens": 100,
        },
        timeout=30.0,
    )
    assert response.status_code == 200
    print(f"✓ Streaming response received")
    return response


def test_metrics():
    """Test metrics endpoint."""
    response = httpx.get(f"{BASE_URL}/metrics")
    assert response.status_code == 200
    print("✓ Metrics endpoint accessible")
    return response.text


def test_concurrent_requests():
    """Test concurrent requests."""
    print("\n--- Test: Concurrent Requests ---")
    import concurrent.futures

    def make_request(idx):
        start = time.time()
        response = httpx.post(
            f"{BASE_URL}/inference",
            json={"prompt": f"Concurrent test {idx}", "max_tokens": 50},
            timeout=30.0,
        )
        return {
            "index": idx,
            "status": response.status_code,
            "latency_ms": (time.time() - start) * 1000,
        }

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(make_request, i) for i in range(5)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    successful = [r for r in results if r["status"] == 200]
    print(f"✓ {len(successful)}/5 concurrent requests succeeded")

    return results


if __name__ == "__main__":
    print("=== AI Infrastructure — Inference Server Tests ===\n")

    try:
        test_health()
        test_model_info()
        test_single_inference()
        test_batch_inference()
        test_streaming()
        test_metrics()
        test_concurrent_requests()
        print("\n✓ All tests passed!")
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
