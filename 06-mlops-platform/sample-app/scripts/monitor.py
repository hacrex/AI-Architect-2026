"""Script to check monitoring."""
from app.monitoring import Monitor


def main():
    monitor = Monitor()

    # Check health
    health = monitor.check_health("enterprise-rag")
    print(f"Health Status: {health.status}")
    print(f"Quality Score: {health.quality_score}")
    print(f"Drift Detected: {health.drift_detected}")
    print(f"Latency P95: {health.latency_p95}ms")
    print(f"Error Rate: {health.error_rate}")

    # Get drift report
    print("\nDrift Report:")
    report = monitor.get_drift_report("enterprise-rag", "7d")
    print(f"Data Drift: {report.data_drift}")
    print(f"Concept Drift: {report.concept_drift}")
    print(f"Recommendation: {report.recommendation}")

    # Get metrics summary
    print("\nMetrics Summary:")
    summary = monitor.get_metrics_summary("enterprise-rag")
    for k, v in summary.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
