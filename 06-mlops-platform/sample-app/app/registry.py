"""Model registry for versioning and managing models."""
import uuid
from datetime import datetime
from typing import Optional
from app.models import ModelVersion, ModelStage


class ModelRegistry:
    """Central registry for model versions and promotions."""

    def __init__(self):
        self._models: dict[str, list[ModelVersion]] = {}

    def register(self, name: str, version: str, source_experiment: Optional[str] = None,
                 metrics: dict = None, artifacts: dict = None, description: str = "") -> ModelVersion:
        """Register a new model version."""
        if name not in self._models:
            self._models[name] = []

        # Check if version already exists
        for m in self._models[name]:
            if m.version == version:
                raise ValueError(f"Model {name} version {version} already exists")

        model = ModelVersion(
            name=name,
            version=version,
            source_experiment=source_experiment,
            metrics=metrics or {},
            artifacts=artifacts or {},
            description=description
        )
        self._models[name].append(model)
        return model

    def get_model(self, name: str, version: str) -> Optional[ModelVersion]:
        """Get a specific model version."""
        for m in self._models.get(name, []):
            if m.version == version:
                return m
        return None

    def list_models(self, name: Optional[str] = None) -> dict[str, list[ModelVersion]]:
        """List all models or a specific model's versions."""
        if name:
            return {name: self._models.get(name, [])}
        return self._models

    def list_versions(self, name: str) -> list[ModelVersion]:
        """List all versions of a model."""
        return self._models.get(name, [])

    def promote(self, name: str, version: str, stage: ModelStage, approved_by: str = "system") -> ModelVersion:
        """Promote a model to a new stage."""
        model = self.get_model(name, version)
        if not model:
            raise ValueError(f"Model {name} version {version} not found")

        # Validate promotion path
        valid_transitions = {
            ModelStage.EXPERIMENT: [ModelStage.STAGING],
            ModelStage.STAGING: [ModelStage.CANARY, ModelStage.PRODUCTION],
            ModelStage.CANARY: [ModelStage.PRODUCTION],
            ModelStage.PRODUCTION: [ModelStage.ARCHIVED],
        }

        allowed = valid_transitions.get(model.stage, [])
        if stage not in allowed:
            raise ValueError(f"Cannot promote from {model.stage} to {stage}")

        model.stage = stage
        model.approved_by = approved_by
        model.updated_at = datetime.utcnow()
        return model

    def rollback(self, name: str, reason: str) -> ModelVersion:
        """Rollback to the previous production version."""
        versions = self._models.get(name, [])
        prod_versions = [v for v in versions if v.stage == ModelStage.PRODUCTION]

        if len(prod_versions) < 2:
            raise ValueError(f"No previous version to rollback to for {name}")

        # Sort by created_at descending
        prod_versions.sort(key=lambda v: v.created_at, reverse=True)
        current = prod_versions[0]
        previous = prod_versions[1]

        # Archive current, restore previous
        current.stage = ModelStage.ARCHIVED
        current.updated_at = datetime.utcnow()
        previous.stage = ModelStage.PRODUCTION
        previous.updated_at = datetime.utcnow()

        return previous

    def get_production_model(self, name: str) -> Optional[ModelVersion]:
        """Get the current production version of a model."""
        versions = self._models.get(name, [])
        for v in versions:
            if v.stage == ModelStage.PRODUCTION:
                return v
        return None

    def get_model_lineage(self, name: str) -> list[dict]:
        """Get the full lineage of a model."""
        versions = self._models.get(name, [])
        lineage = []
        for v in sorted(versions, key=lambda x: x.created_at):
            lineage.append({
                "version": v.version,
                "stage": v.stage.value,
                "source_experiment": v.source_experiment,
                "created_at": v.created_at.isoformat(),
                "metrics": v.metrics
            })
        return lineage
