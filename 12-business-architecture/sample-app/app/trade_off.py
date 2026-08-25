"""Trade-off Analysis — evaluate architectural alternatives."""
from datetime import datetime
from typing import Optional
from app.models import TradeOff


class TradeOffAnalyzer:
    """Create and manage trade-off analyses."""

    def __init__(self):
        self._trade_offs: dict[str, TradeOff] = {}
        self._seed_trade_offs()

    def _seed_trade_offs(self):
        self.create_trade_off(TradeOff(
            id="to-001",
            title="Model Strategy",
            dimension_a="Simplicity",
            dimension_b="Control",
            options=[
                {"name": "Managed", "simplicity": 5, "control": 1, "cost": 1, "flexibility": 2},
                {"name": "Self-Hosted", "simplicity": 2, "control": 5, "cost": 4, "flexibility": 4},
                {"name": "Hybrid", "simplicity": 3, "control": 4, "cost": 3, "flexibility": 5},
            ],
            winner="Hybrid",
            rationale="Development needs simplicity (managed). Production needs control (self-hosted). Hybrid provides both with fallback flexibility."
        ))

        self.create_trade_off(TradeOff(
            id="to-002",
            title="Vector Database",
            dimension_a="Cost",
            dimension_b="Features",
            options=[
                {"name": "Pinecone", "cost": 1, "features": 4, "ops_burden": 1, "vendor_lock": 5},
                {"name": "Qdrant", "cost": 4, "features": 4, "ops_burden": 3, "vendor_lock": 1},
                {"name": "Weaviate", "cost": 3, "features": 5, "ops_burden": 3, "vendor_lock": 1},
                {"name": "pgvector", "cost": 5, "features": 2, "ops_burden": 1, "vendor_lock": 2},
            ],
            winner="Qdrant",
            rationale="Best balance of features, cost, and no vendor lock-in. Namespace isolation handles multi-department needs."
        ))

        self.create_trade_off(TradeOff(
            id="to-003",
            title="Agent Authorization",
            dimension_a="Security",
            dimension_b="Simplicity",
            options=[
                {"name": "Allow-all with Logging", "security": 1, "simplicity": 5, "audit": 3, "flexibility": 5},
                {"name": "Static Whitelist", "security": 3, "simplicity": 4, "audit": 2, "flexibility": 1},
                {"name": "Policy Engine", "security": 5, "simplicity": 2, "audit": 5, "flexibility": 4},
            ],
            winner="Policy Engine",
            rationale="Enterprise security requires fine-grained control and full audit trail. Policy overhead is justified by risk reduction."
        ))

        self.create_trade_off(TradeOff(
            id="to-004",
            title="Caching Strategy",
            dimension_a="Cost Savings",
            dimension_b="Complexity",
            options=[
                {"name": "No Caching", "cost_savings": 0, "complexity": 1, "stale_risk": 0},
                {"name": "Exact Match", "cost_savings": 2, "complexity": 2, "stale_risk": 1},
                {"name": "Semantic Cache", "cost_savings": 5, "complexity": 4, "stale_risk": 3},
            ],
            winner="Semantic Cache",
            rationale="30-40% cost reduction for common query patterns justifies the complexity. Stale risk manageable with TTL."
        ))

        self.create_trade_off(TradeOff(
            id="to-005",
            title="Observability Stack",
            dimension_a="Visibility",
            dimension_b="Cost",
            options=[
                {"name": "CloudWatch/Stackdriver", "visibility": 3, "cost": 2, "integration": 4, "customization": 2},
                {"name": "OpenTelemetry + Grafana", "visibility": 5, "cost": 4, "integration": 3, "customization": 5},
                {"name": "Datadog", "visibility": 5, "cost": 1, "integration": 5, "customization": 3},
            ],
            winner="OpenTelemetry + Grafana",
            rationale="Best visibility and customization. Open source avoids vendor lock-in. Self-hosted Grafana controls cost."
        ))

    def create_trade_off(self, to: TradeOff) -> TradeOff:
        self._trade_offs[to.id] = to
        return to

    def get_trade_off(self, to_id: str) -> Optional[TradeOff]:
        return self._trade_offs.get(to_id)

    def list_trade_offs(self) -> list[TradeOff]:
        return list(self._trade_offs.values())

    def evaluate(self, to_id: str, weights: dict[str, float] = None) -> dict:
        to = self._trade_offs.get(to_id)
        if not to:
            return {"error": "Trade-off not found"}

        if weights is None:
            weights = {k: 1.0 for k in to.options[0] if k not in ("name",)}

        scored = []
        for opt in to.options:
            score = sum(opt.get(k, 0) * weights.get(k, 0) for k in weights if k != "name")
            scored.append({"name": opt["name"], "score": round(score, 2), "details": opt})

        scored.sort(key=lambda x: x["score"], reverse=True)

        return {
            "title": to.title,
            "winner": to.winner,
            "rationale": to.rationale,
            "scored_options": scored,
            "weights": weights,
        }

    def get_summary(self) -> dict:
        tos = list(self._trade_offs.values())
        return {
            "total_trade_offs": len(tos),
            "trade_offs": [
                {"id": t.id, "title": t.title, "winner": t.winner}
                for t in tos
            ]
        }

    def format_trade_off(self, to_id: str) -> str:
        to = self._trade_offs.get(to_id)
        if not to:
            return f"Trade-off {to_id} not found"
        lines = [
            f"# {to.title}",
            "",
            f"**Dimensions:** {to.dimension_a} vs {to.dimension_b}",
            "",
            "## Options",
        ]
        for opt in to.options:
            lines.append(f"\n### {opt['name']}")
            for k, v in opt.items():
                if k != "name":
                    lines.append(f"- {k}: {v}")
        lines.extend([
            "",
            f"## Winner: {to.winner}",
            "",
            "## Rationale",
            to.rationale,
        ])
        return "\n".join(lines)
