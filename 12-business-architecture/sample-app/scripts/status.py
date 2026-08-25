"""Business Architecture Demo — portfolio status report."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.orchestrator import PortfolioOrchestrator


def main():
    print("=" * 60)
    print("AI Business Architecture — Portfolio Status")
    print("=" * 60)

    orch = PortfolioOrchestrator()

    print("\n1. PORTFOLIO")
    summary = orch.portfolio.get_summary()
    print(f"   Projects:    {summary['total_projects']}")
    print(f"   Use Cases:   {summary['total_use_cases']}")
    print(f"   By Status:   {summary['use_cases_by_status']}")
    for p in summary['projects']:
        print(f"   - {p['name']} ({p['demonstrates']} components)")

    print("\n2. USE CASE PRIORITIZATION")
    for uc in orch.prioritize_use_cases():
        print(f"   {uc['score']:5.2f} | {uc['name']:35s} | {uc['status']:12s} | {uc['owner']}")

    print("\n3. COST SUMMARY")
    cost_summary = orch.costs.get_summary()
    print(f"   Total Models:  {cost_summary['total_models']}")
    print(f"   Total Annual:  ${cost_summary['total_annual_cost']:,.0f}")
    for m in cost_summary['models']:
        print(f"   - {m['name']}: ${m['annual_cost']:,.0f}/year ({m['items']} items)")

    print("\n4. VALUE SUMMARY")
    value_summary = orch.metrics.get_summary()
    print(f"   Business Values: {value_summary['total_business_values']}")
    print(f"   Employees:       {value_summary['total_employees_affected']:,}")
    print(f"   Annual Value:    ${value_summary['total_annual_value']:,.0f}")

    print("\n5. ADRs")
    adr_summary = orch.adrs.get_summary()
    print(f"   Total: {adr_summary['total_adrs']}")
    for a in adr_summary['adr_list']:
        print(f"   - {a['id']}: {a['title']} ({a['status']})")

    print("\n6. TRADE-OFFS")
    to_summary = orch.trade_offs.get_summary()
    for t in to_summary['trade_offs']:
        print(f"   - {t['title']}: Winner = {t['winner']}")

    print("\n7. EXECUTIVE BRIEFS")
    brief_summary = orch.briefs.get_summary()
    for b in brief_summary['briefs']:
        print(f"   - {b['project']}: {b['requirements']} requirements, {b['decisions']} decisions")

    print(f"\n{'=' * 60}")
    print("Status report complete.")


if __name__ == "__main__":
    main()
