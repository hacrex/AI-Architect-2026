"""Metrics Collector — gather and aggregate metrics across all layers."""
import time
import statistics
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Optional
from app.models import MetricPoint, MetricSeries


class MetricsCollector:
    """Collect, aggregate, and query metrics across infrastructure, application, and AI layers."""

    def __init__(self, retention_seconds: int = 86400):
        self.retention_seconds = retention_seconds
        self._series: dict[str, MetricSeries] = {}
        self._counters: dict[str, float] = defaultdict(float)
        self._gauges: dict[str, float] = {}
        self._histograms: dict[str, list[float]] = defaultdict(list)

    def record(self, name: str, value: float, labels: dict[str, str] = None,
               unit: str = ""):
        point = MetricPoint(name=name, value=value, labels=labels or {}, unit=unit)
        key = self._series_key(name, labels or {})
        if key not in self._series:
            self._series[key] = MetricSeries(name=name, labels=labels or {})
        self._series[key].points.append(point)
        self._cleanup_old(key)

    def increment(self, name: str, value: float = 1.0, labels: dict[str, str] = None):
        key = self._series_key(name, labels or {})
        self._counters[key] += value
        self.record(name, self._counters[key], labels)

    def gauge(self, name: str, value: float, labels: dict[str, str] = None):
        key = self._series_key(name, labels or {})
        self._gauges[key] = value
        self.record(name, value, labels)

    def histogram(self, name: str, value: float, labels: dict[str, str] = None):
        key = self._series_key(name, labels or {})
        self._histograms[key].append(value)
        if len(self._histograms[key]) > 10000:
            self._histograms[key] = self._histograms[key][-5000:]
        self.record(name, value, labels)

    def get_series(self, name: str, labels: dict[str, str] = None,
                   last_n: int = 100) -> MetricSeries:
        key = self._series_key(name, labels or {})
        series = self._series.get(key, MetricSeries(name=name, labels=labels or {}))
        return MetricSeries(
            name=series.name,
            points=series.points[-last_n:],
            labels=series.labels
        )

    def get_latest(self, name: str, labels: dict[str, str] = None) -> Optional[float]:
        key = self._series_key(name, labels or {})
        series = self._series.get(key)
        if series and series.points:
            return series.points[-1].value
        return self._gauges.get(key, self._counters.get(key))

    def get_histogram_stats(self, name: str, labels: dict[str, str] = None) -> dict:
        key = self._series_key(name, labels or {})
        values = self._histograms.get(key, [])
        if not values:
            return {"count": 0, "min": 0, "max": 0, "mean": 0, "p50": 0, "p95": 0, "p99": 0}
        sorted_vals = sorted(values)
        return {
            "count": len(sorted_vals),
            "min": round(sorted_vals[0], 4),
            "max": round(sorted_vals[-1], 4),
            "mean": round(statistics.mean(sorted_vals), 4),
            "p50": round(self._percentile(sorted_vals, 50), 4),
            "p95": round(self._percentile(sorted_vals, 95), 4),
            "p99": round(self._percentile(sorted_vals, 99), 4),
        }

    def get_rate(self, name: str, labels: dict[str, str] = None,
                 window_seconds: int = 60) -> float:
        key = self._series_key(name, labels or {})
        series = self._series.get(key)
        if not series or not series.points:
            return 0.0
        cutoff = datetime.utcnow() - timedelta(seconds=window_seconds)
        recent = [p for p in series.points if p.timestamp >= cutoff]
        return len(recent) / window_seconds if window_seconds > 0 else 0.0

    def list_metrics(self) -> list[dict]:
        metrics = []
        for key, series in self._series.items():
            latest = series.points[-1].value if series.points else 0
            metrics.append({
                "name": series.name,
                "labels": series.labels,
                "latest_value": latest,
                "points": len(series.points),
                "unit": series.points[-1].unit if series.points else ""
            })
        return metrics

    def get_infrastructure_summary(self) -> dict:
        return {
            "gpu_utilization": self.get_latest("gpu_utilization") or 0,
            "gpu_memory_used_gb": self.get_latest("gpu_memory_used_gb") or 0,
            "cpu_utilization": self.get_latest("cpu_utilization") or 0,
            "memory_utilization": self.get_latest("memory_utilization") or 0,
            "request_rate": round(self.get_rate("requests_total"), 2),
            "error_rate": round(self.get_rate("errors_total"), 2),
            "queue_depth": self.get_latest("queue_depth") or 0,
        }

    def get_ai_summary(self) -> dict:
        return {
            "total_llm_calls": self.get_latest("llm_calls_total") or 0,
            "total_tokens": self.get_latest("tokens_total") or 0,
            "avg_latency_ms": self.get_histogram_stats("llm_latency_ms").get("mean", 0),
            "p95_latency_ms": self.get_histogram_stats("llm_latency_ms").get("p95", 0),
            "ttft_p50_ms": self.get_histogram_stats("ttft_ms").get("p50", 0),
            "tokens_per_second": self.get_latest("tokens_per_second") or 0,
            "retrieval_relevance_avg": self.get_latest("retrieval_relevance") or 0,
            "cache_hit_rate": self.get_latest("cache_hit_rate") or 0,
        }

    def _series_key(self, name: str, labels: dict[str, str]) -> str:
        label_str = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
        return f"{name}{{{label_str}}}" if label_str else name

    def _cleanup_old(self, key: str):
        if key in self._series:
            cutoff = datetime.utcnow() - timedelta(seconds=self.retention_seconds)
            self._series[key].points = [
                p for p in self._series[key].points if p.timestamp >= cutoff
            ]

    def _percentile(self, sorted_vals: list[float], pct: float) -> float:
        if not sorted_vals:
            return 0.0
        idx = int(len(sorted_vals) * pct / 100)
        idx = min(idx, len(sorted_vals) - 1)
        return sorted_vals[idx]
