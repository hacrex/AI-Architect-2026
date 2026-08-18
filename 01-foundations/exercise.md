# Day 01 — Exercise

**Estimated Time**: 2-3 hours total

| Artifact | Task | Time |
|----------|------|------|
| 0 | Run the sample app | 15 min |
| 1 | Architecture diagram | 45 min |
| 2 | Architecture notes | 45 min |
| 3 | Answer 17 questions | 30-60 min |

---

## Artifact 0 — Run the Sample App

Before designing your own, explore the working implementation.

```bash
cd 01-foundations/sample-app
pip install -r requirements.txt
cp config/.env.example config/.env
# Edit .env with your API key
python seed.py
uvicorn app.main:app --reload --port 8000
```

Test it:
```bash
python test_app.py
```

This gives you a working reference architecture to compare against your own design.

---

## Artifact 1 — Architecture Diagram

---

## Artifact 1 — Architecture Diagram

Create the architecture for the AI Knowledge Assistant.

Use draw.io, Excalidraw, Mermaid, or whatever diagramming tool you prefer.

Your diagram should include:
- Client application (Employee interface)
- Authentication layer
- API Gateway
- AI Application service
- Retrieval layer (embedding + vector search)
- Model Gateway
- Model providers (managed + self-hosted)
- Vector database
- Document storage
- Observability (logging, metrics, tracing)
- Security controls

---

## Artifact 2 — Architecture Notes

Write a one-page document covering:

### Problem
What are we building and why?

### Requirements
- Functional requirements
- Non-functional requirements (latency, availability, scale)
- Security requirements
- Cost constraints

### Components
List each component and its responsibility.

### Data Flow
How does a request flow from user to response?

### Dependencies
What external services does this system depend on?

### Security
- Authentication mechanism
- Authorization model
- Data protection
- Audit logging

### Failure Scenarios
For each critical component, describe:
- What happens when it fails
- How the system degrades
- Recovery strategy

### Scaling Considerations
How does the architecture change as user count grows?

---

## Artifact 3 — Architecture Questions

Answer the 17 questions from the architecture notes.

Don't search for the "correct answer." Think first. That's the point of this exercise.

### Architecture
1. Why do we need an API Gateway?
2. Why should the model be behind a Model Gateway?
3. Where should authentication happen?
4. Where should authorization happen?
5. Where should conversation state live?

### Data
6. Where are documents stored?
7. Where are embeddings stored?
8. How do we handle document updates?
9. How do we handle document deletion?

### Reliability
10. What happens if the LLM provider goes down?
11. What happens if the vector database goes down?
12. What happens if the model takes 30 seconds to respond?

### Security
13. Can every employee access every document?
14. How do we prevent sensitive data from entering prompts?

### Cost
15. What happens when usage increases 100x?
16. How do we control token consumption?

### Business
17. How do we know this system is actually useful?

---

## Deliverable

One architecture diagram + one-page architecture notes + answers to 17 questions.
