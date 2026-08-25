"""Script to demonstrate incident investigation."""
import sys
sys.path.insert(0, ".")

from pipelines.observability_pipeline import ObservabilityPipeline


def main():
    pipeline = ObservabilityPipeline()

    print("=== AI Incident Investigation Demo ===\n")

    pipeline.simulate_traffic(50)

    print("--- Incident: AI answers became worse ---\n")

    investigation = pipeline.run_incident_investigation()

    print(f"Incident: {investigation['incident']}\n")
    print("Investigation Steps:")
    for step in investigation["investigation_steps"]:
        status_icon = "OK" if step["result"] == "healthy" else "!!" if step["result"] in ("DEGRADED", "ROOT CAUSE") else ">>"
        print(f"  Step {step['step']}: [{status_icon}] {step['check']}")
        print(f"    Result: {step['result']}")
        print(f"    Detail: {step['detail']}\n")

    print(f"Conclusion: {investigation['conclusion']}")

    print("\n--- Alert Evaluation ---")
    alert_result = pipeline.alert_manager.evaluate({
        "p95_latency_ms": 6000,
        "error_rate_pct": 0.5,
        "retrieval_relevance": 65.0,
        "daily_cost_usd": 120.0,
    })
    print(f"  Rules evaluated: {len(pipeline.alert_manager._rules)}")
    print(f"  Alerts fired: {len(alert_result)}")
    for a in alert_result:
        print(f"    [{a.severity.value.upper()}] {a.name}: {a.message}")

    print("\n--- Drift Detection ---")
    for i in range(15):
        pipeline.drift_detector.add_sample("retrieval_relevance", 0.85 + (i * 0.002))
    for i in range(10):
        pipeline.drift_detector.add_sample("retrieval_relevance", 0.55 + (i * 0.005))

    status = pipeline.drift_detector.get_summary()
    print(f"  Metrics tracked: {status['total_metrics_tracked']}")
    print(f"  Drifting: {status['drifting_metrics']}")
    print(f"  Drift events: {status['total_drift_events']}")
    for name, stats in status.get("metrics", {}).items():
        print(f"    {name}: {stats.get('status', 'unknown')} (drift_count: {stats.get('drift_count', 0)})")


if __name__ == "__main__":
    main()
