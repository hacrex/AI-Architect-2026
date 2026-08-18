from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from enum import Enum


class ComplexityLevel(str, Enum):
    SIMPLE = "simple"
    NORMAL = "normal"
    COMPLEX = "complex"


class QueryRequest(BaseModel):
    query: str = Field(..., description="The user query")
    model: Optional[str] = Field(None, description="Specific model to use")
    top_k: Optional[int] = Field(5, description="Number of context documents")


class AutoQueryRequest(BaseModel):
    query: str = Field(..., description="The user query (will be auto-routed)")
    force_model: Optional[str] = Field(None, description="Override routing decision")


class CompareRequest(BaseModel):
    query: str = Field(..., description="The query to compare across models")
    models: List[str] = Field(
        default=["gpt-3.5-turbo", "gpt-4"],
        description="Models to compare",
    )
    metrics: List[str] = Field(
        default=["quality", "latency", "tokens"],
        description="Metrics to collect",
    )


class BenchmarkRequest(BaseModel):
    category: Optional[str] = Field("all", description="Prompt category")
    models: List[str] = Field(
        default=["gpt-3.5-turbo", "gpt-4"],
        description="Models to benchmark",
    )
    iterations: int = Field(3, description="Number of iterations per prompt")


class LLMResponse(BaseModel):
    content: str
    model_used: str
    tokens_used: int
    input_tokens: int
    output_tokens: int
    latency_ms: float
    finish_reason: str
    cost_estimate: float


class ComparisonResult(BaseModel):
    query: str
    results: List[LLMResponse]
    routing_decision: ComplexityLevel
    recommendation: str


class ModelInfo(BaseModel):
    id: str
    name: str
    provider: str
    context_window: int
    input_cost_per_1k: float
    output_cost_per_1k: float
    estimated_latency_ms: int
    tier: str


class QueryResponse(BaseModel):
    answer: str
    model_used: str
    routing_decision: ComplexityLevel
    tokens_used: int
    latency_ms: float
    cost_estimate: float


class BenchmarkResult(BaseModel):
    prompt: str
    category: str
    model: str
    response: str
    latency_ms: float
    input_tokens: int
    output_tokens: int
    cost_estimate: float


class BenchmarkSummary(BaseModel):
    model: str
    total_prompts: int
    avg_latency_ms: float
    total_input_tokens: int
    total_output_tokens: int
    total_cost: float


class MetricsResponse(BaseModel):
    total_requests: int
    total_tokens: int
    total_cost: float
    avg_latency_ms: float
    requests_by_model: Dict[str, int]
    cost_by_model: Dict[str, float]
