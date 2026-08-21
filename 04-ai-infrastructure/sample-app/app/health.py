from typing import Dict, Any, List
from collections import deque
import time
import statistics


class MetricsCollector:
    """Collect and aggregate inference metrics."""

    def __init__(self, window_size: int = 1000):
        self.window_size = window_size
        self.total_requests = 0
        self.total_tokens = 0
        self.latencies: deque = deque(maxlen=window_size)
        self.tokens_per_request: deque = deque(maxlen=window_size)
        self.start_time = time.time()

    def record_request(
        self,
        latency_ms: float,
        tokens_generated: int,
        batch_size: int = 1,
    ):
        """Record a single request's metrics."""
        self.total_requests += 1
        self.total_tokens += tokens_generated
        self.latencies.append(latency_ms)
        self.tokens_per_request.append(tokens_generated)

    def get_summary(self) -> Dict[str, Any]:
        """Get metrics summary."""
        if not self.latencies:
            return {
                "total_requests": self.total_requests,
                "total_tokens": self.total_tokens,
                "avg_latency_ms": 0,
                "avg_tokens_per_second": 0,
                "p50_latency_ms": 0,
                "p95_latency_ms": 0,
                "p99_latency_ms": 0,
            }

        latencies = list(self.latencies)
        tokens = list(self.tokens_per_request)

        # Calculate percentiles
        sorted_latencies = sorted(latencies)
        p50_idx = int(len(sorted_latencies) * 0.5)
        p95_idx = int(len(sorted_latencies) * 0.95)
        p99_idx = int(len(sorted_latencies) * 0.99)

        avg_latency = statistics.mean(latencies)
        avg_tokens = statistics.mean(tokens) if tokens else 0

        # Tokens per second (assuming avg latency in ms)
        tokens_per_second = (avg_tokens / (avg_latency / 1000)) if avg_latency > 0 else 0

        return {
            "total_requests": self.total_requests,
            "total_tokens": self.total_tokens,
            "avg_latency_ms": round(avg_latency, 2),
            "avg_tokens_per_second": round(tokens_per_second, 2),
            "p50_latency_ms": round(sorted_latencies[p50_idx], 2),
            "p95_latency_ms": round(sorted_latencies[p95_idx], 2),
            "p99_latency_ms": round(sorted_latencies[p99_idx], 2),
            "uptime_seconds": round(time.time() - self.start_time, 2),
        }

    def get_prometheus_metrics(self) -> str:
        """Format metrics for Prometheus scraping."""
        summary = self.get_summary()

        lines = [
            "# HELP inference_requests_total Total number of inference requests",
            "# TYPE inference_requests_total counter",
            f"inference_requests_total {summary['total_requests']}",
            "",
            "# HELP inference_tokens_total Total number of tokens generated",
            "# TYPE inference_tokens_total counter",
            f"inference_tokens_total {summary['total_tokens']}",
            "",
            "# HELP inference_latency_ms Inference latency in milliseconds",
            "# TYPE inference_latency_ms summary",
            f'inference_latency_ms{{quantile="0.5"}} {summary["p50_latency_ms"]}',
            f'inference_latency_ms{{quantile="0.95"}} {summary["p95_latency_ms"]}',
            f'inference_latency_ms{{quantile="0.99"}} {summary["p99_latency_ms"]}',
            f'inference_latency_ms_sum {summary["avg_latency_ms"] * summary["total_requests"]}',
            f"inference_latency_ms_count {summary['total_requests']}",
            "",
            "# HELP inference_tokens_per_second Tokens generated per second",
            "# TYPE inference_tokens_per_second gauge",
            f"inference_tokens_per_second {summary['avg_tokens_per_second']}",
        ]

        return "\n".join(lines)
