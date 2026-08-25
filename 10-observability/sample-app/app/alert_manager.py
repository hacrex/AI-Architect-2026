"""Alert Manager — define, evaluate, and manage alerts for AI systems."""
import uuid
from datetime import datetime
from typing import Optional, Callable
from app.models import Alert, AlertSeverity, AlertState
import config.settings as settings


class AlertRule:
    def __init__(self, name: str, condition: Callable[[dict], bool],
                 severity: AlertSeverity, message_template: str,
                 component: str = ""):
        self.name = name
        self.condition = condition
        self.severity = severity
        self.message_template = message_template
        self.component = component


class AlertManager:
    """Define and evaluate alert rules for AI observability."""

    def __init__(self):
        self._rules: dict[str, AlertRule] = {}
        self._alerts: list[Alert] = []
        self._alert_counts: dict[str, int] = {}
        self._seed_rules()

    def _seed_rules(self):
        self.add_rule(
            name="High Latency",
            condition=lambda m: m.get("p95_latency_ms", 0) > settings.ALERT_LATENCY_THRESHOLD_MS,
            severity=AlertSeverity.WARNING,
            message_template="P95 latency {p95_latency_ms:.0f}ms exceeds threshold {threshold}ms",
            component="application"
        )
        self.add_rule(
            name="High Error Rate",
            condition=lambda m: m.get("error_rate_pct", 0) > settings.ALERT_ERROR_RATE_THRESHOLD,
            severity=AlertSeverity.CRITICAL,
            message_template="Error rate {error_rate_pct:.1f}% exceeds threshold {threshold}%",
            component="application"
        )
        self.add_rule(
            name="Low Retrieval Relevance",
            condition=lambda m: m.get("retrieval_relevance", 100) < settings.ALERT_RETRIEVAL_RELEVANCE_THRESHOLD,
            severity=AlertSeverity.WARNING,
            message_template="Retrieval relevance {retrieval_relevance:.1f}% below threshold {threshold}%",
            component="rag"
        )
        self.add_rule(
            name="High Daily Cost",
            condition=lambda m: m.get("daily_cost_usd", 0) > settings.ALERT_COST_DAILY_LIMIT,
            severity=AlertSeverity.WARNING,
            message_template="Daily cost ${daily_cost_usd:.2f} exceeds budget ${threshold:.2f}",
            component="cost"
        )
        self.add_rule(
            name="GPU Overheating",
            condition=lambda m: m.get("gpu_utilization", 0) > 95 and m.get("gpu_temp_c", 0) > 85,
            severity=AlertSeverity.CRITICAL,
            message_template="GPU utilization {gpu_utilization:.0f}% with temperature {gpu_temp_c:.0f}C",
            component="infrastructure"
        )
        self.add_rule(
            name="Quality Degradation",
            condition=lambda m: m.get("quality_delta_pct", 0) > settings.ALERT_QUALITY_DEGRADATION_PCT,
            severity=AlertSeverity.CRITICAL,
            message_template="Quality dropped {quality_delta_pct:.1f}% from baseline",
            component="quality"
        )

    def add_rule(self, name: str, condition: Callable, severity: AlertSeverity,
                 message_template: str, component: str = "") -> str:
        rule_id = f"rule-{len(self._rules) + 1:03d}"
        self._rules[rule_id] = AlertRule(
            name=name, condition=condition, severity=severity,
            message_template=message_template, component=component
        )
        return rule_id

    def evaluate(self, metrics: dict) -> list[Alert]:
        fired = []
        for rule_id, rule in self._rules.items():
            try:
                if rule.condition(metrics):
                    alert = self._fire_alert(rule, metrics)
                    fired.append(alert)
                else:
                    self._resolve_alerts_by_name(rule.name)
            except Exception:
                pass
        return fired

    def _fire_alert(self, rule: AlertRule, metrics: dict) -> Alert:
        message = rule.message_template
        for key, value in metrics.items():
            placeholder = "{" + key + "}"
            if placeholder in message:
                if isinstance(value, float):
                    message = message.replace(placeholder, f"{value:.2f}")
                else:
                    message = message.replace(placeholder, str(value))

        for key in ["threshold"]:
            placeholder = "{" + key + "}"
            if placeholder in message:
                message = message.replace(placeholder, "N/A")

        existing = [a for a in self._alerts
                    if a.name == rule.name and a.state == AlertState.FIRING]
        if existing:
            existing[0].message = message
            existing[0].attributes.update(metrics)
            return existing[0]

        alert = Alert(
            id=f"alert-{uuid.uuid4().hex[:8]}",
            name=rule.name,
            severity=rule.severity,
            state=AlertState.FIRING,
            condition=rule.name,
            message=message,
            component=rule.component,
            attributes=metrics
        )
        self._alerts.append(alert)
        self._alert_counts[rule.name] = self._alert_counts.get(rule.name, 0) + 1
        return alert

    def _resolve_alerts_by_name(self, name: str):
        for alert in self._alerts:
            if alert.name == name and alert.state == AlertState.FIRING:
                alert.state = AlertState.RESOLVED
                alert.resolved_at = datetime.utcnow()

    def list_alerts(self, state: AlertState = None, severity: AlertSeverity = None,
                    limit: int = 50) -> list[dict]:
        alerts = self._alerts
        if state:
            alerts = [a for a in alerts if a.state == state]
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
        return [
            {
                "id": a.id,
                "name": a.name,
                "severity": a.severity.value,
                "state": a.state.value,
                "message": a.message,
                "component": a.component,
                "triggered_at": a.triggered_at.isoformat(),
                "resolved_at": a.resolved_at.isoformat() if a.resolved_at else None
            }
            for a in alerts[-limit:]
        ]

    def get_active_alerts(self) -> list[dict]:
        return self.list_alerts(state=AlertState.FIRING)

    def get_alert_summary(self) -> dict:
        firing = sum(1 for a in self._alerts if a.state == AlertState.FIRING)
        resolved = sum(1 for a in self._alerts if a.state == AlertState.RESOLVED)
        by_severity = {}
        for a in self._alerts:
            if a.state == AlertState.FIRING:
                by_severity[a.severity.value] = by_severity.get(a.severity.value, 0) + 1
        return {
            "total_alerts": len(self._alerts),
            "firing": firing,
            "resolved": resolved,
            "by_severity": by_severity,
            "alert_counts": self._alert_counts,
            "rules_count": len(self._rules)
        }

    def list_rules(self) -> list[dict]:
        return [
            {"id": rid, "name": r.name, "severity": r.severity.value, "component": r.component}
            for rid, r in self._rules.items()
        ]
