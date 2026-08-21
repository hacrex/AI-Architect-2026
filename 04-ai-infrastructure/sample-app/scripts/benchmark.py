"""Benchmark script for inference server."""

import httpx
import time
import json
from typing import List, Dict


BASE_URL = "http://localhost:8003"


def benchmark_single_request(num_requests: int = 10) -> Dict:
    """Benchmark single request latency."""
    print(f"\n=== Single Request Benchmark ({num_requests} requests) ===")

    latencies = []
    tokens_generated = []

    for i in range(num_requests):
        start = time.time()
        response = httpx.post(
            f"{BASE_URL}/inference",
            json={
                "prompt": f"What is containerization? Request {i+1}",
                "max_tokens": 100,
            },
            timeout=30.0,
        )
        latency = (time.time() - start) * 1000

        if response.status_code == 200:
            data = response.json()
            latencies.append(latency)
            tokens_generated.append(data["tokens_generated"])
            print(f"  Request {i+1}: {latency:.2f}ms, {data['tokens_generated']} tokens")
        else:
            print(f"  Request {i+1}: FAILED ({response.status_code})")

    if latencies:
        avg_latency = sum(latencies) / len(latencies)
        avg_tokens = sum(tokens_generated) / len(tokens_generated)
        throughput = avg_tokens / (avg_latency / 1000) if avg_latency > 0 else 0

        return {
            "test": "single_request",
            "requests": num_requests,
            "avg_latency_ms": round(avg_latency, 2),
            "avg_tokens": round(avg_tokens, 2),
            "throughput_tokens_per_sec": round(throughput, 2),
        }
    return {"test": "single_request", "error": "No successful requests"}


def benchmark_batch_request(batch_sizes: List[int] = [1, 4, 8, 16]) -> List[Dict]:
    """Benchmark batch request performance."""
    print("\n=== Batch Request Benchmark ===")

    results = []

    for batch_size in batch_sizes:
        prompts = [f"What is Docker? Batch item {i}" for i in range(batch_size)]

        start = time.time()
        response = httpx.post(
            f"{BASE_URL}/inference/batch",
            json={
                "prompts": prompts,
                "max_tokens": 100,
            },
            timeout=60.0,
        )
        total_latency = (time.time() - start) * 1000

        if response.status_code == 200:
            data = response.json()
            result = {
                "test": "batch_request",
                "batch_size": batch_size,
                "total_latency_ms": round(total_latency, 2),
                "avg_latency_ms": data["avg_latency_ms"],
                "throughput_per_second": data["throughput_per_second"],
            }
            results.append(result)
            print(f"  Batch {batch_size}: {total_latency:.2f}ms total, {data['throughput_per_second']:.2f} req/s")
        else:
            print(f"  Batch {batch_size}: FAILED ({response.status_code})")

    return results


def benchmark_concurrency(num_concurrent: int = 10) -> Dict:
    """Benchmark concurrent requests."""
    print(f"\n=== Concurrency Benchmark ({num_concurrent} concurrent) ===")

    import concurrent.futures

    def make_request(idx: int):
        start = time.time()
        response = httpx.post(
            f"{BASE_URL}/inference",
            json={
                "prompt": f"What is Kubernetes? Concurrent request {idx}",
                "max_tokens": 100,
            },
            timeout=30.0,
        )
        latency = (time.time() - start) * 1000
        return {
            "index": idx,
            "latency_ms": latency,
            "success": response.status_code == 200,
        }

    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent) as executor:
        futures = [executor.submit(make_request, i) for i in range(num_concurrent)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    total_time = (time.time() - start) * 1000

    successful = [r for r in results if r["success"]]
    latencies = [r["latency_ms"] for r in successful]

    if latencies:
        avg_latency = sum(latencies) / len(latencies)
        throughput = num_concurrent / (total_time / 1000) if total_time > 0 else 0

        return {
            "test": "concurrency",
            "concurrent_requests": num_concurrent,
            "successful": len(successful),
            "failed": num_concurrent - len(successful),
            "total_time_ms": round(total_time, 2),
            "avg_latency_ms": round(avg_latency, 2),
            "throughput_requests_per_sec": round(throughput, 2),
        }
    return {"test": "concurrency", "error": "No successful requests"}


def run_all_benchmarks():
    """Run all benchmarks."""
    print("=== AI Infrastructure — Inference Server Benchmark ===")
    print(f"Target: {BASE_URL}\n")

    # Check server health
    try:
        health = httpx.get(f"{BASE_URL}/health")
        if health.status_code != 200:
            print("Server is not healthy. Aborting benchmarks.")
            return
        print("Server is healthy. Starting benchmarks...")
    except Exception as e:
        print(f"Cannot connect to server: {e}")
        return

    all_results = []

    # Single request benchmark
    result = benchmark_single_request(10)
    all_results.append(result)

    # Batch benchmark
    results = benchmark_batch_request([1, 4, 8, 16])
    all_results.extend(results)

    # Concurrency benchmark
    for concurrency in [1, 5, 10, 25]:
        result = benchmark_concurrency(concurrency)
        all_results.append(result)

    # Save results
    with open("benchmarks/results.json", "w") as f:
        json.dump(all_results, f, indent=2)

    print("\n=== Benchmark Complete ===")
    print("Results saved to benchmarks/results.json")


if __name__ == "__main__":
    run_all_benchmarks()
