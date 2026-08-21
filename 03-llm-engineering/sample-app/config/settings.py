from pydantic_settings import BaseSettings
from typing import Dict, Any
import os


class Settings(BaseSettings):
    # API Configuration
    openai_api_key: str = ""
    anthropic_api_key: str = ""

    # Model Configuration
    default_model: str = "gpt-4"
    fallback_model: str = "gpt-3.5-turbo"
    max_tokens_per_request: int = 2000
    temperature: float = 0.1

    # Agent Configuration
    agent_model_override: Dict[str, str] = {
        "support": "gpt-4",
        "billing": "gpt-4",
        "tech": "gpt-4",
    }

    # Context Configuration
    max_context_tokens: int = 128000
    context_budget: Dict[str, float] = {
        "system": 0.10,
        "persona": 0.10,
        "history": 0.25,
        "retrieval": 0.35,
        "tools": 0.10,
        "buffer": 0.10,
    }

    # Tool Configuration
    max_tool_retries: int = 2
    tool_timeout_seconds: int = 10

    # Orchestrator Configuration
    max_agents_per_query: int = 3
    enable_handoffs: bool = True

    class Config:
        env_file = "config/.env"
        env_file_encoding = "utf-8"


settings = Settings()
