"""LLM Trace — observability for model calls including tokens, latency, and cost."""
import uuid
import time
from datetime import datetime
from typing import Optional
from app.models import LLMCall
import config.settings as settings


class LLMTracer:
    """Trace and analyze LLM calls with token, latency, and cost visibility."""

    def __init__(self):
        self._calls: list[LLMCall] = []
        self._by_provider: dict[str, list[LLMCall]] = {}
        self._by_model: dict[str, list[LLMCall]] = {}

    def record_call(self, provider: str, model: str, input_tokens: int,
                    output_tokens: int, latency_ms: float, ttft_ms: float = 0.0,
                    prompt: str = "", response: str = "",
                    temperature: float = 0.0, max_tokens: int = 0,
                    finish_reason: str = "stop", trace_id: str = "",
                    span_id: str = "") -> LLMCall:
        cost = self._calculate_cost(provider, input_tokens, output_tokens)
        call = LLMCall(
            trace_id=trace_id or uuid.uuid4().hex[:16],
            span_id=span_id or uuid.uuid4().hex[:12],
            provider=provider,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            ttft_ms=ttft_ms,
            latency_ms=latency_ms,
            cost_usd=cost,
            prompt_preview=prompt[:200] if prompt else "",
            response_preview=response[:200] if response else "",
            temperature=temperature,
            max_tokens=max_tokens,
            finish_reason=finish_reason
        )
        self._calls.append(call)
        self._by_provider.setdefault(provider, []).append(call)
        self._by_model.setdefault(model, []).append(call)
        return call

    def _calculate_cost(self, provider: str, input_tokens: int, output_tokens: int) -> float:
        input_cost = (input_tokens / 1_000_000) * settings.LLM_COST_PER_1M_INPUT
        output_cost = (output_tokens / 1_000_000) * settings.LLM_COST_PER_1M_OUTPUT
        return round(input_cost + output_cost, 8)

    def get_summary(self) -> dict:
        if not self._calls:
            return {"total_calls": 0}
        latencies = [c.latency_ms for c in self._calls]
        ttfts = [c.ttft_ms for c in self._calls if c.ttft_ms > 0]
        tokens = [c.total_tokens for c in self._calls]
        costs = [c.cost_usd for c in self._calls]
        return {
            "total_calls": len(self._calls),
            "total_tokens": sum(tokens),
            "total_cost_usd": round(sum(costs), 6),
            "avg_latency_ms": round(sum(latencies) / len(latencies), 1),
            "p95_latency_ms": round(sorted(latencies)[int(len(latencies) * 0.95)] if latencies else 0, 1),
            "avg_ttft_ms": round(sum(ttfts) / len(ttfts), 1) if ttfts else 0,
            "avg_tokens_per_call": round(sum(tokens) / len(tokens), 0) if tokens else 0,
            "cost_per_call": round(sum(costs) / len(costs), 8) if costs else 0,
        }

    def get_by_provider(self) -> dict:
        result = {}
        for provider, calls in self._by_provider.items():
            latencies = [c.latency_ms for c in calls]
            result[provider] = {
                "calls": len(calls),
                "total_tokens": sum(c.total_tokens for c in calls),
                "total_cost_usd": round(sum(c.cost_usd for c in calls), 6),
                "avg_latency_ms": round(sum(latencies) / len(latencies), 1) if latencies else 0,
            }
        return result

    def get_by_model(self) -> dict:
        result = {}
        for model, calls in self._by_model.items():
            latencies = [c.latency_ms for c in calls]
            result[model] = {
                "calls": len(calls),
                "total_tokens": sum(c.total_tokens for c in calls),
                "total_cost_usd": round(sum(c.cost_usd for c in calls), 6),
                "avg_latency_ms": round(sum(latencies) / len(latencies), 1) if latencies else 0,
            }
        return result

    def get_token_distribution(self) -> dict:
        input_tokens = [c.input_tokens for c in self._calls]
        output_tokens = [c.output_tokens for c in self._calls]
        return {
            "input": {
                "min": min(input_tokens) if input_tokens else 0,
                "max": max(input_tokens) if input_tokens else 0,
                "avg": round(sum(input_tokens) / len(input_tokens), 0) if input_tokens else 0,
                "total": sum(input_tokens),
            },
            "output": {
                "min": min(output_tokens) if output_tokens else 0,
                "max": max(output_tokens) if output_tokens else 0,
                "avg": round(sum(output_tokens) / len(output_tokens), 0) if output_tokens else 0,
                "total": sum(output_tokens),
            }
        }

    def list_calls(self, provider: str = None, model: str = None,
                   limit: int = 50) -> list[dict]:
        calls = self._calls
        if provider:
            calls = [c for c in calls if c.provider == provider]
        if model:
            calls = [c for c in calls if c.model == model]
        return [
            {
                "trace_id": c.trace_id,
                "provider": c.provider,
                "model": c.model,
                "input_tokens": c.input_tokens,
                "output_tokens": c.output_tokens,
                "latency_ms": c.latency_ms,
                "ttft_ms": c.ttft_ms,
                "cost_usd": c.cost_usd,
                "finish_reason": c.finish_reason,
                "timestamp": c.timestamp.isoformat()
            }
            for c in calls[-limit:]
        ]
