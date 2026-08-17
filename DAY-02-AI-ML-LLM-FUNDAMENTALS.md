# Day 02 — AI/ML & LLM Fundamentals

## Objective

Understand enough machine learning and LLM internals to make architecture decisions without becoming a model researcher.

## Learn

### Machine learning

- Training vs inference
- Supervised vs unsupervised learning
- Evaluation
- Generalization
- Model drift

### Deep learning

- Neural networks
- Parameters
- GPUs
- Training compute
- Inference compute

### Transformers

Understand:

- tokens
- embeddings
- attention
- context windows
- positional information
- transformer layers

### Model lifecycle

Understand:

- pretraining
- instruction tuning
- fine-tuning
- quantization
- inference

## Architecture decisions

Ask:

- Is an LLM actually required?
- Can a smaller model solve the problem?
- Is fine-tuning necessary?
- Is RAG a better solution?
- What latency is acceptable?
- What happens when the model is unavailable?

## Exercise

Compare three possible approaches to the same problem:

1. Traditional software
2. Small/specialized ML model
3. LLM

Create a decision table covering:

- accuracy
- latency
- cost
- complexity
- privacy
- maintainability

## Deliverable

A one-page model-selection decision matrix.
