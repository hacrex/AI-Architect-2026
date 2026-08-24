"""Observability — tracing, metrics, and cost tracking."""
import uuid
import time
from datetime import datetime
from typing import Optional
from app.models import TraceSpan, RequestTrace, RequestStatus


class Tracer:
    """Distributed tracing for AI requests."""

    def __init__(self):
        self._traces: dict[str, RequestTrace] = {}

    def start_trace(self, request_id: str, user_id: str) -> RequestTrace:
        trace = RequestTrace(
            request_id=request_id,
            user_id=user_id
        )
        self._traces[request_id] = trace
        return trace

    def add_span(self, request_id: str, name: str, parent_id: str = None,
                 attributes: dict = None) -> Optional[TraceSpan]:
        trace = self._traces.get(request_id)
        if not trace:
            return None

        span = TraceSpan(
            span_id=f"span-{uuid.uuid4().hex[:8]}",
            parent_id=parent_id,
            name=name,
            attributes=attributes or {}
        )
        trace.spans.append(span)
        return span

    def end_span(self, request_id: str, span_id: str, status: str = "ok"):
        trace = self._traces.get(request_id)
        if not trace:
            return

        for span in trace.spans:
            if span.span_id == span_id:
                span.end_time = datetime.utcnow()
                span.status = status
                if span.start_time:
                    span.duration_ms = (span.end_time - span.start_time).total_seconds() * 1000
                break

    def complete_trace(self, request_id: str, model_used: str = "",
                       total_tokens: int = 0, total_cost: float = 0.0,
                       status: RequestStatus = RequestStatus.COMPLETED):
        trace = self._traces.get(request_id)
        if not trace:
            return

        trace.model_used = model_used
        trace.total_tokens = total_tokens
        trace.total_cost_usd = total_cost
        trace.status = status

        if trace.spans:
            earliest = min(s.start_time for s in trace.spans if s.start_time)
            latest = max(s.end_time for s in trace.spans if s.end_time) or datetime.utcnow()
            trace.total_latency_ms = (latest - earliest).total_seconds() * 1000

    def get_trace(self, request_id: str) -> Optional[RequestTrace]:
        return self._traces.get(request_id)

    def get_traces(self, user_id: str = None, limit: int = 50) -> list[RequestTrace]:
        traces = list(self._traces.values())
        if user_id:
            traces = [t for t in traces if t.user_id == user_id]
        return sorted(traces, key=lambda t: t.created_at, reverse=True)[:limit]


class MetricsCollector:
    """Collect and aggregate metrics."""

    def __init__(self):
        self._metrics: list[dict] = []

    def record(self, name: str, value: float, tags: dict = None):
        self._metrics.append({
            "name": name,
            "value": value,
            "tags": tags or {},
            "timestamp": datetime.utcnow().isoformat()
        })

    def get_metric(self, name: str, limit: int = 100) -> list[dict]:
        return [m for m in self._metrics if m["name"] == name][-limit:]

    def get_summary(self, name: str) -> dict:
        values = [m["value"] for m in self._metrics if m["name"] == name]
        if not values:
            return {"name": name, "count": 0}

        return {
            "name": name,
            "count": len(values),
            "mean": round(sum(values) / len(values), 4),
            "min": round(min(values), 4),
            "max": round(max(values), 4),
            "p95": round(sorted(values)[int(len(values) * 0.95)] if len(values) > 1 else values[0], 4)
        }

    def get_all_summaries(self) -> dict:
        names = set(m["name"] for m in self._metrics)
        return {name: self.get_summary(name) for name in names}


class CostTracker:
    """Track AI costs per request, model, and user."""

    def __init__(self):
        self._costs: list[dict] = []

    def record(self, request_id: str, user_id: str, model: str,
               provider: str, input_tokens: int, output_tokens: int,
               cost_usd: float):
        self._costs.append({
            "request_id": request_id,
            "user_id": user_id,
            "model": model,
            "provider": provider,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost_usd": cost_usd,
            "timestamp": datetime.utcnow().isoformat()
        })

    def get_total_cost(self, time_range_hours: int = 24) -> float:
        cutoff = datetime.utcnow().timestamp() - (time_range_hours * 3600)
        return sum(
            c["cost_usd"] for c in self._costs
            if datetime.fromisoformat(c["timestamp"]).timestamp() >= cutoff
        )

    def get_cost_by_model(self) -> dict:
        by_model = {}
        for c in self._costs:
            model = c["model"]
            if model not in by_model:
                by_model[model] = {"total_cost": 0.0, "total_requests": 0, "total_tokens": 0}
            by_model[model]["total_cost"] += c["cost_usd"]
            by_model[model]["total_requests"] += 1
            by_model[model]["total_tokens"] += c["input_tokens"] + c["output_tokens"]
        return by_model

    def get_cost_by_user(self) -> dict:
        by_user = {}
        for c in self._costs:
            user = c["user_id"]
            if user not in by_user:
                by_user[user] = {"total_cost": 0.0, "total_requests": 0}
            by_user[user]["total_cost"] += c["cost_usd"]
            by_user[user]["total_requests"] += 1
        return by_user

    def get_budget_status(self, user_id: str, budget_usd: float) -> dict:
        user_cost = sum(c["cost_usd"] for c in self._costs if c["user_id"] == user_id)
        return {
            "user_id": user_id,
            "spent_usd": round(user_cost, 4),
            "budget_usd": budget_usd,
            "remaining_usd": round(budget_usd - user_cost, 4),
            "utilization_pct": round((user_cost / budget_usd) * 100, 2) if budget_usd > 0 else 0
        }


class ObservabilityService:
    """Complete observability subsystem."""

    def __init__(self):
        self.tracer = Tracer()
        self.metrics = MetricsCollector()
        self.cost_tracker = CostTracker()

    def record_request(self, request_id: str, user_id: str, model: str,
                       provider: str, input_tokens: int, output_tokens: int,
                       latency_ms: float, cost_usd: float, status: str = "completed"):
        self.metrics.record("request.latency_ms", latency_ms, {"model": model, "provider": provider})
        self.metrics.record("request.tokens", input_tokens + output_tokens, {"model": model})
        self.metrics.record("request.cost_usd", cost_usd, {"model": model})

        self.cost_tracker.record(
            request_id=request_id,
            user_id=user_id,
            model=model,
            provider=provider,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost_usd
        )

    def get_dashboard(self) -> dict:
        return {
            "metrics_summary": self.metrics.get_all_summaries(),
            "cost_by_model": self.cost_tracker.get_cost_by_model(),
            "total_cost_24h": self.cost_tracker.get_total_cost(24),
            "active_traces": len(self.tracer.get_traces(limit=1000))
        }
