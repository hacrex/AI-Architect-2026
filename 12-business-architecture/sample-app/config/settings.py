"""Configuration for the AI Business Architecture app."""
import os
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Portfolio
PORTFOLIO_NAME = os.getenv("PORTFOLIO_NAME", "AI Architecture Portfolio")
PORTFOLIO_AUTHOR = os.getenv("PORTFOLIO_AUTHOR", "AI Architect")

# Cost Model
CURRENCY = os.getenv("CURRENCY", "USD")
DEFAULT_HOURLY_RATE = float(os.getenv("DEFAULT_HOURLY_RATE", "60"))
DEFAULT_WORKING_DAYS_PER_YEAR = int(os.getenv("DEFAULT_WORKING_DAYS_PER_YEAR", "220"))

# ROI
DEFAULT_DISCOUNT_RATE = float(os.getenv("DEFAULT_DISCOUNT_RATE", "0.1"))

# Business Metrics
DEFAULT_SATISFACTION_SCALE = int(os.getenv("DEFAULT_SATISFACTION_SCALE", "5"))
DEFAULT_TARGET_UPTIME = float(os.getenv("DEFAULT_TARGET_UPTIME", "99.9"))

# ADR
ADR_STATUS_OPTIONS = ["proposed", "accepted", "deprecated", "superseded"]

# Review
REVIEW_TIME_LIMIT_MINUTES = int(os.getenv("REVIEW_TIME_LIMIT_MINUTES", "45"))
