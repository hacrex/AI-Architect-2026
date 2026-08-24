"""Configuration for the AI System Architecture."""
import os
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


# Gateway
GATEWAY_RATE_LIMIT = int(os.getenv("GATEWAY_RATE_LIMIT", "100"))
GATEWAY_RATE_WINDOW = int(os.getenv("GATEWAY_RATE_WINDOW", "60"))

# RAG
RAG_TOP_K = int(os.getenv("RAG_TOP_K", "5"))
RAG_MAX_CONTEXT_TOKENS = int(os.getenv("RAG_MAX_CONTEXT_TOKENS", "4096"))

# Model Router
MODEL_ROUTER_TIMEOUT = int(os.getenv("MODEL_ROUTER_TIMEOUT", "30"))
MODEL_ROUTER_MAX_RETRIES = int(os.getenv("MODEL_ROUTER_MAX_RETRIES", "3"))
MODEL_CIRCUIT_BREAKER_THRESHOLD = int(os.getenv("MODEL_CIRCUIT_BREAKER_THRESHOLD", "3"))

# Agent
AGENT_MAX_STEPS = int(os.getenv("AGENT_MAX_STEPS", "5"))
AGENT_MAX_TOOL_CALLS = int(os.getenv("AGENT_MAX_TOOL_CALLS", "10"))

# Context
CONTEXT_MAX_TOKENS = int(os.getenv("CONTEXT_MAX_TOKENS", "4096"))

# Security
SECURITY_DEFAULT_BUDGET_USD = float(os.getenv("SECURITY_DEFAULT_BUDGET_USD", "10.0"))
SECURITY_ADMIN_BUDGET_USD = float(os.getenv("SECURITY_ADMIN_BUDGET_USD", "100.0"))

# Observability
OBSERVABILITY_RETENTION_HOURS = int(os.getenv("OBSERVABILITY_RETENTION_HOURS", "168"))

# Cost
COST_ALERT_THRESHOLD_USD = float(os.getenv("COST_ALERT_THRESHOLD_USD", "50.0"))
