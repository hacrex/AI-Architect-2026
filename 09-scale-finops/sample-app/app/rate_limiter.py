"""Rate Limiter — token bucket algorithm for request throttling."""
import time
from datetime import datetime
from app.models import RateLimitBucket


class RateLimiter:
    """Token bucket rate limiter with per-user and global limits."""

    def __init__(self, capacity: int = 60, refill_rate: float = 1.0):
        self.default_capacity = capacity
        self.default_refill_rate = refill_rate
        self._buckets: dict[str, RateLimitBucket] = {}

    def _get_or_create_bucket(self, name: str) -> RateLimitBucket:
        if name not in self._buckets:
            self._buckets[name] = RateLimitBucket(
                name=name,
                capacity=self.default_capacity,
                refill_rate_per_sec=self.default_refill_rate,
                tokens=float(self.default_capacity)
            )
        return self._buckets[name]

    def _refill(self, bucket: RateLimitBucket):
        now = time.time()
        elapsed = now - bucket.last_refill.timestamp()
        new_tokens = elapsed * bucket.refill_rate_per_sec
        bucket.tokens = min(float(bucket.capacity), bucket.tokens + new_tokens)
        bucket.last_refill = datetime.utcnow()

    def allow(self, name: str = "global", tokens_needed: int = 1) -> dict:
        bucket = self._get_or_create_bucket(name)
        self._refill(bucket)

        if bucket.tokens >= tokens_needed:
            bucket.tokens -= tokens_needed
            return {
                "allowed": True,
                "remaining": int(bucket.tokens),
                "capacity": bucket.capacity,
                "retry_after_seconds": 0
            }
        else:
            retry_after = (tokens_needed - bucket.tokens) / bucket.refill_rate_per_sec if bucket.refill_rate_per_sec > 0 else float('inf')
            return {
                "allowed": False,
                "remaining": 0,
                "capacity": bucket.capacity,
                "retry_after_seconds": round(retry_after, 2)
            }

    def configure_bucket(self, name: str, capacity: int, refill_rate: float):
        self._buckets[name] = RateLimitBucket(
            name=name,
            capacity=capacity,
            refill_rate_per_sec=refill_rate,
            tokens=float(capacity)
        )

    def get_status(self, name: str = "global") -> dict:
        bucket = self._get_or_create_bucket(name)
        self._refill(bucket)
        return {
            "name": bucket.name,
            "tokens": round(bucket.tokens, 2),
            "capacity": bucket.capacity,
            "refill_rate_per_sec": bucket.refill_rate_per_sec,
            "utilization_pct": round((1 - bucket.tokens / bucket.capacity) * 100, 1)
        }

    def list_buckets(self) -> list[dict]:
        return [self.get_status(b.name) for b in self._buckets.values()]

    def reset(self, name: str = "global"):
        if name in self._buckets:
            self._buckets[name].tokens = float(self._buckets[name].capacity)
