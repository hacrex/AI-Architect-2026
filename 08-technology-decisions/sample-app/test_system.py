"""Tests for the Technology Decisions sample app."""
import sys
sys.path.insert(0, ".")

from app.decision_engine import DecisionEngine, WeightedScorer, ConstraintValidator
from app.adr_manager import ADRManager
from app.build_buy_analyzer import BuildBuyAnalyzer, BuildCostCalculator, BuyCostCalculator
from app.constraint_validator import ConstraintManager
from pipelines.decision_pipeline import DecisionPipeline
from app.models import TechnologyCategory, DecisionCriteria, ConstraintType


def test_decision_engine():
    print("=== Testing Decision Engine ===")
    engine = DecisionEngine()

    matrices = engine.list_matrices()
    print(f"Matrices: {len(matrices)}")
    assert len(matrices) >= 3

    m = engine.get_matrix("matrix-001")
    assert m is not None
    print(f"Model Hosting Matrix: {m.title}")
    print(f"  Options: {len(m.options)}")
    print(f"  Scores: {len(m.scores)}")
    print(f"  Selected: {m.selected_option}")

    for s in m.scores:
        print(f"  - {s.option_name}: {s.weighted_score} (disqualified={s.is_disqualified})")

    assert m.selected_option is not None
    print("PASSED\n")


def test_weighted_scorer():
    print("=== Testing Weighted Scorer ===")
    scorer = WeightedScorer()

    criteria = [
        DecisionCriteria(name="capability", weight=0.5),
        DecisionCriteria(name="cost", weight=0.5)
    ]
    scores = {"capability": 9, "cost": 7}
    weighted = scorer.calculate_weighted_score(scores, criteria)
    print(f"Weighted score: {weighted}")
    assert weighted == 8.0

    print("PASSED\n")


def test_constraint_validator():
    print("=== Testing Constraint Validator ===")
    validator = ConstraintValidator()

    validator.add_constraint("budget", "Must be under $10k/month", eliminates=["expensive option"])

    violations = validator.validate("expensive option")
    print(f"Violations for 'expensive option': {len(violations)}")
    assert len(violations) == 1

    violations = validator.validate("cheap option")
    print(f"Violations for 'cheap option': {len(violations)}")
    assert len(violations) == 0

    print("PASSED\n")


def test_adr_manager():
    print("=== Testing ADR Manager ===")
    mgr = ADRManager()

    adrs = mgr.list_adrs()
    print(f"ADRs: {len(adrs)}")
    assert len(adrs) >= 3

    summary = mgr.get_adr_summary()
    for s in summary:
        print(f"  {s['id']}: {s['title']} ({s['status']})")
        print(f"    Options: {s['options_count']}, Revisit conditions: {s['revisit_conditions_count']}")

    adr = mgr.get_adr("ADR-001")
    assert adr is not None
    assert adr.decision != ""
    assert len(adr.revisit_conditions) > 0
    print(f"ADR-001 has {len(adr.revisit_conditions)} revisit conditions")

    markdown = mgr.format_adr_markdown("ADR-001")
    assert "# ADR-001" in markdown
    assert "Revisit Conditions" in markdown
    print("Markdown format includes all sections")

    print("PASSED\n")


def test_build_buy_analyzer():
    print("=== Testing Build vs Buy Analyzer ===")
    analyzer = BuildBuyAnalyzer()

    analyses = analyzer.list_analyses()
    print(f"Analyses: {len(analyses)}")
    assert len(analyses) >= 3

    for a in analyses:
        comparisons = analyzer.compare_options(a.id)
        print(f"\n  {a.component}:")
        print(f"    Recommendation: {a.recommendation}")
        for c in comparisons:
            print(f"    - {c['name']}: ${c['total_5yr_cost']:,.0f} (5yr)")

    print("PASSED\n")


