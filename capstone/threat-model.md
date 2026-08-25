# Capstone — Threat Model

## Threat Summary

| Threat Category | Threats Identified | Highest Severity |
|-----------------|-------------------|------------------|
| Prompt injection | 3 | Critical |
| Data exfiltration | 2 | Critical |
| Privilege escalation | 2 | High |
| Supply chain | 2 | High |
| Availability | 2 | Medium |
| Integrity | 1 | Medium |

## Detailed Threat Analysis

### T-001: Direct Prompt Injection

- **Description:** User crafts input that overrides system instructions, causing the model to ignore safety rules or reveal confidential information
- **Attack vector:** Malicious prompt text in user input
- **Impact:** Data leakage, unauthorized actions, system manipulation
- **Likelihood:** High
- **Mitigation:** Input validation, prompt guard with pattern matching, output filtering, instruction hierarchy enforcement
- **Residual risk:** Low — pattern-based detection may miss novel attacks

### T-002: Indirect Prompt Injection

- **Description:** Malicious instructions embedded in retrieved documents influence model behavior during RAG augmentation
- **Attack vector:** Poisoned documents in the knowledge base
- **Impact:** Data exfiltration, unauthorized tool use, incorrect responses
- **Likelihood:** Medium
- **Mitigation:** Document scanning, content policy enforcement, separation of data and instructions in prompts, document source verification
- **Residual risk:** Medium — sophisticated injections may evade detection

### T-003: Prompt Injection via Agent Tools

- **Description:** Agent tool responses contain injected instructions that manipulate the agent's behavior
- **Attack vector:** Compromised external API or database returning manipulated content
- **Impact:** Agent performs unauthorized actions, data exfiltration
- **Likelihood:** Low
- **Mitigation:** Tool output sanitization, agent permission limits, human approval for high-risk actions
- **Residual risk:** Low — tool output scanning adds defense layer

### T-004: Unauthorized Document Retrieval

- **Description:** User retrieves documents they are not authorized to access due to missing or bypassed access controls
- **Attack vector:** Manipulated query, missing permission filters, API abuse
- **Impact:** Confidential data exposure, compliance violation
- **Likelihood:** High
- **Mitigation:** Authorization-aware retrieval, metadata filtering, department-level isolation, audit logging
- **Residual risk:** Low — defense in depth with multiple filter layers

### T-005: Sensitive Data Leakage in Responses

- **Description:** Model response contains sensitive information (PII, confidential data) visible to unauthorized users
- **Attack vector:** Overly broad retrieval, model hallucination, context window overflow
- **Impact:** Data breach, compliance violation, reputational damage
- **Likelihood:** Medium
- **Mitigation:** Output PII filtering, sensitivity-aware generation, response validation, data classification enforcement
- **Residual risk:** Medium — model behavior is not fully deterministic

### T-006: Sensitive Data in Logs

- **Description:** Traces and logs contain sensitive user data, query content, or document excerpts
- **Attack vector:** Over-verbose logging, missing redaction
- **Impact:** Data exposure through log access, compliance violation
- **Likelihood:** Medium
- **Mitigation:** Data redaction in logs, access controls on observability, retention policies, log content auditing
- **Residual risk:** Low — redaction rules can be validated

### T-007: Excessive Agent Permissions

- **Description:** Agent has access to tools with broader permissions than necessary, enabling unauthorized actions
- **Attack vector:** Overly permissive tool policies, missing least-privilege enforcement
- **Impact:** Unauthorized data access, destructive actions, cost overrun
- **Likelihood:** Medium
- **Mitigation:** Policy-based authorization, tool-level permissions, human approval for high-risk actions, audit logging
- **Residual risk:** Low — policy engine enforces granular controls

### T-008: Compromised API Credentials

- **Description:** API keys or tokens leaked, allowing unauthorized access to model providers or internal services
- **Attack vector:** Code repository exposure, log leakage, social engineering
- **Impact:** Unauthorized model usage, data access, cost overrun
- **Likelihood:** Low
- **Mitigation:** Secret management (Vault), credential rotation, access logging, anomaly detection
- **Residual risk:** Low — rotation limits exposure window

### T-009: Malicious Dependencies

- **Description:** Compromised package or model artifact introduces backdoor into the system
- **Attack vector:** Supply chain attack on Python packages, model weights, or container images
- **Impact:** System compromise, data exfiltration, backdoor access
- **Likelihood:** Low
- **Mitigation:** Dependency scanning, artifact signing, container image verification, supply chain monitoring
- **Residual risk:** Low — scanning catches known vulnerabilities

### T-010: Model Provider Outage

- **Description:** Primary model provider becomes unavailable, causing system degradation
- **Attack vector:** Provider infrastructure failure, rate limiting, account suspension
- **Impact:** Service degradation, inability to generate responses
- **Likelihood:** Medium
- **Mitigation:** Multi-provider fallback, self-hosted backup, cached responses, graceful degradation
- **Residual risk:** Low — fallback chain ensures availability

### T-011: Cost Overrun via Abuse

- **Description:** Malicious or excessive usage causes unexpected cost spike
- **Attack vector:** Automated queries, prompt stuffing, token amplification
- **Impact:** Budget overrun, service disruption for other users
- **Likelihood:** Medium
- **Mitigation:** Rate limiting, token budgets per user, cost alerts, semantic caching, model routing
- **Residual risk:** Low — multiple cost control layers

### T-012: Cross-Tenant Data Exposure

- **Description:** One department's data visible to another due to missing namespace isolation
- **Attack vector:** Missing permission filters, shared vector store without namespaces
- **Impact:** Confidential data exposure, trust violation, compliance breach
- **Likelihood:** Medium
- **Mitigation:** Department-level namespaces in vector DB, authorization context in retrieval, audit logging
- **Residual risk:** Low — namespace isolation is enforced at query time

## Security Controls

| Control | Implementation | Owner | Status |
|---------|---------------|-------|--------|
| Authentication | SSO + JWT (RS256) | Security | Implemented |
| Authorization | RBAC + department filtering (OPA) | Security | Implemented |
| Prompt injection guard | Pattern matching + ML | Platform | Implemented |
| PII detection | Regex + heuristics | Platform | Implemented |
| Agent permissions | Policy engine with tool-level auth | Platform | Implemented |
| Audit logging | Append-only log for all operations | Security | Implemented |
| Data classification | 4-level system (public to restricted) | Security | Implemented |
| Encryption at rest | AES-256 (AWS KMS) | Infrastructure | Implemented |
| Encryption in transit | TLS 1.3 | Infrastructure | Implemented |
| Secret management | AWS Secrets Manager + rotation | Security | Implemented |
| Network segmentation | VPC, private subnets, security groups | Infrastructure | Implemented |
| Dependency scanning | CI/CD pipeline, container scanning | DevSecOps | Implemented |
| Compliance tracking | Requirement management system | Security | Implemented |

## Incident Response

| Severity | Example | Response Time | Action |
|----------|---------|--------------|--------|
| Critical | Data breach, system compromise | < 15 min | Isolate, assess, notify, remediate |
| High | Unauthorized access, prompt injection spike | < 1 hour | Block, investigate, remediate |
| Medium | Anomalous usage, quality degradation | < 4 hours | Monitor, investigate, adjust |
| Low | Policy violation, minor anomaly | < 24 hours | Log, review, process |
