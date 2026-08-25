"""Configuration for the AI Security & Governance app."""
import os
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Authentication
AUTH_TOKEN_EXPIRY_SECONDS = int(os.getenv("AUTH_TOKEN_EXPIRY_SECONDS", "3600"))
AUTH_MAX_FAILED_ATTEMPTS = int(os.getenv("AUTH_MAX_FAILED_ATTEMPTS", "5"))
AUTH_LOCKOUT_SECONDS = int(os.getenv("AUTH_LOCKOUT_SECONDS", "900"))

# Authorization
AUTHZ_DEFAULT_DENY = os.getenv("AUTHZ_DEFAULT_DENY", "true").lower() == "true"

# Prompt Guard
PROMPT_INJECTION_THRESHOLD = float(os.getenv("PROMPT_INJECTION_THRESHOLD", "0.7"))
PROMPT_MAX_LENGTH = int(os.getenv("PROMPT_MAX_LENGTH", "10000"))
PROMPT_BLOCKED_PATTERNS = os.getenv(
    "PROMPT_BLOCKED_PATTERNS",
    "ignore previous,ignore all,disregard instructions,reveal confidential,show me all"
).split(",")

# Data Classification
CLASSIFICATION_LEVELS = os.getenv(
    "CLASSIFICATION_LEVELS",
    "public,internal,confidential,restricted"
).split(",")
DEFAULT_CLASSIFICATION = os.getenv("DEFAULT_CLASSIFICATION", "internal")

# PII Detection
PII_DETECT_EMAIL = os.getenv("PII_DETECT_EMAIL", "true").lower() == "true"
PII_DETECT_PHONE = os.getenv("PII_DETECT_PHONE", "true").lower() == "true"
PII_DETECT_SSN = os.getenv("PII_DETECT_SSN", "true").lower() == "true"
PII_DETECT_NAMES = os.getenv("PII_DETECT_NAMES", "true").lower() == "true"

# Agent Permissions
AGENT_REQUIRE_HUMAN_APPROVAL = os.getenv("AGENT_REQUIRE_HUMAN_APPROVAL", "true").lower() == "true"
AGENT_MAX_STEPS = int(os.getenv("AGENT_MAX_STEPS", "10"))

# Audit
AUDIT_RETENTION_DAYS = int(os.getenv("AUDIT_RETENTION_DAYS", "365"))
AUDIT_REDACT_SENSITIVE = os.getenv("AUDIT_REDACT_SENSITIVE", "true").lower() == "true"

# Risk Assessment
RISK_LEVELS = os.getenv("RISK_LEVELS", "low,medium,high,critical").split(",")
DEFAULT_RISK_LEVEL = os.getenv("DEFAULT_RISK_LEVEL", "medium")

# Compliance
COMPLIANCE_CHECK_INTERVAL_HOURS = int(os.getenv("COMPLIANCE_CHECK_INTERVAL_HOURS", "24"))
