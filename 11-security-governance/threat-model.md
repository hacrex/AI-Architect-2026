# Day 11 — AI Threat Model

## Threat Categories

| Threat | Severity | Likelihood | Impact | Category |
|--------|----------|------------|--------|----------|
| Prompt injection | Critical | High | Data leakage, unauthorized actions | Injection |
| Indirect prompt injection | Critical | Medium | Data leakage, behavior manipulation | Injection |
| Data exfiltration via response | Critical | Medium | Sensitive data exposure | Leakage |
| Sensitive data in logs/traces | High | Medium | Observability platform becomes sensitive | Leakage |
| Cross-tenant data exposure | Critical | Medium | Regulatory violation, trust erosion | Leakage |
| Unauthorized document retrieval | High | High | Access to documents user shouldn't see | Privilege |
| Over-privileged agent tool | High | Medium | Agent performs unauthorized actions | Privilege |
| Excessive agent permissions | Medium | High | Privilege escalation, blast radius increase | Privilege |
| Compromised API credential | Critical | Low | Full system compromise | Integrity |
| Malicious dependency | High | Low | Backdoor, data theft | Integrity |
| Model behavior degradation | Medium | Medium | Reduced quality, loss of trust | Integrity |
| Unauthorized model/prompt change | High | Medium | Behavior change without oversight | Integrity |
| Model poisoning | High | Low | Degraded model quality | Integrity |
| Secrets exposure | Critical | Medium | Account compromise | Integrity |
| Denial of service via token exhaustion | Medium | Medium | Service unavailability, cost overrun | Availability |

---

## Detailed Threat Analysis

### Threat 1: Prompt Injection

| Field | Value |
|-------|-------|
| Threat ID | T-001 |
| Threat Name | Prompt Injection |
| Category | Injection |
| Description | User crafts input that overrides system instructions, causing the model to ignore safety policies or reveal confidential information |
| Attack Vector | User-facing chat interface, API endpoint |
| Impact | Critical |
| Likelihood | High |
| Risk Score | Critical |
| Mitigation | Input validation, instruction hierarchy, output filtering, guardrails |
| Detection | Anomalous output patterns, instruction override attempts logged |
| Response | Block request, alert security team, investigate source |
| Residual Risk | Medium — sophisticated attacks may bypass filters |

### Threat 2: Indirect Prompt Injection

| Field | Value |
|-------|-------|
| Threat ID | T-002 |
| Threat Name | Indirect Prompt Injection |
| Category | Injection |
| Description | Malicious instructions embedded in documents that get retrieved by RAG and influence model behavior |
| Attack Vector | Documents entering the knowledge base |
| Impact | Critical |
| Likelihood | Medium |
| Risk Score | High |
| Mitigation | Document scanning, content policy enforcement, separation of data and instructions |
| Detection | Anomalous model behavior after document ingestion, output analysis |
| Response | Quarantine document, re-scan corpus, update detection rules |
| Residual Risk | Medium — novel injection patterns may evade detection |

### Threat 3: Unauthorized Document Retrieval

| Field | Value |
|-------|-------|
| Threat ID | T-003 |
| Threat Name | Unauthorized Document Retrieval |
| Category | Privilege |
| Description | User retrieves documents they are not authorized to access due to missing or incorrect authorization filtering in RAG |
| Attack Vector | Query construction, metadata filtering bypass |
| Impact | High |
| Likelihood | High |
| Risk Score | High |
| Mitigation | Authorization-aware retrieval, metadata-based filtering, access control at retrieval layer |
| Detection | Audit logging of retrieved documents, access anomaly detection |
| Response | Block access, review authorization rules, investigate query patterns |
| Residual Risk | Low — if authorization is properly implemented at retrieval layer |

### Threat 4: Sensitive Data Leakage in Response

| Field | Value |
|-------|-------|
| Threat ID | T-004 |
| Threat Name | Sensitive Data Leakage |
| Category | Leakage |
| Description | Model response contains sensitive information that should not be visible to the requesting user |
| Attack Vector | Indirect — through legitimate queries that surface sensitive context |
| Impact | Critical |
| Likelihood | Medium |
| Risk Score | High |
| Mitigation | Output filtering, sensitivity-aware response generation, user-level filtering |
| Detection | PII scanning of outputs, sensitivity classification of responses |
| Response | Block response, investigate context assembly, update filtering |
| Residual Risk | Medium — edge cases in context sensitivity |

