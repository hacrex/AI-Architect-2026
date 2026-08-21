from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from enum import Enum


class AgentType(str, Enum):
    SUPPORT = "support"
    BILLING = "billing"
    TECH = "tech"


class ToolCall(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]
    result: Optional[str] = None


class AgentResponse(BaseModel):
    agent: str
    content: str
    tool_calls: List[ToolCall] = []
    model_used: str
    tokens_used: int
    latency_ms: float


class QueryRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class QueryResponse(BaseModel):
    answer: str
    agent_used: str
    orchestration_plan: Optional[List[str]] = None
    tool_calls: List[ToolCall] = []
    tokens_used: int
    latency_ms: float


class AgentInfo(BaseModel):
    name: str
    description: str
    tools: List[str]
    model: str


class ToolInfo(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]
