"""Model router — multi-provider routing with fallback."""
import uuid
import random
from datetime import datetime
from typing import Optional
from app.models import ModelProvider, ModelRoute


class ModelRouter:
    """Route requests to the best model based on requirements."""

    def __init__(self):
        self._routes: list[ModelRoute] = [
            ModelRoute(
                provider=ModelProvider.OPENAI,
                model_name="gpt-4",
                endpoint="https://api.openai.com/v1/chat/completions",
                priority=1,
                max_tokens=8192,
                cost_per_1k_input=0.03,
                cost_per_1k_output=0.06
            ),
            ModelRoute(
                provider=ModelProvider.AZURE_OPENAI,
                model_name="gpt-4",
                endpoint="https://your-resource.openai.azure.com/",
                priority=2,
                max_tokens=8192,
                cost_per_1k_input=0.03,
                cost_per_1k_output=0.06
            ),
            ModelRoute(
                provider=ModelProvider.ANTHROPIC,
                model_name="claude-3-sonnet",
                endpoint="https://api.anthropic.com/v1/messages",
                priority=3,
                max_tokens=4096,
                cost_per_1k_input=0.015,
                cost_per_1k_output=0.075
            ),
            ModelRoute(
                provider=ModelProvider.SELF_HOSTED,
                model_name="llama-3-70b",
                endpoint="http://vllm-service:8000/v1/chat/completions",
                priority=4,
                max_tokens=4096,
                cost_per_1k_input=0.0,
                cost_per_1k_output=0.0
            ),
        ]
        self._failure_counts: dict[str, int] = {}
        self._circuit_open: dict[str, bool] = {}

    def select_model(self, requirements: dict = None) -> ModelRoute:
        reqs = requirements or {}
        max_cost = reqs.get("max_cost_per_1k", float("inf"))
        min_tokens = reqs.get("min_tokens", 0)
        preferred_provider = reqs.get("provider")

        available = []
        for route in self._routes:
            if self._circuit_open.get(route.model_name, False):
                continue
            if route.cost_per_1k_input > max_cost:
                continue
            if route.max_tokens < min_tokens:
                continue
            if preferred_provider and route.provider != preferred_provider:
                continue
            available.append(route)

        if not available:
            available = [r for r in self._routes if not self._circuit_open.get(r.model_name, False)]
        if not available:
            available = self._routes[:1]

        available.sort(key=lambda r: r.priority)
        return available[0]

    def record_failure(self, model_name: str):
        self._failure_counts[model_name] = self._failure_counts.get(model_name, 0) + 1
        if self._failure_counts[model_name] >= 3:
            self._circuit_open[model_name] = True

    def record_success(self, model_name: str):
        self._failure_counts[model_name] = 0
        self._circuit_open[model_name] = False

    def get_fallback_chain(self, primary: ModelRoute) -> list[ModelRoute]:
        chain = []
        for route in sorted(self._routes, key=lambda r: r.priority):
            if route.model_name != primary.model_name:
                chain.append(route)
        return chain

    def estimate_cost(self, model_name: str, input_tokens: int, output_tokens: int) -> float:
        for route in self._routes:
            if route.model_name == model_name:
                input_cost = (input_tokens / 1000) * route.cost_per_1k_input
                output_cost = (output_tokens / 1000) * route.cost_per_1k_output
                return round(input_cost + output_cost, 6)
        return 0.0

    def list_routes(self) -> list[dict]:
        return [
            {
                "provider": r.provider.value,
                "model": r.model_name,
                "priority": r.priority,
                "max_tokens": r.max_tokens,
                "cost_per_1k_input": r.cost_per_1k_input,
                "cost_per_1k_output": r.cost_per_1k_output,
                "circuit_open": self._circuit_open.get(r.model_name, False),
                "failure_count": self._failure_counts.get(r.model_name, 0)
            }
            for r in self._routes
        ]

    def get_stats(self) -> dict:
        return {
            "total_routes": len(self._routes),
            "circuit_open": sum(1 for v in self._circuit_open.values() if v),
            "total_failures": sum(self._failure_counts.values())
        }
