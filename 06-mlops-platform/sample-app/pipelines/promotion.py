"""Model promotion workflow."""
from datetime import datetime
from typing import Optional
from app.registry import ModelRegistry
from app.evaluation import EvaluationPipeline
from app.deployment import DeploymentEngine
from app.models import ModelStage


class PromotionWorkflow:
    """Orchestrate model promotion through stages."""

    def __init__(self, registry: ModelRegistry, evaluator: EvaluationPipeline,
                 deployer: DeploymentEngine):
        self.registry = registry
        self.evaluator = evaluator
        self.deployer = deployer

    def promote_to_staging(self, name: str, version: str, test_dataset: str,
                           approved_by: str = "system") -> dict:
        """Promote model from experiment to staging."""
        result = {"model": name, "version": version, "steps": []}

        # Step 1: Run evaluation
        evaluation = self.evaluator.evaluate(
            model=name,
            version=version,
            test_dataset=test_dataset,
            metrics=["accuracy", "safety", "cost", "latency"]
        )
        result["steps"].append({
            "step": "evaluation",
            "passed": evaluation.passed,
            "details": self.evaluator.get_gate_summary(evaluation.id)
        })

        if not evaluation.passed:
            result["status"] = "failed"
            result["reason"] = "evaluation_failed"
            return result

        # Step 2: Register in registry
        try:
            model = self.registry.get_model(name, version)
            if not model:
                model = self.registry.register(
                    name=name,
                    version=version,
                    source_experiment=f"auto-from-eval-{evaluation.id}",
                    metrics=evaluation.metrics
                )
            result["steps"].append({"step": "registered", "status": "success"})
        except ValueError as e:
            result["status"] = "failed"
            result["reason"] = str(e)
            return result

        # Step 3: Promote to staging
        try:
            self.registry.promote(name, version, ModelStage.STAGING, approved_by)
            result["steps"].append({"step": "promoted_to_staging", "status": "success"})
        except ValueError as e:
            result["status"] = "failed"
            result["reason"] = str(e)
            return result

        # Step 4: Deploy to staging
        deployment = self.deployer.deploy(name, version, "staging")
        result["steps"].append({
            "step": "deployed_to_staging",
            "deployment_id": deployment.id
        })

        result["status"] = "success"
        result["stage"] = "staging"
        return result

    def promote_to_production(self, name: str, version: str,
                              use_canary: bool = True) -> dict:
        """Promote model from staging to production."""
        result = {"model": name, "version": version, "steps": []}

        # Step 1: Promote to canary/production
        target_stage = ModelStage.CANARY if use_canary else ModelStage.PRODUCTION
        try:
            self.registry.promote(name, version, target_stage)
            result["steps"].append({
                "step": f"promoted_to_{target_stage.value}",
                "status": "success"
            })
        except ValueError as e:
            result["status"] = "failed"
            result["reason"] = str(e)
            return result

        # Step 2: Deploy
        if use_canary:
            deployment = self.deployer.canary(
                name, version,
                initial_percentage=5,
                increment=25,
                observation_period_seconds=60
            )
        else:
            deployment = self.deployer.deploy(name, version, "production")

        result["steps"].append({
            "step": "deployed",
            "deployment_id": deployment.id,
            "status": deployment.status.value
        })

        if deployment.status.value in ["healthy"]:
            # Step 3: Final promotion to production
            try:
                self.registry.promote(name, version, ModelStage.PRODUCTION)
                result["steps"].append({"step": "promoted_to_production", "status": "success"})
            except ValueError as e:
                result["status"] = "failed"
                result["reason"] = str(e)
                return result

        result["status"] = "success"
        result["stage"] = "production"
        return result

    def rollback(self, name: str, reason: str = "manual") -> dict:
        """Rollback a model to previous version."""
        result = {"model": name, "reason": reason, "steps": []}

        # Step 1: Rollback in registry
        try:
            previous = self.registry.rollback(name, reason)
            result["steps"].append({
                "step": "registry_rollback",
                "previous_version": previous.version,
                "status": "success"
            })
        except ValueError as e:
            result["status"] = "failed"
            result["reason"] = str(e)
            return result

        # Step 2: Deploy previous version
        deployment = self.deployer.rollback(name, reason)
        result["steps"].append({
            "step": "deployment_rollback",
            "deployment_id": deployment.id
        })

        result["status"] = "success"
        return result
