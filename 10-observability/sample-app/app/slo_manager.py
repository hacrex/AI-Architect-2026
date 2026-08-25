"""SLO Manager — track service level indicators, objectives, and error budgets."""
import uuid
from datetime import datetime
from typing import Optional
from app.models import SLI, SLO, SLOState
import config.settings as settings


class SLOManager:
    """Manage SLIs, SLOs, and error budgets for AI systems."""

    def __init__(self):
        self._slos: dict[str, SLO] = {}
        self._slis: list[SLI] = []
        self._seed_slos()

    def _seed_slos(self):
        self.create_slo(
            name="Availability",
            description="Percentage of successful AI requests",
            target=settings.SLO_AVAILABILITY_TARGET,
            current=99.95,
            window_seconds=86400
        )
        self.create_slo(
            name="Latency P95",
            description="P95 response latency under target",
            target=settings.SLO_LATENCY_P95_TARGET_MS,
            current=3200.0,
            window_seconds=3600
        )
        self.create_slo(
            name="Task Success",
            description="Percentage of AI tasks completed successfully",
            target=settings.SLO_TASK_SUCCESS_TARGET,
            current=92.5,
            window_seconds=86400
        )
        self.create_slo(
            name="Groundedness",
            description="Percentage of responses grounded in retrieved context",
            target=settings.SLO_GROUNDEDNESS_TARGET,
            current=96.2,
            window_seconds=86400
        )

    def create_slo(self, name: str, description: str, target: float,
                   current: float, window_seconds: int = 86400) -> SLO:
        slo_id = f"slo-{len(self._slos) + 1:03d}"
        state = self._evaluate_state(name, current, target)
        error_budget = self._calculate_error_budget(name, current, target)
        slo = SLO(
            id=slo_id,
            name=name,
            description=description,
            target=target,
            current=current,
            state=state,
            error_budget_remaining_pct=error_budget,
            window_seconds=window_seconds
        )
        self._slos[slo_id] = slo
        return slo

    def record_sli(self, name: str, value: float, unit: str = ""):
        sli = SLI(name=name, value=value, unit=unit, description=f"{name} measurement")
        self._slis.append(sli)
        for slo in self._slos.values():
            if slo.name == name:
                slo.current = value
                slo.state = self._evaluate_state(name, value, slo.target)
                slo.error_budget_remaining_pct = self._calculate_error_budget(
                    name, value, slo.target
                )
                slo.last_updated = datetime.utcnow()

    def _evaluate_state(self, name: str, current: float, target: float) -> SLOState:
        if name in ("Latency P95",):
            if current <= target * 0.8:
                return SLOState.HEALTHY
            elif current <= target:
                return SLOState.AT_RISK
            else:
                return SLOState.BREACHED
        else:
            if current >= target:
                return SLOState.HEALTHY
            elif current >= target * 0.95:
                return SLOState.AT_RISK
            else:
                return SLOState.BREACHED

    def _calculate_error_budget(self, name: str, current: float, target: float) -> float:
        if name in ("Latency P95",):
            if current <= target * 0.8:
                return 100.0
            elif current <= target:
                return round((target - current) / (target * 0.2) * 100, 1)
            else:
                return 0.0
        else:
            if current >= target:
                return 100.0
            elif current >= target * 0.95:
                return round((current - target * 0.95) / (target * 0.05) * 100, 1)
            else:
                return 0.0

    def get_slo(self, slo_id: str) -> Optional[SLO]:
        return self._slos.get(slo_id)

    def list_slos(self) -> list[SLO]:
        return list(self._slos.values())

    def get_summary(self) -> dict:
        slos = list(self._slos.values())
        healthy = sum(1 for s in slos if s.state == SLOState.HEALTHY)
        at_risk = sum(1 for s in slos if s.state == SLOState.AT_RISK)
        breached = sum(1 for s in slos if s.state == SLOState.BREACHED)
        return {
            "total_slos": len(slos),
            "healthy": healthy,
            "at_risk": at_risk,
            "breached": breached,
            "overall_health": "healthy" if breached == 0 and at_risk == 0
                              else "degraded" if breached == 0
                              else "critical",
            "slo_details": [
                {
                    "name": s.name,
                    "state": s.state.value,
                    "target": s.target,
                    "current": s.current,
                    "error_budget_remaining_pct": s.error_budget_remaining_pct
                }
                for s in slos
            ]
        }

    def get_error_budgets(self) -> dict:
        return {
            s.name: {
                "target": s.target,
                "current": s.current,
                "budget_remaining_pct": s.error_budget_remaining_pct,
                "state": s.state.value
            }
            for s in self._slos.values()
        }

    def get_sli_history(self, name: str, limit: int = 100) -> list[dict]:
        slis = [s for s in self._slis if s.name == name]
        return [
            {"value": s.value, "unit": s.unit, "timestamp": s.timestamp.isoformat()}
            for s in slis[-limit:]
        ]
