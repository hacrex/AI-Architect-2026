"""ADR Manager — Architecture Decision Records."""
from datetime import datetime
from typing import Optional
from app.models import ADR, ADRStatus


class ADRManager:
    """Create and manage Architecture Decision Records."""

    def __init__(self):
        self._adrs: dict[str, ADR] = {}
        self._seed_adrs()

    def _seed_adrs(self):
        self.create_adr(ADR(
            id="ADR-001",
            title="Managed vs Self-Hosted Models",
            status=ADRStatus.ACCEPTED,
            context="Need to serve multiple AI models for internal applications with cost control and reliability.",
            options=[
                {"name": "Managed (OpenAI, Anthropic)", "pros": ["Simple", "Fast", "No ops"], "cons": ["Higher per-token cost", "Vendor lock-in"]},
                {"name": "Self-Hosted (Llama, Mistral)", "pros": ["Lower marginal cost", "Control", "Privacy"], "cons": ["High fixed cost", "GPU ops burden"]},
                {"name": "Hybrid", "pros": ["Flexibility", "Fallback", "Cost optimization"], "cons": ["Complexity", "Dual monitoring"]},
            ],
            decision="Hybrid approach — managed for development and fallback, self-hosted for production scale.",
            rationale="Development velocity requires managed models. Production economics require self-hosted. Hybrid provides both.",
            consequences=["More complex routing", "Need model gateway", "Dual monitoring"],
            revisit_conditions=["Self-hosted model quality matches managed", "Managed costs decrease significantly"]
        ))

        self.create_adr(ADR(
            id="ADR-002",
            title="Vector Database Strategy",
            status=ADRStatus.ACCEPTED,
            context="Need vector storage for RAG across multiple departments with data isolation.",
            options=[
                {"name": "Pinecone", "pros": ["Fully managed", "Simple"], "cons": ["Expensive at scale", "Vendor lock-in"]},
                {"name": "Qdrant", "pros": ["Open source", "Performant", "Namespace isolation"], "cons": ["Self-hosted ops"]},
                {"name": "Weaviate", "pros": ["Feature-rich", "GraphQL"], "cons": ["Learning curve"]},
                {"name": "pgvector", "pros": ["Existing PostgreSQL"], "cons": ["Performance limits"]},
            ],
            decision="Qdrant with department-level namespaces.",
            rationale="Open source, good performance, namespace isolation without separate clusters.",
            consequences=["Self-hosted operations", "Kubernetes deployment required"],
            revisit_conditions=["pgvector performance improves", "Need fully managed solution"]
        ))

        self.create_adr(ADR(
            id="ADR-003",
            title="Model Gateway",
            status=ADRStatus.ACCEPTED,
            context="Multiple applications need access to multiple models with routing, caching, and fallback.",
            options=[
                {"name": "Centralized Gateway", "pros": ["Single entry point", "Unified caching", "Centralized monitoring"], "cons": ["Single point of failure", "Additional infrastructure"]},
                {"name": "Direct API Calls", "pros": ["Simple", "No extra infrastructure"], "cons": ["No caching", "No fallback", "Duplicated logic"]},
                {"name": "Library-based", "pros": ["No infrastructure", "In-process"], "cons": ["No central monitoring", "Per-app configuration"]},
            ],
            decision="Centralized model gateway with semantic caching and fallback routing.",
            rationale="Single entry point for routing, caching, fallback, and monitoring provides operational benefits.",
            consequences=["Additional infrastructure", "Gateway must be highly available"],
            revisit_conditions=["Traffic volume too low to justify", "All apps use single provider"]
        ))

        self.create_adr(ADR(
            id="ADR-004",
            title="Kubernetes vs Managed Inference",
            status=ADRStatus.ACCEPTED,
            context="Need GPU infrastructure for self-hosted models with scheduling flexibility.",
            options=[
                {"name": "Kubernetes + GPU Node Pools", "pros": ["Existing expertise", "Flexible scheduling", "Cost control"], "cons": ["GPU operator complexity"]},
                {"name": "SageMaker / Vertex AI", "pros": ["Managed", "Auto-scaling"], "cons": ["Higher cost", "Less control"]},
                {"name": "Bare Metal", "pros": ["Maximum performance", "No orchestration overhead"], "cons": ["Manual scaling", "No resource sharing"]},
            ],
            decision="Kubernetes with GPU node pools and KubeFlow.",
            rationale="Existing Kubernetes expertise, flexible GPU scheduling, cost control at scale.",
            consequences=["Need GPU operator expertise", "Cluster autoscaler configuration"],
            revisit_conditions=["Team Kubernetes expertise lost", "Managed inference costs decrease"]
        ))

        self.create_adr(ADR(
            id="ADR-005",
            title="Multi-Provider Strategy",
            status=ADRStatus.ACCEPTED,
            context="Need to avoid vendor lock-in for model providers while maintaining simplicity.",
            options=[
                {"name": "Abstract Interface + Adapters", "pros": ["Provider flexibility", "Negotiation leverage", "Fallback"], "cons": ["Adapter maintenance"]},
                {"name": "Single Provider", "pros": ["Simple", "Optimized integration"], "cons": ["Vendor lock-in", "No fallback"]},
                {"name": "Provider-specific per App", "pros": ["No abstraction overhead"], "cons": ["Duplicated logic", "No fallback"]},
            ],
            decision="Abstract model interface with provider-specific adapters.",
            rationale="Flexibility to switch providers, negotiate pricing, maintain fallback capability.",
            consequences=["Adapter maintenance", "Interface standardization needed"],
            revisit_conditions=["Single provider dominates", "Abstraction overhead too high"]
        ))

        self.create_adr(ADR(
            id="ADR-006",
            title="Semantic Caching",
            status=ADRStatus.ACCEPTED,
            context="High volume of similar queries causing redundant inference and unnecessary cost.",
            options=[
                {"name": "Redis Semantic Cache", "pros": ["30-40% cost reduction", "Fast lookup", "Existing Redis"], "cons": ["Cache invalidation complexity", "Similarity threshold tuning"]},
                {"name": "Exact Match Cache", "pros": ["Simple", "No false positives"], "cons": ["Low hit rate for similar queries"]},
                {"name": "No Caching", "pros": ["Simple", "No stale data risk"], "cons": ["Full cost per query"]},
            ],
            decision="Redis-based semantic cache with embedding similarity matching.",
            rationale="30-40% cost reduction for common query patterns justifies complexity.",
            consequences=["Cache invalidation logic", "Similarity threshold configuration", "Stale response risk"],
            revisit_conditions=["Query patterns become too diverse", "Cache hit rate drops below 10%"]
        ))

        self.create_adr(ADR(
            id="ADR-007",
            title="Agent Tool Authorization",
            status=ADRStatus.ACCEPTED,
            context="Agents need access to external tools but must be controlled for security and cost.",
            options=[
                {"name": "Policy-based Authorization", "pros": ["Fine-grained control", "Audit trail", "Human approval"], "cons": ["Policy management overhead"]},
                {"name": "Allow-all with Logging", "pros": ["Simple", "Full agent capability"], "cons": ["No control", "Security risk"]},
                {"name": "Static Whitelist", "pros": ["Predictable", "Simple"], "cons": ["Inflexible", "No dynamic policies"]},
            ],
            decision="Policy-based authorization with tool-level permissions and human approval for high-risk actions.",
            rationale="Fine-grained control, audit trail, and human approval are essential for enterprise security.",
            consequences=["Policy engine deployment", "Policy authoring workflow", "Audit log storage"],
            revisit_conditions=["Agent simplicity required", "All tools are low-risk"]
        ))

    def create_adr(self, adr: ADR) -> ADR:
        self._adrs[adr.id] = adr
        return adr

    def get_adr(self, adr_id: str) -> Optional[ADR]:
        return self._adrs.get(adr_id)

    def list_adrs(self) -> list[ADR]:
        return list(self._adrs.values())

    def get_by_status(self, status: ADRStatus) -> list[ADR]:
        return [a for a in self._adrs.values() if a.status == status]

    def update_status(self, adr_id: str, status: ADRStatus) -> Optional[ADR]:
        adr = self._adrs.get(adr_id)
        if not adr:
            return None
        adr.status = status
        adr.updated_at = datetime.utcnow()
        return adr

    def get_summary(self) -> dict:
        adrs = list(self._adrs.values())
        by_status = {}
        for a in adrs:
            by_status[a.status.value] = by_status.get(a.status.value, 0) + 1
        return {
            "total_adrs": len(adrs),
            "by_status": by_status,
            "adr_list": [
                {"id": a.id, "title": a.title, "status": a.status.value}
                for a in adrs
            ]
        }

    def format_adr(self, adr_id: str) -> str:
        adr = self._adrs.get(adr_id)
        if not adr:
            return f"ADR {adr_id} not found"
        lines = [
            f"# {adr.id}: {adr.title}",
            "",
            f"**Status:** {adr.status.value}",
            "",
            "## Context",
            adr.context,
            "",
            "## Options",
        ]
        for i, opt in enumerate(adr.options, 1):
            lines.append(f"\n### Option {i}: {opt['name']}")
            lines.append(f"- Pros: {', '.join(opt.get('pros', []))}")
            lines.append(f"- Cons: {', '.join(opt.get('cons', []))}")
        lines.extend([
            "",
            "## Decision",
            adr.decision,
            "",
            "## Rationale",
            adr.rationale,
            "",
            "## Consequences",
            *[f"- {c}" for c in adr.consequences],
            "",
            "## Revisit Conditions",
            *[f"- {r}" for r in adr.revisit_conditions],
        ])
        return "\n".join(lines)
