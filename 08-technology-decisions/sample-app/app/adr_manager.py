"""ADR Manager — Architecture Decision Records with full template."""
import uuid
from datetime import datetime
from app.models import ADR, DecisionStatus


class ADRManager:
    """Manage Architecture Decision Records."""

    def __init__(self):
        self._adrs: dict[str, ADR] = {}
        self._seed_adrs()

    def _seed_adrs(self):
        self.create_adr(
            title="Model Hosting Strategy",
            context="The Enterprise AI Knowledge Assistant requires an inference strategy that balances cost, latency, privacy, and operational burden.\n\n"
                    "Requirements:\n"
                    "- 10,000 employees\n"
                    "- Sensitive enterprise documents\n"
                    "- Predictable production traffic\n"
                    "- High availability\n"
                    "- Multiple AI workloads\n\n"
                    "Hard Constraints:\n"
                    "- Sensitive data must remain within our environment\n"
                    "- Must support enterprise IAM\n"
                    "- Team has 0 GPU engineers",
            options=[
                "Option A: Managed proprietary models (OpenAI, Anthropic)",
                "Option B: Self-hosted open-weight models (Llama, Mistral)",
                "Option C: Hybrid — managed for general, self-hosted for sensitive"
            ],
            decision="Use a hybrid model architecture — managed for general workloads, self-hosted for sensitive data.",
            rationale="Hybrid allows routing sensitive workloads to self-hosted while leveraging managed for general tasks. "
                     "This provides provider flexibility, compliance for sensitive data, and fallback capability.",
            consequences={
                "benefits": [
                    "Provider flexibility and reduced single-provider dependency",
                    "Data-sensitive workloads remain controlled within our environment",
                    "Fallback options when providers experience outages",
                    "Workload-specific model selection based on requirements",
                    "Cost optimization across different volume tiers"
                ],
                "costs": [
                    "More platform complexity (model gateway, routing logic)",
                    "Multiple evaluation paths (must benchmark models across providers)",
                    "Additional operational overhead (managed + self-hosted)",
                    "Team needs to develop self-hosting expertise",
                    "Integration complexity with multiple APIs"
                ]
            },
            revisit_conditions=[
                "Traffic changes significantly — if self-hosted utilization is too low",
                "Pricing changes — if managed API costs drop 50%+",
                "Privacy requirements change — if regulations require all data on-premise",
                "Self-hosted utilization becomes uneconomical",
                "Model capabilities change substantially — if open-weight matches proprietary",
                "Team capability changes — if we hire GPU/ML engineers"
            ],
            metrics_to_track={
                "managed_api_cost_month": "< $2,000",
                "self_hosted_gpu_cost_month": "< $5,000",
                "sensitive_routing_pct": "100% self-hosted",
                "fallback_frequency": "Track"
            }
        )

        self.create_adr(
            title="Vector Storage Strategy",
            context="We need to store and retrieve embeddings for RAG across multiple document types.\n\n"
                    "Requirements:\n"
                    "- 10,000+ documents\n"
                    "- Metadata filtering for document-level permissions\n"
                    "- Scalability for growing document corpus\n"
                    "- Team familiarity with PostgreSQL",
            options=[
                "Option A: PostgreSQL + pgvector (extend existing database)",
                "Option B: Dedicated Vector DB (Pinecone, managed)",
                "Option C: Managed Vector Service (Weaviate Cloud)"
            ],
            decision="Use PostgreSQL + pgvector for vector storage.",
            rationale="PostgreSQL + pgvector leverages existing infrastructure and team knowledge. "
                     "It avoids vendor lock-in, keeps costs predictable, and provides sufficient capability "
                     "for our current scale. Can migrate to dedicated vector DB if scale requires.",
            consequences={
                "benefits": [
                    "Leverages existing PostgreSQL expertise",
                    "No additional vendor relationship",
                    "Cost-effective at current scale",
                    "Transactional consistency with relational data",
                    "pgvector extension actively maintained"
                ],
                "costs": [
                    "Limited advanced vector features compared to dedicated DBs",
                    "May need migration at very high scale",
                    "Performance tuning required for large datasets",
                    "No managed SLA for vector operations"
                ]
            },
            revisit_conditions=[
                "Document corpus exceeds 1M vectors with latency requirements",
                "Need for advanced vector features (hybrid search, generative search)",
                "pgvector performance becomes bottleneck",
                "Team expertise shifts away from PostgreSQL"
            ],
            metrics_to_track={
                "document_count": "Track",
                "query_latency_p95": "< 100ms",
                "index_size_gb": "Track"
            }
        )

        self.create_adr(
            title="Inference Platform Strategy",
            context="We need a model serving platform that supports multiple model types and deployment patterns.\n\n"
                    "Requirements:\n"
                    "- Support managed API and self-hosted models\n"
                    "- Kubernetes-based deployment\n"
                    "- Cost optimization at scale\n"
                    "- Team can operate with current expertise",
            options=[
                "Option A: Managed API only (OpenAI, Anthropic)",
                "Option B: vLLM on Kubernetes (self-hosted)",
                "Option C: KServe (Kubernetes-native model serving)",
                "Option D: Hybrid (Managed + vLLM)"
            ],
            decision="Use a hybrid inference platform — managed API for general workloads, vLLM for self-hosted sensitive workloads.",
            rationale="Hybrid balances managed simplicity for general workloads with self-hosted control for sensitive data. "
                     "vLLM provides efficient inference on our GPU infrastructure.",
            consequences={
                "benefits": [
                    "Best cost optimization across workload types",
                    "Compliance for sensitive data workloads",
                    "Fallback capability between managed and self-hosted",
                    "Flexibility to add new model providers"
                ],
                "costs": [
                    "Need to maintain both managed and self-hosted infrastructure",
                    "Different operational procedures for each platform",
                    "Team needs vLLM and Kubernetes expertise",
                    "Monitoring complexity across platforms"
                ]
            },
            revisit_conditions=[
                "Self-hosted utilization drops below 30%",
                "Managed API pricing drops significantly",
                "Team acquires dedicated ML infrastructure engineers",
                "New inference platform emerges with better cost/performance"
            ],
            metrics_to_track={
                "managed_requests_pct": "Track",
                "self_hosted_requests_pct": "Track",
                "avg_latency_ms": "< 200ms",
                "gpu_utilization": "Track"
            }
        )

    def create_adr(self, title: str, context: str, options: list[str],
                   decision: str, rationale: str = "",
                   consequences: dict = None,
                   revisit_conditions: list[str] = None,
                   metrics_to_track: dict[str, str] = None) -> ADR:
        adr_id = f"ADR-{len(self._adrs) + 1:03d}"
        adr = ADR(
            id=adr_id,
            title=title,
            context=context,
            options=options,
            decision=decision,
            rationale=rationale,
            consequences=consequences or {},
            revisit_conditions=revisit_conditions or [],
            status=DecisionStatus.ACCEPTED,
            metrics_to_track=metrics_to_track or {}
        )
        self._adrs[adr_id] = adr
        return adr

    def get_adr(self, adr_id: str) -> ADR:
        return self._adrs.get(adr_id)

    def list_adrs(self) -> list[ADR]:
        return list(self._adrs.values())

    def update_status(self, adr_id: str, status: DecisionStatus) -> ADR:
        adr = self._adrs.get(adr_id)
        if adr:
            adr.status = status
        return adr

    def get_adr_summary(self) -> list[dict]:
        return [
            {
                "id": a.id,
                "title": a.title,
                "decision": a.decision,
                "status": a.status.value,
                "options_count": len(a.options),
                "revisit_conditions_count": len(a.revisit_conditions)
            }
            for a in self._adrs.values()
        ]

    def format_adr_markdown(self, adr_id: str) -> str:
        adr = self._adrs.get(adr_id)
        if not adr:
            return f"ADR {adr_id} not found"

        lines = [
            f"# {adr.id}: {adr.title}",
            "",
            f"**Status**: {adr.status.value}",
            f"**Created**: {adr.created_at.isoformat()}",
            "",
            "## Context",
            "",
            adr.context,
            "",
            "## Options",
            "",
        ]
        for opt in adr.options:
            lines.append(f"- {opt}")
        lines.extend([
            "",
            "## Decision",
            "",
            adr.decision,
            "",
            "## Rationale",
            "",
            adr.rationale,
            "",
            "## Consequences",
            "",
        ])

        if adr.consequences.get("benefits"):
            lines.append("### Benefits")
            lines.append("")
            for b in adr.consequences["benefits"]:
                lines.append(f"- {b}")
            lines.append("")

        if adr.consequences.get("costs"):
            lines.append("### Costs")
            lines.append("")
            for c in adr.consequences["costs"]:
                lines.append(f"- {c}")
            lines.append("")

        if adr.revisit_conditions:
            lines.append("## Revisit Conditions")
            lines.append("")
            for rc in adr.revisit_conditions:
                lines.append(f"- {rc}")
            lines.append("")

        if adr.metrics_to_track:
            lines.append("## Metrics to Track")
            lines.append("")
            for k, v in adr.metrics_to_track.items():
                lines.append(f"- **{k}**: {v}")
            lines.append("")

        return "\n".join(lines)
