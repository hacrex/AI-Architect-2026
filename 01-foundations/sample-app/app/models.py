from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    model: Optional[str] = None
    stream: Optional[bool] = False


class RetrievalResult(BaseModel):
    content: str
    source: str
    score: float
    metadata: dict = {}


class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    model: str
    tokens_used: int
    latency_ms: float


class LLMResponse(BaseModel):
    content: str
    model_used: str
    tokens_used: int
    finish_reason: str


class User(BaseModel):
    id: str
    name: str
    email: str
    roles: List[str]
    document_permissions: List[str]
    is_admin: bool = False


class HealthResponse(BaseModel):
    status: str
    version: str
    components: dict
    timestamp: datetime = datetime.now()


class Document(BaseModel):
    id: str
    content: str
    metadata: dict
    embedding: Optional[List[float]] = None
    created_at: datetime = datetime.now()
