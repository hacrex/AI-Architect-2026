"""Portfolio Manager — manage AI architecture portfolio projects."""
from datetime import datetime
from typing import Optional
from app.models import Project, UseCase, UseCaseStatus, Priority


class PortfolioManager:
    """Manage AI architecture portfolio projects and use cases."""

    def __init__(self):
        self._projects: dict[str, Project] = {}
        self._use_cases: dict[str, UseCase] = {}
        self._seed_projects()
        self._seed_use_cases()

    def _seed_projects(self):
        self.create_project(Project(
            id="proj-001",
            name="Enterprise AI Knowledge Platform",
            description="RAG-based knowledge assistant for 10,000 employees",
            business_context="10,000 employees spending 40% of time searching for information across 15+ systems",
            requirements=["Enterprise IAM", "Sub-2s response", "99.9% uptime", "Real-time ingestion", "Department isolation"],
            architecture_components=["API Gateway", "AI Gateway", "RAG Pipeline", "Model Gateway", "Vector Store", "Observability", "Security"],
            key_decisions=["Multi-model routing", "Hybrid search", "Async ingestion", "Department-level authorization"],
            demonstrates=["RAG architecture", "Enterprise IAM", "Multi-model strategy", "Observability", "FinOps"]
        ))

        self.create_project(Project(
            id="proj-002",
            name="AI Inference Platform",
            description="Shared GPU platform serving 50+ models across 5 teams",
            business_context="Each team manages model deployments independently, duplicating effort and cost",
            requirements=["Multiple models", "Multiple teams", "Variable traffic", "GPU infrastructure", "Cost control"],
            architecture_components=["AI Gateway", "Model Router", "GPU Cluster", "Model Cache", "Fallback Router", "Monitoring"],
            key_decisions=["Gateway pattern", "Semantic caching", "GPU time-sharing", "Fallback strategy"],
            demonstrates=["Platform architecture", "GPU management", "Cost optimization", "Multi-tenant serving"]
        ))

        self.create_project(Project(
            id="proj-003",
            name="Agent Platform",
            description="Enterprise agent platform with policy-based authorization",
            business_context="Ad-hoc agent implementations with no governance, security, or cost controls",
            requirements=["Tool authorization", "Audit logging", "Cost budgets", "Human approval", "Loop prevention"],
            architecture_components=["Agent Runtime", "Policy Engine", "Tool Registry", "Audit Logger", "Circuit Breaker"],
            key_decisions=["Policy-based authorization", "Mandatory audit logging", "Cost budgets per agent", "Human approval workflow"],
            demonstrates=["Modern AI architecture", "Policy-driven security", "Audit and governance", "Cost controls"]
        ))

        self.create_project(Project(
            id="proj-004",
            name="AI Platform Cost Architecture",
            description="FinOps model for transparent AI spending",
            business_context="No visibility into AI spending, unpredictable costs, no optimization levers",
            requirements=["Cost tracking", "Budget alerts", "Optimization recommendations", "Break-even analysis"],
            architecture_components=["Cost Tracker", "Token Counter", "GPU Monitor", "Budget Manager", "Optimization Engine"],
            key_decisions=["Cost per task metric", "Semantic caching for savings", "Hybrid break-even model"],
            demonstrates=["Economic analysis", "Cost optimization", "FinOps implementation"]
        ))

        self.create_project(Project(
            id="proj-005",
            name="AI Security Architecture",
            description="Comprehensive security posture for AI systems",
            business_context="AI introduces new attack surfaces without existing security controls",
            requirements=["Prompt injection protection", "PII detection", "Agent authorization", "Audit trail", "Compliance"],
            architecture_components=["Prompt Guard", "Data Classifier", "Agent Permissions", "Audit Logger", "Compliance Tracker"],
            key_decisions=["Defense in depth", "Policy-based authorization", "Mandatory audit logging", "Compliance tracking"],
            demonstrates=["Threat modeling", "Security controls", "Compliance tracking", "Audit implementation"]
        ))

    def _seed_use_cases(self):
        self.create_use_case(UseCase(
            id="uc-001", name="Internal Knowledge Assistant",
            description="RAG-based Q&A for enterprise documentation",
            business_value=5, feasibility=5, data_readiness=4, risk=3, cost=3, time_to_value=4,
            status=UseCaseStatus.PRIORITIZED, owner="Platform Engineering"
        ))
        self.create_use_case(UseCase(
            id="uc-002", name="Customer Support Bot",
            description="Automated customer support with human escalation",
            business_value=5, feasibility=4, data_readiness=4, risk=3, cost=3, time_to_value=4,
            status=UseCaseStatus.PRIORITIZED, owner="Customer Success"
        ))
        self.create_use_case(UseCase(
            id="uc-003", name="Code Review Assistant",
            description="Automated code review suggestions",
            business_value=3, feasibility=5, data_readiness=5, risk=2, cost=2, time_to_value=5,
            status=UseCaseStatus.IN_PROGRESS, owner="Engineering"
        ))
        self.create_use_case(UseCase(
            id="uc-004", name="Marketing Copy Assistant",
            description="AI-assisted marketing content generation",
            business_value=3, feasibility=4, data_readiness=3, risk=2, cost=2, time_to_value=4,
            status=UseCaseStatus.IDENTIFIED, owner="Marketing"
        ))
        self.create_use_case(UseCase(
            id="uc-005", name="Autonomous Production Deployment",
            description="AI-driven production deployment decisions",
            business_value=5, feasibility=2, data_readiness=3, risk=5, cost=4, time_to_value=2,
            status=UseCaseStatus.REJECTED, owner="Platform Engineering"
        ))

    def create_project(self, project: Project) -> Project:
        self._projects[project.id] = project
        return project

    def get_project(self, project_id: str) -> Optional[Project]:
        return self._projects.get(project_id)

    def list_projects(self) -> list[Project]:
        return list(self._projects.values())

    def create_use_case(self, use_case: UseCase) -> UseCase:
        self._use_cases[use_case.id] = use_case
        return use_case

    def get_use_case(self, uc_id: str) -> Optional[UseCase]:
        return self._use_cases.get(uc_id)

    def list_use_cases(self) -> list[UseCase]:
        return list(self._use_cases.values())

    def prioritize_use_cases(self) -> list[UseCase]:
        ucs = list(self._use_cases.values())
        return sorted(ucs, key=lambda u: u.weighted_score(), reverse=True)

    def get_summary(self) -> dict:
        projects = list(self._projects.values())
        ucs = list(self._use_cases.values())
        by_status = {}
        for uc in ucs:
            by_status[uc.status.value] = by_status.get(uc.status.value, 0) + 1
        return {
            "total_projects": len(projects),
            "total_use_cases": len(ucs),
            "use_cases_by_status": by_status,
            "projects": [
                {"id": p.id, "name": p.name, "demonstrates": len(p.demonstrates)}
                for p in projects
            ]
        }
