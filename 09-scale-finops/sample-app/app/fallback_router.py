"""Fallback Router — provider failover with timeout-based routing."""
import time
from datetime import datetime
from typing import Optional
from app.models import FallbackRoute, FallbackAction, ModelProvider


class FallbackRouter:
    """Route requests through a chain of providers with timeout-based fallback."""

    def __init__(self, timeout_seconds: float = 5.0, max_retries: int = 2):
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self._routes: list[FallbackRoute] = []
        self._stats: dict[str, dict] = {}

    def add_route(self, route: FallbackRoute):
        self._routes.append(route)
        self._routes.sort(key=lambda r: r.priority)
        self._stats[route.id] = {
            "total": 0, "success": 0, "timeout": 0, "error": 0
        }

    def route_request(self, query: str) -> dict:
        for route in self._routes:
            if not route.is_enabled:
                continue

            self._stats[route.id]["total"] += 1
            start = time.time()

            try:
                result = self._simulate_inference(route, query)
                elapsed = time.time() - start

                if elapsed > route.timeout_seconds:
                    self._stats[route.id]["timeout"] += 1
                    continue

                self._stats[route.id]["success"] += 1
                return {
                    "provider": route.provider.value,
                    "model": route.model,
                    "response": result,
                    "latency_ms": round(elapsed * 1000, 1),
                    "action": FallbackAction.FALLBACK_PROVIDER.value
                    if route.priority > 0 else "primary",
                    "fallback_chain_position": route.priority
                }
            except Exception:
                self._stats[route.id]["error"] += 1
                continue

        return {
            "provider": None,
            "model": None,
            "response": "All providers unavailable. Please try again later.",
            "latency_ms": 0,
            "action": FallbackAction.FAIL.value,
            "fallback_chain_position": -1
        }

    def _simulate_inference(self, route: FallbackRoute, query: str) -> str:
        base_latency = 0.1 + (route.priority * 0.2)
        time.sleep(min(base_latency, 0.05))

        if route.provider == ModelProvider.SELF_HOSTED:
            return f"[Self-Hosted {route.model}] Response to: {query[:50]}"
        return f"[{route.provider.value}/{route.model}] Response to: {query[:50]}"

    def get_stats(self) -> dict:
        return self._stats

    def list_routes(self) -> list[dict]:
        return [
            {
                "id": r.id,
                "name": r.name,
                "provider": r.provider.value,
                "model": r.model,
                "priority": r.priority,
                "timeout_seconds": r.timeout_seconds,
                "is_enabled": r.is_enabled
            }
            for r in self._routes
        ]

    def disable_route(self, route_id: str) -> bool:
        for r in self._routes:
            if r.id == route_id:
                r.is_enabled = False
                return True
        return False

    def enable_route(self, route_id: str) -> bool:
        for r in self._routes:
            if r.id == route_id:
                r.is_enabled = True
                return True
        return False
