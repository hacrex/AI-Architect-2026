"""Pydantic models for AI Observability."""
from datetime import datetime
from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel, Field


class TraceStatus(str, Enum):
    OK = "ok"
    ERROR = "error"
    TIMEOUT = "timeout"
    DEGRADED = "degraded"


class AlertSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertState(str, Enum):
    FIRING = "firing"
    RESOLVED = "resolved"
    PENDING = "pending"


class SLOState(str, Enum):
    HEALTHY = "healthy"
    AT_RISK = "at_risk"
    BREACHED = "breached"


class DriftStatus(str, Enum):
    NORMAL = "normal"
    DRIFT_DETECTED = "drift_detected"
    BASELINE = "baseline"


class MetricPoint(BaseModel):
    name: str
    value: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    labels: dict[str, str] = Field(default_factory=dict)
    unit: str = ""


class MetricSeries(BaseModel):
    name: str
    points: list[MetricPoint] = Field(default_factory=list)
    labels: dict[str, str] = Field(default_factory=dict)


class LogEntry(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    level: str = "INFO"
    message: str
    component: str = ""
    trace_id: str = ""
    span_id: str = ""
    attributes: dict[str, Any] = Field(default_factory=dict)


class Span(BaseModel):
    trace_id: str
    span_id: str
    parent_span_id: str = ""
    name: str
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    duration_ms: float = 0.0
    status: TraceStatus = TraceStatus.OK
    attributes: dict[str, Any] = Field(default_factory=dict)
    events: list[dict[str, Any]] = Field(default_factory=list)


class Trace(BaseModel):
    trace_id: str
    spans: list[Span] = Field(default_factory=list)
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    total_duration_ms: float = 0.0
    status: TraceStatus = TraceStatus.OK
    root_operation: str = ""


class LLMCall(BaseModel):
    trace_id: str
    span_id: str
    provider: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    ttft_ms: float = 0.0
    latency_ms: float = 0.0
    cost_usd: float = 0.0
    prompt_preview: str = ""
    response_preview: str = ""
    temperature: float = 0.0
    max_tokens: int = 0
    finish_reason: str = ""
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class RAGEvent(BaseModel):
    trace_id: str
    span_id: str
    query: str
    query_embedding_ms: float = 0.0
    retrieval_ms: float = 0.0
    reranking_ms: float = 0.0
    documents_retrieved: int = 0
    documents_reranked: int = 0
    top_relevance_score: float = 0.0
    avg_relevance_score: float = 0.0
    context_tokens: int = 0
    authorized: bool = True
    filtered_count: int = 0
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AgentStep(BaseModel):
    step_number: int
    action: str
    tool_name: str = ""
    tool_input: str = ""
    tool_output: str = ""
    reasoning: str = ""
    duration_ms: float = 0.0
    status: TraceStatus = TraceStatus.OK
    tokens_used: int = 0


class AgentRun(BaseModel):
    trace_id: str
    agent_name: str
    steps: list[AgentStep] = Field(default_factory=list)
    total_steps: int = 0
    total_duration_ms: float = 0.0
    total_tokens: int = 0
    status: TraceStatus = TraceStatus.OK
    loop_detected: bool = False
    loop_count: int = 0
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class SLI(BaseModel):
    name: str
    description: str
    value: float
    unit: str = ""
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class SLO(BaseModel):
    id: str
    name: str
    description: str
    target: float
    current: float
    state: SLOState = SLOState.HEALTHY
    error_budget_remaining_pct: float = 100.0
    window_seconds: int = 86400
    last_updated: datetime = Field(default_factory=datetime.utcnow)


class Alert(BaseModel):
    id: str
    name: str
    severity: AlertSeverity
    state: AlertState = AlertState.FIRING
    condition: str
    message: str
    component: str = ""
    triggered_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None
    attributes: dict[str, Any] = Field(default_factory=dict)


class DriftSample(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metric_name: str
    value: float
    baseline_mean: float = 0.0
    baseline_std: float = 0.0
    z_score: float = 0.0
    is_drift: bool = False
