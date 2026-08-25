"""Script to view all decision matrices and their status."""
import sys
sys.path.insert(0, ".")

from app.decision_engine import DecisionEngine
from app.adr_manager import ADRManager
from app.build_buy_analyzer import BuildBuyAnalyzer
from app.constraint_validator import ConstraintManager


def main():
    print("=== Technology Decisions — Full Status ===\n")

    engine = DecisionEngine()
    print("--- Decision Matrices ---")
    for m in engine.list_matrices():
        print(f"\n  {m.id}: {m.title}")
        print(f"    Category: {m.category.value}")
        print(f"    Options: {len(m.options)}")
        print(f"    Scores: {len(m.scores)}")
        print(f"    Selected: {m.selected_option}")
        print(f"    Rationale: {m.rationale[:80]}...")
        for s in m.scores:
            status = "DISQUALIFIED" if s.is_disqualified else f"Score: {s.weighted_score}"
            print(f"      - {s.option_name}: {status}")

    adr_mgr = ADRManager()
    print("\n--- Architecture Decision Records ---")
    for adr in adr_mgr.list_adrs():
        print(f"\n  {adr.id}: {adr.title}")
        print(f"    Status: {adr.status.value}")
        print(f"    Decision: {adr.decision[:80]}...")
        print(f"    Options considered: {len(adr.options)}")
        print(f"    Revisit conditions: {len(adr.revisit_conditions)}")

    analyzer = BuildBuyAnalyzer()
    print("\n--- Build vs Buy Analyses ---")
    for analysis in analyzer.list_analyses():
        print(f"\n  {analysis.id}: {analysis.component}")
        print(f"    Recommendation: {analysis.recommendation}")
        print(f"    Options: {len(analysis.options)}")
        comparisons = analyzer.compare_options(analysis.id)
        for c in comparisons:
            print(f"      - {c['name']}: ${c['total_5yr_cost']:,.0f} (5yr)")

    constraints = ConstraintManager()
    print("\n--- Hard Constraints ---")
    for c in constraints.get_all_constraints():
        print(f"  - {c.name}")
        print(f"    {c.description[:80]}...")
        if c.eliminates_options:
            print(f"    Eliminates: {', '.join(c.eliminates_options)}")


if __name__ == "__main__":
    main()
