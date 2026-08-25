"""Tests for the AI Observability sample app."""
import sys
sys.path.insert(0, ".")

from app.metrics import MetricsCollector
from app.logger import StructuredLogger
from app.tracer import DistributedTracer
from app.llm_trace import LLMTracer
from app.rag_monitor import RAGMonitor
from app.agent_trace import AgentTracer
from app.slo_manager import SLOManager
from app.alert_manager import AlertManager
from app.drift_detector import DriftDetector
from app.models import TraceStatus, AlertSeverity, AlertState, SLOState, DriftStatus
from pipelines.observability_pipeline import ObservabilityPipeline


def test_metrics():
    print("=== Testing Metrics Collector ===")
    mc = MetricsCollector()

    mc.record("test_metric", 42.0)
    assert mc.get_latest("test_metric") == 42.0
    print(f"  Record + Get: {mc.get_latest('test_metric')}")

    mc.increment("counter_test")
    mc.increment("counter_test")
    assert mc.get_latest("counter_test") == 2.0
    print(f"  Counter: {mc.get_latest('counter_test')}")

    mc.gauge("gauge_test", 75.5)
    assert mc.get_latest("gauge_test") == 75.5
    print(f"  Gauge: {mc.get_latest('gauge_test')}")

    for i in range(10):
        mc.histogram("hist_test", float(i * 10))
    stats = mc.get_histogram_stats("hist_test")
    print(f"  Histogram: count={stats['count']}, p50={stats['p50']}, p95={stats['p95']}")
    assert stats["count"] == 10

    mc.gauge("gpu_utilization", 72.0)
    mc.gauge("cpu_utilization", 45.0)
    mc.increment("requests_total")
    summary = mc.get_infrastructure_summary()
    print(f"  Infrastructure summary: {len(summary)} metrics")
    assert "gpu_utilization" in summary

    ai_summary = mc.get_ai_summary()
    print(f"  AI summary: {len(ai_summary)} metrics")
    assert "total_llm_calls" in ai_summary

    print("PASSED\n")


def test_logger():
    print("=== Testing Structured Logger ===")
    logger = StructuredLogger(level="DEBUG")

    logger.info("Test message", component="test")
    logger.warning("Warning message", component="test")
    logger.error("Error message", component="llm")

    entries = logger.get_entries()
    print(f"  Total entries: {len(entries)}")
    assert len(entries) == 3

    errors = logger.get_entries(level="ERROR")
    print(f"  Error entries: {len(errors)}")
    assert len(errors) == 1

    llm_entries = logger.get_entries(component="llm")
    print(f"  LLM entries: {len(llm_entries)}")
    assert len(llm_entries) == 1

    logger.log_llm_call("openai", "gpt-4o", 1000, 500, 1200.0)
    logger.log_retrieval("test query", 5, 150.0, 0.85)
    logger.log_agent_step("research-agent", 1, "search", "web_search", 300.0)

    summary = logger.get_summary()
    print(f"  Summary: {summary['total_entries']} entries")
    print(f"  By level: {summary['by_level']}")
    print(f"  By component: {summary['by_component']}")

    print("PASSED\n")


def test_tracer():
    print("=== Testing Distributed Tracer ===")
    tracer = DistributedTracer()

    trace_id = tracer.start_trace("ai_request")
    print(f"  Trace started: {trace_id}")

    span1 = tracer.start_span(trace_id, "api_gateway")
    span2 = tracer.start_span(trace_id, "llm_call", span1)
    tracer.end_span(span2, TraceStatus.OK, {"model": "gpt-4o"})
    tracer.end_span(span1, TraceStatus.OK)

    trace = tracer.get_trace(trace_id)
    print(f"  Spans: {len(trace.spans)}")
    assert len(trace.spans) == 3

    tree = tracer.get_trace_tree(trace_id)
    print(f"  Tree root: {tree['root_operation']}")
    print(f"  Tree spans: {tree['span_count']}")
    assert tree["span_count"] == 3

    summary = tracer.get_trace_summary()
    print(f"  Summary: {summary['total_traces']} traces, {summary['total_spans']} spans")

    tracer.start_trace("another_request")
    traces = tracer.list_traces()
    print(f"  Listed traces: {len(traces)}")

    print("PASSED\n")


