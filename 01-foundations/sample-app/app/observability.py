from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class MetricsCollector:
    """Simple metrics collector for observability."""

    def __init__(self):
        self.request_count = 0
        self.successful_queries = 0
        self.failed_queries = 0
        self.latencies: List[float] = []
        self.token_usage: List[int] = []
        self.hourly_requests: Dict[str, int] = defaultdict(int)
        self.start_time = datetime.now()

    def record_request_latency(self, latency: float):
        self.request_count += 1
        self.latencies.append(latency)

        hour_key = datetime.now().strftime("%Y-%m-%d-%H")
        self.hourly_requests[hour_key] += 1

    def record_successful_query(self):
        self.successful_queries += 1

    def record_failed_query(self):
        self.failed_queries += 1

    def record_token_usage(self, tokens: int):
        self.token_usage.append(tokens)

    def get_summary(self) -> dict:
        avg_latency = (
            sum(self.latencies) / len(self.latencies) if self.latencies else 0
        )
        p95_latency = (
            sorted(self.latencies)[int(len(self.latencies) * 0.95)]
            if self.latencies
            else 0
        )
        total_tokens = sum(self.token_usage)

        uptime = datetime.now() - self.start_time

        return {
            "uptime_seconds": int(uptime.total_seconds()),
            "total_requests": self.request_count,
            "successful_queries": self.successful_queries,
            "failed_queries": self.failed_queries,
            "success_rate": (
                round(self.successful_queries / max(self.request_count, 1) * 100, 2)
            ),
            "average_latency_ms": round(avg_latency * 1000, 2),
            "p95_latency_ms": round(p95_latency * 1000, 2),
            "total_tokens_used": total_tokens,
            "average_tokens_per_query": (
                round(total_tokens / max(self.successful_queries, 1), 2)
            ),
            "hourly_breakdown": dict(self.hourly_requests),
        }
