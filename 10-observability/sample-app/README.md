# AI Observability — Sample App

A working prototype demonstrating **full-stack AI observability** — metrics, structured logging, distributed tracing, LLM observability, RAG quality monitoring, agent workflow tracing, SLI/SLO management, alerting, and drift detection from Day 10.

> **Building on Day 09**: This app adds the operational nervous system — visibility into every layer from infrastructure to business outcomes.

## Architecture

```
                         USERS
                           │
                           ▼
                    ┌─────────────┐
                    │  FastAPI    │
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
    ┌─────────┐     ┌───────────┐     ┌───────────┐
    │ Metrics │     │  Logger   │     │  Tracer   │
    │Collector│     │ (Structured)│    │(Distributed)│
    └────┬────┘     └─────┬─────┘     └─────┬─────┘
         │                │                 │
         └────────────────┼─────────────────┘
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │ LLM Trace│    │ RAG      │    │ Agent    │
    │          │    │ Monitor  │    │ Trace    │
    └────┬─────┘    └────┬─────┘    └────┬─────┘
         │               │               │
         └───────────────┼───────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │   SLO    │    │  Alert   │    │  Drift   │
    │ Manager  │    │ Manager  │    │ Detector │
    └──────────┘    └──────────┘    └──────────┘
```

## Project Structure

```
sample-app/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application
│   ├── models.py                  # Pydantic models
│   ├── metrics.py                 # Metrics collection & aggregation
│   ├── logger.py                  # Structured logging with context
│   ├── tracer.py                  # Distributed tracing with span trees
│   ├── llm_trace.py               # LLM call observability
│   ├── rag_monitor.py             # RAG quality & retrieval monitoring
│   ├── agent_trace.py             # Agent workflow tracing
│   ├── slo_manager.py             # SLI/SLO & error budgets
│   ├── alert_manager.py           # Alert rules & evaluation
│   └── drift_detector.py          # Statistical drift detection
├── config/
│   ├── settings.py                # Configuration
│   └── .env.example               # Environment template
├── pipelines/
│   ├── __init__.py
│   └── observability_pipeline.py  # End-to-end observability workflow
├── scripts/
│   ├── status.py                  # View full system status
│   ├── trace_demo.py              # Trace visualization demo
│   └── incident.py                # Incident investigation demo
├── requirements.txt
└── test_system.py                 # Test all components
```

## Quick Start

```bash
# 1. Navigate to sample-app
cd 10-observability/sample-app

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the API
uvicorn app.main:app --reload --port 8010

# 5. Open API docs
# http://localhost:8010/docs
```

## Core Components

### 1. Metrics Collector

Collect and aggregate metrics across infrastructure, application, and AI layers:

```python
from app.metrics import MetricsCollector

mc = MetricsCollector()
mc.gauge("gpu_utilization", 72.0)
mc.increment("requests_total")
mc.histogram("llm_latency_ms", 1500.0)

summary = mc.get_ai_summary()
```

### 2. Structured Logger

JSON-structured logging with trace context propagation:

```python
from app.logger import StructuredLogger

logger = StructuredLogger(level="INFO")
logger.log_llm_call("openai", "gpt-4o", 1000, 500, 1200.0)
logger.log_retrieval("query", 5, 150.0, relevance_score=0.85)
logger.log_agent_step("agent", 1, "search", "web_search", 300.0)
```

### 3. Distributed Tracer

Follow requests across components with span trees:

```python
from app.tracer import DistributedTracer

tracer = DistributedTracer()
trace_id = tracer.start_trace("ai_request")
span = tracer.start_span(trace_id, "llm_call")
tracer.end_span(span, TraceStatus.OK, {"model": "gpt-4o"})

tree = tracer.get_trace_tree(trace_id)
```

### 4. LLM Tracer

Observability for model calls with tokens, latency, and cost:

```python
from app.llm_trace import LLMTracer

lt = LLMTracer()
call = lt.record_call("openai", "gpt-4o", 2000, 500, 1500.0)
print(f"Cost: ${call.cost_usd:.6f}")
```

### 5. RAG Monitor

Observe retrieval quality, relevance, and context assembly:

```python
from app.rag_monitor import RAGMonitor

rm = RAGMonitor()
event = rm.record_event("query", 5, 150.0, top_relevance_score=0.92)
summary = rm.get_summary()
```

### 6. Agent Tracer

Trace multi-step agent workflows with loop detection:

```python
from app.agent_trace import AgentTracer

at = AgentTracer()
trace_id = at.start_run("research-agent")
at.add_step("search", tool_name="web_search", duration_ms=300)
at.end_run(TraceStatus.OK)
```

### 7. SLO Manager

Track service level indicators, objectives, and error budgets:

```python
from app.slo_manager import SLOManager

sm = SLOManager()
sm.record_sli("Availability", 99.95)
summary = sm.get_summary()
```

### 8. Alert Manager

Define and evaluate alert rules:

```python
from app.alert_manager import AlertManager

am = AlertManager()
fired = am.evaluate({"p95_latency_ms": 7000, "retrieval_relevance": 65.0})
```

