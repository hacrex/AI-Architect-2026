"""Pydantic models for Scale, Reliability & AI FinOps."""
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class ModelProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    AZURE = "azure"
    SELF_HOSTED = "self_hosted"


class FallbackAction(str, Enum):
    RETRY = "retry"
    FALLBACK_PROVIDER = "fallback_provider"
    FALLBACK_MODEL = "fallback_model"
    USE_CACHE = "use_cache"
    DEGRADE = "degrade"
    FAIL = "fail"


class CacheEntry(BaseModel):
    key: str
    query_hash: str
    response: str
    tokens_saved: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    ttl_seconds: int = 3600
    access_count: int = 0
    embedding: list[float] = Field(default_factory=list)


class ProviderConfig(BaseModel):
    name: ModelProvider
    model: str
    api_key: str = ""
    max_tokens: int = 4096
    timeout_seconds: float = 10.0
    cost_per_1m_input: float = 3.0
    cost_per_1m_output: float = 15.0
    priority: int = 0
    is_enabled: bool = True


class FallbackRoute(BaseModel):
    id: str
    name: str
    provider: ModelProvider
    model: str
    priority: int
    timeout_seconds: float = 5.0
    max_retries: int = 1
    is_enabled: bool = True


class CircuitBreakerState(BaseModel):
    name: str
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    success_count: int = 0
    last_failure_time: Optional[datetime] = None
    failure_threshold: int = 5
    recovery_timeout_seconds: int = 30
    half_open_max_calls: int = 3
    half_open_calls: int = 0


class RateLimitBucket(BaseModel):
    name: str
    capacity: int = 60
    refill_rate_per_sec: float = 1.0
    tokens: float = 60.0
    last_refill: datetime = Field(default_factory=datetime.utcnow)


class CostRecord(BaseModel):
    id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    provider: ModelProvider
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    embedding_tokens: int = 0
    vector_searches: int = 0
    gpu_seconds: float = 0.0
    total_cost_usd: float = 0.0
    request_id: str = ""
    cached: bool = False


class CostSummary(BaseModel):
    period: str
    total_cost_usd: float
    model_cost_usd: float
    gpu_cost_usd: float
    embedding_cost_usd: float
    retrieval_cost_usd: float
    total_requests: int
    cached_requests: int
    cache_savings_usd: float
    cost_per_request: float
    cost_per_user: float


class CapacityEstimate(BaseModel):
    layer: str
    current_capacity: float
    peak_capacity: float
    utilization_pct: float
    bottleneck: bool
    recommendation: str


class ScalePlan(BaseModel):
    id: str
    name: str
    baseline_requests_per_sec: float
    peak_requests_per_sec: float
    layers: list[CapacityEstimate]
    monthly_cost_estimate: float
    first_bottleneck: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CacheStats(BaseModel):
    total_entries: int
    hit_count: int
    miss_count: int
    hit_rate_pct: float
    tokens_saved: int
    estimated_savings_usd: float
    avg_age_seconds: float
    expired_entries: int
