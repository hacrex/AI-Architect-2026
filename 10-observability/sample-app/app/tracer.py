"""Distributed Tracer — follow requests across components with span trees."""
import uuid
from datetime import datetime
from typing import Optional
from app.models import Span, Trace, TraceStatus


class DistributedTracer:
    """Distributed tracing with span hierarchy and trace context propagation."""

    def __init__(self, sample_rate: float = 1.0, max_spans: int = 100):
        self.sample_rate = sample_rate
        self.max_spans = max_spans
        self._traces: dict[str, Trace] = {}
        self._active_spans: dict[str, Span] = {}

    def start_trace(self, operation: str, attributes: dict = None) -> str:
        trace_id = uuid.uuid4().hex[:16]
        trace = Trace(
            trace_id=trace_id,
            root_operation=operation,
            start_time=datetime.utcnow()
        )
        self._traces[trace_id] = trace
        self.start_span(trace_id, operation, attributes=attributes or {})
        return trace_id

    def start_span(self, trace_id: str, name: str, parent_span_id: str = "",
                   attributes: dict = None) -> str:
        span_id = uuid.uuid4().hex[:12]
        span = Span(
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=parent_span_id,
            name=name,
            start_time=datetime.utcnow(),
            attributes=attributes or {}
        )
        self._active_spans[span_id] = span
        trace = self._traces.get(trace_id)
        if trace:
            trace.spans.append(span)
        return span_id

    def end_span(self, span_id: str, status: TraceStatus = TraceStatus.OK,
                 attributes: dict = None):
        span = self._active_spans.pop(span_id, None)
        if not span:
            return
        span.end_time = datetime.utcnow()
        span.duration_ms = (span.end_time - span.start_time).total_seconds() * 1000
        span.status = status
        if attributes:
            span.attributes.update(attributes)

    def add_event(self, span_id: str, name: str, attributes: dict = None):
        span = self._active_spans.get(span_id)
        if span:
            span.events.append({
                "name": name,
                "timestamp": datetime.utcnow().isoformat(),
                "attributes": attributes or {}
            })

    def get_trace(self, trace_id: str) -> Optional[Trace]:
        trace = self._traces.get(trace_id)
        if trace and trace.spans:
            trace.total_duration_ms = sum(s.duration_ms for s in trace.spans)
            trace.end_time = max(
                (s.end_time for s in trace.spans if s.end_time),
                default=None
            )
        return trace

    def get_trace_tree(self, trace_id: str) -> dict:
        trace = self._traces.get(trace_id)
        if not trace:
            return {"error": f"Trace {trace_id} not found"}

        span_map = {s.span_id: s for s in trace.spans}
        root_spans = [s for s in trace.spans if not s.parent_span_id]

        def build_tree(span):
            children = [s for s in trace.spans if s.parent_span_id == span.span_id]
            return {
                "span_id": span.span_id,
                "name": span.name,
                "duration_ms": round(span.duration_ms, 2),
                "status": span.status.value,
                "attributes": span.attributes,
                "events": span.events,
                "children": [build_tree(c) for c in children]
            }

        return {
            "trace_id": trace_id,
            "root_operation": trace.root_operation,
            "total_duration_ms": round(trace.total_duration_ms, 2),
            "span_count": len(trace.spans),
            "status": trace.status.value,
            "tree": [build_tree(r) for r in root_spans]
        }

    def list_traces(self, limit: int = 50) -> list[dict]:
        traces = sorted(self._traces.values(),
                        key=lambda t: t.start_time, reverse=True)[:limit]
        return [
            {
                "trace_id": t.trace_id,
                "root_operation": t.root_operation,
                "total_duration_ms": round(t.total_duration_ms, 2),
                "span_count": len(t.spans),
                "status": t.status.value,
                "start_time": t.start_time.isoformat()
            }
            for t in traces
        ]

    def get_slowest_traces(self, limit: int = 10) -> list[dict]:
        traces = sorted(self._traces.values(),
                        key=lambda t: t.total_duration_ms, reverse=True)[:limit]
        return [
            {
                "trace_id": t.trace_id,
                "root_operation": t.root_operation,
                "total_duration_ms": round(t.total_duration_ms, 2),
                "span_count": len(t.spans)
            }
            for t in traces
        ]

    def get_trace_summary(self) -> dict:
        traces = list(self._traces.values())
        if not traces:
            return {"total_traces": 0, "avg_duration_ms": 0}
        durations = [t.total_duration_ms for t in traces if t.total_duration_ms > 0]
        errors = sum(1 for t in traces if t.status == TraceStatus.ERROR)
        return {
            "total_traces": len(traces),
            "avg_duration_ms": round(sum(durations) / len(durations), 2) if durations else 0,
            "max_duration_ms": round(max(durations), 2) if durations else 0,
            "error_traces": errors,
            "error_rate_pct": round(errors / len(traces) * 100, 2) if traces else 0,
            "total_spans": sum(len(t.spans) for t in traces)
        }
