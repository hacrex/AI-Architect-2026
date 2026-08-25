"""Script to view full observability system status."""
import sys
sys.path.insert(0, ".")

from pipelines.observability_pipeline import ObservabilityPipeline


def main():
    pipeline = ObservabilityPipeline()

    print("=== Simulating Traffic ===")
    result = pipeline.simulate_traffic(50)
    print(f"  Requests: {result['requests']}")
    print(f"  Traces: {result['traces']}")
    print(f"  LLM Calls: {result['llm_calls']}")
    print(f"  RAG Events: {result['rag_events']}")

    status = pipeline.get_full_status()

    print("\n=== Infrastructure ===")
    infra = status["infrastructure"]
    for k, v in infra.items():
        print(f"  {k}: {v}")

    print("\n=== AI Metrics ===")
    ai = status["ai_metrics"]
    for k, v in ai.items():
        print(f"  {k}: {v}")

    print("\n=== Traces ===")
    traces = status["traces"]
    for k, v in traces.items():
        print(f"  {k}: {v}")

    print("\n=== LLM ===")
    llm = status["llm"]
    for k, v in llm.items():
        print(f"  {k}: {v}")

    print("\n=== RAG ===")
    rag = status["rag"]
    for k, v in rag.items():
        print(f"  {k}: {v}")

    print("\n=== Agents ===")
    agents = status["agents"]
    for k, v in agents.items():
        print(f"  {k}: {v}")

    print("\n=== SLOs ===")
    slos = status["slos"]
    print(f"  Overall: {slos.get('overall_health', 'unknown')}")
    for s in slos.get("slo_details", []):
        print(f"  {s['name']}: {s['state']} (current: {s['current']}, target: {s['target']})")

    print("\n=== Alerts ===")
    alerts = status["alerts"]
    print(f"  Firing: {alerts.get('firing', 0)}")
    print(f"  Resolved: {alerts.get('resolved', 0)}")

    print("\n=== Drift ===")
    drift = status["drift"]
    print(f"  Metrics tracked: {drift.get('total_metrics_tracked', 0)}")
    print(f"  Drifting: {drift.get('drifting_metrics', 0)}")
    print(f"  Drift events: {drift.get('total_drift_events', 0)}")


if __name__ == "__main__":
    main()
