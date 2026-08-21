from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Model Configuration
    model_name: str = "gpt2"  # Default to small model for demo
    model_device: str = "cpu"  # "cpu" or "cuda"
    max_tokens: int = 2048
    temperature: float = 0.7

    # Server Configuration
    workers: int = 1
    batch_size: int = 16
    max_concurrent_requests: int = 100
    request_timeout: int = 60

    # Batching Configuration
    batch_timeout_ms: int = 100  # Max wait time for batch formation
    dynamic_batching: bool = True

    # Monitoring
    enable_metrics: bool = True
    metrics_port: int = 9090

    # Fallback Configuration
    fallback_api_url: Optional[str] = None
    fallback_api_key: Optional[str] = None

    # GPU Configuration (for future use)
    gpu_memory_fraction: float = 0.8
    gpu_device_id: int = 0

    class Config:
        env_file = "config/.env"
        env_file_encoding = "utf-8"


settings = Settings()
