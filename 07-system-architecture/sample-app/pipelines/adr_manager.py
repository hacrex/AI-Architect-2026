"""Architecture Decision Records pipeline."""
import uuid
from datetime import datetime
from app.models import ADR


class ADRManager:
    """Manage Architecture Decision Records."""

    def __init__(self):
        self._adrs: dict[str, ADR] = {}
        self._seed_adrs()

    def _seed_adrs(self):
        self.create_adr(
            title="Model Strategy",
            context="We need multiple AI workloads with different quality and latency requirements.",
            options=[
                "Single model for all workloads",
                "Multiple models with routing",
                "Managed models only",
                "Self-hosted models only"
            ],
            decision="Use a model gateway with multiple providers.",
            consequences={
                "benefits": ["routing flexibility", "fallback capability", "reduced coupling"],
                "costs": ["additional platform complexity", "provider integration work"]
            }
        )

        self.create_adr(
            title="Data / Vector Strategy",
            context="We need to store and retrieve embeddings for RAG across multiple document types.",
            options=[
                "Single vector DB for all data",
                "Separate vector DBs per domain",
                "Vector DB + relational DB hybrid"
            ],
            decision="Use a managed vector DB with metadata filtering and a relational DB for structured data.",
            consequences={
                "benefits": ["managed service reduces ops burden", "metadata filtering enables permissions"],
                "costs": ["vendor lock-in risk", "cost grows with volume"]
            }
        )

        self.create_adr(
            title="Managed vs Self-Hosted",
            context="We need to balance cost, control, and operational complexity.",
            options=[
                "All managed services",
                "All self-hosted",
                "Hybrid approach"
            ],
            decision="Use managed services for non-differentiating capabilities, self-host for core AI inference.",
            consequences={
                "benefits": ["lower ops burden", "cost control for high volume", "flexibility"],
                "costs": ["mixed operational model", "integration complexity"]
            }
        )

    def create_adr(self, title: str, context: str, options: list[str],
                   decision: str, consequences: dict = None) -> ADR:
        adr_id = f"ADR-{len(self._adrs) + 1:03d}"
        adr = ADR(
            id=adr_id,
            title=title,
            context=context,
            options=options,
            decision=decision,
            consequences=consequences or {}
        )
        self._adrs[adr_id] = adr
        return adr

    def get_adr(self, adr_id: str) -> ADR:
        return self._adrs.get(adr_id)

    def list_adrs(self) -> list[ADR]:
        return list(self._adrs.values())

    def get_adr_summary(self) -> list[dict]:
        return [
            {"id": a.id, "title": a.title, "decision": a.decision, "status": a.status}
            for a in self._adrs.values()
        ]
