import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)


class Settings:
    # API Keys
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")

    # Models
    default_model: str = os.getenv("DEFAULT_MODEL", "gpt-4")
    fallback_model: str = os.getenv("FALLBACK_MODEL", "gpt-3.5-turbo")

    # Tokens
    max_tokens_per_request: int = int(os.getenv("MAX_TOKENS", "1000"))

    # Cost estimation (per 1K tokens)
    gpt4_input_cost: float = float(os.getenv("GPT4_INPUT_COST", "0.03"))
    gpt4_output_cost: float = float(os.getenv("GPT4_OUTPUT_COST", "0.06"))
    gpt35_input_cost: float = float(os.getenv("GPT35_INPUT_COST", "0.001"))
    gpt35_output_cost: float = float(os.getenv("GPT35_OUTPUT_COST", "0.002"))

    # Routing thresholds (word count)
    simple_threshold: int = int(os.getenv("SIMPLEX_THRESHOLD", "50"))
    complex_threshold: int = int(os.getenv("COMPLEX_THRESHOLD", "200"))

    # Model characteristics
    model_info = {
        "gpt-3.5-turbo": {
            "name": "GPT-3.5 Turbo",
            "provider": "openai",
            "context_window": 16385,
            "input_cost": 0.001,
            "output_cost": 0.002,
            "latency_ms": 500,
            "tier": "simple",
        },
        "gpt-4": {
            "name": "GPT-4",
            "provider": "openai",
            "context_window": 128000,
            "input_cost": 0.03,
            "output_cost": 0.06,
            "latency_ms": 2000,
            "tier": "complex",
        },
        "gpt-4-turbo": {
            "name": "GPT-4 Turbo",
            "provider": "openai",
            "context_window": 128000,
            "input_cost": 0.01,
            "output_cost": 0.03,
            "latency_ms": 1500,
            "tier": "complex",
        },
        "claude-3-haiku": {
            "name": "Claude 3 Haiku",
            "provider": "anthropic",
            "context_window": 200000,
            "input_cost": 0.00025,
            "output_cost": 0.00125,
            "latency_ms": 400,
            "tier": "simple",
        },
        "claude-3-sonnet": {
            "name": "Claude 3 Sonnet",
            "provider": "anthropic",
            "context_window": 200000,
            "input_cost": 0.003,
            "output_cost": 0.015,
            "latency_ms": 1000,
            "tier": "normal",
        },
        "claude-3-opus": {
            "name": "Claude 3 Opus",
            "provider": "anthropic",
            "context_window": 200000,
            "input_cost": 0.015,
            "output_cost": 0.075,
            "latency_ms": 3000,
            "tier": "complex",
        },
    }


settings = Settings()
