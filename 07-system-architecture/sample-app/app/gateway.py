"""AI Gateway — central routing, rate limiting, and policy enforcement."""
import uuid
import time
from datetime import datetime
from typing import Optional
from app.models import AIRequest, AIResponse, SecurityContext, RequestStatus


class RateLimiter:
    """Simple in-memory rate limiter."""

    def __init__(self):
        self._requests: dict[str, list[float]] = {}

    def is_allowed(self, user_id: str, limit: int = 100, window_seconds: int = 60) -> bool:
        now = time.time()
        if user_id not in self._requests:
            self._requests[user_id] = []

        self._requests[user_id] = [
            t for t in self._requests[user_id] if now - t < window_seconds
        ]

        if len(self._requests[user_id]) >= limit:
            return False

        self._requests[user_id].append(now)
        return True

    def get_usage(self, user_id: str) -> int:
        now = time.time()
        if user_id not in self._requests:
            return 0
        return len([t for t in self._requests[user_id] if now - t < 60])


class PolicyEngine:
    """Enforce policies on AI requests."""

    def __init__(self):
        self._policies: dict[str, dict] = {
            "default": {
                "max_tokens": 4096,
                "allowed_models": ["gpt-4", "gpt-3.5-turbo", "claude-3"],
                "blocked_patterns": ["password", "secret", "api_key"],
                "require_sources": True,
            }
        }

    def check_request(self, request: AIRequest, security_ctx: SecurityContext) -> dict:
        policy = self._policies.get("default", {})
        violations = []

        if len(request.query) > 10000:
            violations.append("query_too_long")

        blocked = [p for p in policy.get("blocked_patterns", []) if p in request.query.lower()]
        if blocked:
            violations.append(f"blocked_pattern:{blocked[0]}")

        if request.max_context_tokens > policy.get("max_tokens", 4096):
            violations.append("context_tokens_exceeded")

        return {
            "allowed": len(violations) == 0,
            "violations": violations,
            "policy": "default"
        }


class AIGateway:
    """Central AI Gateway for authentication, rate limiting, and policy enforcement."""

    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.policy_engine = PolicyEngine()
        self._request_log: list[dict] = []

    def process_request(self, request: AIRequest, security_ctx: SecurityContext) -> dict:
        request_id = f"gw-{uuid.uuid4().hex[:8]}"

        if not self.rate_limiter.is_allowed(request.user_id, security_ctx.rate_limit):
            return {
                "request_id": request_id,
                "allowed": False,
                "reason": "rate_limit_exceeded",
                "usage": self.rate_limiter.get_usage(request.user_id),
                "limit": security_ctx.rate_limit
            }

        policy_check = self.policy_engine.check_request(request, security_ctx)
        if not policy_check["allowed"]:
            return {
                "request_id": request_id,
                "allowed": False,
                "reason": "policy_violation",
                "violations": policy_check["violations"]
            }

        self._request_log.append({
            "request_id": request_id,
            "user_id": request.user_id,
            "timestamp": datetime.utcnow().isoformat(),
            "query_length": len(request.query),
            "use_agent": request.use_agent
        })

        return {
            "request_id": request_id,
            "allowed": True,
            "rate_usage": self.rate_limiter.get_usage(request.user_id)
        }

    def get_request_log(self, limit: int = 50) -> list[dict]:
        return self._request_log[-limit:]

    def get_stats(self) -> dict:
        return {
            "total_requests": len(self._request_log),
            "unique_users": len(set(r["user_id"] for r in self._request_log)),
            "agent_requests": sum(1 for r in self._request_log if r.get("use_agent"))
        }
