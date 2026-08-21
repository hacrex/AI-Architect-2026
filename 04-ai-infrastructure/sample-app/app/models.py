from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class InferenceRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 512
    temperature: Optional[float] = 0.7
    stream: Optional[bool] = False


class BatchInferenceRequest(BaseModel):
    prompts: List[str]
    max_tokens: Optional[int] = 512
    temperature: Optional[float] = 0.7


class InferenceResponse(BaseModel):
    generated_text: str
    tokens_generated: int
    latency_ms: float
    model_used: str
    batch_size: int = 1


class BatchInferenceResponse(BaseModel):
    results: List[InferenceResponse]
    total_latency_ms: float
    avg_latency_ms: float
    throughput_per_second: float


class HealthResponse(BaseModel):
    status: str
    version: str
    model_loaded: bool
    gpu_available: bool
    gpu_memory_used: Optional[float] = None
    gpu_memory_total: Optional[float] = None
    uptime_seconds: float


class ModelInfoResponse(BaseModel):
    model_name: str
    model_device: str
    max_tokens: int
    batch_size: int
    parameters: Optional[Dict[str, Any]] = None


class MetricsResponse(BaseModel):
    total_requests: int
    total_tokens: int
    avg_latency_ms: float
    avg_tokens_per_second: float
    p50_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    gpu_utilization: Optional[float] = None