### 9. Drift Detector

Detect statistical drift in metrics:

```python
from app.drift_detector import DriftDetector

dd = DriftDetector()
dd.seed_baselines()
sample = dd.add_sample("retrieval_relevance", 0.45)
print(f"Drift: {sample.is_drift}")
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | System health check |
| GET | /metrics | List all metrics |
| GET | /metrics/infrastructure | Infrastructure metrics summary |
| GET | /metrics/ai | AI metrics summary |
| GET | /metrics/histogram/{name} | Histogram statistics |
| POST | /metrics/record | Record a metric |
| GET | /logs | List log entries |
| GET | /logs/summary | Log summary |
| GET | /traces | List distributed traces |
| GET | /traces/slowest | Slowest traces |
| GET | /traces/{trace_id} | Trace tree visualization |
| POST | /traces/start | Start a new trace |
| GET | /llm/calls | LLM call history |
| GET | /llm/summary | LLM usage summary |
| GET | /llm/by-provider | Cost by provider |
| GET | /llm/tokens | Token distribution |
| GET | /rag/events | RAG event history |
| GET | /rag/summary | RAG quality summary |
| GET | /rag/relevance | Relevance distribution |
| GET | /rag/latency | Retrieval latency breakdown |
| GET | /agents/runs | Agent run history |
| GET | /agents/summary | Agent workflow summary |
| GET | /agents/tools | Tool usage statistics |
| GET | /slos | SLO status summary |
| GET | /slos/errors | Error budget status |
| POST | /slos/{id}/sli | Record SLI value |
| GET | /alerts | Alert history |
| GET | /alerts/active | Active alerts |
| GET | /alerts/summary | Alert summary |
| GET | /alerts/rules | Alert rules |
| POST | /alerts/evaluate | Evaluate alert rules |
| GET | /drift | Drift status |
| GET | /drift/events | Drift events |
| GET | /drift/{metric} | Metric drift detail |
| POST | /drift/record | Record drift sample |
| GET | /architecture/overview | Architecture overview |

## Running the Tests

```bash
# Run all tests
python test_system.py

# View full system status
python scripts/status.py

# Trace visualization demo
python scripts/trace_demo.py

# Incident investigation demo
python scripts/incident.py
```

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
# Metrics
METRICS_RETENTION_SECONDS=86400

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Tracing
TRACE_SAMPLE_RATE=1.0
TRACE_MAX_SPANS=100

# LLM
LLM_COST_PER_1M_INPUT=3.0
LLM_COST_PER_1M_OUTPUT=15.0

# RAG
RAG_RELEVANCE_THRESHOLD=0.7
RAG_MAX_LATENCY_MS=500.0

# SLO
SLO_AVAILABILITY_TARGET=99.9
SLO_LATENCY_P95_TARGET_MS=5000
SLO_TASK_SUCCESS_TARGET=90.0
SLO_GROUNDEDNESS_TARGET=95.0

# Alerts
ALERT_LATENCY_THRESHOLD_MS=5000
ALERT_ERROR_RATE_THRESHOLD=1.0
ALERT_RETRIEVAL_RELEVANCE_THRESHOLD=70.0
ALERT_COST_DAILY_LIMIT=500.0

# Drift
DRIFT_WINDOW_SIZE=1000
DRIFT_BASELINE_SIZE=5000
```

## Key Concepts Demonstrated

| Concept | Implementation |
|---------|----------------|
| Metrics Collection | Gauges, counters, histograms with aggregation |
| Structured Logging | JSON logs with trace context and component tagging |
| Distributed Tracing | Span hierarchy with trace context propagation |
| LLM Observability | Token tracking, TTFT, cost per call, provider/model breakdown |
| RAG Monitoring | Retrieval relevance, latency breakdown, context size tracking |
| Agent Tracing | Multi-step workflows, tool usage, loop detection |
| SLI/SLO Management | Error budgets, state evaluation, health status |
| Alerting | Rule-based evaluation with severity and state management |
| Drift Detection | Z-score based statistical drift detection |

## Pre-seeded Configuration

### SLOs
- **Availability**: 99.9% target
- **Latency P95**: < 5000ms target
- **Task Success**: 90% target
- **Groundedness**: 95% target

### Alert Rules
- High Latency (> 5000ms P95)
- High Error Rate (> 1%)
- Low Retrieval Relevance (< 70%)
- High Daily Cost (> $500)
- GPU Overheating (> 95% util + > 85C)
- Quality Degradation (> 10% drop)

## Next Steps

After running this sample app, you should understand:

1. How to collect metrics across all AI system layers
2. How structured logging enables search and correlation
3. How distributed tracing follows requests across components
4. How to observe LLM calls with token, latency, and cost visibility
5. How to monitor RAG retrieval quality and relevance
6. How to trace agent workflows and detect loops
7. How SLIs, SLOs, and error budgets measure reliability
8. How to define and evaluate alert rules
9. How to detect statistical drift in metrics

Move to **Day 11 → AI Security & Governance** to learn about securing and governing AI systems.
