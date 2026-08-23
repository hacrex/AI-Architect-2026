"""Monitoring and drift detection for deployed models."""
import uuid
import random
from datetime import datetime, timedelta
from typing import Optional
from app.models import ModelHealth, DriftReport


class Monitor:
    """Monitor deployed models for health and drift."""

    def __init__(self):
        self._health_checks: dict[str, list[ModelHealth]] = {}
        self._alerts: list[dict] = []

    def check_health(self, model: str) -> ModelHealth:
        """Check current health of a model."""
        # Simulate health check
        quality_score = round(random.uniform(0.75, 0.98), 3)
        drift_detected = random.random() > 0.85  # 15% chance of drift
        latency_p95 = random.randint(800, 2500)
        error_rate = round(random.uniform(0.001, 0.05), 4)

        status = "healthy"
        if quality_score < 0.8 or error_rate > 0.03:
            status = "degraded"
        if quality_score < 0.7 or error_rate > 0.1:
            status = "unhealthy"

        health = ModelHealth(
            model=model,
            status=status,
            quality_score=quality_score,
            drift_detected=drift_detected,
            latency_p95=latency_p95,
            error_rate=error_rate
        )

        # Store health check
        if model not in self._health_checks:
            self._health_checks[model] = []
        self._health_checks[model].append(health)

        # Generate alert if needed
        if status != "healthy":
            self._alerts.append({
                "model": model,
                "status": status,
                "quality_score": quality_score,
                "drift_detected": drift_detected,
                "timestamp": datetime.utcnow().isoformat()
            })

        return health

    def get_health_history(self, model: str, hours: int = 24) -> list[ModelHealth]:
        """Get health check history for a model."""
        checks = self._health_checks.get(model, [])
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        return [h for h in checks if h.last_checked >= cutoff]

    def get_drift_report(self, model: str, time_range: str = "7d") -> DriftReport:
        """Get drift report for a model."""
        # Simulate drift detection
        data_drift = round(random.uniform(0, 0.3), 3)
        concept_drift = round(random.uniform(0, 0.2), 3)

        # Generate quality trend
        quality_trend = [round(random.uniform(0.75, 0.95), 3) for _ in range(7)]

        # Generate recommendation
        if data_drift > 0.2 or concept_drift > 0.15:
            recommendation = "Consider retraining with updated data"
        elif data_drift > 0.1 or concept_drift > 0.1:
            recommendation = "Monitor closely, may need attention"
        else:
            recommendation = "Model is stable, no action needed"

        return DriftReport(
            model=model,
            time_range=time_range,
            data_drift=data_drift,
            concept_drift=concept_drift,
            quality_trend=quality_trend,
            recommendation=recommendation
        )

    def get_alerts(self, model: str = None, limit: int = 10) -> list[dict]:
        """Get recent alerts."""
        alerts = self._alerts
        if model:
            alerts = [a for a in alerts if a["model"] == model]
        return alerts[-limit:]

    def get_metrics_summary(self, model: str) -> dict:
        """Get metrics summary for a model."""
        checks = self._health_checks.get(model, [])
        if not checks:
            return {"error": "No health checks found"}

        recent = checks[-10:] if len(checks) > 10 else checks

        return {
            "model": model,
            "total_checks": len(checks),
            "avg_quality": round(sum(h.quality_score for h in recent) / len(recent), 3),
            "avg_latency": round(sum(h.latency_p95 for h in recent) / len(recent), 0),
            "avg_error_rate": round(sum(h.error_rate for h in recent) / len(recent), 4),
            "drift_detected": any(h.drift_detected for h in recent),
            "status_distribution": {
                "healthy": sum(1 for h in recent if h.status == "healthy"),
                "degraded": sum(1 for h in recent if h.status == "degraded"),
                "unhealthy": sum(1 for h in recent if h.status == "unhealthy"),
            }
        }
