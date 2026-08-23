"""Experiment tracking for ML experiments."""
import uuid
from datetime import datetime
from typing import Optional
from app.models import Experiment, ExperimentCreate


class ExperimentTracker:
    """Track ML experiments with parameters, metrics, and results."""

    def __init__(self):
        self._experiments: dict[str, Experiment] = {}

    def create_experiment(self, name: str, dataset_version: str, model: str,
                          prompt_template: str, parameters: dict) -> Experiment:
        """Create a new experiment."""
        exp_id = f"exp-{uuid.uuid4().hex[:8]}"
        experiment = Experiment(
            id=exp_id,
            name=name,
            dataset_version=dataset_version,
            model=model,
            prompt_template=prompt_template,
            parameters=parameters,
            status="running"
        )
        self._experiments[exp_id] = experiment
        return experiment

    def get_experiment(self, experiment_id: str) -> Optional[Experiment]:
        """Get experiment by ID."""
        return self._experiments.get(experiment_id)

    def list_experiments(self, name: Optional[str] = None) -> list[Experiment]:
        """List all experiments, optionally filtered by name."""
        experiments = list(self._experiments.values())
        if name:
            experiments = [e for e in experiments if e.name == name]
        return sorted(experiments, key=lambda e: e.created_at, reverse=True)

    def log_results(self, experiment_id: str, metrics: dict) -> Experiment:
        """Log metrics results for an experiment."""
        experiment = self._experiments.get(experiment_id)
        if not experiment:
            raise ValueError(f"Experiment {experiment_id} not found")
        experiment.metrics.update(metrics)
        experiment.status = "completed"
        experiment.updated_at = datetime.utcnow()
        return experiment

    def log_metric(self, experiment_id: str, key: str, value: float) -> Experiment:
        """Log a single metric."""
        return self.log_results(experiment_id, {key: value})

    def compare_experiments(self, experiment_ids: list[str]) -> dict:
        """Compare multiple experiments."""
        comparison = {"experiments": [], "best": {}}
        for exp_id in experiment_ids:
            exp = self._experiments.get(exp_id)
            if exp:
                comparison["experiments"].append({
                    "id": exp.id,
                    "name": exp.name,
                    "metrics": exp.metrics,
                    "parameters": exp.parameters
                })
        # Find best by accuracy if available
        valid_exps = [e for e in comparison["experiments"] if "accuracy" in e["metrics"]]
        if valid_exps:
            best = max(valid_exps, key=lambda e: e["metrics"]["accuracy"])
            comparison["best"] = best["id"]
        return comparison
