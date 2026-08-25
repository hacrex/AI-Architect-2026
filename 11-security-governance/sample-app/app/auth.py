"""Authentication & Authorization — identity management and access control."""
import uuid
import hashlib
from datetime import datetime, timedelta
from typing import Optional
from app.models import User, AuthToken, AuthorizationContext, AuthorizationResult
import config.settings as settings


class Authenticator:
    """User authentication with brute-force protection."""

    def __init__(self):
        self._users: dict[str, User] = {}
        self._tokens: dict[str, AuthToken] = {}
        self._seed_users()

    def _seed_users(self):
        self.create_user("alice", "Alice Chen", "alice@company.com",
                         roles=["engineer"], departments=["engineering"])
        self.create_user("bob", "Bob Singh", "bob@company.com",
                         roles=["hr_manager"], departments=["hr"])
        self.create_user("carol", "Carol Davis", "carol@company.com",
                         roles=["finance_analyst"], departments=["finance"])
        self.create_user("dave", "Dave Wilson", "dave@company.com",
                         roles=["security_officer"], departments=["security", "engineering", "hr", "finance"])
        self.create_user("eve", "Eve Martinez", "eve@company.com",
                         roles=["contractor"], departments=[])

    def create_user(self, user_id: str, name: str, email: str,
                    roles: list[str] = None, departments: list[str] = None) -> User:
        user = User(
            id=user_id, name=name, email=email,
            roles=roles or [], departments=departments or []
        )
        self._users[user_id] = user
        return user

    def authenticate(self, user_id: str) -> dict:
        user = self._users.get(user_id)
        if not user:
            return {"authenticated": False, "reason": "User not found"}

        if not user.is_active:
            return {"authenticated": False, "reason": "Account disabled"}

        if user.locked_until and user.locked_until > datetime.utcnow():
            remaining = (user.locked_until - datetime.utcnow()).seconds
            return {"authenticated": False, "reason": f"Account locked for {remaining}s"}

        token = self._create_token(user)
        user.failed_attempts = 0
        return {
            "authenticated": True,
            "token": token.token,
            "user_id": user.id,
            "expires_at": token.expires_at.isoformat()
        }

    def validate_token(self, token: str) -> Optional[User]:
        auth_token = self._tokens.get(token)
        if not auth_token:
            return None
        if auth_token.expires_at < datetime.utcnow():
            del self._tokens[token]
            return None
        return self._users.get(auth_token.user_id)

    def _create_token(self, user: User) -> AuthToken:
        token_value = uuid.uuid4().hex
        token = AuthToken(
            token=token_value,
            user_id=user.id,
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(seconds=settings.AUTH_TOKEN_EXPIRY_SECONDS),
            scopes=user.roles
        )
        self._tokens[token_value] = token
        return token

    def get_user(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)

    def list_users(self) -> list[dict]:
        return [
            {"id": u.id, "name": u.name, "email": u.email,
             "roles": u.roles, "departments": u.departments,
             "is_active": u.is_active}
            for u in self._users.values()
        ]


class Authorizer:
    """RBAC + department-based authorization for RAG-aware access control."""

    def __init__(self, default_deny: bool = True):
        self.default_deny = default_deny
        self._policies: dict[str, dict] = {}
        self._seed_policies()

    def _seed_policies(self):
        self.add_policy("engineer", "document", ["read"], ["engineering", "public"])
        self.add_policy("hr_manager", "document", ["read", "write"], ["hr", "public"])
        self.add_policy("finance_analyst", "document", ["read", "write"], ["finance", "public"])
        self.add_policy("security_officer", "document", ["read", "write"],
                        ["security", "engineering", "hr", "finance", "public"])
        self.add_policy("contractor", "document", ["read"], ["public"])

        self.add_policy("engineer", "ticket", ["read", "create"], ["engineering"])
        self.add_policy("hr_manager", "ticket", ["read", "create"], ["hr"])
        self.add_policy("finance_analyst", "ticket", ["read"], ["finance"])
        self.add_policy("security_officer", "ticket", ["read", "create", "close"], ["all"])

    def add_policy(self, role: str, resource_type: str,
                   actions: list[str], departments: list[str]):
        key = f"{role}:{resource_type}"
        self._policies[key] = {
            "role": role,
            "resource_type": resource_type,
            "actions": actions,
            "departments": departments
        }

    def authorize(self, context: AuthorizationContext) -> AuthorizationResult:
        for role in context.roles:
            key = f"{role}:{context.resource_type}"
            policy = self._policies.get(key)
            if not policy:
                continue

            if context.action not in policy["actions"]:
                continue

            if "all" in policy["departments"]:
                return AuthorizationResult(
                    allowed=True, reason="Full access granted",
                    user_id=context.user_id,
                    resource_type=context.resource_type, action=context.action
                )

            if context.resource_department in policy["departments"]:
                return AuthorizationResult(
                    allowed=True, reason=f"Access granted via role '{role}'",
                    user_id=context.user_id,
                    resource_type=context.resource_type, action=context.action
                )

        if self.default_deny:
            return AuthorizationResult(
                allowed=False, reason="No matching policy",
                user_id=context.user_id,
                resource_type=context.resource_type, action=context.action
            )

        return AuthorizationResult(
            allowed=True, reason="Default allow",
            user_id=context.user_id,
            resource_type=context.resource_type, action=context.action
        )

    def get_allowed_departments(self, user_id: str, roles: list[str],
                                resource_type: str) -> list[str]:
        departments = set()
        for role in roles:
            key = f"{role}:{resource_type}"
            policy = self._policies.get(key)
            if policy:
                if "all" in policy["departments"]:
                    return ["all"]
                departments.update(policy["departments"])
        return list(departments)

    def list_policies(self) -> list[dict]:
        return list(self._policies.values())
