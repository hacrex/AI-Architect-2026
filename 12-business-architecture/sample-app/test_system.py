"""Business Architecture Demo — comprehensive tests."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models import (
    Priority, UseCaseStatus, ADRStatus, RiskLevel, ArchitecturePhase,
    UseCase, ADR, TradeOff, CostItem, CostModel, BusinessMetric,
    BusinessValue, Risk, Project, ReviewSection, ArchitectureReview,
    ExecutiveBrief
)
from app.portfolio import PortfolioManager
from app.adr import ADRManager
from app.cost_model import CostManager
from app.business_metrics import BusinessMetricsManager
from app.trade_off import TradeOffAnalyzer
from app.review import ReviewManager
from app.executive_brief import ExecutiveBriefManager
from app.orchestrator import PortfolioOrchestrator
from pipelines.portfolio_pipeline import PortfolioPipeline
from datetime import datetime


def test_models():
    print("Testing Pydantic models...")
    uc = UseCase(id="uc-test", name="Test UC", description="desc",
                 business_value=5, feasibility=4, data_readiness=3,
                 risk=2, cost=3, time_to_value=4)
    assert uc.weighted_score() > 0
    assert uc.status == UseCaseStatus.IDENTIFIED

    adr = ADR(id="adr-test", title="Test ADR", context="ctx", decision="dec", rationale="rat")
    assert adr.status == ADRStatus.PROPOSED

    to = TradeOff(id="to-test", title="Test TO", dimension_a="A", dimension_b="B",
                  options=[{"name": "opt1", "score": 5}], winner="opt1", rationale="r")
    assert to.winner == "opt1"

    ci = CostItem(name="Item", category="infra", annual_cost=1000)
    cm = CostModel(id="cm-test", name="Test CM", items=[ci])
    assert cm.total_cost() == 1000
    assert cm.by_category() == {"infra": 1000}

    bm = BusinessMetric(name="Metric", category="efficiency", baseline=10, target=5, unit="min")
    bv = BusinessValue(id="bv-test", name="Test BV", employees_affected=100,
                       time_saved_minutes_per_day=15, hourly_rate=60)
    assert bv.annual_productivity_value() > 0
    assert bv.roi(10000) > 0
    assert bv.payback_months(10000) > 0

    risk = Risk(id="r-test", name="Test Risk", description="desc",
                impact=RiskLevel.HIGH, likelihood=RiskLevel.MEDIUM, mitigation="mit")
    assert risk.impact == RiskLevel.HIGH

    proj = Project(id="p-test", name="Test Project", description="desc",
                   business_context="ctx")
    assert proj.name == "Test Project"

    section = ReviewSection(phase=ArchitecturePhase.PROBLEM, question="What problem?")
    review = ArchitectureReview(project_id="p-test", project_name="Test", sections=[section])
    assert len(review.sections) == 1

    brief = ExecutiveBrief(project_name="Test", problem="p", users="u", outcome="o",
                           architecture_summary="arch")
    assert brief.project_name == "Test"

    print("  PASS: All Pydantic models OK")


def test_portfolio():
    print("Testing PortfolioManager...")
    pm = PortfolioManager()

    projects = pm.list_projects()
    assert len(projects) >= 5

    ucs = pm.list_use_cases()
    assert len(ucs) >= 5

    prioritized = pm.prioritize_use_cases()
    assert len(prioritized) >= 5
    assert prioritized[0].weighted_score() >= prioritized[-1].weighted_score()

    summary = pm.get_summary()
    assert summary["total_projects"] >= 5
    assert summary["total_use_cases"] >= 5

    print("  PASS: PortfolioManager OK")


def test_adr():
    print("Testing ADRManager...")
    am = ADRManager()

    adrs = am.list_adrs()
    assert len(adrs) >= 7

    adr = am.get_adr("ADR-001")
    assert adr is not None
    assert adr.status == ADRStatus.ACCEPTED

    accepted = am.get_by_status(ADRStatus.ACCEPTED)
    assert len(accepted) >= 5

    updated = am.update_status("ADR-001", ADRStatus.DEPRECATED)
    assert updated.status == ADRStatus.DEPRECATED

    formatted = am.format_adr("ADR-001")
    assert "Managed vs Self-Hosted" in formatted

    summary = am.get_summary()
    assert summary["total_adrs"] >= 7

    print("  PASS: ADRManager OK")


def test_cost_model():
    print("Testing CostManager...")
    cm = CostManager()

    models = cm.list_cost_models()
    assert len(models) >= 3

    model = cm.get_cost_model("cost-001")
    assert model is not None
    assert model.total_cost() > 0

    breakdown = model.by_category()
    assert "model" in breakdown
    assert "infrastructure" in breakdown

    summary = cm.get_summary()
    assert summary["total_models"] >= 3
    assert summary["total_annual_cost"] > 0

    print("  PASS: CostManager OK")


def test_business_metrics():
    print("Testing BusinessMetricsManager...")
    bm = BusinessMetricsManager()

    values = bm.list_business_values()
    assert len(values) >= 3

    bv = bm.get_business_value("bv-001")
    assert bv is not None
    assert bv.annual_productivity_value() > 0

    productivity = bm.calculate_productivity(10000, 20, 60, 220)
    assert productivity["annual_value"] > 0
    assert productivity["employees"] == 10000

    value_summary = bm.get_value_summary("bv-001")
    assert "annual_productivity_value" in value_summary
    assert "roi_pct" in value_summary

    summary = bm.get_summary()
    assert summary["total_business_values"] >= 3
    assert summary["total_employees_affected"] > 0

    print("  PASS: BusinessMetricsManager OK")


def test_trade_offs():
    print("Testing TradeOffAnalyzer...")
    ta = TradeOffAnalyzer()

    tos = ta.list_trade_offs()
    assert len(tos) >= 5

    to = ta.get_trade_off("to-001")
    assert to is not None
    assert to.winner == "Hybrid"

    evaluation = ta.evaluate("to-001")
    assert "scored_options" in evaluation
    assert len(evaluation["scored_options"]) >= 3

    formatted = ta.format_trade_off("to-001")
    assert "Model Strategy" in formatted

    summary = ta.get_summary()
    assert summary["total_trade_offs"] >= 5

    print("  PASS: TradeOffAnalyzer OK")


def test_reviews():
    print("Testing ReviewManager...")
    rm = ReviewManager()

    reviews = rm.list_reviews()
    assert len(reviews) >= 1

    checklist = rm.get_checklist()
    assert len(checklist) == 14

    answered = rm.answer_question("proj-001", ArchitecturePhase.PROBLEM,
                                   "Information scattered across systems")
    assert answered is not None

    summary = rm.get_summary()
    assert summary["total_reviews"] >= 1

    formatted = rm.format_review("proj-001")
    assert "Enterprise AI Knowledge Platform" in formatted

    print("  PASS: ReviewManager OK")


def test_executive_briefs():
    print("Testing ExecutiveBriefManager...")
    eb = ExecutiveBriefManager()

    briefs = eb.list_briefs()
    assert len(briefs) >= 2

    brief = eb.get_brief("Enterprise AI Knowledge Platform")
    assert brief is not None
    assert len(brief.requirements) >= 6
    assert len(brief.top_decisions) >= 3

    formatted = eb.format_brief("Enterprise AI Knowledge Platform")
    assert "Problem" in formatted
    assert "Architecture" in formatted

    summary = eb.get_summary()
    assert summary["total_briefs"] >= 2

    print("  PASS: ExecutiveBriefManager OK")


def test_orchestrator():
    print("Testing PortfolioOrchestrator...")
    orch = PortfolioOrchestrator()

    status = orch.get_full_status()
    assert "portfolio" in status
    assert "adrs" in status
    assert "costs" in status
    assert "metrics" in status
    assert "trade_offs" in status
    assert "reviews" in status
    assert "briefs" in status

    prioritized = orch.prioritize_use_cases()
    assert len(prioritized) >= 5
    assert "score" in prioritized[0]

    analysis = orch.get_project_cost_analysis("proj-001")
    assert "project" in analysis
    assert "cost" in analysis
    assert "value" in analysis
    assert "roi" in analysis

    report = orch.generate_portfolio_report()
    assert "AI Architecture Portfolio Report" in report
    assert "Enterprise AI Knowledge Platform" in report

    print("  PASS: PortfolioOrchestrator OK")


def test_pipeline():
    print("Testing PortfolioPipeline...")
    pipeline = PortfolioPipeline()

    prioritization = pipeline.run_prioritization()
    assert "total_use_cases" in prioritization
    assert "prioritized" in prioritization

    cost_analysis = pipeline.run_cost_analysis("proj-001")
    assert "project" in cost_analysis

    trade_off_eval = pipeline.run_trade_off_evaluation("to-001")
    assert "winner" in trade_off_eval

    report = pipeline.run_full_portfolio_report()
    assert "Portfolio Report" in report

    status = pipeline.get_status()
    assert "portfolio" in status

    print("  PASS: PortfolioPipeline OK")


def main():
    print("=" * 60)
    print("AI Business Architecture — System Tests")
    print("=" * 60)
    print()

    tests = [
        test_models,
        test_portfolio,
        test_adr,
        test_cost_model,
        test_business_metrics,
        test_trade_offs,
        test_reviews,
        test_executive_briefs,
        test_orchestrator,
        test_pipeline,
    ]

    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"  FAIL: {test.__name__}: {e}")
            import traceback
            traceback.print_exc()

    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)}")
    if failed == 0:
        print("ALL TESTS PASSED!")
    else:
        print("SOME TESTS FAILED")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
