"""Security — authentication, authorization, and policy enforcement."""
import uuid
import hashlib
from datetime import datetime
from typing import Optional
from app.models import SecurityContext


class IdentityProvider:
    """Simulated identity provider."""

    def __init__(self):
        self._users: dict[str, dict] = {
            "user-001": {
                "user_id": "user-001",
                "email": "alice@company.com",
                "name": "Alice Johnson",
                "roles": ["employee", "engineering"],
                "department": "engineering",
                "active": True
            },
            "user-002": {
                "user_id": "user-002",
                "email": "bob@company.com",
                "name": "Bob Smith",
                "roles": ["employee", "hr"],
                "department": "hr",
                "active": True
            },
            "admin-001": {
                "user_id": "admin-001",
                "email": "admin@company.com",
                "name": "Admin User",
                "roles": ["employee", "admin", "security"],
                "department": "it",
                "active": True
            }
        }
        self._tokens: dict[str, str] = {}

    def authenticate(self, email: str, password: str) -> Optional[str]:
        for uid, user in self._users.items():
            if user["email"] == email and user["active"]:
                token = f"token-{uuid.uuid4().hex[:12]}"
                self._tokens[token] = uid
                return token
        return None

    def validate_token(self, token: str) -> Optional[dict]:
        user_id = self._tokens.get(token)
        if user_id:
            return self._users.get(user_id)
        return None

    def get_user(self, user_id: str) -> Optional[dict]:
        return self._users.get(user_id)


class AuthorizationEngine:
    """Role-based access control for AI resources."""

    def __init__(self):
        self._permissions: dict[str, list[str]] = {
            "employee": ["read_public_docs", "ask_questions"],
            "engineering": ["read_engineering_docs", "read_public_docs", "ask_questions"],
            "hr": ["read_hr_docs", "read_public_docs", "ask_questions"],
            "admin": ["read_all_docs", "manage_users", "manage_models", "view_audit_log"],
            "security": ["read_security_docs", "read_all_docs", "view_audit_log"]
        }
        self._document_permissions: dict[str, list[str]] = {
            "hr/policy-remote-work.md": ["all"],
            "hr/policy-pto.md": ["all"],
            "hr/benefits-overview.md": ["all"],
            "security/data-classification.md": ["admin", "security"],
            "engineering/architecture-guide.md": ["engineering"],
            "engineering/api-standards.md": ["engineering"],
            "finance/expense-policy.md": ["all"],
            "legal/data-privacy.md": ["legal", "admin"]
        }

    def check_permission(self, user_roles: list[str], permission: str) -> bool:
        for role in user_roles:
            if permission in self._permissions.get(role, []):
                return True
        return False

    def get_document_access(self, user_roles: list[str]) -> list[str]:
        accessible = []
        for doc, allowed_roles in self._document_permissions.items():
            if "all" in allowed_roles or any(r in allowed_roles for r in user_roles):
                accessible.append(doc)
        return accessible

    def get_security_context(self, user_id: str, roles: list[str]) -> SecurityContext:
        accessible_docs = self.get_document_access(roles)

        rate_limit = 100
        token_budget = 10000
        if "admin" in roles:
            rate_limit = 500
            token_budget = 50000
        elif "engineering" in roles:
            rate_limit = 200
            token_budget = 20000

        return SecurityContext(
            user_id=user_id,
            roles=roles,
            document_permissions=accessible_docs,
            allowed_models=["gpt-4", "gpt-3.5-turbo", "claude-3"],
            rate_limit=rate_limit,
            token_budget=token_budget
        )


class AuditLogger:
    """Audit log for all AI operations."""

    def __init__(self):
        self._log: list[dict] = []

    def log(self, event_type: str, user_id: str, details: dict = None):
        self._log.append({
            "event_id": f"audit-{uuid.uuid4().hex[:8]}",
            "event_type": event_type,
            "user_id": user_id,
            "details": details or {},
            "timestamp": datetime.utcnow().isoformat()
        })

    def get_events(self, user_id: str = None, event_type: str = None,
                   limit: int = 100) -> list[dict]:
        events = self._log
        if user_id:
            events = [e for e in events if e["user_id"] == user_id]
        if event_type:
            events = [e for e in events if e["event_type"] == event_type]
        return events[-limit:]

    def get_summary(self) -> dict:
        by_type = {}
        for e in self._log:
            t = e["event_type"]
            by_type[t] = by_type.get(t, 0) + 1
        return {"total_events": len(self._log), "by_type": by_type}


class SecurityService:
    """Complete security subsystem."""

    def __init__(self):
        self.identity_provider = IdentityProvider()
        self.authorization = AuthorizationEngine()
        self.audit_logger = AuditLogger()

    def authenticate(self, email: str, password: str) -> dict:
        token = self.identity_provider.authenticate(email, password)
        if token:
            self.audit_logger.log("authentication", email, {"status": "success"})
            return {"authenticated": True, "token": token}
        self.audit_logger.log("authentication", email, {"status": "failed"})
        return {"authenticated": False, "reason": "invalid_credentials"}

    def authorize_request(self, token: str, action: str = "ask_questions") -> dict:
        user = self.identity_provider.validate_token(token)
        if not user:
            return {"authorized": False, "reason": "invalid_token"}

        has_permission = self.authorization.check_permission(user["roles"], action)
        self.audit_logger.log("authorization", user["user_id"], {
            "action": action,
            "granted": has_permission
        })

        return {
            "authorized": has_permission,
            "user_id": user["user_id"],
            "roles": user["roles"]
        }

    def get_security_context(self, user_id: str) -> SecurityContext:
        user = self.identity_provider.get_user(user_id)
        if not user:
            return SecurityContext(user_id=user_id, roles=[])
        return self.authorization.get_security_context(user_id, user["roles"])
