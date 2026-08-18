# Security — Threat Model

## Threat categories

| Threat | Severity | Likelihood | Impact |
|--------|----------|------------|--------|
| Prompt injection | Critical | High | Data leakage, unauthorized actions |
| Data exfiltration | Critical | Medium | Sensitive data exposure |
| Model poisoning | High | Low | Degraded model quality |
| Secrets exposure | Critical | Medium | Account compromise |
| Insecure tool use | High | Medium | Unauthorized API access |
| Supply chain attack | High | Low | Compromised dependencies |
| Excessive permissions | Medium | High | Privilege escalation |
| Tenant data leakage | Critical | Medium | Cross-tenant exposure |

## Mitigation matrix

| Threat | Mitigation | Owner | Monitoring Signal |
|--------|-----------|-------|-------------------|
| Prompt injection | Input validation, output filtering | Security | Rejection rate, flagged outputs |
| Data exfiltration | DLP policies, access controls | Data team | Unusual query patterns |
| Secrets exposure | Vault, rotation, scanning | Platform | Secret scan alerts |
| Model poisoning | Training data validation | ML team | Model quality metrics |
| Tenant isolation | Namespace isolation, RBAC | Platform | Cross-tenant query attempts |

## Governance checklist

- [ ] AI risk assessment completed
- [ ] Model cards published
- [ ] Data lineage documented
- [ ] Human oversight process defined
- [ ] Audit logging enabled
- [ ] Retention policy defined
- [ ] Incident response plan tested
