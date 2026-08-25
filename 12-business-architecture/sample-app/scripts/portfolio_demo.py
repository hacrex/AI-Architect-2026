"""Business Architecture Demo — portfolio and trade-off demonstration."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.orchestrator import PortfolioOrchestrator


def main():
    print("=" * 60)
    print("AI Business Architecture — Portfolio Demo")
    print("=" * 60)

    orch = PortfolioOrchestrator()

    print("\n--- Project Details ---")
    for p in orch.portfolio.list_projects():
        print(f"\n  {p.name}")
        print(f"    Context: {p.business_context}")
        print(f"    Requirements: {len(p.requirements)}")
        print(f"    Components: {len(p.architecture_components)}")
        print(f"    Key Decisions: {len(p.key_decisions)}")
        print(f"    Demonstrates: {', '.join(p.demonstrates)}")

    print("\n--- Cost Analysis ---")
    for project_id in ["proj-001", "proj-002", "proj-003"]:
        analysis = orch.get_project_cost_analysis(project_id)
        if "error" not in analysis:
            print(f"\n  {analysis['project']}:")
            if "cost" in analysis:
                print(f"    Annual Cost: ${analysis['cost']['total_annual']:,.0f}")
                print(f"    Breakdown: {analysis['cost']['breakdown']}")
            if "value" in analysis:
                print(f"    Annual Value: ${analysis['value']['annual_productivity']:,.0f}")
                print(f"    Employees: {analysis['value']['employees_affected']:,}")
            if "roi" in analysis:
                print(f"    ROI: {analysis['roi']['roi_pct']}%")
                print(f"    Payback: {analysis['roi']['payback_months']} months")

    print("\n--- Trade-off Evaluations ---")
    for to in orch.trade_offs.list_trade_offs():
        result = orch.trade_offs.evaluate(to.id)
        print(f"\n  {to.title}:")
        print(f"    Winner: {result['winner']}")
        for opt in result['scored_options']:
            print(f"    - {opt['name']}: {opt['score']}")

    print(f"\n{'=' * 60}")
    print("Portfolio demo complete.")


if __name__ == "__main__":
    main()