### Threat 5: Sensitive Data in Observability

| Field | Value |
|-------|-------|
| Threat ID | T-005 |
| Threat Name | Sensitive Data in Logs and Traces |
| Category | Leakage |
| Description | Traces, logs, and metrics contain sensitive user data, making the observability platform a sensitive data repository |
| Attack Vector | Indirect — through standard logging of AI interactions |
| Impact | High |
| Likelihood | Medium |
| Risk Score | Medium |
| Mitigation | Data redaction in logs, access control on observability, retention policies |
| Detection | Periodic audit of log content, PII scanning of traces |
| Response | Redact sensitive data, tighten access controls, update logging policies |
| Residual Risk | Low — with proper redaction policies |

### Threat 6: Over-Privileged Agent Tool

| Field | Value |
|-------|-------|
| Threat ID | T-006 |
| Threat Name | Over-Privileged Agent Tool |
| Category | Privilege |
| Description | Agent has access to tools with broader permissions than necessary, enabling unauthorized actions |
| Attack Vector | Agent tool configuration, policy engine bypass |
| Impact | High |
| Likelihood | Medium |
| Risk Score | Medium |
| Mitigation | Least privilege tool configuration, policy engine enforcement, human approval for high-risk actions |
| Detection | Tool usage monitoring, action audit logging |
| Response | Revoke excessive permissions, investigate agent behavior |
| Residual Risk | Low — with proper least-privilege implementation |

### Threat 7: Compromised API Credential

| Field | Value |
|-------|-------|
| Threat ID | T-007 |
| Threat Name | Compromised API Credential |
| Category | Integrity |
| Description | API keys or tokens are leaked, allowing unauthorized access to AI services |
| Attack Vector | Code repositories, logs, configuration files, supply chain |
| Impact | Critical |
| Likelihood | Low |
| Risk Score | High |
| Mitigation | Secret management (vault), credential rotation, access logging |
| Detection | Anomalous API usage patterns, credential scan alerts |
| Response | Rotate credentials, investigate source, audit usage |
| Residual Risk | Low — with proper secret management |

### Threat 8: Malicious Dependency

| Field | Value |
|-------|-------|
| Threat ID | T-008 |
| Threat Name | Malicious Dependency |
| Category | Integrity |
| Description | A compromised package or model artifact introduces backdoor or data theft |
| Attack Vector | Package manager, model registry, container images |
| Impact | High |
| Likelihood | Low |
| Risk Score | Medium |
| Mitigation | Dependency scanning, container scanning, artifact signing, supply chain verification |
| Detection | Package integrity checks, behavioral monitoring |
| Response | Isolate affected systems, identify scope, update dependencies |
| Residual Risk | Low — with proper supply chain controls |

### Threat 9: Cross-Tenant Data Exposure

| Field | Value |
|-------|-------|
| Threat ID | T-009 |
| Threat Name | Cross-Tenant Data Exposure |
| Category | Leakage |
| Description | One tenant's data is visible to another tenant due to missing isolation |
| Attack Vector | Query construction, vector database configuration |
| Impact | Critical |
| Likelihood | Medium |
| Risk Score | High |
| Mitigation | Tenant isolation at retrieval layer, namespace separation, access validation |
| Detection | Cross-tenant query detection, tenant isolation audit |
| Response | Block access, investigate isolation controls, notify affected tenants |
| Residual Risk | Low — with proper tenant isolation |

### Threat 10: Model Behavior Degradation

| Field | Value |
|-------|-------|
| Threat ID | T-010 |
| Threat Name | Model Behavior Degradation |
| Category | Integrity |
| Description | Model quality degrades due to provider changes, data drift, or adversarial inputs |
| Attack Vector | Provider model updates, data distribution changes |
| Impact | Medium |
| Likelihood | Medium |
| Risk Score | Medium |
| Mitigation | Continuous evaluation, drift detection, fallback models, version pinning |
| Detection | Quality metrics degradation, drift detection alerts |
| Response | Investigate root cause, rollback if needed, update evaluation |
| Residual Risk | Low — with proper monitoring |

