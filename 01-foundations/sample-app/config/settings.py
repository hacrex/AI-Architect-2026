from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # LLM Providers
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    default_model: str = "gpt-4"
    fallback_model: str = "gpt-3.5-turbo"

    # Vector Database
    chroma_persist_dir: str = "./data/chroma"

    # Application
    app_env: str = "development"
    log_level: str = "INFO"
    debug: bool = False

    # Rate Limiting
    rate_limit_requests_per_minute: int = 60

    # Cost Control
    max_tokens_per_request: int = 2000
    daily_token_budget: int = 1_000_000

    # Timeouts
    llm_timeout_seconds: int = 30
    retrieval_timeout_seconds: int = 5

    model_config = {"env_file": "config/.env", "env_file_encoding": "utf-8"}


settings = Settings()