def test_llm_tracer():
    print("=== Testing LLM Tracer ===")
    lt = LLMTracer()

    c1 = lt.record_call("openai", "gpt-4o", 2000, 500, 1500.0, ttft_ms=300.0)
    c2 = lt.record_call("anthropic", "claude-3", 3000, 800, 2200.0)
    c3 = lt.record_call("openai", "gpt-4o", 1000, 200, 900.0, ttft_ms=150.0)

    summary = lt.get_summary()
    print(f"  Total calls: {summary['total_calls']}")
    print(f"  Total tokens: {summary['total_tokens']}")
    print(f"  Total cost: ${summary['total_cost_usd']:.6f}")
    print(f"  Avg latency: {summary['avg_latency_ms']:.1f}ms")
    assert summary["total_calls"] == 3
    assert c1.cost_usd > 0

    by_provider = lt.get_by_provider()
    print(f"  Providers: {list(by_provider.keys())}")
    assert "openai" in by_provider
    assert "anthropic" in by_provider

    by_model = lt.get_by_model()
    print(f"  Models: {list(by_model.keys())}")

    tokens = lt.get_token_distribution()
    print(f"  Token range: {tokens['input']['min']}-{tokens['input']['max']} input")

    print("PASSED\n")


def test_rag_monitor():
    print("=== Testing RAG Monitor ===")
    rm = RAGMonitor()

    rm.record_event("query 1", 5, 150.0, top_relevance_score=0.92, context_tokens=1250)
    rm.record_event("query 2", 3, 200.0, top_relevance_score=0.65, context_tokens=750)
    rm.record_event("query 3", 8, 100.0, top_relevance_score=0.88, context_tokens=2000)

    summary = rm.get_summary()
    print(f"  Total events: {summary['total_events']}")
    print(f"  Avg relevance: {summary['avg_relevance_score']:.4f}")
    print(f"  Avg docs: {summary['avg_documents_retrieved']:.1f}")
    assert summary["total_events"] == 3

    distribution = rm.get_relevance_distribution()
    print(f"  Relevance bins: {len(distribution['bins'])}")

    latency = rm.get_latency_breakdown()
    print(f"  Latency breakdown: {list(latency.keys())}")

    print("PASSED\n")


def test_agent_tracer():
    print("=== Testing Agent Tracer ===")
    at = AgentTracer()

    trace_id = at.start_run("research-agent")
    at.add_step("reason", reasoning="Analyzing query", duration_ms=150, tokens_used=50)
    at.add_step("search", tool_name="web_search", duration_ms=300)
    at.add_step("retrieve", tool_name="vector_db", duration_ms=200)
    at.add_step("respond", tool_name="llm", duration_ms=1200, tokens_used=200)
    at.end_run(TraceStatus.OK)

    detail = at.get_run_detail(trace_id)
    print(f"  Agent: {detail['agent_name']}")
    print(f"  Steps: {detail['total_steps']}")
    print(f"  Duration: {detail['total_duration_ms']:.1f}ms")
    print(f"  Loop detected: {detail['loop_detected']}")
    assert detail["total_steps"] == 4

    summary = at.get_summary()
    print(f"  Summary: {summary['total_runs']} runs, {summary['total_steps']} steps")
    assert summary["total_runs"] == 1

    tools = at.get_tool_usage()
    print(f"  Tools used: {list(tools.keys())}")

    print("PASSED\n")