### Threat 11: Unauthorized Model/Prompt Change

| Field | Value |
|-------|-------|
| Threat ID | T-011 |
| Threat Name | Unauthorized Model or Prompt Change |
| Category | Integrity |
| Description | System prompt or model configuration is modified without proper review and approval |
| Attack Vector | Configuration management, insider threat |
| Impact | High |
| Likelihood | Medium |
| Risk Score | Medium |
| Mitigation | Change management process, version control, approval workflow |
| Detection | Configuration change detection, prompt version tracking |
| Response | Revert change, investigate source, update controls |
| Residual Risk | Low — with proper change management |

### Threat 12: Denial of Service via Token Exhaustion

| Field | Value |
|-------|-------|
| Threat ID | T-012 |
| Threat Name | Denial of Service via Token Exhaustion |
| Category | Availability |
| Description | Adversary sends requests designed to consume excessive tokens, causing service degradation or cost overrun |
| Attack Vector | User-facing API, chat interface |
| Impact | Medium |
| Likelihood | Medium |
| Risk Score | Medium |
| Mitigation | Rate limiting, token budgets, cost alerts, input length limits |
| Detection | Token usage anomalies, cost alerts |
| Response | Rate limit user, investigate source, adjust limits |
| Residual Risk | Low — with proper rate limiting |

---

## Mitigation Matrix

| Threat | Mitigation | Owner | Detection Signal | Response Time |
|--------|-----------|-------|------------------|---------------|
| Prompt injection | Input validation, guardrails, output filtering | Security | Rejection rate, flagged outputs | Immediate |
| Indirect prompt injection | Document scanning, content policy | Security + Data | Anomalous behavior after ingestion | Hours |
| Unauthorized retrieval | RAG authorization, metadata filtering | Platform | Access anomaly detection | Immediate |
| Data leakage | Output filtering, PII detection | Security | PII scan alerts | Immediate |
| Observability leakage | Log redaction, access control | Platform | Log content audit | Hours |
| Over-privileged tools | Least privilege, policy engine | Platform | Tool usage monitoring | Hours |
| Compromised credentials | Vault, rotation, scanning | Security | Anomalous API usage | Immediate |
| Malicious dependency | Scanning, signing, verification | Platform | Integrity check failures | Hours |
| Cross-tenant exposure | Tenant isolation, namespace separation | Platform | Cross-tenant query attempts | Immediate |
| Model degradation | Evaluation, drift detection | ML team | Quality metric degradation | Hours |
| Unauthorized changes | Change management, version control | Platform | Config change alerts | Hours |
| Token exhaustion | Rate limiting, cost alerts | Platform | Token usage anomalies | Minutes |

---

## Risk Heat Map

```
                    LIKELIOWHOOD
                    Low      Medium    High     Critical
                ┌─────────┬─────────┬─────────┬─────────┐
    Critical    │ T-007   │ T-001   │         │         │
                │ T-008   │ T-002   │         │         │
                │         │ T-004   │         │         │
   I            │         │ T-009   │         │         │
   M   High     │ T-010   │ T-005   │ T-003   │         │
   P            │ T-011   │ T-006   │         │         │
   A            │         │ T-012   │         │         │
   C   Medium   │         │         │         │         │
   T            │         │         │         │         │
                ├─────────┼─────────┼─────────┼─────────┤
      Low       │         │         │         │         │
                │         │         │         │         │
                └─────────┴─────────┴─────────┴─────────┘
```

---

## Governance Checklist

- [ ] AI risk assessment completed
- [ ] Model cards published
- [ ] Data lineage documented
- [ ] Human oversight process defined
- [ ] Audit logging enabled
- [ ] Retention policy defined
- [ ] Incident response plan tested
- [ ] Threat model reviewed quarterly
- [ ] Security controls tested annually
- [ ] Compliance evidence collected
- [ ] AI inventory maintained
- [ ] Owner assigned for each AI system
- [ ] Responsible AI principles documented
- [ ] Bias evaluation completed
- [ ] Explainability approach defined
