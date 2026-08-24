# AI Architect 2026 — Project Requirements

Complete requirements extracted from all 12 days, architecture folder, and capstone.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [User Requirements](#2-user-requirements)
3. [Functional Requirements by Domain](#3-functional-requirements-by-domain)
4. [Non-Functional Requirements](#4-non-functional-requirements)
5. [Deliverables by Day](#5-deliverables-by-day)
6. [Sample App Requirements](#6-sample-app-requirements)
7. [Architecture Artifact Requirements](#7-architecture-artifact-requirements)
8. [Portfolio Completion Checklist](#8-portfolio-completion-checklist)
9. [Architect Competency Requirements](#9-architect-competency-requirements)

---

## 1. Project Overview

### Purpose

A 12-day learning series that takes engineers from building AI features to designing production-ready AI systems.

### Target Audience

- Cloud Engineers
- DevOps Engineers
- Platform Engineers
- Software Engineers
- Data Engineers
- ML Engineers
- AI Engineers

### Success Criteria

By completion, the learner can:

- Understand AI and data foundations
- Design LLM and agentic architectures
- Design AI infrastructure and deployment platforms
- Evaluate technology choices
- Design for scale, reliability, and failure
- Model AI costs and apply FinOps thinking
- Build observability into AI systems
- Design security and governance
- Connect architecture decisions to business outcomes
- Document decisions with diagrams, ADRs, trade-off analyses, and success metrics

---

## 2. User Requirements

### 2.1 End Users

| User Type | Description | Primary Needs |
|-----------|-------------|---------------|
| Employee (10,000) | General staff across departments | Find answers, understand policies, search knowledge |
| Engineering | Technical staff | Access technical docs, architecture guides, API standards |
| HR | Human resources | Access HR policies, benefits, onboarding materials |
| Finance | Finance team | Expense policies, budget information |
| Legal/Compliance | Legal staff | Privacy policies, compliance documentation |
| Security | IT security | Security docs, data classification, incident procedures |
| Administrators | System admins | Manage users, models, access, monitoring |
| Developers | AI/app developers | Build, test, deploy AI applications |

### 2.2 User Stories

| ID | Story | Priority | Source |
|----|-------|----------|--------|
| US-01 | As an employee, I want to ask questions in natural language and get accurate answers with sources so I can find information quickly | High | Day 01, 03 |
| US-02 | As an employee, I want to see which documents the answer came from so I can verify correctness | High | Day 01 |
| US-03 | As an employee, I want to ask follow-up questions in conversation so I can refine my understanding | Medium | Day 03 |
| US-04 | As an employee, I want the system to respond within 2 seconds for simple questions so my workflow is not interrupted | High | Day 01, 09 |
| US-05 | As an employee, I want to access only documents I am authorized to see so sensitive information is protected | High | Day 05, 07 |
| US-06 | As an engineer, I want to search technical documentation and architecture guides so I can follow standards | High | Day 01, 05 |
| US-07 | As an HR user, I want to find policy information without searching through multiple systems | Medium | Day 01 |
| US-08 | As an administrator, I want to see who is using the system and what they are asking so I can improve content | Medium | Day 10 |
| US-09 | As a developer, I want the system to be available 99.9% of the time so I can rely on it for my work | High | Day 01, 07 |
| US-10 | As an employee, I want to get help even when the primary AI model is unavailable so I am not blocked | High | Day 02, 07 |
| US-11 | As a security user, I want all queries logged for audit purposes so we maintain compliance | High | Day 07, 11 |
| US-12 | As an administrator, I want to control which model is used for different query types to optimize cost | Medium | Day 02, 09 |
| US-13 | As an employee, I want the AI to understand my department context so answers are relevant to my role | Medium | Day 03, 05 |
| US-14 | As a manager, I want to see cost and usage reports per department so I can manage budget | Medium | Day 09, 10 |
| US-15 | As an employee, I want to be told when the AI is unsure rather than getting a wrong answer | High | Day 01, 11 |

### 2.3 User Experience Requirements

| ID | Requirement | Target | Source |
|----|-------------|--------|--------|
| UX-01 | Response time for simple queries | < 2 seconds | Day 01, 09 |
| UX-02 | Response time for complex RAG queries | < 5 seconds | Day 09 |
| UX-03 | Source attribution | Every answer includes sources | Day 01 |
| UX-04 | Confidence indication | System indicates when uncertain | Day 01, 11 |
| UX-05 | Conversation context | Maintain context across follow-ups | Day 03 |
| UX-06 | Graceful degradation | Cached or partial answers when components fail | Day 07 |
| UX-07 | Error messages | Clear, actionable error messages | Day 06, 07 |
| UX-08 | Accessibility | Standard web accessibility compliance | Day 01 |

### 2.4 User Access Requirements

| Role | Document Access | Model Access | Agent Access | Rate Limit |
|------|----------------|--------------|--------------|------------|
| Employee | Public docs | Standard models | Search only | 100 req/min |
| Engineering | Public + Engineering docs | Standard + self-hosted | Search + database | 200 req/min |
| HR | Public + HR docs | Standard models | Search only | 100 req/min |
| Finance | Public + Finance docs | Standard models | Search only | 100 req/min |
| Security | All docs | All models | Search + security tools | 200 req/min |
| Admin | All docs | All models | All tools | 500 req/min |

### 2.5 User Acceptance Criteria

| Scenario | Expected Behavior | Priority |
|----------|-------------------|----------|
| User asks "What is our remote work policy?" | Returns answer with source link to HR policy doc | High |
| User asks follow-up question | Maintains conversation context | Medium |
| User asks about unauthorized document | Returns "I don't have access to that information" | High |
| Primary model is down | System uses fallback model, user gets answer | High |
| User asks something the AI is unsure about | System indicates low confidence | High |
| User asks complex multi-step question | Agent uses tools, returns synthesized answer | Medium |
| System is under heavy load | Responses may be slower but still available | Medium |
| User queries at 2am | System available (automated, no human needed) | Low |

---

## 3. Functional Requirements by Domain

### 2.1 AI Application Layer

| ID | Requirement | Source |
|----|-------------|--------|
| FR-AI-01 | Support RAG (retrieval-augmented generation) for knowledge-intensive queries | Day 01, 03, 05, 07 |
| FR-AI-02 | Support agentic workflows with tool calling | Day 03, 07 |
| FR-AI-03 | Provide source attribution for all answers | Day 01 |
| FR-AI-04 | Support multi-turn conversations with context | Day 03 |
| FR-AI-05 | Implement context engineering (system, conversation, retrieved, prompt, response buffer) | Day 03 |
| FR-AI-06 | Support synchronous and asynchronous AI processing | Day 07 |
| FR-AI-07 | Support event-driven document ingestion | Day 07 |
| FR-AI-08 | Provide graceful degradation when components fail | Day 07 |

### 2.2 Model Layer

| ID | Requirement | Source |
|----|-------------|--------|
| FR-M-01 | Support multiple model providers (OpenAI, Azure OpenAI, Anthropic, self-hosted) | Day 02, 07 |
| FR-M-02 | Implement model routing based on request complexity (simple/normal/complex) | Day 02, 03, 07 |
| FR-M-03 | Provide automatic fallback chain when primary model fails | Day 02, 07 |
| FR-M-04 | Support managed and self-hosted model deployments | Day 04 |
| FR-M-05 | Track token usage and cost per model | Day 02, 09 |
| FR-M-06 | Support model evaluation with quality, safety, cost, latency gates | Day 06 |
| FR-M-07 | Implement circuit breaker pattern for failing model providers | Day 07 |

### 2.3 Data Layer

| ID | Requirement | Source |
|----|-------------|--------|
| FR-D-01 | Support document ingestion (parse, chunk, embed, store) | Day 05 |
| FR-D-02 | Support multiple chunking strategies (fixed-size, structure-aware, semantic) | Day 05 |
| FR-D-03 | Implement hybrid search (keyword + vector) | Day 05 |
| FR-D-04 | Support reranking of retrieval results | Day 05 |
| FR-D-05 | Store and query embeddings with metadata filtering | Day 05 |
| FR-D-06 | Support document-level permission filtering at retrieval | Day 05, 07 |
| FR-D-07 | Support real-time and batch document ingestion | Day 05, 07 |
| FR-D-08 | Maintain data freshness with configurable SLAs | Day 05 |
| FR-D-09 | Handle document updates and deletions gracefully | Day 05 |

### 2.4 Infrastructure Layer

| ID | Requirement | Source |
|----|-------------|--------|
| FR-I-01 | Support GPU-based inference serving | Day 04 |
| FR-I-02 | Implement Kubernetes-native model serving (KServe) | Day 04 |
| FR-I-03 | Support autoscaling based on demand | Day 04, 09 |
| FR-I-04 | Support horizontal scaling of AI services | Day 09 |
| FR-I-05 | Implement continuous batching for GPU utilization | Day 04 |
| FR-I-06 | Support scale-to-zero for non-critical workloads | Day 04 |

### 2.5 Platform Layer

| ID | Requirement | Source |
|----|-------------|--------|
| FR-P-01 | Provide model registry with versioning | Day 06 |
| FR-P-02 | Implement experiment tracking | Day 06 |
| FR-P-03 | Support CI/CD pipeline with AI evaluation gates | Day 06 |
| FR-P-04 | Support canary deployment (5% to 25% to 50% to 100%) | Day 06 |
| FR-P-05 | Support blue-green and shadow deployment | Day 06 |
| FR-P-06 | Implement drift detection (data, model, concept) | Day 06 |
| FR-P-07 | Support rollback with verification | Day 06 |
| FR-P-08 | Provide self-service portal/CLI for developers | Day 06 |
| FR-P-09 | Support GitOps for deployments | Day 06 |

### 2.6 Security Layer

| ID | Requirement | Source |
|----|-------------|--------|
| FR-S-01 | Implement enterprise authentication (SSO/OAuth/OIDC) | Day 07, 11 |
| FR-S-02 | Implement role-based access control | Day 05, 07, 11 |
| FR-S-03 | Enforce document-level permissions | Day 05, 07 |
| FR-S-04 | Implement tool authorization for agents | Day 03, 07, 11 |
| FR-S-05 | Provide human approval for sensitive agent actions | Day 07 |
| FR-S-06 | Implement full audit logging | Day 07, 11 |
| FR-S-07 | Enforce secrets management | Day 11 |
| FR-S-08 | Implement input validation and output filtering | Day 11 |
| FR-S-09 | Support prompt injection detection | Day 11 |
| FR-S-10 | Support data classification and handling | Day 11 |

### 2.7 Observability Layer

| ID | Requirement | Source |
|----|-------------|--------|
| FR-O-01 | Implement distributed tracing for AI requests | Day 07, 10 |
| FR-O-02 | Track tokens, latency, and cost per request | Day 07, 10 |
| FR-O-03 | Monitor infrastructure metrics (CPU, memory, GPU, network) | Day 10 |
| FR-O-04 | Monitor AI quality metrics (hallucination rate, retrieval relevance, user satisfaction) | Day 10 |
| FR-O-05 | Track cost per model, per user, per department | Day 09, 10 |
| FR-O-06 | Implement alerting with configurable thresholds | Day 10 |
| FR-O-07 | Provide dashboards (System Health, AI Quality, Cost) | Day 10 |
| FR-O-08 | Support user feedback collection | Day 10 |

---

## 4. Non-Functional Requirements

### 4.1 Performance

| ID | Requirement | Target | Source |
|----|-------------|--------|--------|
| NFR-P-01 | API response latency (p95) | < 2s for simple queries | Day 01, 09 |
| NFR-P-02 | API response latency (p95) | < 5s for complex RAG queries | Day 09 |
| NFR-P-03 | First token latency (TTFT) | < 500ms for conversational | Day 04 |
| NFR-P-04 | Throughput | Support 10,000 concurrent users | Day 01, 09 |
| NFR-P-05 | Inference throughput | Scale to 100 req/sec | Day 04, 09 |

### 4.2 Availability

| ID | Requirement | Target | Source |
|----|-------------|--------|--------|
| NFR-A-01 | System availability | 99.9% uptime | Day 01, 07 |
| NFR-A-02 | Model fallback | Automatic failover within 5s | Day 02, 07 |
| NFR-A-03 | Data availability | Vector DB redundancy | Day 05, 07 |
| NFR-A-04 | Disaster recovery | RTO < 1 hour, RPO < 5 minutes | Day 09 |

### 4.3 Security

| ID | Requirement | Target | Source |
|----|-------------|--------|--------|
| NFR-S-01 | Authentication | Enterprise SSO (OAuth 2.0 / OIDC) | Day 07, 11 |
| NFR-S-02 | Authorization | Role-based + document-level permissions | Day 05, 07, 11 |
| NFR-S-03 | Data encryption | At rest (AES-256) and in transit (TLS 1.3) | Day 11 |
| NFR-S-04 | Audit logging | 100% of AI requests logged | Day 07, 11 |
| NFR-S-05 | Secrets | No secrets in code or logs | Day 11 |
| NFR-S-06 | Prompt injection | Detection and prevention | Day 11 |
| NFR-S-07 | Data leakage | Prevent sensitive data in prompts | Day 01, 11 |

### 4.4 Scalability

| ID | Requirement | Target | Source |
|----|-------------|--------|--------|
| NFR-SC-01 | User scale | 10,000 concurrent users | Day 01, 07, 09 |
| NFR-SC-02 | Data scale | 100 million documents | Day 05 |
| NFR-SC-03 | Request scale | 10x traffic growth support | Day 09 |
| NFR-SC-04 | Horizontal scaling | Add nodes without downtime | Day 04, 09 |
| NFR-SC-05 | GPU scaling | Autoscale based on queue depth | Day 04, 09 |

### 4.5 Cost

| ID | Requirement | Target | Source |
|----|-------------|--------|--------|
| NFR-C-01 | Monthly budget | Defined per deployment | Day 09 |
| NFR-C-02 | Cost per request | Tracked and alerted | Day 09, 10 |
| NFR-C-03 | Cost optimization | Semantic caching, model routing | Day 02, 09 |
| NFR-C-04 | Cost visibility | Per user, per model, per department | Day 09, 10 |
| NFR-C-05 | Budget alerts | Notify at 80% and 100% of budget | Day 09, 10 |

### 4.6 Reliability

| ID | Requirement | Target | Source |
|----|-------------|--------|--------|
| NFR-R-01 | Retry with exponential backoff | For transient failures | Day 07, 09 |
| NFR-R-02 | Circuit breaker | Open after 3 consecutive failures | Day 07 |
| NFR-R-03 | Graceful degradation | Cached/fallback responses | Day 07 |
| NFR-R-04 | Queue backpressure | Rate limit when queue full | Day 07, 09 |
| NFR-R-05 | Health checks | Every 30 seconds | Day 06, 07 |

---

## 5. Deliverables by Day

### Day 01 — Foundations

- [ ] Run sample app
- [ ] Architecture diagram (client, auth, API gateway, AI app, retrieval, model gateway, vector DB, observability, security)
- [ ] Architecture notes (problem, requirements, components, data flow, dependencies, security, failure, scaling)
- [ ] Answer 17 architect questions

### Day 02 — AI/ML Fundamentals

- [ ] Model comparison table (2 models, metrics, cost, recommendation)
- [ ] LLM necessity decisions (10 scenarios)
- [ ] RAG vs fine-tuning analysis (8 scenarios)
- [ ] Model routing strategy (8 requests classified, monthly cost estimate)
- [ ] Model evaluation framework (9 criteria, scoring rubric)
- [ ] Answer 12 self-assessment questions

### Day 03 — LLM Engineering

- [ ] Working RAG pipeline (7 steps, 3 test queries)
- [ ] Tool-enabled AI workflow (auth, validation, error handling, audit, rate limiting)
- [ ] Model gateway abstraction (routing, fallback, token tracking)
- [ ] RAG decision document (justification, chunking, embedding, vector DB, cost)
- [ ] Answer 14 self-assessment questions

### Day 04 — AI Infrastructure

- [ ] Model serving experiment (startup, memory, latency, throughput)
- [ ] Concurrency experiment (1/5/10/25/50/100 concurrent requests)
- [ ] Model size comparison (memory, latency, throughput, quality)
- [ ] Managed vs self-hosted analysis
- [ ] AI infrastructure diagram
- [ ] Capacity plan
- [ ] Infrastructure decision record
- [ ] Performance test results
- [ ] Answer 18 architect questions

### Day 05 — Data Architecture

- [ ] Working RAG data pipeline (5+ documents, measurements)
- [ ] Chunking experiment (poor, fixed-size, structure-aware; 3 queries; metrics)
- [ ] Security experiment (2 users, 4 permission-filtered queries)
- [ ] Data architecture diagram
- [ ] Data architecture decision record
- [ ] Answer 16 self-assessment questions

### Day 06 — MLOps Platform

- [ ] AI platform architecture diagram
- [ ] AI CI/CD pipeline (all stages documented)
- [ ] Model lifecycle (states, transitions, approvals, rollback)
- [ ] Platform API design (endpoints with request/response)
- [ ] Drift detection design
- [ ] Rollback strategy
- [ ] Platform deliverable checklist (all items)
- [ ] Answer 18 architect questions

### Day 07 — System Architecture

- [ ] System context diagram
- [ ] Logical architecture diagram
- [ ] Data flow diagrams (request path + ingestion path)
- [ ] Deployment architecture diagram
- [ ] Security architecture diagram
- [ ] Three ADRs (Model Strategy, Data/Vector, Managed vs Self-Hosted)
- [ ] Failure matrix (10+ scenarios)
- [ ] Architecture review (all checklists answered)
- [ ] Answer 18 architect questions

### Day 08 — Technology Decisions

- [ ] One completed ADR for model selection

### Day 09 — Scale, Reliability, FinOps

- [ ] Capacity plan for 10x traffic
- [ ] Cost model
- [ ] Reliability plan

### Day 10 — Observability

- [ ] AI production dashboard (5+ infra metrics, 5+ AI metrics, 3+ cost metrics)
- [ ] Alerting matrix (critical, warning, info)

### Day 11 — Security and Governance

- [ ] AI security threat model (risks classified Critical/High/Medium/Low)
- [ ] Governance checklist (mitigation, owner, monitoring, residual risk)

### Day 12 — Business Architecture

- [ ] One-page architecture decision record (complete system)

---

## 6. Sample App Requirements

### Days with Sample Apps

| Day | Components | Key Features |
|-----|-----------|--------------|
| 01 | FastAPI app, config, seed data | Enterprise AI Knowledge Assistant with RAG |
| 02 | Model comparison, routing demo | Model selection and routing strategies |
| 03 | Orchestrator, agents (3), tools (3) | Multi-agent orchestration with tool calling |
| 04 | Inference server, load test, benchmark | GPU inference serving and performance testing |
| 05 | Ingestion, chunker, embeddings, vector DB, retrieval, metadata, auth | Complete RAG pipeline with permissions |
| 06 | Registry, monitoring, experiment, evaluation, deployment, CI/CD | Full MLOps platform |
| 07 | Gateway, RAG, agents, model router, context, observability, security | Complete system architecture |

### Sample App Technical Requirements

- FastAPI as the web framework
- Pydantic for data models
- In-memory storage (simulated for learning)
- Environment-based configuration
- Comprehensive test scripts
- README with architecture diagrams and usage instructions

---

## 7. Architecture Artifact Requirements

### Diagram Types Required

| Type | Folder | Content |
|------|--------|---------|
| Context Diagram | architecture/context-diagram/ | Users, external systems, platform boundary |
| Logical Architecture | architecture/logical-architecture/ | Layered component view |
| Data Flow | architecture/data-flow/ | Request path, ingestion path |
| Deployment Architecture | architecture/deployment-architecture/ | K8s, GPU nodes, services, data stores |
| Security Architecture | architecture/security-architecture/ | Identity, authorization, audit boundaries |

### ADR Requirements

Each ADR must include:

1. **Context** — What is the problem?
2. **Options** — What alternatives exist?
3. **Decision** — What was chosen?
4. **Consequences** — Benefits and costs

Minimum ADRs:

- ADR-001: Model Strategy
- ADR-002: Data/Vector Strategy
- ADR-003: Managed vs Self-Hosted

---

## 8. Portfolio Completion Checklist

### Architecture Artifacts

- [ ] System context diagram
- [ ] Logical architecture diagram
- [ ] Data flow diagrams (request + ingestion)
- [ ] Deployment architecture diagram
- [ ] Security architecture diagram

### Decision Records

- [ ] ADR-001: Model Strategy
- [ ] ADR-002: Data/Vector Strategy
- [ ] ADR-003: Managed vs Self-Hosted
- [ ] Additional ADRs as needed

### Operational Artifacts

- [ ] Cost model (monthly breakdown, cost per request, scaling projections)
- [ ] Capacity plan (traffic, GPU, scaling strategy)
- [ ] Reliability strategy (failure modes, fallbacks, recovery)
- [ ] Observability plan (dashboards, alerts, feedback loops)

### Governance Artifacts

- [ ] Security threat model (classified risks, mitigations)
- [ ] Governance checklist (ownership, monitoring, residual risk)
- [ ] Compliance review

### Business Artifacts

- [ ] Business-value scorecard (cost/task, resolution rate, satisfaction, automation %)
- [ ] One-page architecture decision record (complete system)

---

## 9. Architect Competency Requirements

### Knowledge Domains

| Domain | Competency | Source |
|--------|-----------|--------|
| Architecture | Requirements before technology | Day 01 |
| Architecture | Boundaries, interfaces, controls | Day 07 |
| Architecture | Relationships over components | Day 07 |
| Architecture | ADRs and trade-off documentation | Day 08 |
| AI/ML | Model capabilities and limitations | Day 02 |
| AI/ML | RAG vs fine-tuning decisions | Day 02, 03 |
| AI/ML | Context engineering | Day 03 |
| AI/ML | Agent design and tool security | Day 03, 07 |
| Infrastructure | GPU, Kubernetes, inference serving | Day 04 |
| Infrastructure | Managed vs self-hosted trade-offs | Day 04, 08 |
| Data | Chunking, embeddings, vector retrieval | Day 05 |
| Data | Data governance and freshness | Day 05 |
| Platform | MLOps lifecycle and CI/CD for AI | Day 06 |
| Platform | Evaluation, drift, rollback | Day 06 |
| Reliability | Failure domains, circuit breakers, fallback | Day 07, 09 |
| Cost | Token economics, FinOps, cost modeling | Day 02, 09 |
| Observability | Tracing, metrics, alerting for AI | Day 10 |
| Security | Prompt injection, data leakage, tool auth | Day 11 |
| Business | ROI, business value, portfolio management | Day 12 |

### Core Principle

> An AI Architect does not simply ask "Which model or framework should I use?" The architect asks "What system should we design, why is this the right trade-off, how will it scale, what will it cost, what can fail, how will we govern it, and what business outcome will it produce?"
