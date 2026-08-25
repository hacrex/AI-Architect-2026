# Day 11 — AI Security & Governance Exercise

## Overview

Design a complete security and governance architecture for an Enterprise AI Knowledge Platform serving 10,000 employees with sensitive documents across Engineering, HR, Finance, and Security departments.

---

## Part 1: Security Architecture

Design the security flow for the complete AI request lifecycle.

### Request flow with security controls

```
User Request
    ↓
┌─────────────────┐
│ Authentication   │ → Who is this user?
└────────┬────────┘
         ↓
┌─────────────────┐
│ Authorization    │ → What can they access?
└────────┬────────┘
         ↓
┌─────────────────┐
│ Input Validation │ → Is this a safe request?
└────────┬────────┘
         ↓
┌─────────────────┐
│ Prompt Guard     │ → Is this prompt injection?
└────────┬────────┘
         ↓
┌─────────────────┐
│ Data Classifier  │ → Does this contain PII?
└────────┬────────┘
         ↓
┌─────────────────┐
│ RAG with         │ → Retrieve only authorized docs
│ Authz Filtering  │
└────────┬────────┘
         ↓
┌─────────────────┐
│ Agent Policy     │ → Is this tool allowed?
└────────┬────────┘
         ↓
┌─────────────────┐
│ Output Filter    │ → Does response leak sensitive data?
└────────┬────────┘
         ↓
┌─────────────────┐
│ Audit Log        │ → Record everything
└─────────────────┘
```

### For each boundary, define:

| Boundary | Control | Implementation | Evidence |
|----------|---------|----------------|----------|
| Authentication | | | |
| Authorization | | | |
| Input Validation | | | |
| Prompt Guard | | | |
| Data Classification | | | |
| RAG Filtering | | | |
| Agent Policy | | | |
| Output Filter | | | |
| Audit Log | | | |

---

## Part 2: Threat Model

Create a threat model with at least 10 threats.

### Threat template

For each threat, fill in:

| Field | Value |
|-------|-------|
| Threat ID | |
| Threat Name | |
| Category | (Injection / Leakage / Privilege / Integrity / Availability) |
| Description | |
| Attack Vector | |
| Impact | (Critical / High / Medium / Low) |
| Likelihood | (Critical / High / Medium / Low) |
| Risk Score | Impact × Likelihood |
| Mitigation | |
| Detection | |
| Response | |
| Residual Risk | |

### Required threats

| # | Threat | Category |
|---|--------|----------|
| 1 | Prompt injection | Injection |
| 2 | Indirect prompt injection | Injection |
| 3 | Unauthorized document retrieval | Privilege |
| 4 | Sensitive data leakage in response | Leakage |
| 5 | Sensitive data in logs/traces | Leakage |
| 6 | Over-privileged agent tool | Privilege |
| 7 | Compromised API credential | Integrity |
| 6 | Malicious dependency | Integrity |
| 7 | Cross-tenant data exposure | Leakage |
| 8 | Model behavior degradation | Integrity |
| 9 | Unauthorized model/prompt change | Integrity |
| 10 | Excessive token consumption | Availability |

---

## Part 3: Authorization Model

Design the authorization model for RAG-aware access control.

### User roles and data access

| Role | Engineering | HR | Finance | Security | Public |
|------|-------------|-----|---------|----------|--------|
| Engineer | Read | — | — | — | Read |
| HR Manager | — | Read/Write | Read | — | Read |
| Finance Analyst | — | — | Read/Write | — | Read |
| Security Officer | Read | Read | Read | Read/Write | Read |
| CEO | Read | Read | Read | Read | Read |
| Contractor | — | — | — | — | Read |

### Design the retrieval filter

For a given user, how does the system filter documents?

```
User Request
    ↓
┌─────────────────┐
│ User Identity    │
└────────┬────────┘
         ↓
┌─────────────────┐
│ Role Mapping     │ → ["engineering", "public"]
└────────┬────────┘
         ↓
┌─────────────────┐
│ Document Filter  │ → WHERE department IN ["engineering", "public"]
└────────┬────────┘
         ↓
┌─────────────────┐
│ Vector Search    │ → Only authorized documents
└────────┬────────┘
```

---

## Part 4: Agent Permission Model

Design the permission model for AI agents.

### Agent tool permissions

| Agent | Tool | Allowed Actions | Data Scope | Human Approval |
|-------|------|-----------------|------------|----------------|
| Knowledge Agent | Vector Search | Read | Authorized only | No |
| Knowledge Agent | Web Search | Read | Public | No |
| Ticket Agent | Ticket API | Create | Engineering | No |
| Ticket Agent | Ticket API | Close | Engineering | Yes |
| Code Agent | Code Repository | Read | Assigned repos | No |
| Code Agent | Code Repository | Write | Assigned repos | Yes |
| Admin Agent | User Management | Read | All | No |
| Admin Agent | User Management | Write | All | Yes |
| Deployment Agent | CI/CD | Read | All | No |
| Deployment Agent | CI/CD | Execute | All | Yes |

### Design the policy engine

