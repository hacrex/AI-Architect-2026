"""Pydantic models for the MLOps platform."""
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class ModelStage(str, Enum):
    EXPERIMENT = "experiment"
    STAGING = "staging"
    CANARY = "canary"
    PRODUCTION = "production"
    ARCHIVED = "archived"


class DeploymentStatus(str, Enum):
    PENDING = "pending"
    DEPLOYING = "deploying"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class EvalGateStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"


# Experiment Models
class ExperimentCreate(BaseModel):
    name: str
    dataset_version: str
    model: str
    prompt_template: str
    parameters: dict = Field(default_factory=dict)


class Experiment(BaseModel):
    id: str
    name: str
    dataset_version: str
    model: str
    prompt_template: str
    parameters: dict
    metrics: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "created"


# Model Registry Models
class ModelRegister(BaseModel):
    name: str
    version: str
    source_experiment: Optional[str] = None
    metrics: dict = Field(default_factory=dict)
    artifacts: dict = Field(default_factory=dict)
    description: str = ""


class ModelVersion(BaseModel):
    name: str
    version: str
    stage: ModelStage = ModelStage.EXPERIMENT
    source_experiment: Optional[str] = None
    metrics: dict = Field(default_factory=dict)
    artifacts: dict = Field(default_factory=dict)
    description: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    approved_by: Optional[str] = None


class ModelPromote(BaseModel):
    name: str
    version: str
    stage: ModelStage
    approved_by: str = "system"


class ModelRollback(BaseModel):
    name: str
    reason: str


# Evaluation Models
class EvaluationRun(BaseModel):
    model: str
    version: str
    test_dataset: str
    metrics: list[str] = Field(default_factory=lambda: ["accuracy", "safety", "cost", "latency"])


class EvalGate(BaseModel):
    name: str
    threshold: float
    actual: float
    status: EvalGateStatus


class EvaluationResult(BaseModel):
    id: str
    model: str
    version: str
    test_dataset: str
    metrics: dict = Field(default_factory=dict)
    gates: list[EvalGate] = Field(default_factory=list)
    passed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)


# Deployment Models
class DeploymentRequest(BaseModel):
    model: str
    version: str
    environment: str = "staging"


class CanaryRequest(BaseModel):
    model: str
    version: str
    initial_percentage: int = 5
    increment: int = 25
    observation_period_seconds: int = 60


class Deployment(BaseModel):
    id: str
    model: str
    version: str
    environment: str
    status: DeploymentStatus = DeploymentStatus.PENDING
    canary_percentage: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Monitoring Models
class ModelHealth(BaseModel):
    model: str
    status: str
    quality_score: float
    drift_detected: bool
    latency_p95: float
    error_rate: float
    last_checked: datetime = Field(default_factory=datetime.utcnow)


class DriftReport(BaseModel):
    model: str
    time_range: str
    data_drift: float
    concept_drift: float
    quality_trend: list[float] = Field(default_factory=list)
    recommendation: str
