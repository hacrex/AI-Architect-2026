# Day 03 — LLM Engineering

> **Building on Day 02**: Yesterday we learned AI/ML fundamentals — transformers, embeddings, vector databases, RAG concepts, model routing, and cost models. Today we move from understanding the model to designing systems around the model.

An AI Architect doesn't just understand models. An AI Architect understands how to turn a model into a useful, reliable, controllable production system.

Today, we build the application layer that sits between the user and the model.

---

## Table of Contents

1. [From LLM to AI Application](#1-from-llm-to-ai-application)
2. [The Six Core Building Blocks](#2-the-six-core-building-blocks)
3. [RAG — Retrieval-Augmented Generation](#3-rag--retrieval-augmented-generation)
4. [RAG Is More Than a Vector Database](#4-rag-is-more-than-a-vector-database)
5. [Retrieval](#5-retrieval)
6. [RAG and Access Control](#6-rag-and-access-control)
7. [Context Engineering](#7-context-engineering)
8. [The Context Assembly Layer](#8-the-context-assembly-layer)
9. [Tool Calling](#9-tool-calling)
10. [Tool Calling Creates New Risks](#10-tool-calling-creates-new-risks)
11. [Agents](#11-agents)
12. [Do We Always Need Multi-Agent Systems?](#12-do-we-always-need-multi-agent-systems)
13. [Agent State](#13-agent-state)
14. [Memory](#14-memory)
15. [Model Routing](#15-model-routing)
16. [Batch vs Real-Time AI](#16-batch-vs-real-time-ai)
17. [The AI Gateway](#17-the-ai-gateway)
18. [Provider Abstraction](#18-provider-abstraction)
19. [Today's Architecture](#19-todays-architecture)
20. [Day 03 Hands-On Exercise](#20-day-03-hands-on-exercise)
21. [Day 03 Architecture Questions](#21-day-03-architecture-questions)
22. [Day 03 Deliverables](#22-day-03-deliverables)
23. [Key Takeaways](#23-key-takeaways)

> **Sample App**: See `sample-app/` for a working multi-agent orchestration implementation.

## The Goal of Day 03

You do not need to become a prompt engineer or master every agent framework.

You need to understand:

- How to turn an LLM into a production system
- The six core building blocks of LLM applications
- Why RAG is more than a vector database
- How context engineering affects answer quality
- Why tool calling creates new security boundaries
- When multi-agent architecture adds value vs complexity
- How to design an AI Gateway for provider abstraction

---

## Objective

Learn the architecture patterns behind production LLM applications — moving from understanding the model to designing systems around the model.

## 1. From LLM to AI Application

A common beginner architecture:

```
User → Prompt → LLM → Answer
```

It works for a demo. But enterprise applications quickly become:

```
                         ┌───────────────┐
                         │   User/App    │
                         └───────┬───────┘
                                 ↓
                         ┌───────────────┐
                         │  API Gateway  │
                         └───────┬───────┘
                                 ↓
                       ┌───────────────────┐
                       │  AI Application   │
                       └─────────┬─────────┘
                                 ↓
                    ┌────────────┼────────────┐
                    ↓            ↓            ↓
                  RAG          Agents       Tools
                    ↓            ↓            ↓
               Vector DB       State       APIs
                    │            │            │
                    └────────────┼────────────┘
                                 ↓
                         ┌───────────────┐
                         │ Model Gateway │
                         └───────┬───────┘
                                 ↓
                       ┌──────────────────┐
                       │ Models / LLMs    │
                       └──────────────────┘
```

Now we're doing LLM Engineering.

## 2. The Six Core Building Blocks

Today, concentrate on six things:

1. **RAG** — Retrieval-Augmented Generation
2. **Context Engineering** — Right information in the right order
3. **Tool Calling** — Let the model take actions
4. **Agents** — Reasoning through tasks with tools
5. **Memory and State** — Retaining information across interactions
6. **Model Routing** — Directing requests to the right model

These components can be combined in different ways depending on the workload.

## 3. RAG — Retrieval-Augmented Generation

The most important pattern for enterprise AI.

Imagine your company has:

- 10,000 PDFs
- 5,000 Wiki pages
- 2,000 policies
- 1,000 technical documents

You can't expect the model to magically know all of them.

Instead, build an ingestion pipeline:

```
Documents → Chunking → Embeddings → Vector Store
```

Then when the user asks something:

```
User Question → Query Embedding → Retriever → Relevant Documents
             → Context → LLM → Answer
```

That's RAG.

## 4. RAG Is More Than a Vector Database

This is an important architect-level distinction.

A simplistic RAG architecture:

```
Documents → Vector DB → LLM
```

A production architecture:

```
                  Documents
                     ↓
              Ingestion Pipeline
                     ↓
               Processing/OCR
                     ↓
                  Chunking
                     ↓
                Embeddings
                     ↓
              ┌─────────────┐
              │ Vector DB   │
              └──────┬──────┘
                     │
User → Query → Retrieval → Reranking
                         ↓
                   Context Builder
                         ↓
                        LLM
                         ↓
                    Validation
                         ↓
                      Answer
```

Every stage creates architectural decisions.

## 5. Retrieval

Suppose the user asks:

> "What is our Kubernetes security policy?"

The retriever shouldn't return 500 random documents. It should identify the most relevant information.

Possible pipeline:

```
Query → Query Understanding → Semantic Search → Metadata Filtering
     → Hybrid Search → Reranking → Top-K Documents
```

**Architectural questions:**

- How many documents should we retrieve?
- Should keyword search be combined with semantic search?
- Do we need reranking?
- How do we filter by user permissions?
- How fresh must the information be?

## 6. RAG and Access Control

One of the most important production considerations.

Imagine:

- Employee A → Finance documents only
- Employee B → Engineering documents only
- Admin → All documents

Your vector database cannot simply return the most semantically similar document. It must also respect authorization.

Safer conceptual flow:

```
User → Identity → Authorization Context → Query → Retrieval
     → Permission Filtering → Relevant Documents → LLM
```

Without this, you could build a technically excellent RAG system that leaks confidential information.

This is where AI architecture meets security architecture.

## 7. Context Engineering

An LLM doesn't need every piece of information you have. It needs the right information.

```
Too Little Context → Poor Answer
Too Much Context → Noise + Cost + Latency
Right Context → Better Answer
```

Context engineering is about deciding:

- What information enters the context
- In what order
- How much information enters
- What should be excluded
- How conversation history is managed
- How tool results are represented
- How retrieved information is prioritized

## 8. The Context Assembly Layer

A useful architecture pattern:

```
                    User Query
                         ↓
              ┌────────────────────┐
              │ Context Assembly    │
              └─────────┬──────────┘
                        │
        ┌───────────────┼────────────────┐
        ↓               ↓                ↓
 Conversation       Retrieved         Tool
   History          Knowledge          Results
        │               │                │
        └───────────────┼────────────────┘
                        ↓
                 Context Window
                        ↓
                       LLM
```

This layer becomes extremely important as AI applications become more sophisticated.

## 9. Tool Calling

An LLM normally generates text. But enterprise applications need actions.

Example: "Check my AWS server status."

The model cannot inspect AWS. It needs a tool.

```
User → LLM → Tool Selection → AWS API → Tool Result → LLM → Answer
```

Another example: "Create a Jira ticket for this incident."

```
User → Agent → Jira Tool → Jira API → Result → Agent → User
```

Now your LLM has moved from generating text to interacting with systems.

## 10. Tool Calling Creates New Risks

This is where architects need to become careful.

Suppose an agent has:

- AWS Tool
- Database Tool
- Email Tool
- Jira Tool
- Production Deployment Tool

What happens if the model makes the wrong decision? What if a malicious prompt tricks it?

Tools need:

- **Authentication** — Verify who is calling
- **Authorization** — Verify what they can do
- **Least privilege** — Minimum required permissions
- **Validation** — Verify inputs before execution
- **Approval workflows** — Human review for sensitive actions
- **Audit logging** — Record every invocation
- **Rate limits** — Prevent abuse
- **Safe defaults** — Deny by default

The more powerful the tool, the more important the control plane becomes.

## 11. Agents

An agent is an AI system capable of reasoning through a task and interacting with tools or other components.

```
Goal → Agent → Reason/Decide → Tool → Observe Result
     → Reason Again → Next Action → Final Result
```

A simple agent:

```
User → Agent → Search Tool → Answer
```

A more complex agent:

```
                   Orchestrator
                  /      |      \
                 /       |       \
                ↓        ↓        ↓
           Research   Database   Security
             Agent      Agent      Agent
                \        |        /
                 \       |       /
                  Shared State
```

This is where multi-agent architecture begins.

## 12. Do We Always Need Multi-Agent Systems?

No. This is another important architecture decision.

Sometimes:

```
User → LLM → Tool → Answer
```

is enough.

Don't build:

```
10 Agents → 5 Orchestrators → 20 Tools → Multiple Models
```

just because the architecture looks impressive.

More agents mean:

- More latency
- More failure points
- More state
- More cost
- More debugging
- More security complexity

**The architect's question:** Does the additional complexity produce enough value?

## 13. Agent State

Agents need state. Consider:

> User: "Find the latest incident."
> Agent: "Found INC-1024."
> User: "Who fixed it?"

The agent needs to understand what "it" refers to. That requires state.

```
Conversation → State Store → Agent → Tools
```

State may contain:

- Conversation history
- Task progress
- Tool results
- Intermediate decisions
- User preferences
- Workflow status

This becomes important when agents run for a long time.

## 14. Memory

Don't confuse memory with context.

| Context | Memory |
|---------|--------|
| Information currently provided to the model | Information retained across interactions or tasks |
| Current conversation | User preferences, previous projects, workflow state |

Architecturally:

```
                 Agent
                   │
        ┌──────────┴──────────┐
        ↓                     ↓
   Short-term             Long-term
     State                  Memory
        ↓                     ↓
   Current Task          Persistent Store
```

Memory architecture needs careful consideration around:

- Privacy
- Retention
- Deletion
- User isolation
- Correctness

## 15. Model Routing

We introduced this yesterday. Today, connect it with LLM applications.

Instead of:

```
Application → One LLM
```

Use:

```
Application → Model Gateway → Request Classification
                              │
                    ┌─────────┼─────────┐
                    ↓         ↓         ↓
                  Small    Medium     Large
                    ↓         ↓         ↓
                   Fast    Balanced  Powerful
```

Routing can consider:

- Request complexity
- Cost
- Latency
- Data sensitivity
- Availability
- Model capability

This becomes extremely powerful at scale.

## 16. Batch vs Real-Time AI

Not every AI workload needs immediate responses.

**Real-time:**

```
Customer Question → LLM → Response
```

Latency matters.

**Batch:**

```
1M Documents → Queue → Workers → LLM → Results
```

Throughput and cost may matter more than individual response latency.

This is an architectural decision.

## 17. The AI Gateway

Now let's bring everything together.

```
                         Users
                           │
                           ▼
                    ┌─────────────┐
                    │ API Gateway │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ AI Gateway  │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ↓            ↓            ↓
           RAG          Agents       Routing
              │            │            │
              ↓            ↓            ↓
          Retrieval       Tools       Models
              │            │            │
              └────────────┼────────────┘
                           ↓
                    Context Assembly
                           ↓
                         LLMs
```

The AI Gateway can become the control point for:

- Model routing
- Authentication
- Rate limiting
- Token tracking
- Logging
- Policy enforcement
- Fallback
- Provider abstraction

## 18. Provider Abstraction

Don't tightly couple your entire application to one model provider.

Instead:

```
Application → AI Interface → Model Gateway
                              │
                    ┌─────────┼─────────┐
                    ↓         ↓         ↓
                   LLM1     LLM2     LLM3
```

If pricing changes, latency increases, a provider has an outage, or another model becomes better — you can change the backend without redesigning the entire application.

This is loose coupling in practice.

## 19. Today's Architecture

Let's evolve our Enterprise AI Knowledge Assistant.

**Day 01:**

```
User → Application → API Gateway → RAG → Vector DB → LLM
```

**Day 02:**

Added:

```
Model Gateway → Multiple Models
```

**Day 03:**

```
                           User
                            │
                            ▼
                     ┌─────────────┐
                     │ API Gateway │
                     └──────┬──────┘
                            │
                            ▼
                     ┌─────────────┐
                     │ AI Gateway  │
                     └──────┬──────┘
                            │
              ┌─────────────┼─────────────┐
              ↓             ↓             ↓
             RAG          Agent          Router
              │             │             │
              ↓             ↓             ↓
         Retriever        Tools        Models
              │             │             │
              ↓             ↓             │
          Vector DB       APIs             │
              │             │              │
              └─────────────┼──────────────┘
                            ↓
                    Context Assembly
                            ↓
                     Model Gateway
                            ↓
                  ┌─────────┼─────────┐
                  ↓         ↓         ↓
               Small      Medium     Large
```

Now we have something that looks much closer to a real AI platform.

## 20. Day 03 Hands-On Exercise

Extend the project you started on Day 1.

**Build a RAG pipeline:**

```
Documents → Chunking → Embeddings → Vector DB → Retriever
         → Context → LLM → Answer
```

**Then add:**

- **Tool** — Create one tool the AI can call (e.g., `get_server_status()`, `search_internal_docs()`, `get_weather()`)
- **Model Gateway** — Add a simple `generate()` abstraction instead of calling a specific provider directly everywhere

## 21. Day 03 Architecture Questions

Before finishing today, answer these:

### RAG
1. When should you use RAG?
2. When should you use fine-tuning?
3. Why is retrieval quality important?
4. Why is metadata filtering important?
5. Why must RAG respect authorization?

### Context and Tools
6. What is context engineering?
7. What is tool calling?
8. Why are tools a security boundary?

### Agents
9. When does an application actually need an agent?
10. When does multi-agent architecture make sense?

### State and Memory
11. What is the difference between context and memory?

### Processing
12. When should AI processing be asynchronous?

### Architecture
13. Why do we need an AI Gateway?
14. Why should applications avoid tight coupling to one model provider?
15. What happens if your primary model provider becomes unavailable?

## 22. Day 03 Deliverables

By the end of today, you should have:

### Architecture

- RAG Architecture Diagram

### Implementation

- Working RAG prototype
- One tool-enabled AI workflow

### Design

- AI Gateway / Model Gateway abstraction

### Documentation

Write a short decision document:

> "Why did I choose RAG, and what would make me replace or extend it with another architecture?"

## 23. Key Takeaways

```
┌─────────────────────────────────────────────────────────────────┐
│                     DAY 03 KEY TAKEAWAYS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. An LLM alone is not an AI application                       │
│                                                                 │
│  2. Six core building blocks: RAG, Context, Tools, Agents,     │
│     Memory, Model Routing                                       │
│                                                                 │
│  3. RAG is more than a vector database — production RAG has    │
│     ingestion, retrieval, reranking, permission filtering       │
│                                                                 │
│  4. Context engineering = right info, right order, right amount │
│                                                                 │
│  5. Tools are a security boundary — they need auth, least      │
│     privilege, validation, audit logging                        │
│                                                                 │
│  6. Multi-agent adds complexity — only use when value justifies│
│                                                                 │
│  7. AI Gateway = control point for routing, auth, rate limiting│
│     token tracking, fallback, provider abstraction              │
│                                                                 │
│  8. Provider abstraction = loose coupling = flexibility         │
│                                                                 │
│  9. Don't leave thinking "I learned RAG and agents." Leave     │
│     understanding how they become architectural components.     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

> **Next**: See Day 04 (`04-ai-infrastructure/`) to understand the infrastructure that makes these patterns production-ready.
