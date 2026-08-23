"""Evaluation pipeline with quality gates."""
import uuid
import random
from datetime import datetime
from app.models import EvaluationResult, EvalGate, EvalGateStatus


class EvaluationPipeline:
    """Run evaluations with quality gates before deployment."""

    # Default gate thresholds
    DEFAULT_GATES = {
        "accuracy": {"threshold": 0.85, "direction": "min"},
        "safety": {"threshold": 0.95, "direction": "min"},
        "cost": {"threshold": 1000, "direction": "max"},
        "latency": {"threshold": 2000, "direction": "max"},
    }

    def __init__(self, gate_config: dict = None):
        self.gates = gate_config or self.DEFAULT_GATES
        self._evaluations: dict[str, EvaluationResult] = {}

    def evaluate(self, model: str, version: str, test_dataset: str,
                 metrics: list[str] = None) -> EvaluationResult:
        """Run evaluation on a model version."""
        eval_id = f"eval-{uuid.uuid4().hex[:8]}"

        # Simulate evaluation metrics (in real app, run actual evaluation)
        simulated_metrics = self._simulate_evaluation(model, version, test_dataset)

        # Check gates
        gates = []
        all_passed = True
        for metric_name in metrics or self.gates.keys():
            if metric_name in simulated_metrics:
                actual = simulated_metrics[metric_name]
                gate_config = self.gates.get(metric_name, {})
                threshold = gate_config.get("threshold", 0)
                direction = gate_config.get("direction", "min")

                # Check if gate passes
                if direction == "min":
                    passed = actual >= threshold
                else:
                    passed = actual <= threshold

                gate = EvalGate(
                    name=metric_name,
                    threshold=threshold,
                    actual=actual,
                    status=EvalGateStatus.PASS if passed else EvalGateStatus.FAIL
                )
                gates.append(gate)
                if not passed:
                    all_passed = False

        result = EvaluationResult(
            id=eval_id,
            model=model,
            version=version,
            test_dataset=test_dataset,
            metrics=simulated_metrics,
            gates=gates,
            passed=all_passed
        )
        self._evaluations[eval_id] = result
        return result

    def get_evaluation(self, eval_id: str) -> EvaluationResult:
        """Get evaluation result by ID."""
        return self._evaluations.get(eval_id)

    def list_evaluations(self, model: str = None) -> list[EvaluationResult]:
        """List evaluations, optionally filtered by model."""
        evals = list(self._evaluations.values())
        if model:
            evals = [e for e in evals if e.model == model]
        return sorted(evals, key=lambda e: e.created_at, reverse=True)

    def _simulate_evaluation(self, model: str, version: str, test_dataset: str) -> dict:
        """Simulate evaluation metrics."""
        # In a real system, this would run actual evaluation
        # Here we simulate realistic metrics
        seed = hash(f"{model}-{version}-{test_dataset}") % 1000
        random.seed(seed)

        return {
            "accuracy": round(random.uniform(0.75, 0.95), 3),
            "safety": round(random.uniform(0.88, 0.99), 3),
            "cost": random.randint(500, 1500),
            "latency": random.randint(800, 2500),
            "groundedness": round(random.uniform(0.80, 0.98), 3),
            "relevance": round(random.uniform(0.78, 0.96), 3),
        }

    def passed_all_gates(self, eval_id: str) -> bool:
        """Check if an evaluation passed all gates."""
        result = self._evaluations.get(eval_id)
        if result:
            return result.passed
        return False

    def get_gate_summary(self, eval_id: str) -> dict:
        """Get a summary of gate results."""
        result = self._evaluations.get(eval_id)
        if not result:
            return {"error": "Evaluation not found"}

        summary = {
            "model": result.model,
            "version": result.version,
            "passed": result.passed,
            "gates": []
        }

        for gate in result.gates:
            summary["gates"].append({
                "name": gate.name,
                "threshold": gate.threshold,
                "actual": gate.actual,
                "status": gate.status.value
            })

        return summary
