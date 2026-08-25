"""Drift Detector — detect changes in model behavior, retrieval quality, and data patterns."""
import math
import uuid
from datetime import datetime
from collections import deque
from typing import Optional
from app.models import DriftSample, DriftStatus
import config.settings as settings


class DriftDetector:
    """Detect statistical drift in metrics using z-score analysis."""

    def __init__(self, window_size: int = None, baseline_size: int = None,
                 threshold: float = None, check_interval: int = None):
        self.window_size = window_size or settings.DRIFT_WINDOW_SIZE
        self.baseline_size = baseline_size or settings.DRIFT_BASELINE_SIZE
        self.threshold = threshold or settings.DRIFT_SIMILARITY_THRESHOLD
        self.check_interval = check_interval or settings.DRIFT_CHECK_INTERVAL
        self._baselines: dict[str, deque] = {}
        self._windows: dict[str, deque] = {}
        self._samples: dict[str, list[DriftSample]] = {}
        self._drift_events: list[dict] = []
        self._request_count = 0

    def add_baseline(self, metric_name: str, value: float):
        if metric_name not in self._baselines:
            self._baselines[metric_name] = deque(maxlen=self.baseline_size)
        self._baselines[metric_name].append(value)

    def add_sample(self, metric_name: str, value: float) -> Optional[DriftSample]:
        self._request_count += 1
        if metric_name not in self._windows:
            self._windows[metric_name] = deque(maxlen=self.window_size)
        if metric_name not in self._samples:
            self._samples[metric_name] = []
        self._windows[metric_name].append(value)

        baseline = self._baselines.get(metric_name)
        if not baseline or len(baseline) < 10:
            return None

        baseline_mean = sum(baseline) / len(baseline)
        baseline_std = math.sqrt(
            sum((x - baseline_mean) ** 2 for x in baseline) / len(baseline)
        )

        if baseline_std == 0:
            z_score = 0.0
        else:
            z_score = abs(value - baseline_mean) / baseline_std

        is_drift = z_score > 2.0

        sample = DriftSample(
            metric_name=metric_name,
            value=value,
            baseline_mean=round(baseline_mean, 6),
            baseline_std=round(baseline_std, 6),
            z_score=round(z_score, 4),
            is_drift=is_drift
        )
        self._samples[metric_name].append(sample)

        if is_drift:
            self._drift_events.append({
                "metric": metric_name,
                "value": value,
                "baseline_mean": round(baseline_mean, 6),
                "z_score": round(z_score, 4),
                "timestamp": datetime.utcnow().isoformat()
            })

        return sample

    def get_status(self, metric_name: str) -> DriftStatus:
        samples = self._samples.get(metric_name, [])
        if not samples:
            return DriftStatus.BASELINE
        recent = samples[-10:]
        drift_count = sum(1 for s in recent if s.is_drift)
        if drift_count >= 5:
            return DriftStatus.DRIFT_DETECTED
        return DriftStatus.NORMAL

    def get_metric_stats(self, metric_name: str) -> dict:
        samples = self._samples.get(metric_name, [])
        if not samples:
            return {"samples": 0}
        values = [s.value for s in samples]
        z_scores = [s.z_score for s in samples]
        baseline = self._baselines.get(metric_name, [])
        baseline_mean = sum(baseline) / len(baseline) if baseline else 0
        return {
            "samples": len(samples),
            "current_value": values[-1] if values else 0,
            "baseline_mean": round(baseline_mean, 6),
            "avg_z_score": round(sum(z_scores) / len(z_scores), 4) if z_scores else 0,
            "max_z_score": round(max(z_scores), 4) if z_scores else 0,
            "drift_count": sum(1 for s in samples if s.is_drift),
            "status": self.get_status(metric_name).value
        }

    def get_all_metrics_status(self) -> dict:
        return {
            name: self.get_metric_stats(name)
            for name in self._samples.keys()
        }

    def get_drift_events(self, limit: int = 50) -> list[dict]:
        return self._drift_events[-limit:]

    def get_summary(self) -> dict:
        all_metrics = self.get_all_metrics_status()
        drifting = sum(1 for m in all_metrics.values() if m.get("status") == "drift_detected")
        return {
            "total_metrics_tracked": len(self._samples),
            "drifting_metrics": drifting,
            "total_drift_events": len(self._drift_events),
            "baselines_configured": len(self._baselines),
            "window_size": self.window_size,
            "baseline_size": self.baseline_size,
            "threshold": self.threshold,
            "metrics": all_metrics
        }

    def seed_baselines(self):
        self.add_baseline("retrieval_relevance", 0.85)
        self.add_baseline("retrieval_relevance", 0.82)
        self.add_baseline("retrieval_relevance", 0.88)
        self.add_baseline("retrieval_relevance", 0.84)
        self.add_baseline("retrieval_relevance", 0.86)
        self.add_baseline("llm_latency_ms", 1200.0)
        self.add_baseline("llm_latency_ms", 1100.0)
        self.add_baseline("llm_latency_ms", 1300.0)
        self.add_baseline("llm_latency_ms", 1150.0)
        self.add_baseline("llm_latency_ms", 1250.0)
        self.add_baseline("token_usage_per_request", 2500.0)
        self.add_baseline("token_usage_per_request", 2300.0)
        self.add_baseline("token_usage_per_request", 2700.0)
        self.add_baseline("token_usage_per_request", 2400.0)
        self.add_baseline("token_usage_per_request", 2600.0)
