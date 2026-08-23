"""Script to run evaluation."""
from app.evaluation import EvaluationPipeline


def main():
    evaluator = EvaluationPipeline()

    # Run evaluation
    result = evaluator.evaluate(
        model="enterprise-rag",
        version="1.0.0",
        test_dataset="test-v1.json",
        metrics=["accuracy", "safety", "cost", "latency"]
    )

    print(f"Evaluation: {result.id}")
    print(f"Model: {result.model} v{result.version}")
    print(f"Passed: {result.passed}")
    print("\nMetrics:")
    for k, v in result.metrics.items():
        print(f"  {k}: {v}")
    print("\nGates:")
    for gate in result.gates:
        status = "PASS" if gate.status.value == "pass" else "FAIL"
        print(f"  {gate.name}: {gate.actual} (threshold: {gate.threshold}) [{status}]")


if __name__ == "__main__":
    main()