```
Agent Action Request
    ↓
┌─────────────────┐
│ Agent Identity   │
└────────┬────────┘
         ↓
┌─────────────────┐
│ Tool Policy      │ → Is this tool allowed for this agent?
└────────┬────────┘
         ↓
┌─────────────────┐
│ Action Policy    │ → Is this action allowed?
└────────┬────────┘
         ↓
┌─────────────────┐
│ Data Scope       │ → Is this data in scope?
└────────┬────────┘
         ↓
┌─────────────────┐
│ Risk Assessment  │ → Does this require human approval?
└────────┬────────┘
         ↓
┌─────────────────┐
│ Decision         │ → Allow / Deny / Require Approval
└─────────────────┘
```

---

## Part 5: PII Detection & Redaction

Design the PII detection and handling system.

### Detection rules

| PII Type | Pattern | Handling | Example |
|----------|---------|----------|---------|
| Email | Regex | Mask domain | j***@***.com |
| Phone | Regex | Mask digits | +91 XXXXX XXXXX |
| SSN | Regex | Remove | [REDACTED] |
| Credit Card | Regex | Remove | [REDACTED] |
| Name | NER | Pseudonymize | [PERSON_1] |
| Address | NER | Pseudonymize | [ADDRESS_1] |
| Salary | Keyword + Context | Remove | [REDACTED] |
| Medical | Keyword + Context | Remove | [REDACTED] |

### Processing pipeline

```
User Input
    ↓
┌─────────────────┐
│ PII Scanner      │ → Detect email, phone, SSN, etc.
└────────┬────────┘
         ↓
┌─────────────────┐
│ Classification   │ → Sensitivity level (Public/Internal/Confidential/Restricted)
└────────┬────────┘
         ↓
┌─────────────────┐
│ Policy Decision  │ → Allow / Mask / Block
└────────┬────────┘
         ↓
┌─────────────────┐
│ Redaction        │ → Apply masking or removal
└────────┬────────┘
         ↓
┌─────────────────┐
│ Audit Log        │ → Record what was redacted
└─────────────────┘
```

---

## Part 6: Governance Record

Create a governance record for the AI system.

### System information

| Field | Value |
|-------|-------|
| System Name | |
| Owner | |
| Business Purpose | |
| Users | |
| Data Sources | |
| Models Used | |
| Risk Level | |
| Environment | |
| Last Review | |
| Next Review | |
| Status | |

### Applicable policies

| Policy | Status | Last Evidence |
|--------|--------|---------------|
| Data Classification Policy | | |
| Access Control Policy | | |
| Encryption Policy | | |
| Retention Policy | | |
| Incident Response Policy | | |
| Acceptable Use Policy | | |
| Third-Party Risk Policy | | |
| AI Ethics Policy | | |

### Controls implemented

| Control | Type | Status | Evidence |
|---------|------|--------|----------|
| IAM integration | Preventive | | |
| RAG authorization | Preventive | | |
| Prompt injection guard | Preventive | | |
| PII detection | Preventive | | |
| Audit logging | Detective | | |
| Output filtering | Preventive | | |
| Agent permissions | Preventive | | |
| Human approval | Corrective | | |

---

## Part 7: Compliance Checklist

Map requirements to architecture controls.

### For each requirement:

| Requirement | Architecture Control | Implementation | Evidence | Status |
|-------------|---------------------|----------------|----------|--------|
| Data must be encrypted at rest | | | | |
| Data must be encrypted in transit | | | | |
| Users must be authenticated | | | | |
| Access must be authorized | | | | |
| Sensitive data must be redacted | | | | |
| Actions must be auditable | | | | |
| Secrets must be managed securely | | | | |
| AI decisions must be explainable | | | | |
| Model risks must be assessed | | | | |
| Human oversight for high-risk | | | | |

---

## Part 8: Incident Response Plan

Design the incident response plan for AI-specific security incidents.

### Scenario: Sensitive data leaked through AI response

**Detection**
- How do we know? _______________
- Who gets notified? _______________
- What dashboard shows it? _______________

**Containment**
- Step 1: _______________
- Step 2: _______________
- Step 3: _______________

**Investigation**
- Step 1: Check audit logs for the request
- Step 2: Identify what data was exposed
- Step 3: Identify who received the data
- Step 4: Check if data was cached or logged
- Step 5: Assess blast radius

**Mitigation**
- Option A: _______________
- Option B: _______________
- Option C: _______________

**Recovery**
- Step 1: _______________
- Step 2: _______________
- Step 3: _______________

**Post-Incident**
- [ ] Update threat model
- [ ] Add missing control
- [ ] Update runbook
- [ ] Notify affected parties
- [ ] Report to compliance (if required)

---

## Deliverables

1. **Security architecture diagram** — all boundaries with controls
2. **Threat model** — 10+ threats with risk scores
3. **Authorization model** — role-based RAG filtering
4. **Agent permission model** — tool-level access control
5. **PII detection rules** — detection patterns and handling
6. **Governance record** — system ownership and policies
7. **Compliance checklist** — requirements mapped to controls
8. **Incident response plan** — AI-specific security incidents
