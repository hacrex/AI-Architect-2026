"""Portfolio Orchestrator — unified business architecture management."""
from app.portfolio import PortfolioManager
from app.adr import ADRManager
from app.cost_model import CostManager
from app.business_metrics import BusinessMetricsManager
from app.trade_off import TradeOffAnalyzer
from app.review import ReviewManager
from app.executive_brief import ExecutiveBriefManager


class PortfolioOrchestrator:
    """Unified orchestrator for AI architecture portfolio."""

    def __init__(self):
        self.portfolio = PortfolioManager()
        self.adrs = ADRManager()
        self.costs = CostManager()
        self.metrics = BusinessMetricsManager()
        self.trade_offs = TradeOffAnalyzer()
        self.reviews = ReviewManager()
        self.briefs = ExecutiveBriefManager()

    def get_full_status(self) -> dict:
        return {
            "portfolio": self.portfolio.get_summary(),
            "adrs": self.adrs.get_summary(),
            "costs": self.costs.get_summary(),
            "metrics": self.metrics.get_summary(),
            "trade_offs": self.trade_offs.get_summary(),
            "reviews": self.reviews.get_summary(),
            "briefs": self.briefs.get_summary(),
        }

    def prioritize_use_cases(self) -> list[dict]:
        ucs = self.portfolio.prioritize_use_cases()
        return [
            {"id": uc.id, "name": uc.name, "score": uc.weighted_score(),
             "status": uc.status.value, "owner": uc.owner}
            for uc in ucs
        ]

    def get_project_cost_analysis(self, project_id: str) -> dict:
        project = self.portfolio.get_project(project_id)
        if not project:
            return {"error": "Project not found"}

        cost_model_id = f"cost-{project_id.split('-')[-1]}"
        cost_model = self.costs.get_cost_model(cost_model_id)

        bv_id = f"bv-{project_id.split('-')[-1]}"
        business_value = self.metrics.get_business_value(bv_id)

        result = {
            "project": project.name,
            "demonstrates": project.demonstrates,
        }

        if cost_model:
            result["cost"] = {
                "total_annual": cost_model.total_cost(),
                "breakdown": cost_model.by_category(),
            }

        if business_value:
            result["value"] = {
                "annual_productivity": business_value.annual_productivity_value(),
                "employees_affected": business_value.employees_affected,
                "time_saved_minutes": business_value.time_saved_minutes_per_day,
            }

            if cost_model:
                roi_data = self.costs.calculate_roi(business_value, cost_model_id)
                result["roi"] = roi_data

        return result

    def generate_portfolio_report(self) -> str:
        lines = ["# AI Architecture Portfolio Report", ""]

        lines.append("## Projects")
        for p in self.portfolio.list_projects():
            lines.append(f"\n### {p.name}")
            lines.append(f"**Context:** {p.business_context}")
            lines.append(f"**Demonstrates:** {', '.join(p.demonstrates)}")

        lines.append("\n## Use Case Prioritization")
        for uc in self.prioritize_use_cases():
            lines.append(f"- **{uc['name']}** (score: {uc['score']}, status: {uc['status']})")

        lines.append("\n## Architecture Decision Records")
        for adr in self.adrs.list_adrs():
            lines.append(f"- **{adr.id}: {adr.title}** ({adr.status.value})")

        lines.append("\n## Trade-off Analyses")
        for to in self.trade_offs.list_trade_offs():
            lines.append(f"- **{to.title}** → Winner: {to.winner}")

        lines.append("\n## Cost Summary")
        cost_summary = self.costs.get_summary()
        lines.append(f"- Total annual cost: ${cost_summary['total_annual_cost']:,.0f}")

        lines.append("\n## Value Summary")
        value_summary = self.metrics.get_summary()
        lines.append(f"- Total employees affected: {value_summary['total_employees_affected']:,}")
        lines.append(f"- Total annual value: ${value_summary['total_annual_value']:,.0f}")

        return "\n".join(lines)
