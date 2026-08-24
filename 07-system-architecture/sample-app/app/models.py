"""Pydantic models for the AI System Architecture."""
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class ModelProvider(str, Enum):
    OPENAI = "openai"
    AZURE_OPENAI = "azure_openai"
    ANTHROPIC = "anthropic"
    SELF_HOSTED = "self_hosted"


class RequestStatus(str, Enum):
    RECEIVED = "received"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    DEGRADED = "degraded"


class AgentAction(str, Enum):
    SEARCH = "search"
    DATABASE = "database"
    API_CALL = "api_call"
    EMAIL = "email"
    CREATE_TICKET = "create_ticket"


class RetrievalResult(BaseModel):
    chunk_id: str
    content: str
    score: float
    source: str
    metadata: dict = Field(default_factory=dict)


class ModelRoute(BaseModel):
    provider: ModelProvider
    model_name: str
    endpoint: str
    priority: int
    max_tokens: int = 4096
    cost_per_1k_input: float = 0.0
    cost_per_1k_output: float = 0.0


class AIRequest(BaseModel):
    query: str
    user_id: str
    session_id: Optional[str] = None
    use_agent: bool = False
    max_context_tokens: int = 4096
    temperature: float = 0.2


class AIResponse(BaseModel):
    request_id: str
    answer: str
    sources: list[dict] = Field(default_factory=list)
    model_used: str
    provider: str
    tokens_used: int = 0
    latency_ms: float = 0.0
    cost_usd: float = 0.0
    status: RequestStatus = RequestStatus.COMPLETED
    metadata: dict = Field(default_factory=dict)


class AgentPlan(BaseModel):
    steps: list[dict] = Field(default_factory=list)
    tools_needed: list[str] = Field(default_factory=list)
    estimated_tokens: int = 0


class AgentExecution(BaseModel):
    plan: AgentPlan
    results: list[dict] = Field(default_factory=list)
    final_answer: str = ""
    total_tokens: int = 0
    total_tool_calls: int = 0


class SecurityContext(BaseModel):
    user_id: str
    roles: list[str] = Field(default_factory=list)
    document_permissions: list[str] = Field(default_factory=list)
    allowed_models: list[str] = Field(default_factory=list)
    rate_limit: int = 100
    token_budget: int = 10000


class TraceSpan(BaseModel):
    span_id: str
    parent_id: Optional[str] = None
    name: str
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    duration_ms: float = 0.0
    status: str = "ok"
    attributes: dict = Field(default_factory=dict)


class RequestTrace(BaseModel):
    request_id: str
    user_id: str
    spans: list[TraceSpan] = Field(default_factory=list)
    total_latency_ms: float = 0.0
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    model_used: str = ""
    status: RequestStatus = RequestStatus.COMPLETED
    created_at: datetime = Field(default_factory=datetime.utcnow)


class FailureScenario(BaseModel):
    component: str
    failure_mode: str
    impact: str
    mitigation: str
    recovery: str


class ADR(BaseModel):
    id: str
    title: str
    context: str
    options: list[str]
    decision: str
    consequences: dict = Field(default_factory=dict)
    status: str = "accepted"
    created_at: datetime = Field(default_factory=datetime.utcnow)
