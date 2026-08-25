"""Executive Brief — one-page architecture communication."""
from datetime import datetime
from typing import Optional
from app.models import ExecutiveBrief


class ExecutiveBriefManager:
    """Create and manage executive architecture briefs."""

    def __init__(self):
        self._briefs: dict[str, ExecutiveBrief] = {}
        self._seed_briefs()

    def _seed_briefs(self):
        self.create_brief(ExecutiveBrief(
            project_name="Enterprise AI Knowledge Platform",
            problem="10,000 employees spend 40% of time searching for information across 15+ disconnected systems, reducing productivity and slowing decision-making.",
            users="Engineering, HR, Finance, Legal — all employees who need internal knowledge",
            outcome="Search time reduced by 50%, knowledge accuracy improved, support resolution time cut from 20 to 10 minutes",
            requirements=[
                "Sub-2-second response time",
                "99.9% availability",
                "Enterprise IAM integration",
                "Department-level data isolation",
                "Real-time document ingestion",
                "Full audit trail",
            ],
            architecture_summary="RAG-based knowledge assistant with API Gateway, AI Gateway for model routing, hybrid search (semantic + keyword), multi-model inference with fallback, and comprehensive observability.",
            top_decisions=[
                "Hybrid model strategy (managed for dev, self-hosted for production)",
                "Qdrant vector database with department namespaces",
                "Centralized model gateway with semantic caching",
            ],
            risks=[
                "Model quality degradation → Continuous evaluation + fallback",
                "Data leakage → Authorization-aware retrieval + PII detection",
                "Cost overrun → FinOps tracking + budget alerts",
            ],
            governance=[
                "AI system inventory and risk assessment",
                "Prompt injection protection",
                "Agent tool authorization",
                "Audit logging for all operations",
                "Compliance tracking",
            ],
            cost_summary="$1.28M/year total ($180K model + $240K infrastructure + $500K engineering + $360K operations)",
            success_metrics=[
                "Resolution time: 20min → 10min",
                "Task success rate: 65% → 85%",
                "User adoption: 0% → 70%",
                "Cost per task: $8.50 → $2.00",
            ]
        ))

        self.create_brief(ExecutiveBrief(
            project_name="AI Inference Platform",
            problem="5 teams manage model deployments independently, duplicating effort, wasting GPU resources, and creating inconsistent reliability.",
            users="20+ applications across engineering, product, support, marketing, data science",
            outcome="Shared platform reducing inference cost by 40%, deployment time from 5 days to 4 hours, GPU utilization from 35% to 75%",
            requirements=[
                "Support 50+ models",
                "Handle 0-10,000 RPM variable traffic",
                "GPU time-sharing across teams",
                "Semantic caching for cost reduction",
                "Fallback to managed APIs",
            ],
            architecture_summary="Centralized AI Gateway with model routing, GPU cluster with Kubernetes orchestration, semantic cache, and fallback to managed providers.",
            top_decisions=[
                "Gateway pattern for unified entry point",
                "Semantic caching (30-40% cost reduction)",
                "Kubernetes GPU scheduling for flexibility",
            ],
            risks=[
                "GPU hardware failure → Multi-node redundancy + managed fallback",
                "Cost spike → Budget alerts + auto-scaling limits",
                "Team adoption → Self-service portal + documentation",
            ],
            governance=[
                "Team-level quotas and budgets",
                "GPU utilization monitoring",
                "Cost allocation per team",
                "Model quality tracking",
            ],
            cost_summary="$1.05M/year ($384K GPU + $400K engineering + $120K managed APIs + $144K operations)",
            success_metrics=[
                "Deployment time: 5 days → 4 hours",
                "GPU utilization: 35% → 75%",
                "Cost per inference: $0.15 → $0.05",
                "Model availability: 95% → 99.9%",
            ]
        ))

    def create_brief(self, brief: ExecutiveBrief) -> ExecutiveBrief:
        self._briefs[brief.project_name] = brief
        return brief

    def get_brief(self, project_name: str) -> Optional[ExecutiveBrief]:
        return self._briefs.get(project_name)

    def list_briefs(self) -> list[ExecutiveBrief]:
        return list(self._briefs.values())

    def get_summary(self) -> dict:
        briefs = list(self._briefs.values())
        return {
            "total_briefs": len(briefs),
            "briefs": [
                {"project": b.project_name, "requirements": len(b.requirements),
                 "decisions": len(b.top_decisions), "risks": len(b.risks)}
                for b in briefs
            ]
        }

    def format_brief(self, project_name: str) -> str:
        brief = self._briefs.get(project_name)
        if not brief:
            return f"Brief for {project_name} not found"
        lines = [
            f"# {brief.project_name} — Architecture Brief",
            "",
            "## Problem",
            brief.problem,
            "",
            "## Users",
            brief.users,
            "",
            "## Outcome",
            brief.outcome,
            "",
            "## Requirements",
            *[f"- {r}" for r in brief.requirements],
            "",
            "## Architecture",
            brief.architecture_summary,
            "",
            "## Key Decisions",
            *[f"{i+1}. {d}" for i, d in enumerate(brief.top_decisions)],
            "",
            "## Risks",
            *[f"- {r}" for r in brief.risks],
            "",
            "## Governance",
            *[f"- {g}" for g in brief.governance],
            "",
            "## Cost",
            brief.cost_summary,
            "",
            "## Success Metrics",
            *[f"- {m}" for m in brief.success_metrics],
        ]
        return "\n".join(lines)
