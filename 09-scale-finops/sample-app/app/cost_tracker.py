"""Cost Tracker — AI FinOps cost monitoring and optimization."""
import uuid
from datetime import datetime, timedelta
from app.models import CostRecord, CostSummary, ModelProvider
import config.settings as settings


class CostTracker:
    """Track and analyze AI infrastructure costs."""

    def __init__(self):
        self._records: list[CostRecord] = []
        self._daily_budget = settings.MONTHLY_BUDGET_LIMIT_USD / 30

    def record_request(self, provider: ModelProvider, model: str,
                       input_tokens: int, output_tokens: int,
                       embedding_tokens: int = 0, vector_searches: int = 0,
                       gpu_seconds: float = 0.0, request_id: str = "",
                       cached: bool = False) -> CostRecord:
        cost = self._calculate_cost(
            provider, input_tokens, output_tokens,
            embedding_tokens, vector_searches, gpu_seconds
        )

        record = CostRecord(
            id=f"cost-{uuid.uuid4().hex[:8]}",
            provider=provider,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            embedding_tokens=embedding_tokens,
            vector_searches=vector_searches,
            gpu_seconds=gpu_seconds,
            total_cost_usd=cost,
            request_id=request_id,
            cached=cached
        )
        self._records.append(record)
        return record

    def _calculate_cost(self, provider: ModelProvider,
                        input_tokens: int, output_tokens: int,
                        embedding_tokens: int, vector_searches: int,
                        gpu_seconds: float) -> float:
        model_cost = (
            (input_tokens / 1_000_000) * settings.COST_PER_1M_INPUT_TOKENS +
            (output_tokens / 1_000_000) * settings.COST_PER_1M_OUTPUT_TOKENS
        )
        embedding_cost = (embedding_tokens / 1_000_000) * settings.COST_PER_1M_EMBEDDING_TOKENS
        retrieval_cost = (vector_searches / 1_000_000) * settings.COST_PER_1M_VECTOR_SEARCH
        gpu_cost = (gpu_seconds / 3600) * settings.GPU_COST_PER_HOUR
        return round(model_cost + embedding_cost + retrieval_cost + gpu_cost, 8)

    def get_summary(self, period: str = "all") -> CostSummary:
        now = datetime.utcnow()
        if period == "day":
            cutoff = now - timedelta(days=1)
        elif period == "week":
            cutoff = now - timedelta(weeks=1)
        elif period == "month":
            cutoff = now - timedelta(days=30)
        else:
            cutoff = datetime.min

        records = [r for r in self._records if r.timestamp >= cutoff]

        total_cost = sum(r.total_cost_usd for r in records)
        model_cost = sum(
            (r.input_tokens / 1_000_000) * settings.COST_PER_1M_INPUT_TOKENS +
            (r.output_tokens / 1_000_000) * settings.COST_PER_1M_OUTPUT_TOKENS
            for r in records
        )
        gpu_cost = sum((r.gpu_seconds / 3600) * settings.GPU_COST_PER_HOUR for r in records)
        embedding_cost = sum(
            (r.embedding_tokens / 1_000_000) * settings.COST_PER_1M_EMBEDDING_TOKENS
            for r in records
        )
        retrieval_cost = sum(
            (r.vector_searches / 1_000_000) * settings.COST_PER_1M_VECTOR_SEARCH
            for r in records
        )

        cached = [r for r in records if r.cached]
        cache_savings = sum(r.total_cost_usd for r in cached)
        total_requests = len(records)
        cost_per_request = total_cost / total_requests if total_requests > 0 else 0

        return CostSummary(
            period=period,
            total_cost_usd=round(total_cost, 6),
            model_cost_usd=round(model_cost, 6),
            gpu_cost_usd=round(gpu_cost, 6),
            embedding_cost_usd=round(embedding_cost, 6),
            retrieval_cost_usd=round(retrieval_cost, 6),
            total_requests=total_requests,
            cached_requests=len(cached),
            cache_savings_usd=round(cache_savings, 6),
            cost_per_request=round(cost_per_request, 8),
            cost_per_user=round(cost_per_request, 8)
        )

    def get_cost_by_provider(self) -> dict:
        by_provider = {}
        for r in self._records:
            p = r.provider.value
            if p not in by_provider:
                by_provider[p] = {"cost": 0, "requests": 0, "tokens": 0}
            by_provider[p]["cost"] += r.total_cost_usd
            by_provider[p]["requests"] += 1
            by_provider[p]["tokens"] += r.input_tokens + r.output_tokens
        return {
            k: {
                "cost_usd": round(v["cost"], 6),
                "requests": v["requests"],
                "total_tokens": v["tokens"]
            }
            for k, v in by_provider.items()
        }

    def get_cost_by_model(self) -> dict:
        by_model = {}
        for r in self._records:
            m = r.model
            if m not in by_model:
                by_model[m] = {"cost": 0, "requests": 0}
            by_model[m]["cost"] += r.total_cost_usd
            by_model[m]["requests"] += 1
        return {
            k: {"cost_usd": round(v["cost"], 6), "requests": v["requests"]}
            for k, v in by_model.items()
        }

    def check_budget(self) -> dict:
        today_cost = self.get_summary("day").total_cost_usd
        return {
            "daily_budget_usd": round(self._daily_budget, 2),
            "today_cost_usd": today_cost,
            "remaining_usd": round(self._daily_budget - today_cost, 6),
            "over_budget": today_cost > self._daily_budget,
            "utilization_pct": round((today_cost / self._daily_budget) * 100, 1)
            if self._daily_budget > 0 else 0
        }

    def list_records(self, limit: int = 50) -> list[dict]:
        recent = sorted(self._records, key=lambda r: r.timestamp, reverse=True)[:limit]
        return [
            {
                "id": r.id,
                "provider": r.provider.value,
                "model": r.model,
                "input_tokens": r.input_tokens,
                "output_tokens": r.output_tokens,
                "cost_usd": r.total_cost_usd,
                "cached": r.cached,
                "timestamp": r.timestamp.isoformat()
            }
            for r in recent
        ]
