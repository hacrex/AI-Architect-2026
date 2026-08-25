# Capstone — Business Case

## Executive Summary

The Enterprise AI Knowledge Assistant reduces the time 10,000 employees spend searching internal documentation by 50%, improving support resolution rates and saving an estimated $27.5M annually in productivity gains against a $1.28M operating cost.

## Problem Statement

- **Current pain point:** Employees spend 40% of their time searching for information across 15+ disconnected systems (wiki, Confluence, Google Drive, SharePoint, email)
- **Affected users:** 10,000 employees across engineering, HR, finance, legal
- **Business impact:** ~$27.5M/year in lost productivity (10,000 employees × 20 min/day × $60/hr × 220 days)
- **Why now:** AI technology (RAG + LLMs) has matured to enable reliable enterprise knowledge retrieval with citations

## Proposed Solution

- **Approach:** RAG-based knowledge assistant with multi-model inference, enterprise security, and observability
- **Key capabilities:**
  - Natural language Q&A over internal documentation
  - Citation-backed responses with source attribution
  - Department-level data isolation and access control
  - Multi-model routing for cost optimization
  - Real-time document ingestion
- **Differentiation:** Enterprise-grade security, audit trail, and cost control — not just a chatbot

## Financial Analysis

### Investment

| Category | One-time | Monthly |
|----------|----------|---------|
| Engineering team (4 engineers) | - | $41,667 |
| Infrastructure (Kubernetes, GPU) | - | $20,000 |
| Model costs (managed APIs) | - | $15,000 |
| Platform operations | - | $10,000 |
| Security & compliance | - | $6,667 |
| Observability | - | $5,000 |
| Maintenance | - | $8,333 |
| **Total** | **-** | **$106,667** |

### Return

| Metric | Year 1 | Year 2 | Year 3 |
|--------|--------|--------|--------|
| Productivity savings | $27,500,000 | $27,500,000 | $27,500,000 |
| Support cost reduction | $500,000 | $750,000 | $1,000,000 |
| Faster onboarding | $200,000 | $300,000 | $400,000 |
| **Total value** | **$28,200,000** | **$28,550,000** | **$28,900,000** |
| Operating cost | $1,280,000 | $1,280,000 | $1,280,000 |
| **Net value** | **$26,920,000** | **$27,270,000** | **$27,620,000** |

### Break-even

- Monthly cost: $106,667
- Monthly value: $2,350,000
- **Break-even point: < 1 month**

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Low user adoption | High | Medium | Change management, training, executive sponsorship |
| Model quality issues | Medium | Low | Evaluation pipeline, human fallback, multiple models |
| Cost overrun | Medium | Low | Budget alerts, caching, model routing |
| Data security breach | Critical | Low | Encryption, IAM, audit logging, compliance |
| Provider outage | Medium | Medium | Multi-provider fallback, self-hosted backup |

## Success Metrics

| Metric | Baseline | Target (6 months) |
|--------|----------|-------------------|
| User adoption | 0% | 70% |
| Resolution time | 20 min | 10 min |
| Task success rate | 65% | 85% |
| Cost per task | $8.50 | $2.00 |
| Employee satisfaction | 3.2/5 | 4.2/5 |

## Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| Foundation | Month 1-2 | Infrastructure, IAM, basic RAG |
| Core | Month 3-4 | Full RAG, agents, multi-model |
| Production | Month 5-6 | Security, observability, FinOps |
| Optimization | Month 7-12 | Caching, routing, continuous improvement |
