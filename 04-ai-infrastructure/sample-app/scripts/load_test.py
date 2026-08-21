"""Load testing script for inference server."""

import httpx
import time
import statistics
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed


BASE_URL = "http://localhost:8003"


def load_test(
    num_requests: int = 100,
    concurrent_users: int = 10,
    ramp_up_seconds: int = 5,
) -> Dict:
    """Run a load test against the inference server."""
    print(f"\n=== Load Test ===")
    print(f"Requests: {num_requests}")
    print(f"Concurrent users: {concurrent_users}")
    print(f"Ramp-up: {ramp_up_seconds}s")

    results: List[Dict] = []
    start_time = time.time()

    def make_request(idx: int) -> Dict:
        # Add delay for ramp-up
        delay = (idx / num_requests) * ramp_up_seconds
        time.sleep(max(0, delay - (time.time() - start_time)))

        request_start = time.time()
        try:
            response = httpx.post(
                f"{BASE_URL}/inference",
                json={
                    "prompt": f"Explain microservices architecture. Request {idx}",
                    "max_tokens": 150,
                },
                timeout=60.0,
            )
            latency = (time.time() - request_start) * 1000

            return {
                "index": idx,
                "latency_ms": latency,
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "tokens": response.json().get("tokens_generated", 0) if response.status_code == 200 else 0,
            }
        except Exception as e:
            latency = (time.time() - request_start) * 1000
            return {
                "index": idx,
                "latency_ms": latency,
                "success": False,
                "status_code": 0,
                "error": str(e),
                "tokens": 0,
            }

    # Execute load test
    with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
        futures = [executor.submit(make_request, i) for i in range(num_requests)]
        results = [f.result() for f in as_completed(futures)]

    total_time = time.time() - start_time

    # Calculate statistics
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    latencies = [r["latency_ms"] for r in successful]
    tokens = [r["tokens"] for r in successful]

    if latencies:
        sorted_latencies = sorted(latencies)
        p50_idx = int(len(sorted_latencies) * 0.5)
        p95_idx = int(len(sorted_latencies) * 0.95)
        p99_idx = int(len(sorted_latencies) * 0.99)

        summary = {
            "total_requests": num_requests,
            "successful": len(successful),
            "failed": len(failed),
            "total_time_seconds": round(total_time, 2),
            "requests_per_second": round(num_requests / total_time, 2),
            "avg_latency_ms": round(statistics.mean(latencies), 2),
            "p50_latency_ms": round(sorted_latencies[p50_idx], 2),
            "p95_latency_ms": round(sorted_latencies[p95_idx], 2),
            "p99_latency_ms": round(sorted_latencies[p99_idx], 2),
            "min_latency_ms": round(min(latencies), 2),
            "max_latency_ms": round(max(latencies), 2),
            "total_tokens": sum(tokens),
            "tokens_per_second": round(sum(tokens) / total_time, 2),
        }
    else:
        summary = {"error": "No successful requests"}

    # Print results
    print("\n=== Results ===")
    for key, value in summary.items():
        print(f"  {key}: {value}")

    return summary


if __name__ == "__main__":
    # Run load test with increasing concurrency
    for concurrency in [1, 5, 10, 25]:
        print(f"\n{'='*50}")
        print(f"Testing with {concurrency} concurrent users")
        result = load_test(
            num_requests=50,
            concurrent_users=concurrency,
            ramp_up_seconds=2,
        )
