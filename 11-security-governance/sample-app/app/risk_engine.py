"""Risk Engine — AI risk assessment and classification."""
from datetime import datetime
from typing import Optional
from app.models import ThreatRecord, ThreatCategory, RiskLevel


class RiskEngine:
    """Assess and manage AI system risks with threat modeling."""

    def __init__(self):
        self._threats: dict[str, ThreatRecord] = {}
        self._risk_scores: dict[str, RiskLevel] = {}
        self._seed_threats()

    def _seed_threats(self):
        threats = [
            ThreatRecord(
                id="T-001", name="Prompt Injection", category=ThreatCategory.INJECTION,
                description="User crafts input that overrides system instructions",
                impact=RiskLevel.CRITICAL, likelihood=RiskLevel.HIGH,
                mitigation="Input validation, guardrails, output filtering",
                detection="Anomalous output patterns, instruction override attempts",
                response="Block request, alert security team"
            ),
            ThreatRecord(
                id="T-002", name="Indirect Prompt Injection", category=ThreatCategory.INJECTION,
                description="Malicious instructions in retrieved documents influence model behavior",
                impact=RiskLevel.CRITICAL, likelihood=RiskLevel.MEDIUM,
                mitigation="Document scanning, content policy, data/instruction separation",
                detection="Anomalous behavior after document ingestion",
                response="Quarantine document, re-scan corpus"
            ),
            ThreatRecord(
                id="T-003", name="Unauthorized Document Retrieval", category=ThreatCategory.PRIVILEGE,
                description="User retrieves documents they are not authorized to access",
                impact=RiskLevel.HIGH, likelihood=RiskLevel.HIGH,
                mitigation="Authorization-aware retrieval, metadata filtering",
                detection="Access anomaly detection, audit logging",
                response="Block access, review authorization rules"
            ),
            ThreatRecord(
                id="T-004", name="Sensitive Data Leakage", category=ThreatCategory.LEAKAGE,
                description="Model response contains sensitive information visible to unauthorized users",
                impact=RiskLevel.CRITICAL, likelihood=RiskLevel.MEDIUM,
                mitigation="Output filtering, PII detection, sensitivity-aware generation",
                detection="PII scanning of outputs, sensitivity classification",
                response="Block response, investigate context assembly"
            ),
            ThreatRecord(
                id="T-005", name="Sensitive Data in Logs", category=ThreatCategory.LEAKAGE,
                description="Traces and logs contain sensitive user data",
                impact=RiskLevel.HIGH, likelihood=RiskLevel.MEDIUM,
                mitigation="Data redaction, access control on observability, retention policies",
                detection="Periodic audit of log content",
                response="Redact data, tighten access controls"
            ),
            ThreatRecord(
                id="T-006", name="Over-Privileged Agent Tool", category=ThreatCategory.PRIVILEGE,
                description="Agent has access to tools with broader permissions than necessary",
                impact=RiskLevel.HIGH, likelihood=RiskLevel.MEDIUM,
                mitigation="Least privilege, policy engine, human approval",
                detection="Tool usage monitoring, action audit logging",
                response="Revoke excessive permissions"
            ),
            ThreatRecord(
                id="T-007", name="Compromised API Credential", category=ThreatCategory.INTEGRITY,
                description="API keys or tokens leaked, allowing unauthorized access",
                impact=RiskLevel.CRITICAL, likelihood=RiskLevel.LOW,
                mitigation="Secret management, credential rotation, access logging",
                detection="Anomalous API usage patterns",
                response="Rotate credentials, investigate source"
            ),
            ThreatRecord(
                id="T-008", name="Malicious Dependency", category=ThreatCategory.INTEGRITY,
                description="Compromised package or model artifact introduces backdoor",
                impact=RiskLevel.HIGH, likelihood=RiskLevel.LOW,
                mitigation="Dependency scanning, artifact signing, supply chain verification",
                detection="Package integrity checks",
                response="Isolate systems, identify scope"
            ),
            ThreatRecord(
                id="T-009", name="Cross-Tenant Data Exposure", category=ThreatCategory.LEAKAGE,
                description="One tenant's data visible to another due to missing isolation",
                impact=RiskLevel.CRITICAL, likelihood=RiskLevel.MEDIUM,
                mitigation="Tenant isolation at retrieval, namespace separation",
                detection="Cross-tenant query detection",
                response="Block access, investigate isolation"
            ),
            ThreatRecord(
                id="T-010", name="Model Behavior Degradation", category=ThreatCategory.INTEGRITY,
                description="Model quality degrades due to provider changes or drift",
                impact=RiskLevel.MEDIUM, likelihood=RiskLevel.MEDIUM,
                mitigation="Continuous evaluation, drift detection, fallback models",
                detection="Quality metrics degradation alerts",
                response="Investigate root cause, rollback if needed"
            ),
        ]
        for t in threats:
            t.risk_score = self._calculate_risk_score(t.impact, t.likelihood)
            self._threats[t.id] = t

    def _calculate_risk_score(self, impact: RiskLevel, likelihood: RiskLevel) -> RiskLevel:
        scores = {RiskLevel.LOW: 1, RiskLevel.MEDIUM: 2, RiskLevel.HIGH: 3, RiskLevel.CRITICAL: 4}
        combined = scores[impact] + scores[likelihood]
        if combined >= 7:
            return RiskLevel.CRITICAL
        elif combined >= 5:
            return RiskLevel.HIGH
        elif combined >= 3:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    def assess_risk(self, system_name: str, data_types: list[str],
                    user_count: int, has_external_access: bool = False) -> dict:
        risk_factors = []
        risk_level = RiskLevel.LOW

        if "confidential" in data_types or "restricted" in data_types:
            risk_factors.append("Sensitive data handling")
            risk_level = RiskLevel.HIGH

        if user_count > 10000:
            risk_factors.append("Large user base")
            if risk_level.value < RiskLevel.MEDIUM.value:
                risk_level = RiskLevel.MEDIUM

        if has_external_access:
            risk_factors.append("External access")
            if risk_level.value < RiskLevel.MEDIUM.value:
                risk_level = RiskLevel.MEDIUM

        if "financial" in data_types or "medical" in data_types:
            risk_factors.append("Regulated data")
            risk_level = RiskLevel.HIGH

        applicable_threats = self._get_applicable_threats(data_types, has_external_access)

        return {
            "system": system_name,
            "risk_level": risk_level.value,
            "risk_factors": risk_factors,
            "applicable_threats": applicable_threats,
            "top_threats": [
                {"name": t.name, "risk_score": t.risk_score.value}
                for t in applicable_threats[:5]
            ],
            "recommended_controls": self._get_recommended_controls(risk_level)
        }

    def _get_applicable_threats(self, data_types: list[str],
                                 has_external: bool) -> list[ThreatRecord]:
        threats = list(self._threats.values())
        if has_external:
            return sorted(threats, key=lambda t: t.risk_score.value, reverse=True)
        return [t for t in threats if t.category != ThreatCategory.AVAILABILITY]

    def _get_recommended_controls(self, risk_level: RiskLevel) -> list[str]:
        base = ["IAM integration", "Audit logging", "Input validation"]
        if risk_level in (RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL):
            base.extend(["RAG authorization", "PII detection", "Output filtering"])
        if risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL):
            base.extend(["Prompt injection guard", "Agent permissions", "Human approval"])
        if risk_level == RiskLevel.CRITICAL:
            base.extend(["Encryption at rest", "Secret management", "Incident response plan"])
        return base

    def get_threat(self, threat_id: str) -> Optional[ThreatRecord]:
        return self._threats.get(threat_id)

    def list_threats(self) -> list[dict]:
        return [
            {
                "id": t.id, "name": t.name, "category": t.category.value,
                "impact": t.impact.value, "likelihood": t.likelihood.value,
                "risk_score": t.risk_score.value
            }
            for t in self._threats.values()
        ]

    def get_risk_matrix(self) -> dict:
        matrix = {}
        for t in self._threats.values():
            key = f"{t.impact.value}:{t.likelihood.value}"
            if key not in matrix:
                matrix[key] = []
            matrix[key].append(t.name)
        return matrix

    def get_summary(self) -> dict:
        threats = list(self._threats.values())
        by_category = {}
        by_risk = {}
        for t in threats:
            by_category[t.category.value] = by_category.get(t.category.value, 0) + 1
            by_risk[t.risk_score.value] = by_risk.get(t.risk_score.value, 0) + 1
        return {
            "total_threats": len(threats),
            "by_category": by_category,
            "by_risk_score": by_risk
        }
