"""Pydantic models for Data Pipeline API."""
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class Department(str, Enum):
    ENGINEERING = "engineering"
    HR = "hr"
    SECURITY = "security"
    FINANCE = "finance"
    LEGAL = "legal"


class Classification(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class ChunkingStrategy(str, Enum):
    FIXED = "fixed"
    SEMANTIC = "semantic"
    STRUCTURE = "structure"


class User(BaseModel):
    user_id: str
    name: str
    department: Department
    clearance: Classification = Classification.INTERNAL


class Document(BaseModel):
    document_id: str
    title: str
    content: str
    department: Department
    classification: Classification = Classification.INTERNAL
    owner: Optional[str] = None
    version: int = 1
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Chunk(BaseModel):
    chunk_id: str
    document_id: str
    text: str
    chunk_index: int
    token_count: int
    department: Department
    classification: Classification
    source: str
    version: int = 1
    created_at: datetime = Field(default_factory=datetime.now)


class IngestRequest(BaseModel):
    document_id: str
    title: str
    content: str
    department: Department
    classification: Classification = Classification.INTERNAL
    owner: Optional[str] = None


class IngestBatchRequest(BaseModel):
    documents: list[IngestRequest]


class QueryRequest(BaseModel):
    query: str
    user_id: str
    top_k: int = 10
    use_hybrid: bool = True
    use_reranking: bool = True


class QueryResult(BaseModel):
    chunk_id: str
    document_id: str
    text: str
    score: float
    department: str
    classification: str
    source: str
    rank: int


class QueryResponse(BaseModel):
    query: str
    results: list[QueryResult]
    total_results: int
    latency_ms: float


class ChunkingCompareRequest(BaseModel):
    document_id: str
    strategies: list[ChunkingStrategy] = [
        ChunkingStrategy.FIXED,
        ChunkingStrategy.SEMANTIC,
        ChunkingStrategy.STRUCTURE,
    ]


class ChunkingCompareResult(BaseModel):
    strategy: ChunkingStrategy
    chunk_count: int
    avg_chunk_size: float
    chunks: list[Chunk]


class ChunkingCompareResponse(BaseModel):
    document_id: str
    results: list[ChunkingCompareResult]


class StatsResponse(BaseModel):
    total_documents: int
    total_chunks: int
    chunks_by_department: dict[str, int]
    chunks_by_classification: dict[str, int]
    avg_chunk_size: float
    embedding_dimensions: int


class HealthResponse(BaseModel):
    status: str
    vectordb: str
    metadata_db: str
    embedding_model: str
