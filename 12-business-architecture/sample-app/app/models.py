"""Pydantic models for AI Business Architecture Portfolio."""
from datetime import datetime
from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel, Field


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class UseCaseStatus(str, Enum):
    IDENTIFIED = "identified"
    PRIORITIZED = "prioritized"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"


class ADRStatus(str, Enum):
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    DEPRECATED = "deprecated"
    SUPERSEDED = "superseded"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ArchitecturePhase(str, Enum):
    PROBLEM = "problem"
    OUTCOME = "outcome"
    REQUIREMENTS = "requirements"
    ARCHITECTURE = "architecture"
    DECISIONS = "decisions"
    RISKS = "risks"
    COST = "cost"
    SUCCESS = "success"


class UseCase(BaseModel):
    id: str
    name: str
    description: str
    business_value: int = Field(ge=1, le=5)
    feasibility: int = Field(ge=1, le=5)
    data_readiness: int = Field(ge=1, le=5)
    risk: int = Field(ge=1, le=5)
    cost: int = Field(ge=1, le=5)
    time_to_value: int = Field(ge=1, le=5)
    status: UseCaseStatus = UseCaseStatus.IDENTIFIED
    owner: str = ""
    dependencies: list[str] = Field(default_factory=list)
    metrics: dict[str, str] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def weighted_score(self, weights: dict[str, float] = None) -> float:
        if weights is None:
            weights = {
                "business_value": 0.25,
                "feasibility": 0.20,
                "data_readiness": 0.20,
                "risk": 0.15,
                "cost": 0.10,
                "time_to_value": 0.10,
            }
        scores = {
            "business_value": self.business_value,
            "feasibility": self.feasibility,
            "data_readiness": self.data_readiness,
            "risk": self.risk,
            "cost": self.cost,
            "time_to_value": self.time_to_value,
        }
        return round(sum(scores[k] * weights.get(k, 0) for k in scores), 2)


class ADR(BaseModel):
    id: str
    title: str
    status: ADRStatus = ADRStatus.PROPOSED
    context: str
    options: list[dict[str, Any]] = Field(default_factory=list)
    decision: str
    rationale: str
    consequences: list[str] = Field(default_factory=list)
    revisit_conditions: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TradeOff(BaseModel):
    id: str
    title: str
    dimension_a: str
    dimension_b: str
    options: list[dict[str, Any]] = Field(default_factory=list)
    winner: str
    rationale: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CostItem(BaseModel):
    name: str
    category: str
    annual_cost: float
    description: str = ""


class CostModel(BaseModel):
    id: str
    name: str
    items: list[CostItem] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def total_cost(self) -> float:
        return sum(item.annual_cost for item in self.items)

    def by_category(self) -> dict[str, float]:
        categories = {}
        for item in self.items:
            categories[item.category] = categories.get(item.category, 0) + item.annual_cost
        return categories


class BusinessMetric(BaseModel):
    name: str
    category: str
    baseline: float
    target: float
    unit: str = ""
    measurement_method: str = ""


class BusinessValue(BaseModel):
    id: str
    name: str
    employees_affected: int = 0
    time_saved_minutes_per_day: float = 0
    working_days_per_year: int = 220
    hourly_rate: float = 60.0
    metrics: list[BusinessMetric] = Field(default_factory=list)
    cost_model_id: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def annual_productivity_value(self) -> float:
        hours_per_year = (self.time_saved_minutes_per_day / 60) * self.working_days_per_year
        return self.employees_affected * hours_per_year * self.hourly_rate

    def roi(self, total_ai_cost: float) -> float:
        value = self.annual_productivity_value()
        if total_ai_cost == 0:
            return 0
        return round((value - total_ai_cost) / total_ai_cost * 100, 1)

    def payback_months(self, total_ai_cost: float) -> float:
        monthly_value = self.annual_productivity_value() / 12
        monthly_cost = total_ai_cost / 12
        if monthly_cost == 0:
            return 0
        return round(monthly_cost / monthly_value * 12, 1) if monthly_value > 0 else 999


class Risk(BaseModel):
    id: str
    name: str
    description: str
    impact: RiskLevel
    likelihood: RiskLevel
    mitigation: str
    detection: str = ""
    response: str = ""
    owner: str = ""


class Project(BaseModel):
    id: str
    name: str
    description: str
    business_context: str
    requirements: list[str] = Field(default_factory=list)
    architecture_components: list[str] = Field(default_factory=list)
    key_decisions: list[str] = Field(default_factory=list)
    risks: list[Risk] = Field(default_factory=list)
    cost_model: Optional[CostModel] = None
    business_value: Optional[BusinessValue] = None
    demonstrates: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ReviewSection(BaseModel):
    phase: ArchitecturePhase
    question: str
    answer: str = ""
    time_minutes: int = 5


class ArchitectureReview(BaseModel):
    project_id: str
    project_name: str
    sections: list[ReviewSection] = Field(default_factory=list)
    total_time_minutes: int = 45
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ExecutiveBrief(BaseModel):
    project_name: str
    problem: str
    users: str
    outcome: str
    requirements: list[str] = Field(default_factory=list)
    architecture_summary: str
    top_decisions: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    governance: list[str] = Field(default_factory=list)
    cost_summary: str = ""
    success_metrics: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
