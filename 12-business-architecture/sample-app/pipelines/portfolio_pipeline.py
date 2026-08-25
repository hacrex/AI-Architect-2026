"""Portfolio Pipeline — orchestrates all business architecture components."""
from app.orchestrator import PortfolioOrchestrator


class PortfolioPipeline:
    """Unified business architecture pipeline."""

    def __init__(self):
        self.orchestrator = PortfolioOrchestrator()

    def run_prioritization(self) -> dict:
        ucs = self.orchestrator.prioritize_use_cases()
        return {
            "total_use_cases": len(ucs),
            "prioritized": ucs,
            "top_recommendation": ucs[0] if ucs else None,
        }

    def run_cost_analysis(self, project_id: str) -> dict:
        return self.orchestrator.get_project_cost_analysis(project_id)

    def run_trade_off_evaluation(self, trade_off_id: str) -> dict:
        return self.orchestrator.trade_offs.evaluate(trade_off_id)

    def run_full_portfolio_report(self) -> str:
        return self.orchestrator.generate_portfolio_report()

    def get_status(self) -> dict:
        return self.orchestrator.get_full_status()
