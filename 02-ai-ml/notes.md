# Day 02 → AI/ML & LLM Fundamentals

> **Building on Day 01**: Yesterday we established the architect mindset — thinking about complete systems, failure domains, and loose coupling. Today we go one layer deeper into AI/ML fundamentals that directly influence architecture decisions.

An AI Architect doesn't just build components. An AI Architect understands the complete system and makes decisions about how those components should work together.

Today, we go one layer deeper.

---

## Table of Contents

1. [Start With the AI Landscape](#1-start-with-the-ai-landscape)
2. [AI vs ML vs Deep Learning vs Generative AI](#2-ai-vs-ml-vs-deep-learning-vs-generative-ai)
3. [The Architect's First Decision](#3-the-architects-first-decision)
4. [Machine Learning Fundamentals You Need](#4-machine-learning-fundamentals-you-need)
5. [Training vs Inference](#5-training-vs-inference)
6. [What Is a Model?](#6-what-is-a-model)
7. [Why Model Size Matters to Architects](#7-why-model-size-matters-to-architects)
8. [Transformers](#8-transformers)
9. [Tokens](#9-tokens)
10. [Context Window](#10-context-window)
11. [Embeddings](#11-embeddings)
12. [Vector Databases](#12-vector-databases)
13. [Attention](#13-attention)
14. [Inference](#14-inference)
15. [Model Evaluation](#15-model-evaluation)
16. [RAG vs Fine-Tuning](#16-rag-vs-fine-tuning)
17. [Managed vs Open-Weight Models](#17-managed-vs-open-weight-models)
18. [Your AI Architecture Decision Framework](#18-your-ai-architecture-decision-framework)
19. [Day 02 Architecture Exercise](#19-day-02-architecture-exercise)
20. [Day 02 Hands-On Lab](#20-day-02-hands-on-lab)
21. [Day 02 Deliverables](#21-day-02-deliverables)
22. [Architect Questions for Day 02](#22-architect-questions-for-day-02)
23. [Key Takeaways](#23-key-takeaways)

> **Sample App**: See `sample-app/` for a working model comparison and routing demo.

## The Goal of Day 02

You do not need to become an ML researcher.

You need enough understanding of AI/ML and LLMs to make architecture-level decisions.

For example:

- Should we use an LLM at all?
- Should we use a smaller model?
- RAG or fine-tuning?
- Managed model or self-hosted?
- Which model fits our latency requirements?
- How much context do we need?
- Why is inference becoming expensive?
- Why does GPU memory matter?
- Why does model size affect architecture?
- What happens when the context window becomes large?

The uploaded roadmap makes this distinction explicitly: the architect needs enough LLM knowledge to judge feasibility, cost, and likely failure points rather than necessarily implementing a transformer from scratch.

---

## 1. Start With the AI Landscape

Before LLMs, understand where they sit in the larger AI ecosystem.

```
Artificial Intelligence
│
├── Machine Learning
│   │
│   ├── Supervised Learning
│   ├── Unsupervised Learning
│   └── Reinforcement Learning
│
└── Deep Learning
    │
    ├── Computer Vision
    ├── Speech
    ├── NLP
    └── Generative AI
         │
         ├── Text Models
         ├── Image Models
         ├── Audio Models
         └── Multimodal Models
              │
              └── Foundation Models
                    │
                    └── LLMs
```

This matters architecturally because not every AI problem requires an LLM.

---

## 2. AI vs ML vs Deep Learning vs Generative AI

These terms are often mixed together.

### Artificial Intelligence

The broadest concept.

AI refers to systems capable of performing tasks that normally require some form of human intelligence.

Examples:

- reasoning
- perception
- planning
- classification
- language understanding

### Machine Learning

Instead of explicitly programming every rule, the system learns patterns from data.

For example:

```
Historical transactions
        ↓
       ML
        ↓
Fraud probability
```

### Deep Learning

Machine learning using neural networks with many layers.

Deep learning powers:

- image recognition
- speech recognition
- language models
- recommendation systems
- autonomous systems

### Generative AI

Models that generate new content.

Examples:

- text
- images
- audio
- video
- code

LLMs are one category of generative AI.

---

## 3. The Architect's First Decision

Before choosing an LLM:

**Do we actually need an LLM?**

Imagine a company wants:

"Calculate employee leave balance."

You don't need an LLM.

A deterministic system is better:

```
Employee ID
     ↓
HR Database
     ↓
Leave Calculation
     ↓
Answer
```

Now consider:

"Explain our leave policy in simple language."

An LLM may be useful.

Now:

"Answer questions about 50,000 internal documents."

You might need:

```
LLM + RAG
```

This gives us a fundamental architecture principle:

> Use the simplest technology that satisfies the requirements.

---

## 4. Machine Learning Fundamentals You Need

You don't need every ML algorithm.

Understand the basic lifecycle.

```
Data
 ↓
Preprocessing
 ↓
Training
 ↓
Validation
 ↓
Evaluation
 ↓
Deployment
 ↓
Inference
 ↓
Monitoring
```

The architect needs to understand where infrastructure and operational requirements appear at each stage.

---

## 5. Training vs Inference

This is critical.

### Training

The model learns from data.

```
Dataset
   ↓
GPU Cluster
   ↓
Training
   ↓
Model
```

Training can require:

- large datasets
- GPUs
- distributed compute
- significant storage
- long-running workloads

### Inference

The trained model is used to generate predictions.

```
User Request
     ↓
Model
     ↓
Prediction
```

For LLM applications:

```
Prompt
  ↓
LLM Inference
  ↓
Generated Tokens
```

Architecture requirements can be very different.

Training may prioritize:

- compute throughput

Inference may prioritize:

- latency + concurrency + cost

---

## 6. What Is a Model?

At a simplified level, a model is a mathematical system containing learned parameters.

For an LLM:

```
Training Data
     ↓
Training Process
     ↓
Parameters
     ↓
Foundation Model
```

When you hear:

- 7B
- 8B
- 70B
- 405B

the number broadly refers to the scale of model parameters.

Larger models generally require substantially more resources, although model quality is not determined by parameter count alone.

This immediately creates an architectural question:

> Do I really need the largest model available?

---

## 7. Why Model Size Matters to Architects

Imagine two models:

| Model A | Model B |
|---------|---------|
| 8B parameters | 70B parameters |

The larger model may offer stronger capabilities for certain workloads.

But it can also mean:

- more GPU memory
- greater infrastructure requirements
- potentially higher latency
- higher inference cost
- more complicated scaling

Therefore:

```
Model Capability
        ↕
Infrastructure Cost
        ↕
Latency
        ↕
Quality
```

Architecture is about finding the right point in that trade-off.

---

## 8. Transformers

This is the most important architecture concept behind modern LLMs.

You don't need to derive the mathematics.

You need to understand the conceptual pipeline.

```
Text
 ↓
Tokens
 ↓
Embeddings
 ↓
Transformer
 ↓
Attention
 ↓
Next-token prediction
 ↓
Generated text
```

The transformer architecture introduced a highly scalable approach to processing sequences using attention mechanisms.

For an AI Architect, three concepts are particularly important:

1. Tokens
2. Embeddings
3. Attention

---

## 9. Tokens

LLMs don't directly see human sentences.

They process tokens.

For example, a sentence might conceptually become:

```
"AI architecture is interesting"

↓

[AI] [architecture] [is] [interesting]
```

Actual tokenization can split words differently depending on the tokenizer.

Why does this matter?

Because tokens affect:

- context size
- inference cost
- latency
- API pricing
- memory requirements

This is why token economics becomes an architectural concern.

---

## 10. Context Window

An LLM doesn't have unlimited working context.

A simplified representation:

```
┌─────────────────────────────┐
│       Context Window        │
│                             │
│ System Instructions         │
│ Conversation                │
│ Retrieved Documents         │
│ Tool Results                │
│ User Prompt                 │
│                             │
└─────────────────────────────┘
              ↓
             LLM
```

The context window affects architecture.

Suppose your RAG system retrieves 100 documents.

You cannot blindly send everything to the model.

You may need:

```
Query
 ↓
Retrieval
 ↓
Filtering
 ↓
Reranking
 ↓
Context Selection
 ↓
LLM
```

This is one reason RAG architecture is more than "put documents into a vector database."

---

## 11. Embeddings

Embeddings convert information into numerical representations.

Conceptually:

```
"Cloud infrastructure"
        ↓
[0.13, -0.72, 0.44, ...]
```

The numbers represent semantic characteristics in a high-dimensional space.

This enables similarity search.

For example:

```
Query:
"How do I deploy Kubernetes?"

              ↓
           Embedding
              ↓
       Vector Similarity
              ↓
 ┌────────────────────────┐
 │ Kubernetes Deployment  │
 │ Container Deployment   │
 │ K8s Infrastructure     │
 └────────────────────────┘
```

This is fundamental to RAG systems.

---

## 12. Vector Databases

The vector database stores embeddings and supports similarity search.

Conceptually:

```
Documents
    ↓
Embedding Model
    ↓
Vectors
    ↓
Vector Database
```

At query time:

```
User Query
    ↓
Query Embedding
    ↓
Similarity Search
    ↓
Relevant Documents
    ↓
LLM
```

Architectural decisions include:

- indexing strategy
- metadata filtering
- scale
- latency
- persistence
- availability
- security
- cost

Examples include:

- PostgreSQL + pgvector
- Qdrant
- Milvus
- Weaviate
- Pinecone

Don't memorize which one is "best."

Learn how to choose.

---

## 13. Attention

Attention is one of the fundamental mechanisms behind transformers.

Conceptually, it allows the model to determine which parts of the input are more relevant when processing another part.

Consider:

"The engineer deployed the model because it was performing well."

The model needs to understand relationships between words and concepts.

At a high level:

```
Tokens
  ↓
Relationships
  ↓
Attention
  ↓
Contextual Representation
```

For architecture purposes, understand the consequence:

Transformers rely heavily on computational resources to process context.

As context and workload increase, inference architecture becomes increasingly important.

---

## 14. Inference

This is where your Cloud/Platform background becomes extremely useful.

Imagine:

```
100 requests/sec
       ↓
LLM
       ↓
Generated tokens
```

Now increase it:

```
1,000 requests/sec
       ↓
LLM
       ↓
GPU Cluster
```

Now the architect must think about:

- GPU utilization
- batching
- concurrency
- memory
- latency
- autoscaling
- queueing
- load balancing

This is why AI infrastructure eventually becomes a distributed systems problem with GPUs added to the equation.

---

## 15. Model Evaluation

A model isn't good simply because its answers sound impressive.

You need to evaluate it.

Potential dimensions:

- Quality
- Accuracy
- Groundedness
- Relevance
- Latency
- Cost
- Safety
- Consistency

For a RAG application, for example:

```
Retrieval Quality
       +
Context Quality
       +
Answer Quality
       +
Groundedness
```

This becomes extremely important later when we design observability and evaluation systems.

---

## 16. RAG vs Fine-Tuning

This is one of the most important architecture decisions.

### RAG

Use external information at query time.

```
Documents
 ↓
Embeddings
 ↓
Vector DB
 ↓
Retrieval
 ↓
Context
 ↓
LLM
```

Useful when knowledge changes frequently.

### Fine-Tuning

Modify model behavior by training it further on a dataset.

Conceptually:

```
Base Model
    +
Training Data
    ↓
Fine-Tuned Model
```

Useful for certain behavior, style, task specialization, or domain adaptation scenarios.

But don't automatically fine-tune because you have domain-specific information.

Ask:

> Is the problem knowledge retrieval or model behavior?

If the problem is:

"The model doesn't know our latest company policies."

RAG may be appropriate.

If the problem is:

"The model needs to consistently follow a specialized output behavior."

Fine-tuning may be worth evaluating.

---

## 17. Managed vs Open-Weight Models

This is another architect-level decision.

### Managed

```
Application
    ↓
API
    ↓
Model Provider
```

Advantages:

- low infrastructure burden
- rapid adoption
- easy scaling

Considerations:

- per-token cost
- provider dependency
- privacy requirements
- rate limits
- vendor lock-in

### Self-hosted

```
Application
    ↓
Inference Gateway
    ↓
Kubernetes
    ↓
GPU
    ↓
Open-Weight Model
```

Advantages:

- more control
- data locality
- customization
- potential economics at sufficient scale

Considerations:

- GPU infrastructure
- operations
- updates
- scaling
- security
- maintenance

There is no universal winner.

The correct answer depends on requirements and constraints. This is exactly the technology-selection mindset emphasized in the uploaded roadmap.

---

## 18. Your AI Architecture Decision Framework

When evaluating a model, use this:

```
                 Model Decision
                       │
       ┌───────────────┼───────────────┐
       ↓               ↓               ↓
    Quality         Latency           Cost
       │               │               │
       └───────────────┼───────────────┘
                       ↓
                    Privacy
                       ↓
                   Security
                       ↓
                Infrastructure
                       ↓
                 Vendor Lock-in
                       ↓
                Team Capability
                       ↓
                Long-term Fit
```

Don't ask:

"Which model is trending?"

Ask:

"Which model best satisfies the workload requirements?"

---

## 19. Day 02 Architecture Exercise

Let's return to yesterday's project:

### Enterprise AI Knowledge Assistant

Yesterday:

```
Employee
   ↓
Application
   ↓
API Gateway
   ↓
AI Assistant
   ↓
RAG
   ↓
Vector DB
   ↓
LLM
```

Today, make the architecture more intelligent.

Add:

```
                Model Gateway
                     │
          ┌──────────┼──────────┐
          ↓          ↓          ↓
      Model A     Model B    Model C
     High Quality Balanced   Low Cost
```

Now define routing rules.

For example:

Complex request → Model A

Normal request → Model B

Simple request → Model C

This introduces **model routing**.

And now you've moved from:

"We use an LLM."

to:

"We have an AI model strategy."

That is architectural thinking.

---

## 20. Day 02 Hands-On Lab

Today, build a small experiment.

### Experiment A

Use one LLM.

Send:

- simple question
- complex question
- long-context question

Record:

- response quality
- latency
- token usage

### Experiment B

Use a second model.

Compare:

| Metric | Model A | Model B |
|--------|---------|---------|
| Quality | | |
| Latency | | |
| Input tokens | | |
| Output tokens | | |
| Cost | | |
| Context handling | | |

Don't worry about getting scientifically perfect results.

The objective is to start thinking in architecture trade-offs.

---

## 21. Day 02 Deliverables

By the end of today, create:

### 1. Model Comparison

At least two models.

### 2. Architecture Decision

Answer:

Which model would you choose for the Enterprise AI Knowledge Assistant and why?

### 3. Model Routing Diagram

```
User
 ↓
AI Gateway
 ↓
Request Classification
 ↓
┌──────────────┬───────────────┐
↓              ↓               ↓
Simple       Normal         Complex
↓              ↓               ↓
Small LLM    Mid LLM       Powerful LLM
```

### 4. One-page Notes

Explain:

- tokens
- embeddings
- context window
- transformers
- inference
- RAG
- fine-tuning
- model routing

---

## 22. Architect Questions for Day 02

Before finishing today, answer these without searching:

1. Why don't all AI applications need an LLM?
2. What is the difference between training and inference?
3. Why do tokens matter for cost?
4. Why does context length matter?
5. What are embeddings?
6. Why do we need vector search?
7. RAG vs fine-tuning: when would you choose each?
8. Why might a smaller model be preferable?
9. When would you self-host an open-weight model?
10. When would you use a managed model?
11. What happens to architecture when inference traffic increases 10x?
12. Why should an enterprise consider a model gateway?

---

## The Most Important Lesson Today

Don't leave Day 02 thinking:

"I learned how LLMs work."

Leave thinking:

"I now understand how model behavior and model characteristics influence system architecture."

That's the difference.

---

## 23. Key Takeaways

```
┌─────────────────────────────────────────────────────────────────┐
│                     DAY 02 KEY TAKEAWAYS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Not every AI problem requires an LLM — use simplest tech   │
│                                                                 │
│  2. Training ≠ Inference — different infrastructure needs       │
│                                                                 │
│  3. Model size (7B, 70B, 405B) = cost/latency/capability trade │
│                                                                 │
│  4. Tokens are the unit of LLM economics — track them          │
│                                                                 │
│  5. Context window is precious — manage it carefully            │
│                                                                 │
│  6. RAG = knowledge retrieval, Fine-tuning = behavior change    │
│                                                                 │
│  7. Model routing can save 50-70% costs vs single model        │
│                                                                 │
│  8. Model Capability ↔ Infrastructure Cost ↔ Latency ↔ Quality │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

> **Next**: See Day 03 (`03-llm-engineering/`) to learn LLM engineering fundamentals.
