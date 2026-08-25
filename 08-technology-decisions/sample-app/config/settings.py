"""Configuration for the Technology Decisions app."""
import os
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


# Decision Engine
DECISION_DEFAULT_WEIGHT_SUM = float(os.getenv("DECISION_DEFAULT_WEIGHT_SUM", "1.0"))
DECISION_MIN_SCORE = float(os.getenv("DECISION_MIN_SCORE", "1.0"))
DECISION_MAX_SCORE = float(os.getenv("DECISION_MAX_SCORE", "10.0"))

# Build vs Buy
BUILDBUY_HOURLY_RATE = float(os.getenv("BUILDBUY_HOURLY_RATE", "150.0"))
BUILDBUY_DEFAULT_MIGRATION_COST = float(os.getenv("BUILDBUY_DEFAULT_MIGRATION_COST", "20000.0"))
BUILDBUY_ANNUAL_PRICE_INCREASE_PCT = float(os.getenv("BUILDBUY_ANNUAL_PRICE_INCREASE_PCT", "5.0"))

# Constraints
CONSTRAINT_HARD_WEIGHT = float(os.getenv("CONSTRAINT_HARD_WEIGHT", "1.0"))
CONSTRAINT_SOFT_WEIGHT = float(os.getenv("CONSTRAINT_SOFT_WEIGHT", "0.5"))

# Budget
MONTHLY_BUDGET_LIMIT_USD = float(os.getenv("MONTHLY_BUDGET_LIMIT_USD", "15000.0"))

# Latency
LATENCY_P95_TARGET_MS = float(os.getenv("LATENCY_P95_TARGET_MS", "200.0"))
