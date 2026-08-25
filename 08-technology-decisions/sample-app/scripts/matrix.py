"""Script to display and interact with decision matrices."""
import sys
sys.path.insert(0, ".")

from app.decision_engine import DecisionEngine


def main():
    engine = DecisionEngine()

    print("=== Technology Decision Matrices ===\n")

    for matrix in engine.list_matrices():
        print(f"{'='*60}")
        print(f"MATRIX: {matrix.title}")
        print(f"ID: {matrix.id}")
        print(f"Category: {matrix.category.value}")
        print(f"{'='*60}")

        print(f"\nCriteria:")
        for c in matrix.criteria:
            bar = "#" * int(c.weight * 40)
            print(f"  {c.name:25s} [{bar:40s}] {c.weight:.0%}")

        print(f"\nOptions:")
        for o in matrix.options:
            print(f"  - {o.name}")
            print(f"    {o.description}")
            print(f"    Monthly cost: ${o.estimated_monthly_cost:,.0f}")
            print(f"    Team expertise required: {o.team_expertise_required}/10")
            print(f"    Operational burden: {o.operational_burden}/10")

        print(f"\nScores (ranked):")
        for i, s in enumerate(matrix.scores, 1):
            status = "DISQUALIFIED" if s.is_disqualified else f"Score: {s.weighted_score:.4f}"
            rank = f"#{i}" if not s.is_disqualified else "  "
            print(f"  {rank} {s.option_name:40s} {status}")
            if s.hard_constraint_violations:
                print(f"      Violations: {', '.join(s.hard_constraint_violations)}")
            if s.scores:
                top_scores = sorted(s.scores.items(), key=lambda x: x[1], reverse=True)[:3]
                print(f"      Top: {', '.join(f'{k}={v}' for k, v in top_scores)}")

        print(f"\nSelected: {matrix.selected_option}")
        print(f"Rationale: {matrix.rationale}")
        print()


if __name__ == "__main__":
    main()
