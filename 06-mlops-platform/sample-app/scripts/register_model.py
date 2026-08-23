"""Script to register a model."""
from app.registry import ModelRegistry
from app.experiment import ExperimentTracker


def main():
    tracker = ExperimentTracker()
    registry = ModelRegistry()

    # Create experiment
    experiment = tracker.create_experiment(
        name="enterprise-rag",
        dataset_version="2024-01-15",
        model="gpt-4",
        prompt_template="Answer based on context: {context}",
        parameters={"temperature": 0.2, "max_tokens": 500}
    )
    print(f"Created experiment: {experiment.id}")

    # Log results
    tracker.log_results(experiment.id, {
        "accuracy": 0.91,
        "safety": 0.97,
        "cost": 750,
        "latency": 1200
    })

    # Register model
    model = registry.register(
        name="enterprise-rag",
        version="1.0.0",
        source_experiment=experiment.id,
        metrics={"accuracy": 0.91, "safety": 0.97},
        description="Enterprise RAG assistant v1"
    )
    print(f"Registered model: {model.name} v{model.version}")
    print(f"Stage: {model.stage}")


if __name__ == "__main__":
    main()
