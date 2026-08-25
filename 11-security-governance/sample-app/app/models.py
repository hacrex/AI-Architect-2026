"""Pydantic models for AI Security & Governance."""
from datetime import datetime
from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ClassificationLevel(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class AuthAction(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_APPROVAL = "require_approval"


class ThreatCategory(str, Enum):
    INJECTION = "injection"
    LEAKAGE = "leakage"
    PRIVILEGE = "privilege"
    INTEGRITY = "integrity"
    AVAILABILITY = "availability"


class User(BaseModel):
    id: str
    name: str
    email: str
    roles: list[str] = Field(default_factory=list)
    departments: list[str] = Field(default_factory=list)
    is_active: bool = True
    failed_attempts: int = 0
    locked_until: Optional[datetime] = None


class AuthToken(BaseModel):
    token: str
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime = Field(default_factory=datetime.utcnow)
    scopes: list[str] = Field(default_factory=list)


class AuthorizationContext(BaseModel):
    user_id: str
    roles: list[str]
    departments: list[str] = Field(default_factory=list)
    resource_type: str
    action: str
    resource_department: str = ""


class AuthorizationResult(BaseModel):
    allowed: bool
    reason: str
    user_id: str
    resource_type: str
    action: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class PromptAnalysis(BaseModel):
    prompt: str
    is_injection: bool = False
    confidence: float = 0.0
    matched_patterns: list[str] = Field(default_factory=list)
    risk_level: RiskLevel = RiskLevel.LOW
    recommendation: str = ""
    sanitized_prompt: str = ""


class PIIDetection(BaseModel):
    text: str
    has_pii: bool = False
    pii_types: list[str] = Field(default_factory=list)
    detections: list[dict[str, Any]] = Field(default_factory=list)
    redacted_text: str = ""
    classification: ClassificationLevel = ClassificationLevel.INTERNAL


class DataClassification(BaseModel):
    content: str
    classification: ClassificationLevel
    confidence: float = 0.0
    indicators: list[str] = Field(default_factory=list)


class AgentTool(BaseModel):
    name: str
    allowed_actions: list[str] = Field(default_factory=list)
    data_scope: list[str] = Field(default_factory=list)
    requires_approval: bool = False
    description: str = ""


class AgentPolicy(BaseModel):
    agent_name: str
    tools: list[AgentTool] = Field(default_factory=list)
    max_steps: int = 10
    require_human_approval_above: RiskLevel = RiskLevel.HIGH


class AgentActionRequest(BaseModel):
    user_id: str = ""
    agent_name: str
    tool_name: str
    action: str
    data_scope: str = ""
    user_context: str = ""


class AgentActionDecision(BaseModel):
    request: AgentActionRequest
    decision: AuthAction
    reason: str
    requires_approval: bool = False
    policy_used: str = ""
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AuditEntry(BaseModel):
    id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: str
    action: str
    resource_type: str
    resource_id: str = ""
    result: str = ""
    details: dict[str, Any] = Field(default_factory=dict)
    risk_level: RiskLevel = RiskLevel.LOW
    ip_address: str = ""


class ThreatRecord(BaseModel):
    id: str
    name: str
    category: ThreatCategory
    description: str
    impact: RiskLevel
    likelihood: RiskLevel
    risk_score: RiskLevel = RiskLevel.LOW
    mitigation: str = ""
    detection: str = ""
    response: str = ""
    residual_risk: RiskLevel = RiskLevel.LOW


class AISystemRecord(BaseModel):
    id: str
    name: str
    owner: str
    purpose: str
    data_sources: list[str] = Field(default_factory=list)
    models: list[str] = Field(default_factory=list)
    risk_level: RiskLevel = RiskLevel.MEDIUM
    environment: str = "production"
    users_count: int = 0
    controls: list[str] = Field(default_factory=list)
    policies: list[str] = Field(default_factory=list)
    last_review: Optional[datetime] = None
    next_review: Optional[datetime] = None
    status: str = "active"


class ComplianceRequirement(BaseModel):
    id: str
    requirement: str
    category: str
    control: str = ""
    implementation: str = ""
    evidence: str = ""
    status: str = "pending"
    last_verified: Optional[datetime] = None


class SecurityEvent(BaseModel):
    id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    event_type: str
    severity: RiskLevel
    source: str
    user_id: str = ""
    details: dict[str, Any] = Field(default_factory=dict)
    blocked: bool = False
