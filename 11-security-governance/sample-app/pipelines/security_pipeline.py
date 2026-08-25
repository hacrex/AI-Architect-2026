"""Security Pipeline — orchestrates all security controls."""
from app.models import (
    AuthorizationContext, AuthorizationResult, AgentActionRequest,
    AgentActionDecision, DataClassification, PromptAnalysis
)
from app.auth import Authenticator, Authorizer
from app.prompt_guard import PromptGuard
from app.data_classifier import DataClassifier
from app.agent_permissions import AgentPermissionEngine
from app.audit_logger import AuditLogger
from app.governance import GovernanceManager
from app.risk_engine import RiskEngine
from app.compliance import ComplianceManager


class SecurityPipeline:
    """Unified security orchestration for AI applications."""

    def __init__(self):
        self.authenticator = Authenticator()
        self.authorizer = Authorizer()
        self.prompt_guard = PromptGuard()
        self.data_classifier = DataClassifier()
        self.agent_permissions = AgentPermissionEngine()
        self.audit = AuditLogger()
        self.governance = GovernanceManager()
        self.risk_engine = RiskEngine()
        self.compliance = ComplianceManager()

    def process_request(self, user_id: str, prompt: str,
                        required_departments: list[str] = None) -> dict:
        result = {
            "user_id": user_id,
            "prompt": prompt[:200],
            "checks": [],
            "allowed": False
        }

        user = self.authenticator.get_user(user_id)
        if not user or not user.is_active:
            result["error"] = "User not found or inactive"
            self.audit.log(user_id=user_id, action="request_denied",
                          resource_type="request", result="user_invalid")
            return result

        prompt_analysis = self.prompt_guard.analyze(prompt)
        result["prompt_check"] = {
            "is_injection": prompt_analysis.is_injection,
            "confidence": prompt_analysis.confidence
        }
        result["checks"].append("prompt_guard")
        self.audit.log_prompt(user_id, prompt_analysis.is_injection,
                             prompt_analysis.confidence)

        if prompt_analysis.is_injection:
            result["error"] = "Prompt injection detected"
            return result

        auth_context = AuthorizationContext(
            user_id=user_id,
            roles=user.roles,
            resource_type="document",
            action="read",
            resource_department=required_departments[0] if required_departments else "public"
        )
        auth_result = self.authorizer.authorize(auth_context)
        result["authorization"] = {
            "allowed": auth_result.allowed,
            "reason": auth_result.reason
        }
        result["checks"].append("authorization")
        self.audit.log_authorization(user_id, "document", "read", auth_result.allowed)

        if not auth_result.allowed:
            result["error"] = f"Authorization denied: {auth_result.reason}"
            return result

        result["allowed"] = True
        return result

    def process_agent_action(self, user_id: str, agent_name: str,
                             tool_name: str, action: str,
                             resource_department: str = "public") -> dict:
        user = self.authenticator.get_user(user_id)
        if not user:
            return {"allowed": False, "error": "User not found"}

        request = AgentActionRequest(
            user_id=user_id, agent_name=agent_name,
            tool_name=tool_name, action=action
        )
        decision = self.agent_permissions.evaluate_action(request)

        self.audit.log_agent_action(user_id, agent_name, tool_name,
                                    action, decision.decision.value)

        return {
            "agent": agent_name,
            "tool": tool_name,
            "action": action,
            "decision": decision.decision.value,
            "reason": decision.reason,
            "requires_approval": decision.requires_approval
        }

    def get_system_status(self) -> dict:
        return {
            "auth": {"users": len(self.authenticator.list_users())},
            "governance": self.governance.get_summary(),
            "risk": self.risk_engine.get_summary(),
            "compliance": self.compliance.get_summary(),
            "audit": self.audit.get_summary(),
            "agent_permissions": self.agent_permissions.get_stats(),
            "prompt_guard": self.prompt_guard.get_stats(),
            "data_classifier": self.data_classifier.get_stats()
        }
