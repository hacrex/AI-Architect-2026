"""Cost Model — AI platform cost tracking and ROI analysis."""
from typing import Optional
from app.models import CostModel, CostItem, BusinessValue
import config.settings as settings


class CostManager:
    """Manage AI platform cost models and ROI calculations."""

    def __init__(self):
        self._cost_models: dict[str, CostModel] = {}
        self._seed_cost_models()

    def _seed_cost_models(self):
        self.create_cost_model(CostModel(
            id="cost-001",
            name="Enterprise AI Knowledge Platform",
            items=[
                CostItem(name="Model Inference (Managed)", category="model", annual_cost=180000,
                         description="GPT-4o, Claude API calls"),
                CostItem(name="GPU Infrastructure", category="infrastructure", annual_cost=240000,
                         description="A100 GPU cluster for self-hosted models"),
                CostItem(name="Engineering Team", category="engineering", annual_cost=500000,
                         description="4 engineers + 1 platform lead"),
                CostItem(name="Platform Operations", category="operations", annual_cost=120000,
                         description="Kubernetes, storage, networking"),
                CostItem(name="Security & Compliance", category="security", annual_cost=80000,
                         description="IAM, audit, compliance tracking"),
                CostItem(name="Observability", category="observability", annual_cost=60000,
                         description="Metrics, logs, traces, dashboards"),
                CostItem(name="Maintenance", category="maintenance", annual_cost=100000,
                         description="Bug fixes, updates, documentation"),
            ]
        ))

        self.create_cost_model(CostModel(
            id="cost-002",
            name="AI Inference Platform",
            items=[
                CostItem(name="GPU Cluster (8x A100)", category="infrastructure", annual_cost=384000,
                         description="Dedicated GPU cluster"),
                CostItem(name="Platform Engineering", category="engineering", annual_cost=400000,
                         description="3 engineers + 1 lead"),
                CostItem(name="Managed API Fallback", category="model", annual_cost=120000,
                         description="OpenAI, Anthropic backup"),
                CostItem(name="Kubernetes & Storage", category="operations", annual_cost=96000,
                         description="Cluster operations"),
                CostItem(name="Monitoring & Alerting", category="observability", annual_cost=48000,
                         description="Prometheus, Grafana, alerts"),
            ]
        ))

        self.create_cost_model(CostModel(
            id="cost-003",
            name="Agent Platform",
            items=[
                CostItem(name="Agent Runtime Infrastructure", category="infrastructure", annual_cost=72000,
                         description="Compute for agent execution"),
                CostItem(name="Policy Engine", category="security", annual_cost=36000,
                         description="OPA/Cedar deployment"),
                CostItem(name="Audit Storage", category="security", annual_cost=24000,
                         description="Append-only audit log"),
                CostItem(name="Tool API Costs", category="model", annual_cost=48000,
                         description="External API calls"),
                CostItem(name="Engineering", category="engineering", annual_cost=300000,
                         description="2 engineers + 1 lead"),
            ]
        ))

    def create_cost_model(self, model: CostModel) -> CostModel:
        self._cost_models[model.id] = model
        return model

    def get_cost_model(self, model_id: str) -> Optional[CostModel]:
        return self._cost_models.get(model_id)

    def list_cost_models(self) -> list[CostModel]:
        return list(self._cost_models.values())

    def calculate_roi(self, business_value: BusinessValue, cost_model_id: str) -> dict:
        cost_model = self._cost_models.get(cost_model_id)
        if not cost_model:
            return {"error": "Cost model not found"}

        total_cost = cost_model.total_cost()
        annual_value = business_value.annual_productivity_value()
        roi_pct = business_value.roi(total_cost)
        payback_months = business_value.payback_months(total_cost)

        return {
            "project": cost_model.name,
            "annual_value": annual_value,
            "annual_cost": total_cost,
            "net_value": annual_value - total_cost,
            "roi_pct": roi_pct,
            "payback_months": payback_months,
            "cost_breakdown": cost_model.by_category(),
        }

    def compare_approaches(self, approaches: list[dict]) -> dict:
        results = []
        for approach in approaches:
            cost_model = self._cost_models.get(approach.get("cost_model_id"))
            if cost_model:
                results.append({
                    "name": approach["name"],
                    "total_annual_cost": cost_model.total_cost(),
                    "cost_breakdown": cost_model.by_category(),
                    "fixed_cost": sum(i.annual_cost for i in cost_model.items if "infrastructure" in i.category),
                    "variable_cost": sum(i.annual_cost for i in cost_model.items if "model" in i.category),
                })
        return {"approaches": results}

    def get_summary(self) -> dict:
        models = list(self._cost_models.values())
        return {
            "total_models": len(models),
            "total_annual_cost": sum(m.total_cost() for m in models),
            "models": [
                {"id": m.id, "name": m.name, "annual_cost": m.total_cost(),
                 "items": len(m.items), "categories": list(m.by_category().keys())}
                for m in models
            ]
        }
