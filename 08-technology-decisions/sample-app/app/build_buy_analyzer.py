"""Build vs Buy Analyzer — evaluate make vs buy decisions with full cost analysis."""
import uuid
from datetime import datetime
from app.models import BuildBuyAnalysis, BuildBuyOption, BuildBuyDecision


class BuildCostCalculator:
    """Calculate full cost of building a component."""

    def calculate_5yr_cost(self, initial_engineering_hours: int,
                           hourly_rate: float = 150.0,
                           infrastructure_monthly: float = 500.0,
                           maintenance_hours_per_month: int = 20,
                           security_hours_per_month: int = 5,
                           monitoring_hours_per_month: int = 5,
                           oncall_hours_per_month: int = 10) -> dict:
        initial_cost = initial_engineering_hours * hourly_rate
        annual_maintenance = (maintenance_hours_per_month + security_hours_per_month +
                              monitoring_hours_per_month + oncall_hours_per_month) * hourly_rate * 12
        annual_infra = infrastructure_monthly * 12
        annual_total = annual_maintenance + annual_infra
        five_year_total = initial_cost + (annual_total * 5)

        return {
            "initial_engineering_cost": round(initial_cost, 2),
            "annual_maintenance_cost": round(annual_maintenance, 2),
            "annual_infrastructure_cost": round(annual_infra, 2),
            "annual_total": round(annual_total, 2),
            "five_year_total": round(five_year_total, 2),
            "breakdown": {
                "initial_hours": initial_engineering_hours,
                "hourly_rate": hourly_rate,
                "maintenance_hours_month": maintenance_hours_per_month,
                "security_hours_month": security_hours_per_month,
                "monitoring_hours_month": monitoring_hours_per_month,
                "oncall_hours_month": oncall_hours_per_month,
                "infrastructure_monthly": infrastructure_monthly
            }
        }


class BuyCostCalculator:
    """Calculate full cost of buying/using a managed service."""

    def calculate_5yr_cost(self, monthly_subscription: float,
                           integration_hours: int = 40,
                           hourly_rate: float = 150.0,
                           migration_cost: float = 0.0,
                           annual_price_increase_pct: float = 5.0) -> dict:
        integration_cost = integration_hours * hourly_rate
        total_subscription = 0.0
        monthly_costs = []

        for year in range(5):
            annual = monthly_subscription * 12 * ((1 + annual_price_increase_pct / 100) ** year)
            total_subscription += annual
            monthly_costs.append({
                "year": year + 1,
                "monthly": round(monthly_subscription * ((1 + annual_price_increase_pct / 100) ** year), 2),
                "annual": round(annual, 2)
            })

        five_year_total = integration_cost + total_subscription + migration_cost

        return {
            "integration_cost": round(integration_cost, 2),
            "total_subscription_5yr": round(total_subscription, 2),
            "migration_cost": round(migration_cost, 2),
            "five_year_total": round(five_year_total, 2),
            "yearly_breakdown": monthly_costs,
            "annual_price_increase_pct": annual_price_increase_pct
        }