def test_build_cost_calculator():
    print("=== Testing Build Cost Calculator ===")
    calc = BuildCostCalculator()

    result = calc.calculate_5yr_cost(
        initial_engineering_hours=500,
        hourly_rate=150.0,
        infrastructure_monthly=500.0,
        maintenance_hours_per_month=20,
        security_hours_per_month=5,
        monitoring_hours_per_month=5,
        oncall_hours_per_month=10
    )

    print(f"Initial cost: ${result['initial_engineering_cost']:,.0f}")
    print(f"Annual maintenance: ${result['annual_maintenance_cost']:,.0f}")
    print(f"Annual infrastructure: ${result['annual_infrastructure_cost']:,.0f}")
    print(f"5-year total: ${result['five_year_total']:,.0f}")

    assert result["five_year_total"] > 0
    print("PASSED\n")


def test_buy_cost_calculator():
    print("=== Testing Buy Cost Calculator ===")
    calc = BuyCostCalculator()

    result = calc.calculate_5yr_cost(
        monthly_subscription=2000.0,
        integration_hours=40,
        hourly_rate=150.0,
        migration_cost=10000.0,
        annual_price_increase_pct=5.0
    )

    print(f"Integration cost: ${result['integration_cost']:,.0f}")
    print(f"5-year subscription: ${result['total_subscription_5yr']:,.0f}")
    print(f"Migration cost: ${result['migration_cost']:,.0f}")
    print(f"5-year total: ${result['five_year_total']:,.0f}")

    assert result["five_year_total"] > 0
    print("PASSED\n")


def test_constraint_manager():
    print("=== Testing Constraint Manager ===")
    mgr = ConstraintManager()

    constraints = mgr.get_all_constraints()
    print(f"Constraints: {len(constraints)}")
    assert len(constraints) >= 5

    summary = mgr.get_constraints_summary()
    for s in summary:
        print(f"  {s['name']} ({s['type']})")

    result = mgr.validate_option("Managed LLM", "External API service")
    print(f"\nValidating 'Managed LLM' (external):")
    print(f"  Valid: {result['is_valid']}")
    print(f"  Violations: {len(result['violations'])}")

    result = mgr.validate_option("PostgreSQL + pgvector", "Existing database")
    print(f"\nValidating 'PostgreSQL + pgvector':")
    print(f"  Valid: {result['is_valid']}")
    print(f"  Satisfied: {len(result['satisfied_constraints'])}")

    print("PASSED\n")


def test_decision_pipeline():
    print("=== Testing Decision Pipeline ===")
    pipeline = DecisionPipeline()

    summary = pipeline.run_full_evaluation()
    print(f"Full evaluation:")
    print(f"  Matrices: {len(summary['matrices'])}")
    print(f"  ADRs: {len(summary['adrs'])}")
    print(f"  Build/Buy: {len(summary['build_buy_analyses'])}")
    print(f"  Constraints: {len(summary['constraints'])}")

    mh = pipeline.evaluate_model_hosting()
    print(f"\nModel Hosting:")
    print(f"  Selected: {mh['matrix']['selected']}")
    print(f"  Scores: {len(mh['matrix']['scores'])}")

    challenge = pipeline.challenge_decision("matrix-001")
    print(f"\nChallenge:")
    print(f"  Selected: {challenge['selected_option']}")
    print(f"  Challenges: {len(challenge['challenges'])}")

    bb = pipeline.get_build_buy_summary()
    print(f"\nBuild vs Buy:")
    for a in bb["analyses"]:
        print(f"  {a['component']}: {a['recommendation']}")

    print("PASSED\n")


if __name__ == "__main__":
    print("Technology Decisions Tests\n")
    test_decision_engine()
    test_weighted_scorer()
    test_constraint_validator()
    test_adr_manager()
    test_build_buy_analyzer()
    test_build_cost_calculator()
    test_buy_cost_calculator()
    test_constraint_manager()
    test_decision_pipeline()
    print("All tests passed!")
