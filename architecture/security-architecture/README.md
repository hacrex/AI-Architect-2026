# Security Architecture — Enterprise AI Knowledge Assistant

## Security Controls

This document describes the security architecture, controls, and compliance considerations.

## Security Architecture Diagram

```
Employee
    │
    ▼
┌─────────────┐
│    WAF      │ ← SQL injection, XSS, prompt injection
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  API GW     │ ← Rate limiting, request validation
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  AuthN      │ ← SSO (Okta/Azure AD), JWT validation
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  AuthZ      │ ← Role-based access, document permissions
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ AI Gateway  │ ← Policy enforcement, data classification
└──────┬──────┘
       │
  ┌────┴─────────────────────────────────┐
  │                                      │
  ▼                                      ▼
┌──────────┐                      ┌──────────┐
│   RAG    │ ← Permission         │  Agent   │ ← Tool auth
│ Pipeline │   filtering          │  System  │   least privilege
└────┬─────┘                      └────┬─────┘
     │                                 │
     └──────────────┬──────────────────┘
                    │
                    ▼
             ┌──────────────┐
             │ Output       │ ← PII detection
             │ Validation   │   sensitive data redaction
             └──────┬───────┘
                    │
                    ▼
             ┌──────────────┐
             │ Audit Log    │ ← Every query + response
             └──────────────┘
```

## Authentication

| Mechanism | Implementation | Purpose |
|-----------|---------------|---------|
| SSO | OIDC (Okta/Azure AD) | Employee identity verification |
| JWT | RS256 signed tokens | Stateless request authentication |
| API Keys | HMAC-SHA256 | Service-to-service authentication |
| mTLS | Certificate-based | Internal service authentication |

### JWT Claims

```json
{
  "sub": "employee@company.com",
  "role": "employee",
  "department": "engineering",
  "clearance": "internal",
  "exp": 1234567890,
  "iss": "sso.company.com"
}
```

## Authorization

### Role-Based Access Control

| Role | Access Level | Document Access |
|------|-------------|-----------------|
| `employee` | Basic | Public + Department |
| `manager` | Elevated | Public + Department + Team |
| `admin` | Full | All documents |
| `hr` | Specialized | HR policies + Employee data |
| `security` | Audit | Security policies + Audit logs |

### Document-Level Permissions

```
Document
├── classification: public | internal | confidential | restricted
├── department: engineering | hr | finance | legal
├── owner: creator employee ID
└── viewers: [role, department, specific_users]
```

### Permission Filtering in RAG

```python
def retrieve_with_permissions(query, user_context):
    # Step 1: Semantic search
    candidates = vector_db.search(query, top_k=50)
    
    # Step 2: Permission filtering
    filtered = [
        doc for doc in candidates
        if has_permission(user_context, doc)
    ]
    
    # Step 3: Return top-K after filtering
    return filtered[:10]
```

## Data Protection

### Encryption

| State | Method | Standard |
|-------|--------|----------|
| At rest | AES-256 | AWS KMS managed |
| In transit | TLS 1.3 | All external connections |
| In processing | Enclave | Confidential computing (optional) |

### PII Detection

```
Input → PII Detector → Redact/Flag → Processing → Output PII Filter → Response
```

PII types detected:
- Email addresses
- Phone numbers
- Social Security Numbers
- Credit card numbers
- Employee IDs
- IP addresses

### Data Classification

| Level | Examples | Handling |
|-------|----------|----------|
| Public | Public policies, FAQs | No restrictions |
| Internal | Internal docs, procedures | Authenticated users |
| Confidential | Financial data, legal docs | Authorized roles only |
| Restricted | Employee PII, trade secrets | Specific individuals only |

## Audit Logging

### What Gets Logged

| Event | Data Captured |
|-------|---------------|
| Authentication | User ID, timestamp, success/failure, IP |
| Query | User ID, query text, timestamp, session ID |
| Retrieval | Documents retrieved, permissions checked |
| Tool invocation | Tool name, parameters, result, user |
| Model call | Model, tokens, latency, cost |
| Response | Response text, PII detected, filtered |
| Admin action | Action type, target, administrator |

### Audit Log Format

```json
{
  "timestamp": "2026-08-21T10:30:00Z",
  "event_type": "query",
  "user_id": "employee@company.com",
  "session_id": "abc-123",
  "query": "What is our vacation policy?",
  "documents_retrieved": ["policy-2026-vacation.pdf"],
  "model_used": "gpt-4",
  "tokens_used": 850,
  "latency_ms": 1200,
  "response_length": 250,
  "pii_detected": false,
  "ip_address": "10.0.1.50"
}
```

## Network Security

```
Internet → WAF → ALB → VPC (private)
                         │
                    ┌────┴────┐
                    │ Public  │ ← ALB, NAT Gateway
                    │ Subnet  │
                    └────┬────┘
                         │
                    ┌────┴────┐
                    │Private  │ ← API nodes, App nodes
                    │ Subnet  │
                    └────┬────┘
                         │
                    ┌────┴────┐
                    │Isolated │ ← GPU nodes, Data stores
                    │ Subnet  │   (no internet access)
                    └─────────┘
```

### Security Groups

| Group | Inbound | Outbound |
|-------|---------|----------|
| ALB | 443 from 0.0.0.0/0 | 8000 to app nodes |
| App | 8000 from ALB | 5432 to RDS, 6379 to Redis |
| GPU | 8000 from app nodes | 443 to model APIs |
| Data | 5432/6379 from app nodes | None |

## Secrets Management

| Secret | Storage | Rotation |
|--------|---------|----------|
| JWT signing key | AWS Secrets Manager | 90 days |
| Model API keys | AWS Secrets Manager | On compromise |
| Database credentials | AWS Secrets Manager | 30 days |
| Encryption keys | AWS KMS | Annual |

## Compliance Considerations

| Requirement | Implementation |
|-------------|---------------|
| GDPR | Data retention policies, right to deletion |
| SOC 2 | Audit logging, access controls, encryption |
| HIPAA | PII detection, data masking, audit trail |
| ISO 27001 | Security controls, incident response |

## Incident Response

| Severity | Response Time | Action |
|----------|--------------|--------|
| Critical (data breach) | < 1 hour | Alert security team, isolate systems |
| High (unauthorized access) | < 4 hours | Block user, review logs |
| Medium (suspicious activity) | < 24 hours | Monitor, investigate |
| Low (policy violation) | < 72 hours | Log, review in next audit |
