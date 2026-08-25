"""Pydantic models for Technology Decisions."""
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class DecisionStatus(str, Enum):
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    DEPRECATED = "deprecated"
    SUPERSEDED = "superseded"


class ConstraintType(str, Enum):
    HARD = "hard"
    SOFT = "soft"


class BuildBuyDecision(str, Enum):
    BUILD = "build"
    BUY = "buy"
    ADOPT = "adopt"
    AVOID = "avoid"


class TechnologyCategory(str, Enum):
    MODEL_HOSTING = "model_hosting"
    VECTOR_STORAGE = "vector_storage"
    INFERENCE_PLATFORM = "inference_platform"
    OBSERVABILITY = "observability"
    AUTHENTICATION = "authentication"
    GATEWAY = "gateway"
    DEPLOYMENT = "deployment"
    DATA_PROCESSING = "data_processing"


class DecisionCriteria(BaseModel):
    name: str
    weight: float = Field(ge=0.0, le=1.0)
    description: str = ""


class TechnologyOption(BaseModel):
    name: str
    category: TechnologyCategory
    description: str = ""
    provider: str = ""
    is_managed: bool = False
    is_open_source: bool = False
    estimated_monthly_cost: float = 0.0
    team_expertise_required: int = Field(default=3, ge=0, le=10)
    operational_burden: int = Field(default=5, ge=0, le=10)


class OptionScore(BaseModel):
    option_name: str
    scores: dict[str, float] = Field(default_factory=dict)
    weighted_score: float = 0.0
    hard_constraint_violations: list[str] = Field(default_factory=list)
    is_disqualified: bool = False


class DecisionMatrix(BaseModel):
    id: str
    category: TechnologyCategory
    title: str
    criteria: list[DecisionCriteria]
    options: list[TechnologyOption]
    scores: list[OptionScore] = Field(default_factory=list)
    hard_constraints: list[str] = Field(default_factory=list)
    selected_option: Optional[str] = None
    rationale: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)


class HardConstraint(BaseModel):
    id: str
    name: str
    description: str
    constraint_type: ConstraintType = ConstraintType.HARD
    eliminates_options: list[str] = Field(default_factory=list)
    is_satisfied: bool = True


class BuildBuyOption(BaseModel):
    name: str
    description: str
    build_cost_5yr: float = 0.0
    buy_cost_5yr: float = 0.0
    is_competitive_advantage: bool = False
    team_can_build: bool = True
    migration_cost: float = 0.0
    time_to_value_weeks: int = 0


class BuildBuyAnalysis(BaseModel):
    id: str
    component: str
    options: list[BuildBuyOption]
    recommendation: str = ""
    rationale: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ADR(BaseModel):
    id: str
    title: str
    context: str
    options: list[str]
    decision: str
    rationale: str = ""
    consequences: dict = Field(default_factory=dict)
    revisit_conditions: list[str] = Field(default_factory=list)
    status: DecisionStatus = DecisionStatus.PROPOSED
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metrics_to_track: dict[str, str] = Field(default_factory=dict)
