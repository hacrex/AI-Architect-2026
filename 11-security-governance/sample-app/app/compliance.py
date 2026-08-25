"""Compliance — track requirements, controls, and evidence."""
from datetime import datetime
from typing import Optional
from app.models import ComplianceRequirement


class ComplianceManager:
    """Track compliance requirements, controls, and evidence."""

    def __init__(self):
        self._requirements: dict[str, ComplianceRequirement] = {}
        self._seed_requirements()

    def _seed_requirements(self):
        reqs = [
            ComplianceRequirement(
                id="COMP-001", requirement="Data must be encrypted at rest",
                category="data_protection", control="AES-256 encryption",
                implementation="Database-level encryption + vector store encryption",
                evidence="Encryption config, key rotation logs", status="implemented"
            ),
            ComplianceRequirement(
                id="COMP-002", requirement="Data must be encrypted in transit",
                category="data_protection", control="TLS 1.3",
                implementation="All API endpoints behind TLS",
                evidence="Certificate configuration, TLS logs", status="implemented"
            ),
            ComplianceRequirement(
                id="COMP-003", requirement="Users must be authenticated",
                category="access_control", control="IAM integration",
                implementation="SSO + JWT tokens with expiry",
                evidence="Auth logs, token configuration", status="implemented"
            ),
            ComplianceRequirement(
                id="COMP-004", requirement="Access must be authorized",
                category="access_control", control="RBAC + department filtering",
                implementation="Role-based policies at retrieval layer",
                evidence="Policy configuration, authorization audit logs", status="implemented"
            ),
            ComplianceRequirement(
                id="COMP-005", requirement="Sensitive data must be redacted",
                category="data_protection", control="PII detection + masking",
                implementation="Input scanning, output filtering, log redaction",
                evidence="Detection logs, redaction statistics", status="implemented"
            ),
            ComplianceRequirement(
                id="COMP-006", requirement="Actions must be auditable",
                category="auditability", control="Comprehensive audit logging",
                implementation="All AI operations logged with user, action, result",
                evidence="Audit log samples, retention policy", status="implemented"
            ),
            ComplianceRequirement(
                id="COMP-007", requirement="Secrets must be managed securely",
                category="security", control="Vault + rotation",
                implementation="Centralized secret management, automatic rotation",
                evidence="Vault config, rotation logs", status="implemented"
            ),
            ComplianceRequirement(
                id="COMP-008", requirement="AI decisions must be explainable",
                category="responsible_ai", control="RAG source attribution",
                implementation="Source documents included with responses",
                evidence="Response format, source tracking", status="implemented"
            ),
            ComplianceRequirement(
                id="COMP-009", requirement="Model risks must be assessed",
                category="risk_management", control="Risk assessment process",
                implementation="Threat modeling, risk classification per system",
                evidence="Risk assessment records, threat model", status="implemented"
            ),
            ComplianceRequirement(
                id="COMP-010", requirement="Human oversight for high-risk actions",
                category="responsible_ai", control="Human-in-the-loop approval",
                implementation="Approval workflow for destructive/privileged actions",
                evidence="Approval workflow config, approval logs", status="implemented"
            ),
        ]
        for r in reqs:
            self._requirements[r.id] = r

    def add_requirement(self, requirement: ComplianceRequirement) -> ComplianceRequirement:
        self._requirements[requirement.id] = requirement
        return requirement

    def update_status(self, req_id: str, status: str,
                      evidence: str = None) -> Optional[ComplianceRequirement]:
        req = self._requirements.get(req_id)
        if not req:
            return None
        req.status = status
        if evidence:
            req.evidence = evidence
        req.last_verified = datetime.utcnow()
        return req

    def get_requirement(self, req_id: str) -> Optional[ComplianceRequirement]:
        return self._requirements.get(req_id)

    def list_requirements(self) -> list[ComplianceRequirement]:
        return list(self._requirements.values())

    def get_by_category(self, category: str) -> list[ComplianceRequirement]:
        return [r for r in self._requirements.values() if r.category == category]

    def get_by_status(self, status: str) -> list[ComplianceRequirement]:
        return [r for r in self._requirements.values() if r.status == status]

    def get_summary(self) -> dict:
        reqs = list(self._requirements.values())
        by_status = {}
        by_category = {}
        for r in reqs:
            by_status[r.status] = by_status.get(r.status, 0) + 1
            by_category[r.category] = by_category.get(r.category, 0) + 1
        implemented = by_status.get("implemented", 0)
        total = len(reqs)
        return {
            "total_requirements": total,
            "implemented": implemented,
            "pending": by_status.get("pending", 0),
            "compliance_pct": round(implemented / total * 100, 1) if total > 0 else 0,
            "by_status": by_status,
            "by_category": by_category
        }

    def get_checklist(self) -> list[dict]:
        return [
            {
                "id": r.id,
                "requirement": r.requirement,
                "category": r.category,
                "status": r.status,
                "control": r.control,
                "last_verified": r.last_verified.isoformat() if r.last_verified else None
            }
            for r in self._requirements.values()
        ]
