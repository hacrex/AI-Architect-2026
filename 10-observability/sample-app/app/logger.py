"""Structured Logger — JSON-structured logging with context propagation."""
import json
import uuid
from datetime import datetime
from typing import Optional
from app.models import LogEntry


class StructuredLogger:
    """Structured logging with trace context and component tagging."""

    def __init__(self, level: str = "INFO"):
        self.level = level.upper()
        self._entries: list[LogEntry] = []
        self._context: dict[str, str] = {}
        self._level_hierarchy = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3, "CRITICAL": 4}

    def set_context(self, **kwargs):
        self._context.update(kwargs)

    def clear_context(self):
        self._context.clear()

    def _should_log(self, level: str) -> bool:
        return self._level_hierarchy.get(level, 0) >= self._level_hierarchy.get(self.level, 0)

    def _log(self, level: str, message: str, component: str = "",
             trace_id: str = "", span_id: str = "", **attributes):
        if not self._should_log(level):
            return None

        attrs = {**self._context, **attributes}
        entry = LogEntry(
            level=level,
            message=message,
            component=component,
            trace_id=trace_id or self._context.get("trace_id", ""),
            span_id=span_id or self._context.get("span_id", ""),
            attributes=attrs
        )
        self._entries.append(entry)
        return entry

    def debug(self, message: str, **kwargs):
        return self._log("DEBUG", message, **kwargs)

    def info(self, message: str, **kwargs):
        return self._log("INFO", message, **kwargs)

    def warning(self, message: str, **kwargs):
        return self._log("WARNING", message, **kwargs)

    def error(self, message: str, **kwargs):
        return self._log("ERROR", message, **kwargs)

    def critical(self, message: str, **kwargs):
        return self._log("CRITICAL", message, **kwargs)

    def log_llm_call(self, provider: str, model: str, input_tokens: int,
                     output_tokens: int, latency_ms: float, **kwargs):
        return self._log(
            "INFO",
            f"LLM call: {provider}/{model} ({input_tokens}+{output_tokens} tokens, {latency_ms:.1f}ms)",
            component="llm",
            provider=provider, model=model,
            input_tokens=input_tokens, output_tokens=output_tokens,
            latency_ms=latency_ms, **kwargs
        )

    def log_retrieval(self, query: str, documents_found: int, latency_ms: float,
                      relevance_score: float = 0.0, **kwargs):
        return self._log(
            "INFO",
            f"Retrieval: {documents_found} docs in {latency_ms:.1f}ms (relevance: {relevance_score:.2f})",
            component="rag",
            query_preview=query[:80], documents_found=documents_found,
            latency_ms=latency_ms, relevance_score=relevance_score, **kwargs
        )

    def log_agent_step(self, agent: str, step: int, action: str,
                       tool: str = "", duration_ms: float = 0.0, **kwargs):
        return self._log(
            "INFO",
            f"Agent '{agent}' step {step}: {action}" + (f" ({tool}, {duration_ms:.1f}ms)" if tool else ""),
            component="agent",
            agent=agent, step=step, action=action,
            tool=tool, duration_ms=duration_ms, **kwargs
        )

    def log_alert(self, alert_name: str, severity: str, message: str, **kwargs):
        return self._log(
            severity.upper(),
            f"ALERT [{severity.upper()}] {alert_name}: {message}",
            component="alerting",
            alert_name=alert_name, **kwargs
        )

    def log_slo(self, slo_name: str, state: str, current: float, target: float, **kwargs):
        return self._log(
            "WARNING" if state != "healthy" else "INFO",
            f"SLO '{slo_name}': {state} (current: {current:.2f}, target: {target:.2f})",
            component="slo",
            slo_name=slo_name, state=state, current=current, target=target, **kwargs
        )

    def get_entries(self, level: str = None, component: str = None,
                    limit: int = 100) -> list[LogEntry]:
        entries = self._entries
        if level:
            entries = [e for e in entries if e.level == level.upper()]
        if component:
            entries = [e for e in entries if e.component == component]
        return entries[-limit:]

    def get_summary(self) -> dict:
        levels = {}
        components = {}
        for e in self._entries:
            levels[e.level] = levels.get(e.level, 0) + 1
            if e.component:
                components[e.component] = components.get(e.component, 0) + 1
        return {
            "total_entries": len(self._entries),
            "by_level": levels,
            "by_component": components,
            "context": self._context
        }

    def clear(self):
        self._entries.clear()
