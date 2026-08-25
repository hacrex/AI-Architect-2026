"""Agent Permissions — tool-level authorization and policy enforcement."""
from datetime import datetime
from app.models import AgentTool, AgentPolicy, AgentActionRequest, AgentActionDecision, AuthAction, RiskLevel
import config.settings as settings


class AgentPermissionEngine:
    """Enforce tool-level permissions for AI agents."""

    def __init__(self):
        self._policies: dict[str, AgentPolicy] = {}
        self._action_log: list[AgentActionDecision] = []
        self._seed_policies()

    def _seed_policies(self):
        self.create_policy(AgentPolicy(
            agent_name="knowledge_agent",
            tools=[
                AgentTool(name="vector_search", allowed_actions=["read"],
                          data_scope=["engineering", "hr", "finance", "public"],
                          requires_approval=False, description="Search knowledge base"),
                AgentTool(name="web_search", allowed_actions=["read"],
                          data_scope=["public"], requires_approval=False,
                          description="Search public web"),
            ],
            max_steps=5
        ))

        self.create_policy(AgentPolicy(
            agent_name="ticket_agent",
            tools=[
                AgentTool(name="ticket_api", allowed_actions=["read", "create"],
                          data_scope=["engineering"], requires_approval=False,
                          description="Manage support tickets"),
                AgentTool(name="ticket_api", allowed_actions=["close", "delete"],
                          data_scope=["all"], requires_approval=True,
                          description="Close or delete tickets"),
            ],
            max_steps=8,
            require_human_approval_above=RiskLevel.MEDIUM
        ))

        self.create_policy(AgentPolicy(
            agent_name="code_agent",
            tools=[
                AgentTool(name="code_repository", allowed_actions=["read"],
                          data_scope=["assigned_repos"], requires_approval=False,
                          description="Read code"),
                AgentTool(name="code_repository", allowed_actions=["write", "merge"],
                          data_scope=["assigned_repos"], requires_approval=True,
                          description="Write or merge code"),
            ],
            max_steps=10,
            require_human_approval_above=RiskLevel.HIGH
        ))

        self.create_policy(AgentPolicy(
            agent_name="admin_agent",
            tools=[
                AgentTool(name="user_management", allowed_actions=["read"],
                          data_scope=["all"], requires_approval=False,
                          description="Read user info"),
                AgentTool(name="user_management", allowed_actions=["write", "delete"],
                          data_scope=["all"], requires_approval=True,
                          description="Modify users"),
                AgentTool(name="deployment", allowed_actions=["read"],
                          data_scope=["all"], requires_approval=False,
                          description="Read deployments"),
                AgentTool(name="deployment", allowed_actions=["execute"],
                          data_scope=["all"], requires_approval=True,
                          description="Execute deployments"),
            ],
            max_steps=5,
            require_human_approval_above=RiskLevel.LOW
        ))

    def create_policy(self, policy: AgentPolicy):
        self._policies[policy.agent_name] = policy

    def evaluate_action(self, request: AgentActionRequest) -> AgentActionDecision:
        policy = self._policies.get(request.agent_name)
        if not policy:
            decision = AgentActionDecision(
                request=request,
                decision=AuthAction.DENY,
                reason=f"No policy found for agent '{request.agent_name}'",
                policy_used="default"
            )
            self._action_log.append(decision)
            return decision

        tool = None
        for t in policy.tools:
            if t.name == request.tool_name and request.action in t.allowed_actions:
                tool = t
                break

        if not tool:
            decision = AgentActionDecision(
                request=request,
                decision=AuthAction.DENY,
                reason=f"Tool '{request.tool_name}' not allowed for agent '{request.agent_name}'",
                policy_used=policy.agent_name
            )
            self._action_log.append(decision)
            return decision

        if tool.requires_approval:
            decision = AgentActionDecision(
                request=request,
                decision=AuthAction.REQUIRE_APPROVAL,
                reason=f"Tool '{request.tool_name}' action '{request.action}' requires human approval",
                requires_approval=True,
                policy_used=policy.agent_name
            )
            self._action_log.append(decision)
            return decision

        decision = AgentActionDecision(
            request=request,
            decision=AuthAction.ALLOW,
            reason=f"Action '{request.action}' allowed on tool '{request.tool_name}'",
            policy_used=policy.agent_name
        )
        self._action_log.append(decision)
        return decision

    def get_policy(self, agent_name: str) -> AgentPolicy:
        return self._policies.get(agent_name)

    def list_policies(self) -> list[dict]:
        return [
            {
                "agent": p.agent_name,
                "tools": len(p.tools),
                "max_steps": p.max_steps,
                "approval_above": p.require_human_approval_above.value
            }
            for p in self._policies.values()
        ]

    def get_action_log(self, limit: int = 50) -> list[dict]:
        return [
            {
                "agent": d.request.agent_name,
                "tool": d.request.tool_name,
                "action": d.request.action,
                "decision": d.decision.value,
                "reason": d.reason,
                "timestamp": d.timestamp.isoformat()
            }
            for d in self._action_log[-limit:]
        ]

    def get_stats(self) -> dict:
        total = len(self._action_log)
        allowed = sum(1 for d in self._action_log if d.decision == AuthAction.ALLOW)
        denied = sum(1 for d in self._action_log if d.decision == AuthAction.DENY)
        approval = sum(1 for d in self._action_log if d.decision == AuthAction.REQUIRE_APPROVAL)
        return {
            "total_evaluations": total,
            "allowed": allowed,
            "denied": denied,
            "require_approval": approval,
            "policies_count": len(self._policies)
        }
