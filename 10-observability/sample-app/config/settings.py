"""Configuration for the AI Observability app."""
import os
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Metrics
METRICS_RETENTION_SECONDS = int(os.getenv("METRICS_RETENTION_SECONDS", "86400"))
METRICS_FLUSH_INTERVAL = int(os.getenv("METRICS_FLUSH_INTERVAL", "10"))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = os.getenv("LOG_FORMAT", "json")
LOG_FILE = os.getenv("LOG_FILE", "")

# Tracing
TRACE_SAMPLE_RATE = float(os.getenv("TRACE_SAMPLE_RATE", "1.0"))
TRACE_MAX_SPANS = int(os.getenv("TRACE_MAX_SPANS", "100"))

# LLM Observability
LLM_TRACE_TOKEN_DETAILS = os.getenv("LLM_TRACE_TOKEN_DETAILS", "true").lower() == "true"
LLM_COST_PER_1M_INPUT = float(os.getenv("LLM_COST_PER_1M_INPUT", "3.0"))
LLM_COST_PER_1M_OUTPUT = float(os.getenv("LLM_COST_PER_1M_OUTPUT", "15.0"))

# RAG Monitoring
RAG_RELEVANCE_THRESHOLD = float(os.getenv("RAG_RELEVANCE_THRESHOLD", "0.7"))
RAG_MIN_DOCUMENTS = int(os.getenv("RAG_MIN_DOCUMENTS", "3"))
RAG_MAX_LATENCY_MS = float(os.getenv("RAG_MAX_LATENCY_MS", "500.0"))

# Agent Tracing
AGENT_MAX_STEPS = int(os.getenv("AGENT_MAX_STEPS", "10"))
AGENT_LOOP_THRESHOLD = int(os.getenv("AGENT_LOOP_THRESHOLD", "3"))
AGENT_TIMEOUT_SECONDS = float(os.getenv("AGENT_TIMEOUT_SECONDS", "30.0"))

# SLO
SLO_AVAILABILITY_TARGET = float(os.getenv("SLO_AVAILABILITY_TARGET", "99.9"))
SLO_LATENCY_P95_TARGET_MS = float(os.getenv("SLO_LATENCY_P95_TARGET_MS", "5000"))
SLO_TASK_SUCCESS_TARGET = float(os.getenv("SLO_TASK_SUCCESS_TARGET", "90.0"))
SLO_GROUNDEDNESS_TARGET = float(os.getenv("SLO_GROUNDEDNESS_TARGET", "95.0"))
SLO_ERROR_BUDGET_PCT = float(os.getenv("SLO_ERROR_BUDGET_PCT", "0.1"))

# Alerting
ALERT_LATENCY_THRESHOLD_MS = float(os.getenv("ALERT_LATENCY_THRESHOLD_MS", "5000"))
ALERT_ERROR_RATE_THRESHOLD = float(os.getenv("ALERT_ERROR_RATE_THRESHOLD", "1.0"))
ALERT_RETRIEVAL_RELEVANCE_THRESHOLD = float(os.getenv("ALERT_RETRIEVAL_RELEVANCE_THRESHOLD", "70.0"))
ALERT_COST_DAILY_LIMIT = float(os.getenv("ALERT_COST_DAILY_LIMIT", "500.0"))
ALERT_QUALITY_DEGRADATION_PCT = float(os.getenv("ALERT_QUALITY_DEGRADATION_PCT", "10.0"))

# Drift Detection
DRIFT_WINDOW_SIZE = int(os.getenv("DRIFT_WINDOW_SIZE", "1000"))
DRIFT_BASELINE_SIZE = int(os.getenv("DRIFT_BASELINE_SIZE", "5000"))
DRIFT_SIMILARITY_THRESHOLD = float(os.getenv("DRIFT_SIMILARITY_THRESHOLD", "0.85"))
DRIFT_CHECK_INTERVAL = int(os.getenv("DRIFT_CHECK_INTERVAL", "100"))
