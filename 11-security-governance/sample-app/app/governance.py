"""Governance — AI system inventory, lifecycle management, and ownership."""
from datetime import datetime, timedelta
from typing import Optional
from app.models import AISystemRecord, RiskLevel


class GovernanceManager:
    """Manage AI system inventory and governance records."""

    def __init__(self):
        self._systems: dict[str, AISystemRecord] = {}
        self._seed_systems()

    def _seed_systems(self):
        self.register_system(AISystemRecord(
            id="ai-001",
            name="Enterprise AI Knowledge Assistant",
            owner="Platform Engineering",
            purpose="Internal knowledge retrieval and Q&A",
            data_sources=["engineering_docs", "hr_docs", "finance_docs", "security_docs"],
            models=["gpt-4o", "claude-3-sonnet", "llama-3-8b"],
            risk_level=RiskLevel.MEDIUM,
            users_count=10000,
            controls=["IAM", "RAG filtering", "Audit logging", "Evaluation", "Human escalation"],
            policies=["Data Classification", "Access Control", "Acceptable Use", "AI Ethics"],
            last_review=datetime(2026, 7, 1),
            next_review=datetime(2026, 10, 1),
            status="active"
        ))

        self.register_system(AISystemRecord(
            id="ai-002",
            name="Customer Support Bot",
            owner="Customer Success",
            purpose="Customer-facing support automation",
            data_sources=["support_tickets", "product_docs", "faq"],
            models=["gpt-4o"],
            risk_level=RiskLevel.MEDIUM,
            users_count=50000,
            controls=["Content filtering", "Human escalation", "Audit logging"],
            policies=["Customer Data Protection", "Acceptable Use"],
            last_review=datetime(2026, 6, 15),
            next_review=datetime(2026, 9, 15),
            status="active"
        ))

        self.register_system(AISystemRecord(
            id="ai-003",
            name="Code Review Assistant",
            owner="Engineering",
            purpose="Automated code review suggestions",
            data_sources=["code_repositories"],
            models=["claude-3-sonnet"],
            risk_level=RiskLevel.LOW,
            users_count=200,
            controls=["Repository access control", "No write access", "Audit logging"],
            policies=["Code Quality", "Security Scanning"],
            last_review=datetime(2026, 7, 10),
            next_review=datetime(2026, 10, 10),
            status="active"
        ))

    def register_system(self, system: AISystemRecord) -> AISystemRecord:
        self._systems[system.id] = system
        return system

    def get_system(self, system_id: str) -> Optional[AISystemRecord]:
        return self._systems.get(system_id)

    def update_system(self, system_id: str, **kwargs) -> Optional[AISystemRecord]:
        system = self._systems.get(system_id)
        if not system:
            return None
        for key, value in kwargs.items():
            if hasattr(system, key):
                setattr(system, key, value)
        return system

    def list_systems(self) -> list[AISystemRecord]:
        return list(self._systems.values())

    def get_by_risk(self, risk_level: RiskLevel) -> list[AISystemRecord]:
        return [s for s in self._systems.values() if s.risk_level == risk_level]

    def get_reviews_due(self) -> list[AISystemRecord]:
        now = datetime.utcnow()
        return [
            s for s in self._systems.values()
            if s.next_review and s.next_review <= now
        ]

    def get_summary(self) -> dict:
        systems = list(self._systems.values())
        by_risk = {}
        by_status = {}
        for s in systems:
            by_risk[s.risk_level.value] = by_risk.get(s.risk_level.value, 0) + 1
            by_status[s.status] = by_status.get(s.status, 0) + 1
        return {
            "total_systems": len(systems),
            "by_risk_level": by_risk,
            "by_status": by_status,
            "reviews_due": len(self.get_reviews_due()),
            "total_users": sum(s.users_count for s in systems)
        }

    def format_record(self, system_id: str) -> str:
        system = self._systems.get(system_id)
        if not system:
            return f"System {system_id} not found"
        lines = [
            f"# AI System Record: {system.name}",
            "",
            f"**ID**: {system.id}",
            f"**Owner**: {system.owner}",
            f"**Purpose**: {system.purpose}",
            f"**Risk Level**: {system.risk_level.value}",
            f"**Environment**: {system.environment}",
            f"**Users**: {system.users_count:,}",
            f"**Status**: {system.status}",
            "",
            "## Data Sources",
            *[f"- {d}" for d in system.data_sources],
            "",
            "## Models",
            *[f"- {m}" for m in system.models],
            "",
            "## Controls",
            *[f"- {c}" for c in system.controls],
            "",
            "## Policies",
            *[f"- {p}" for p in system.policies],
            "",
            f"**Last Review**: {system.last_review.isoformat() if system.last_review else 'Never'}",
            f"**Next Review**: {system.next_review.isoformat() if system.next_review else 'Not scheduled'}",
        ]
        return "\n".join(lines)
