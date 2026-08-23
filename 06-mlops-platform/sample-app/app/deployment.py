"""Deployment engine with canary and rollback support."""
import uuid
import time
from datetime import datetime
from typing import Optional
from app.models import Deployment, DeploymentStatus


class DeploymentEngine:
    """Manage model deployments with canary strategy."""

    def __init__(self):
        self._deployments: dict[str, Deployment] = {}
        self._active_deployments: dict[str, str] = {}  # model -> deployment_id

    def deploy(self, model: str, version: str, environment: str = "staging") -> Deployment:
        """Deploy a model to an environment."""
        deploy_id = f"deploy-{uuid.uuid4().hex[:8]}"

        deployment = Deployment(
            id=deploy_id,
            model=model,
            version=version,
            environment=environment,
            status=DeploymentStatus.DEPLOYING
        )
        self._deployments[deploy_id] = deployment

        # Simulate deployment
        deployment.status = DeploymentStatus.HEALTHY
        deployment.updated_at = datetime.utcnow()

        # Track active deployment
        if environment == "production":
            self._active_deployments[model] = deploy_id

        return deployment

    def get_deployment(self, deployment_id: str) -> Optional[Deployment]:
        """Get deployment by ID."""
        return self._deployments.get(deployment_id)

    def list_deployments(self, model: str = None, environment: str = None) -> list[Deployment]:
        """List deployments with optional filters."""
        deployments = list(self._deployments.values())
        if model:
            deployments = [d for d in deployments if d.model == model]
        if environment:
            deployments = [d for d in deployments if d.environment == environment]
        return sorted(deployments, key=lambda d: d.created_at, reverse=True)

    def canary(self, model: str, version: str, initial_percentage: int = 5,
               increment: int = 25, observation_period_seconds: int = 60) -> Deployment:
        """Deploy with canary strategy."""
        deploy_id = f"deploy-canary-{uuid.uuid4().hex[:8]}"

        deployment = Deployment(
            id=deploy_id,
            model=model,
            version=version,
            environment="production",
            status=DeploymentStatus.DEPLOYING,
            canary_percentage=initial_percentage
        )
        self._deployments[deploy_id] = deployment

        # Simulate canary rollout
        current_percentage = initial_percentage
        while current_percentage < 100:
            # Simulate health check
            is_healthy = self._check_canary_health(model, version, current_percentage)

            if not is_healthy:
                deployment.status = DeploymentStatus.DEGRADED
                self.rollback(model, f"canary_health_check_failed_at_{current_percentage}%")
                return deployment

            # Increase percentage
            current_percentage = min(current_percentage + increment, 100)
            deployment.canary_percentage = current_percentage
            deployment.updated_at = datetime.utcnow()

            if current_percentage >= 100:
                deployment.status = DeploymentStatus.HEALTHY
                break

        self._active_deployments[model] = deploy_id
        return deployment

    def rollback(self, model: str, reason: str = "manual") -> Deployment:
        """Rollback a model to previous version."""
        # Find current active deployment
        active_id = self._active_deployments.get(model)
        if active_id:
            deployment = self._deployments.get(active_id)
            if deployment:
                deployment.status = DeploymentStatus.ROLLED_BACK
                deployment.updated_at = datetime.utcnow()

        # Deploy previous version (simulated)
        rollback_deploy_id = f"deploy-rollback-{uuid.uuid4().hex[:8]}"
        rollback = Deployment(
            id=rollback_deploy_id,
            model=model,
            version="previous",
            environment="production",
            status=DeploymentStatus.HEALTHY
        )
        self._deployments[rollback_deploy_id] = rollback
        self._active_deployments[model] = rollback_deploy_id

        return rollback

    def pause(self, deployment_id: str) -> Deployment:
        """Pause traffic to a deployment."""
        deployment = self._deployments.get(deployment_id)
        if deployment:
            deployment.status = DeploymentStatus.DEPLOYING  # Simulate paused
            deployment.updated_at = datetime.utcnow()
        return deployment

    def resume(self, deployment_id: str) -> Deployment:
        """Resume traffic to a deployment."""
        deployment = self._deployments.get(deployment_id)
        if deployment:
            deployment.status = DeploymentStatus.HEALTHY
            deployment.updated_at = datetime.utcnow()
        return deployment

    def _check_canary_health(self, model: str, version: str, percentage: int) -> bool:
        """Simulate canary health check."""
        # In production, this would check actual metrics
        # Simulate occasional failures for realism
        import random
        return random.random() > 0.05  # 95% success rate

    def get_active_deployment(self, model: str) -> Optional[Deployment]:
        """Get the active production deployment for a model."""
        active_id = self._active_deployments.get(model)
        return self._deployments.get(active_id)
