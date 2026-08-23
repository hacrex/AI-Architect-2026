# MLOps — Exercise

## Task

Design an internal AI platform for 20 engineering teams.

Teams should be able to:

- register models
- run evaluations
- deploy models
- expose APIs
- monitor workloads
- roll back deployments

---

## Exercise 1: AI Platform Architecture

Design a complete AI platform architecture for the Enterprise AI Knowledge Assistant.

### Requirements

The platform must support:

1. **Developer Experience**
   - Self-service portal or CLI
   - Templates for common patterns (RAG, Agent, Inference)
   - SDK for integration

2. **Control Plane**
   - Model registry with versioning
   - Evaluation pipeline with quality gates
   - Deployment management (staging, canary, production)
   - Governance and access control

3. **Data Plane**
   - RAG pipeline
   - Agent orchestration
   - Inference serving
   - Vector database

4. **Infrastructure**
   - Kubernetes + GPU
   - Observability stack
   - Secrets management

### Deliverable

Create a platform architecture diagram showing:

```
Developer → Portal → Control Plane → Data Plane → Infrastructure
```

Include all components and their relationships.

---

## Exercise 2: AI CI/CD Pipeline

Design a CI/CD pipeline for AI applications.

### Pipeline Stages

```
Git Push
  │
  ▼
Build
  │
  ▼
Unit Tests
  │
  ▼
Integration Tests
  │
  ▼
Security Scan
  │
  ▼
AI Evaluation
  │
  ├── Quality Gate
  ├── Safety Gate
  ├── Cost Gate
  └── Latency Gate
  │
  ▼
Registry
  │
  ▼
Staging
  │
  ▼
Canary (5% → 25% → 50% → 100%)
  │
  ▼
Production
  │
  ▼
Monitoring
```

### Deliverable

Document each stage with:

- What happens
- What tools are used
- What gates must pass
- What happens on failure

---

## Exercise 3: Model Lifecycle

Design the complete lifecycle for a model from experiment to production.

### Stages

1. **Experiment**
   - Dataset version
   - Model configuration
   - Prompt template
   - Parameters

2. **Evaluate**
   - Quality metrics
   - Safety metrics
   - Cost metrics
   - Latency metrics

3. **Register**
   - Version
   - Source
   - Evaluation results
   - Approval status

4. **Deploy**
   - Staging
   - Canary
   - Production

5. **Monitor**
   - Drift detection
   - Quality monitoring
   - Cost tracking
   - Usage analytics

6. **Improve**
   - Feedback loop
   - Retraining triggers
   - Prompt optimization

### Deliverable

Create a visual lifecycle diagram with:

- States and transitions
- Approval gates
- Feedback loops
- Rollback paths

---

## Exercise 4: Platform API Design

Design a conceptual API for the AI platform.

### Endpoints to Design

```yaml
# Application Management
POST   /api/v1/applications
GET    /api/v1/applications
GET    /api/v1/applications/{id}
DELETE /api/v1/applications/{id}

# Model Registry
POST   /api/v1/models
GET    /api/v1/models
GET    /api/v1/models/{id}
POST   /api/v1/models/{id}/promote
POST   /api/v1/models/{id}/rollback

# Deployment
POST   /api/v1/deployments
GET    /api/v1/deployments
GET    /api/v1/deployments/{id}
PUT    /api/v1/deployments/{id}
DELETE /api/v1/deployments/{id}

# Evaluation
POST   /api/v1/evaluations
GET    /api/v1/evaluations
GET    /api/v1/evaluations/{id}

# Observability
GET    /api/v1/metrics
GET    /api/v1/traces
GET    /api/v1/alerts
```

### Deliverable

For each endpoint, define:

- Request body
- Response body
- Status codes
- Error handling

---

## Exercise 5: Drift Detection Design

Design a drift detection system for the Enterprise AI Knowledge Assistant.

### Drift Types to Detect

1. **Data Drift**
   - Input distribution changes
   - Document corpus changes
   - User query patterns

2. **Model Drift**
   - Output quality degradation
   - Response time changes
   - Token usage changes

3. **Concept Drift**
   - Accuracy changes over time
   - Relevance changes
   - Safety score changes

### Detection Strategy

Design:

- Monitoring metrics
- Alert thresholds
- Automated response
- Human review triggers

### Deliverable

Create a drift detection plan with:

- Metrics to monitor
- Thresholds
- Alerting rules
- Response actions

---

## Exercise 6: Rollback Strategy

Design a rollback strategy for AI deployments.

### Scenarios

1. **Bad Model Deployment**
   - Quality dropped below threshold
   - Safety violation detected
   - Latency spike

2. **Bad Prompt Change**
   - Answer quality degraded
   - Hallucinations increased
   - User complaints

3. **Bad Data Update**
   - Retrieval quality dropped
   - Outdated information
   - Incorrect answers

### Rollback Process

Design:

- Detection mechanism
- Decision process
- Execution steps
- Verification
- Communication

### Deliverable

Create a rollback runbook with:

- Triggers
- Steps
- Verification
- Post-mortem process

---

## Platform Deliverable Checklist

Create these artifacts:

### 1. AI Platform Architecture

- [ ] Developer experience layer
- [ ] Control plane
- [ ] Data plane
- [ ] Model registry
- [ ] Evaluation platform
- [ ] Deployment system
- [ ] Infrastructure

### 2. AI CI/CD Pipeline

- [ ] Build stage
- [ ] Test stage
- [ ] Security scan
- [ ] AI evaluation
- [ ] Quality gates
- [ ] Registry
- [ ] Staging
- [ ] Canary deployment
- [ ] Production
- [ ] Monitoring

### 3. Model Lifecycle

- [ ] Experiment tracking
- [ ] Evaluation pipeline
- [ ] Model registry
- [ ] Approval workflow
- [ ] Deployment strategy
- [ ] Monitoring system
- [ ] Feedback loop

### 4. Platform API

- [ ] Application endpoints
- [ ] Model registry endpoints
- [ ] Deployment endpoints
- [ ] Evaluation endpoints
- [ ] Observability endpoints
- [ ] Error handling

### 5. Operations

- [ ] Drift detection
- [ ] Rollback strategy
- [ ] Incident response
- [ ] Post-mortem process

---

## Architect Questions

Answer these questions before moving on:

1. What problem does MLOps solve?
2. How does MLOps differ from traditional DevOps?
3. What additional concerns appear with LLM applications?
4. Why do organizations need an AI platform?
5. What belongs in a model registry?
6. Why is evaluation part of deployment?
7. How can an AI system degrade without code changes?
8. What is model drift?
9. What is data drift?
10. Why use canary deployment for models?
11. What is shadow deployment?
12. What should an AI CI/CD pipeline validate?
13. What is the difference between an AI control plane and data plane?
14. What should developers manage themselves?
15. What should the platform abstract away?
16. How would you support both traditional ML and GenAI?
17. How would you roll back a bad model?
18. How would you know a model is becoming worse in production?

---

## Success Criteria

Your exercise is complete when you can:

1. Explain the full AI platform architecture
2. Design a CI/CD pipeline for AI applications
3. Define the model lifecycle from experiment to production
4. Design platform APIs
5. Implement drift detection
6. Handle rollbacks
7. Answer all architect questions

---

## Next Steps

After completing Day 06, move to:

**Day 07 → AI System Architecture**

How do all these layers become one coherent AI system architecture?
