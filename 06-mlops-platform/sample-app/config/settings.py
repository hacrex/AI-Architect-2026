"""Configuration for the MLOps platform."""
import os
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


# Registry
REGISTRY_BACKEND = os.getenv("REGISTRY_BACKEND", "sqlite")
REGISTRY_DB_PATH = os.getenv("REGISTRY_DB_PATH", str(DATA_DIR / "registry.db"))

# Evaluation Gates
EVAL_QUALITY_THRESHOLD = float(os.getenv("EVAL_QUALITY_THRESHOLD", "0.85"))
EVAL_SAFETY_THRESHOLD = float(os.getenv("EVAL_SAFETY_THRESHOLD", "0.95"))
EVAL_COST_THRESHOLD = int(os.getenv("EVAL_COST_THRESHOLD", "1000"))
EVAL_LATENCY_THRESHOLD = int(os.getenv("EVAL_LATENCY_THRESHOLD", "2000"))

# Deployment
DEPLOY_STAGING_URL = os.getenv("DEPLOY_STAGING_URL", "http://localhost:8081")
DEPLOY_PRODUCTION_URL = os.getenv("DEPLOY_PRODUCTION_URL", "http://localhost:8082")
CANARY_INITIAL_PERCENTAGE = int(os.getenv("CANARY_INITIAL_PERCENTAGE", "5"))
CANARY_INCREMENT = int(os.getenv("CANARY_INCREMENT", "25"))
CANARY_OBSERVATION_PERIOD = int(os.getenv("CANARY_OBSERVATION_PERIOD", "60"))

# Monitoring
MONITOR_CHECK_INTERVAL = int(os.getenv("MONITOR_CHECK_INTERVAL", "60"))
DRIFT_THRESHOLD = float(os.getenv("DRIFT_THRESHOLD", "0.1"))