class BuildBuyAnalyzer:
    """Complete Build vs Buy analysis engine."""

    def __init__(self):
        self.build_calculator = BuildCostCalculator()
        self.buy_calculator = BuyCostCalculator()
        self._analyses: dict[str, BuildBuyAnalysis] = {}
        self._seed_analyses()

    def _seed_analyses(self):
        self.analyze_component(
            component="Vector Search",
            options=[
                BuildBuyOption(
                    name="Build: Custom Vector Retrieval",
                    description="Build a custom vector search system from scratch",
                    build_cost_5yr=450000.0,
                    buy_cost_5yr=0.0,
                    is_competitive_advantage=False,
                    team_can_build=True,
                    migration_cost=50000.0,
                    time_to_value_weeks=12
                ),
                BuildBuyOption(
                    name="Buy: Managed Vector DB (Pinecone)",
                    description="Use Pinecone as managed vector database",
                    build_cost_5yr=0.0,
                    buy_cost_5yr=120000.0,
                    is_competitive_advantage=False,
                    team_can_build=False,
                    migration_cost=30000.0,
                    time_to_value_weeks=2
                ),
                BuildBuyOption(
                    name="Use: PostgreSQL + pgvector",
                    description="Extend existing PostgreSQL with pgvector extension",
                    build_cost_5yr=80000.0,
                    buy_cost_5yr=0.0,
                    is_competitive_advantage=False,
                    team_can_build=True,
                    migration_cost=15000.0,
                    time_to_value_weeks=4
                ),
            ],
            recommendation="Use: PostgreSQL + pgvector",
            rationale="Leverages existing infrastructure, team knowledge, and avoids vendor lock-in. "
                     "Lowest total cost and fastest time to value for current scale."
        )

        self.analyze_component(
            component="Model Gateway",
            options=[
                BuildBuyOption(
                    name="Build: Custom Model Gateway",
                    description="Build custom routing, fallback, and cost tracking",
                    build_cost_5yr=300000.0,
                    buy_cost_5yr=0.0,
                    is_competitive_advantage=False,
                    team_can_build=True,
                    migration_cost=40000.0,
                    time_to_value_weeks=8
                ),
                BuildBuyOption(
                    name="Buy: Managed API Gateway (Kong/AWS)",
                    description="Use existing API gateway with AI plugins",
                    build_cost_5yr=0.0,
                    buy_cost_5yr=60000.0,
                    is_competitive_advantage=False,
                    team_can_build=False,
                    migration_cost=20000.0,
                    time_to_value_weeks=3
                ),
                BuildBuyOption(
                    name="Adopt: Open-Source Gateway (LiteLLM)",
                    description="Adopt open-source model gateway",
                    build_cost_5yr=0.0,
                    buy_cost_5yr=24000.0,
                    is_competitive_advantage=False,
                    team_can_build=True,
                    migration_cost=10000.0,
                    time_to_value_weeks=2
                ),
            ],
            recommendation="Adopt: Open-Source Gateway (LiteLLM)",
            rationale="Open-source gateway provides model routing, fallback, and cost tracking "
                     "without vendor lock-in. Lowest cost and fastest time to value."
        )

        self.analyze_component(
            component="Observability",
            options=[
                BuildBuyOption(
                    name="Build: Custom Tracing System",
                    description="Build distributed tracing, metrics, and cost tracking",
                    build_cost_5yr=500000.0,
                    buy_cost_5yr=0.0,
                    is_competitive_advantage=False,
                    team_can_build=True,
                    migration_cost=60000.0,
                    time_to_value_weeks=16
                ),
                BuildBuyOption(
                    name="Buy: Managed Observability (Datadog)",
                    description="Use Datadog for AI-specific observability",
                    build_cost_5yr=0.0,
                    buy_cost_5yr=300000.0,
                    is_competitive_advantage=False,
                    team_can_build=False,
                    migration_cost=20000.0,
                    time_to_value_weeks=2
                ),
                BuildBuyOption(
                    name="Adopt: Open-Source Stack (Prometheus + Grafana + Jaeger)",
                    description="Use open-source observability stack",
                    build_cost_5yr=0.0,
                    buy_cost_5yr=36000.0,
                    is_competitive_advantage=False,
                    team_can_build=True,
                    migration_cost=15000.0,
                    time_to_value_weeks=4
                ),
            ],
            recommendation="Adopt: Open-Source Stack",
            rationale="Open-source stack provides sufficient observability without vendor lock-in. "
                     "Team has experience with Prometheus and Grafana."
        )

    def analyze_component(self, component: str, options: list[BuildBuyOption],
                          recommendation: str = "", rationale: str = "") -> BuildBuyAnalysis:
        analysis_id = f"analysis-{len(self._analyses) + 1:03d}"
        analysis = BuildBuyAnalysis(
            id=analysis_id,
            component=component,
            options=options,
            recommendation=recommendation,
            rationale=rationale
        )
        self._analyses[analysis_id] = analysis
        return analysis

    def get_analysis(self, analysis_id: str) -> BuildBuyAnalysis:
        return self._analyses.get(analysis_id)

    def list_analyses(self) -> list[BuildBuyAnalysis]:
        return list(self._analyses.values())

    def get_summary(self) -> list[dict]:
        return [
            {
                "id": a.id,
                "component": a.component,
                "options_count": len(a.options),
                "recommendation": a.recommendation
            }
            for a in self._analyses.values()
        ]

    def compare_options(self, analysis_id: str) -> list[dict]:
        analysis = self._analyses.get(analysis_id)
        if not analysis:
            return []

        comparisons = []
        for opt in analysis.options:
            total_cost = opt.build_cost_5yr if opt.build_cost_5yr > 0 else opt.buy_cost_5yr
            comparisons.append({
                "name": opt.name,
                "total_5yr_cost": total_cost,
                "is_competitive_advantage": opt.is_competitive_advantage,
                "team_can_build": opt.team_can_build,
                "time_to_value_weeks": opt.time_to_value_weeks,
                "migration_cost": opt.migration_cost,
                "recommendation_fit": self._score_recommendation(opt)
            })

        comparisons.sort(key=lambda x: x["total_5yr_cost"])
        return comparisons

    def _score_recommendation(self, option: BuildBuyOption) -> str:
        if option.is_competitive_advantage and option.team_can_build:
            return "strong_build"
        elif not option.is_competitive_advantage and not option.team_can_build:
            return "strong_buy"
        elif not option.is_competitive_advantage and option.team_can_build:
            return "evaluate_cost"
        else:
            return "strategic_build"
