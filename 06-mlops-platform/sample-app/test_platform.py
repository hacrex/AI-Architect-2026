"""Test the MLOps platform components."""
import sys
sys.path.insert(0, ".")

from app.experiment import ExperimentTracker
from app.registry import ModelRegistry
from app.evaluation import EvaluationPipeline
from app.deployment import DeploymentEngine
from app.monitoring import Monitor
from app.models import ModelStage
from pipelines.cicd_pipeline import CICDPipeline


def test_experiment_tracker():
    print("=== Testing Experiment Tracker ===")
    tracker = ExperimentTracker()

    # Create experiment
    exp = tracker.create_experiment(
        name="test-exp",
        dataset_version="v1",
        model="gpt-4",
        prompt_template="test",
        parameters={"temp": 0.5}
    )
    print(f"Created: {exp.id}")

    # Log results
    tracker.log_results(exp.id, {"accuracy": 0.92, "latency": 1500})
    print("Logged results")

    # List experiments
    experiments = tracker.list_experiments()
    print(f"Total experiments: {len(experiments)}")
    print("PASSED\n")


def test_model_registry():
    print("=== Testing Model Registry ===")
    registry = ModelRegistry()

    # Register model
    model = registry.register(
        name="test-model",
        version="1.0.0",
        metrics={"accuracy": 0.9}
    )
    print(f"Registered: {model.name} v{model.version}")

    # Promote
    registry.promote("test-model", "1.0.0", ModelStage.STAGING)
    print("Promoted to staging")

    registry.promote("test-model", "1.0.0", ModelStage.PRODUCTION)
    print("Promoted to production")

    # Get production model
    prod = registry.get_production_model("test-model")
    print(f"Production version: {prod.version}")
    print("PASSED\n")


def test_evaluation():
    print("=== Testing Evaluation Pipeline ===")
    evaluator = EvaluationPipeline()

    # Run evaluation
    result = evaluator.evaluate(
        model="test-model",
        version="1.0.0",
        test_dataset="test.json"
    )
    print(f"Evaluation: {result.id}")
    print(f"Passed: {result.passed}")
    print(f"Gates: {len(result.gates)}")
    print("PASSED\n")


def test_deployment():
    print("=== Testing Deployment Engine ===")
    deployer = DeploymentEngine()

    # Deploy
    deployment = deployer.deploy("test-model", "1.0.0", "staging")
    print(f"Deployed: {deployment.id}")
    print(f"Status: {deployment.status.value}")

    # Canary
    canary = deployer.canary("test-model", "1.0.0", 5, 25, 10)
    print(f"Canary: {canary.status.value}")
    print("PASSED\n")


def test_monitoring():
    print("=== Testing Monitoring ===")
    monitor = Monitor()

    # Health check
    health = monitor.check_health("test-model")
    print(f"Status: {health.status}")
    print(f"Quality: {health.quality_score}")

    # Drift report
    report = monitor.get_drift_report("test-model")
    print(f"Data drift: {report.data_drift}")
    print("PASSED\n")


def test_cicd_pipeline():
    print("=== Testing CI/CD Pipeline ===")
    pipeline = CICDPipeline()

    result = pipeline.run("test-model", "1.0.0")
    print(f"Pipeline: {result['pipeline_id']}")
    print(f"Status: {result['status']}")
    print(f"Stages: {len(result['stages'])}")
    print("PASSED\n")


if __name__ == "__main__":
    print("MLOps Platform Tests\n")
    test_experiment_tracker()
    test_model_registry()
    test_evaluation()
    test_deployment()
    test_monitoring()
    test_cicd_pipeline()
    print("All tests passed!")
