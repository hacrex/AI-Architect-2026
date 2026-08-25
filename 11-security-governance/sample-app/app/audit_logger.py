"""Audit Logger — immutable audit trail for all AI operations."""
import uuid
from datetime import datetime, timedelta
from typing import Optional
from app.models import AuditEntry, RiskLevel
import config.settings as settings


class AuditLogger:
    """Record and query audit events for AI system operations."""

    def __init__(self, retention_days: int = None, redact_sensitive: bool = True):
        self.retention_days = retention_days or settings.AUDIT_RETENTION_DAYS
        self.redact_sensitive = redact_sensitive
        self._entries: list[AuditEntry] = []
        self._by_user: dict[str, list[AuditEntry]] = {}
        self._by_action: dict[str, list[AuditEntry]] = {}

    def log(self, user_id: str, action: str, resource_type: str,
            resource_id: str = "", result: str = "success",
            details: dict = None, risk_level: RiskLevel = RiskLevel.LOW,
            ip_address: str = "") -> AuditEntry:
        entry = AuditEntry(
            id=f"audit-{uuid.uuid4().hex[:12]}",
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            result=result,
            details=self._redact(details) if self.redact_sensitive else (details or {}),
            risk_level=risk_level,
            ip_address=ip_address
        )
        self._entries.append(entry)
        self._by_user.setdefault(user_id, []).append(entry)
        self._by_action.setdefault(action, []).append(entry)
        return entry

    def log_auth(self, user_id: str, authenticated: bool, ip_address: str = "") -> AuditEntry:
        return self.log(
            user_id=user_id,
            action="authentication",
            resource_type="auth",
            result="success" if authenticated else "failure",
            risk_level=RiskLevel.LOW if authenticated else RiskLevel.MEDIUM,
            ip_address=ip_address
        )

    def log_authorization(self, user_id: str, resource_type: str,
                          action: str, allowed: bool) -> AuditEntry:
        return self.log(
            user_id=user_id,
            action=f"authorization:{action}",
            resource_type=resource_type,
            result="allowed" if allowed else "denied",
            risk_level=RiskLevel.LOW if allowed else RiskLevel.HIGH
        )

    def log_prompt(self, user_id: str, is_injection: bool,
                   confidence: float) -> AuditEntry:
        return self.log(
            user_id=user_id,
            action="prompt_check",
            resource_type="prompt",
            result="blocked" if is_injection else "allowed",
            details={"confidence": confidence},
            risk_level=RiskLevel.CRITICAL if is_injection else RiskLevel.LOW
        )

    def log_data_access(self, user_id: str, resource_type: str,
                        resource_id: str, classification: str) -> AuditEntry:
        return self.log(
            user_id=user_id,
            action="data_access",
            resource_type=resource_type,
            resource_id=resource_id,
            details={"classification": classification},
            risk_level=RiskLevel.HIGH if classification in ("confidential", "restricted") else RiskLevel.LOW
        )

    def log_agent_action(self, user_id: str, agent: str, tool: str,
                         action: str, decision: str) -> AuditEntry:
        return self.log(
            user_id=user_id,
            action=f"agent:{action}",
            resource_type="agent",
            details={"agent": agent, "tool": tool, "decision": decision},
            risk_level=RiskLevel.HIGH if decision == "denied" else RiskLevel.LOW
        )

    def _redact(self, details: dict) -> dict:
        if not details:
            return {}
        redacted = {}
        sensitive_keys = {"prompt", "response", "document", "content", "text", "email", "phone"}
        for k, v in details.items():
            if any(sk in k.lower() for sk in sensitive_keys):
                redacted[k] = "[REDACTED]"
            else:
                redacted[k] = v
        return redacted

    def query(self, user_id: str = None, action: str = None,
              resource_type: str = None, risk_level: RiskLevel = None,
              since: datetime = None, limit: int = 100) -> list[AuditEntry]:
        entries = self._entries
        if user_id:
            entries = [e for e in entries if e.user_id == user_id]
        if action:
            entries = [e for e in entries if action in e.action]
        if resource_type:
            entries = [e for e in entries if e.resource_type == resource_type]
        if risk_level:
            entries = [e for e in entries if e.risk_level == risk_level]
        if since:
            entries = [e for e in entries if e.timestamp >= since]
        return entries[-limit:]

    def get_summary(self) -> dict:
        total = len(self._entries)
        by_result = {}
        by_risk = {}
        for e in self._entries:
            by_result[e.result] = by_result.get(e.result, 0) + 1
            by_risk[e.risk_level.value] = by_risk.get(e.risk_level.value, 0) + 1
        return {
            "total_entries": total,
            "by_result": by_result,
            "by_risk_level": by_risk,
            "unique_users": len(self._by_user),
            "retention_days": self.retention_days
        }

    def get_user_activity(self, user_id: str) -> dict:
        entries = self._by_user.get(user_id, [])
        actions = {}
        for e in entries:
            actions[e.action] = actions.get(e.action, 0) + 1
        return {
            "user_id": user_id,
            "total_events": len(entries),
            "actions": actions,
            "last_event": entries[-1].timestamp.isoformat() if entries else None
        }

    def list_entries(self, limit: int = 50) -> list[dict]:
        return [
            {
                "id": e.id,
                "timestamp": e.timestamp.isoformat(),
                "user_id": e.user_id,
                "action": e.action,
                "resource_type": e.resource_type,
                "result": e.result,
                "risk_level": e.risk_level.value
            }
            for e in self._entries[-limit:]
        ]