def test_slo_manager():
    print("=== Testing SLO Manager ===")
    sm = SLOManager()

    summary = sm.get_summary()
    print(f"  Total SLOs: {summary['total_slos']}")
    print(f"  Healthy: {summary['healthy']}")
    print(f"  At risk: {summary['at_risk']}")
    print(f"  Breached: {summary['breached']}")
    print(f"  Overall: {summary['overall_health']}")
    assert summary["total_slos"] >= 4

    sm.record_sli("Availability", 99.8)
    sm.record_sli("Latency P95", 4500.0)
    sm.record_sli("Task Success", 88.0)

    slo = sm.get_slo("slo-001")
    print(f"  Availability state: {slo.state.value}")

    budgets = sm.get_error_budgets()
    print(f"  Error budgets: {len(budgets)} entries")

    print("PASSED\n")


def test_alert_manager():
    print("=== Testing Alert Manager ===")
    am = AlertManager()

    rules = am.list_rules()
    print(f"  Rules: {len(rules)}")
    assert len(rules) >= 5

    fired = am.evaluate({
        "p95_latency_ms": 7000,
        "error_rate_pct": 0.5,
        "retrieval_relevance": 65.0,
        "daily_cost_usd": 100.0,
    })
    print(f"  Alerts fired: {len(fired)}")
    for a in fired:
        print(f"    [{a.severity.value}] {a.name}: {a.message}")

    active = am.get_active_alerts()
    print(f"  Active alerts: {len(active)}")

    summary = am.get_alert_summary()
    print(f"  Alert summary: {summary['firing']} firing, {summary['resolved']} resolved")

    print("PASSED\n")


def test_drift_detector():
    print("=== Testing Drift Detector ===")
    dd = DriftDetector(window_size=50, baseline_size=10)

    for _ in range(15):
        dd.add_baseline("retrieval_relevance", 0.85)
    for _ in range(20):
        dd.add_sample("retrieval_relevance", 0.85)

    status = dd.get_status("retrieval_relevance")
    print(f"  Status after normal: {status.value}")
    assert status == DriftStatus.NORMAL

    for _ in range(10):
        dd.add_sample("retrieval_relevance", 0.40)

    status2 = dd.get_status("retrieval_relevance")
    print(f"  Status after drift: {status2.value}")

    stats = dd.get_metric_stats("retrieval_relevance")
    print(f"  Drift count: {stats['drift_count']}")
    print(f"  Max z-score: {stats['max_z_score']}")

    summary = dd.get_summary()
    print(f"  Summary: {summary['total_metrics_tracked']} metrics, {summary['total_drift_events']} events")

    print("PASSED\n")


def test_observability_pipeline():
    print("=== Testing Observability Pipeline ===")
    pipeline = ObservabilityPipeline()

    result = pipeline.simulate_traffic(30)
    print(f"  Traffic: {result['requests']} requests, {result['llm_calls']} LLM calls")
    assert result["requests"] == 30

    status = pipeline.get_full_status()
    print(f"  Status keys: {list(status.keys())}")
    assert "infrastructure" in status
    assert "llm" in status
    assert "rag" in status
    assert "slos" in status
    assert "alerts" in status
    assert "drift" in status

    trace_result = pipeline.simulate_full_request("test query")
    tree = pipeline.tracer.get_trace_tree(trace_result["trace_id"])
    print(f"  Trace spans: {tree['span_count']}")

    agent_result = pipeline.simulate_agent_run("test-agent")
    run = pipeline.agent_tracer.get_run_detail(agent_result["trace_id"])
    print(f"  Agent steps: {run['total_steps']}")

    investigation = pipeline.run_incident_investigation()
    print(f"  Investigation steps: {len(investigation['investigation_steps'])}")

    print("PASSED\n")


if __name__ == "__main__":
    print("AI Observability Tests\n")
    test_metrics()
    test_logger()
    test_tracer()
    test_llm_tracer()
    test_rag_monitor()
    test_agent_tracer()
    test_slo_manager()
    test_alert_manager()
    test_drift_detector()
    test_observability_pipeline()
    print("All tests passed!")
