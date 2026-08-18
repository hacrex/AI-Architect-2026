# Day 02 — Model Comparison & Routing Sample App

A working prototype demonstrating **model comparison**, **model routing**, and **architecture trade-offs** from Day 02.

> **Building on Day 01**: This app extends the Model Gateway pattern from Day 01 (`01-foundations/sample-app/`) by adding complexity-based routing and side-by-side comparison.

## Architecture

```
User Request
      │
      ▼
┌─────────────────────────────────┐
│        FastAPI Gateway          │
│                                 │
│  ┌───────────────────────────┐  │
│  │    Request Classifier     │  │
│  │  (complexity detection)   │  │
│  └───────────────────────────┘  │
│              │                  │
│        ┌─────┴─────┐            │
│        ▼           ▼            │
│  ┌──────────┐ ┌──────────┐      │
│  │  Model   │ │  Model   │      │
│  │  Router  │ │Comparator│      │
│  └──────────┘ └──────────┘      │
│        │           │            │
│        ▼           ▼            │
│  ┌───────────────────────────┐  │
│  │    Model Gateway          │  │
│  │  ┌─────┐ ┌─────┐ ┌─────┐ │  │
│  │  │ GPT │ │ GPT │ │Claude│ │  │
│  │  │ -4  │ │ -3.5│ │ Haiku│ │  │
│  │  └─────┘ └─────┘ └─────┘ │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

## Project Structure

```
sample-app/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── model_router.py      # Request classification & routing
│   ├── model_comparator.py  # Side-by-side model comparison
│   └── model_gateway.py     # LLM provider abstraction
├── config/
│   ├── settings.py          # Configuration management
│   └── .env.example         # Environment variables template
├── requirements.txt         # Python dependencies
├── benchmark.py             # Model benchmarking script
└── test_models.py           # Test script
```

## Quick Start

### 1. Install Dependencies

```bash
cd 02-ai-ml/sample-app
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp config/.env.example config/.env
# Edit config/.env with your API keys
```

### 3. Start the Server

```bash
uvicorn app.main:app --reload --port 8001
```

### 4. Test the API

```bash
python test_models.py
```

Or manually:

```bash
# Health check
curl http://localhost:8001/health

# Single model query
curl -X POST http://localhost:8001/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is 2 + 2?", "model": "gpt-3.5-turbo"}'

# Model comparison
curl -X POST http://localhost:8001/compare \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain the difference between REST and GraphQL."}'

# Auto-routed query
curl -X POST http://localhost:8001/query/auto \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I reset my password?"}'
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check with model status |
| `/query` | POST | Single model query |
| `/query/auto` | POST | Auto-routed query (simple/normal/complex) |
| `/compare` | POST | Compare response from multiple models |
| `/models` | GET | List available models and their characteristics |
| `/metrics` | GET | Token usage and latency metrics |
| `/benchmark` | POST | Run benchmark against test prompts |

## Model Routing Logic

The router classifies requests into three categories:

### Simple Requests
- Short queries (< 50 words)
- Factual questions
- Simple calculations
- → Routed to: **GPT-3.5-turbo** (fast, cheap)

### Normal Requests
- Moderate complexity
- Requires some reasoning
- Standard business queries
- → Routed to: **GPT-4** (balanced)

### Complex Requests
- Multi-step reasoning
- Long context analysis
- Technical deep-dives
- → Routed to: **GPT-4** (quality-focused)

## Model Comparison Features

### Side-by-Side Comparison

Send the same prompt to multiple models and compare:

```json
{
  "query": "Explain the CAP theorem in distributed systems.",
  "models": ["gpt-3.5-turbo", "gpt-4"],
  "metrics": ["quality", "latency", "tokens"]
}
```

### Benchmark Suite

Run a standard set of prompts across models:

```json
{
  "category": "technical",
  "models": ["gpt-3.5-turbo", "gpt-4"],
  "iterations": 3
}
```

## Architecture Patterns Demonstrated

| Pattern | Implementation |
|---------|----------------|
| **Model Routing** | Complexity-based request classification |
| **Model Comparison** | Side-by-side evaluation with metrics |
| **Model Gateway** | Provider abstraction with fallback |
| **Token Tracking** | Cost estimation per request |
| **Latency Measurement** | Response time tracking |
| **Benchmarking** | Standardized evaluation prompts |

## Sample Test Prompts

### Simple
```json
{"query": "What is 2 + 2?"}
{"query": "What color is the sky?"}
{"query": "Define API in one sentence."}
```

### Normal
```json
{"query": "Explain the difference between REST and GraphQL."}
{"query": "What are three best practices for API design?"}
{"query": "Summarize microservices architecture."}
```

### Complex
```json
{"query": "Compare horizontal vs vertical scaling for a cloud-native application handling 10,000 requests per second. Consider cost, latency, and operational complexity."}
{"query": "Design a data pipeline architecture for real-time analytics on 5TB of daily event data."}
{"query": "Analyze the security implications of using LLMs in an enterprise setting."}
```

## Key Concepts (Day 02)

This sample app demonstrates:

1. **Model Routing** — Direct requests to appropriate models based on complexity
2. **Model Comparison** — Side-by-side evaluation with quality metrics
3. **Token Economics** — Track and estimate costs per request
4. **Latency Trade-offs** — Measure response time differences between models
5. **Architecture Decisions** — When to use which model and why
6. **Benchmarking** — Standardized evaluation methodology
7. **Cost Optimization** — Routing simple requests to cheaper models

## Cost Comparison

### Single Model Approach (GPT-4 only)
- 10,000 requests/month
- Average 500 input tokens, 300 output tokens
- Cost: ~$450/month

### Routed Approach (GPT-3.5 + GPT-4)
- 50% simple → GPT-3.5-turbo
- 35% normal → GPT-4
- 15% complex → GPT-4
- Cost: ~$180/month
- **Savings: ~60%**

## Running Benchmarks

```bash
# Run full benchmark suite
python benchmark.py

# Run specific category
python benchmark.py --category technical

# Compare specific models
python benchmark.py --models gpt-3.5-turbo gpt-4
```

## Next Steps

After running this sample app:

1. Fill out the comparison tables in `exercise.md`
2. Design your own model routing strategy
3. Estimate costs for your specific use case
4. Consider: When would you self-host vs use managed?
