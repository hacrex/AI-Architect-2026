"""FastAPI application for AI Observability."""
from datetime import datetime
from fastapi import FastAPI, HTTPException
from typing import Optional
from app.metrics import MetricsCollector
from app.logger import StructuredLogger
from app.tracer import DistributedTracer
from app.llm_trace import LLMTracer
from app.rag_monitor import RAGMonitor
from app.agent_trace import AgentTracer
from app.slo_manager import SLOManager
from app.alert_manager import AlertManager
from app.drift_detector import DriftDetector
from app.models import TraceStatus, AlertSeverity, AlertState
import config.settings as settings

app = FastAPI(
    title="AI Observability API",
    description="Full-stack observability for AI systems — metrics, traces, logs, LLM, RAG, agents, SLOs, alerts, drift",
    version="0.1.0"
)

metrics = MetricsCollector()
logger = StructuredLogger(level=settings.LOG_LEVEL)
tracer = DistributedTracer(sample_rate=settings.TRACE_SAMPLE_RATE)
llm_tracer = LLMTracer()
rag_monitor = RAGMonitor()
agent_tracer = AgentTracer()
slo_manager = SLOManager()
alert_manager = AlertManager()
drift_detector = DriftDetector()
drift_detector.seed_baselines()


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "metrics": "ok",
            "logger": "ok",
            "tracer": "ok",
            "llm_tracer": "ok",
            "rag_monitor": "ok",
            "agent_tracer": "ok",
            "slo_manager": "ok",
            "alert_manager": "ok",
            "drift_detector": "ok"
        }
    }


@app.get("/metrics")
def list_metrics():
    return metrics.list_metrics()


@app.get("/metrics/infrastructure")
def infra_summary():
    return metrics.get_infrastructure_summary()


@app.get("/metrics/ai")
def ai_summary():
    return metrics.get_ai_summary()


@app.get("/metrics/histogram/{name}")
def histogram_stats(name: str):
    return metrics.get_histogram_stats(name)


@app.post("/metrics/record")
def record_metric(name: str, value: float, unit: str = ""):
    metrics.record(name, value, unit=unit)
    return {"recorded": name, "value": value}


@app.post("/metrics/increment")
def increment_metric(name: str, value: float = 1.0):
    metrics.increment(name, value)
    return {"incremented": name}


@app.get("/logs")
def list_logs(level: str = None, component: str = None, limit: int = 100):
    entries = logger.get_entries(level=level, component=component, limit=limit)
    return [
        {
            "timestamp": e.timestamp.isoformat(),
            "level": e.level,
            "message": e.message,
            "component": e.component,
            "trace_id": e.trace_id,
            "attributes": e.attributes
        }
        for e in entries
    ]


@app.get("/logs/summary")
def log_summary():
    return logger.get_summary()


@app.post("/logs/entry")
def add_log(level: str, message: str, component: str = ""):
    entry = logger._log(level, message, component=component)
    return {"logged": True, "level": level}


@app.get("/traces")
def list_traces(limit: int = 50):
    return tracer.list_traces(limit)


@app.get("/traces/slowest")
def slowest_traces(limit: int = 10):
    return tracer.get_slowest_traces(limit)


@app.get("/traces/summary")
def trace_summary():
    return tracer.get_trace_summary()


@app.get("/traces/{trace_id}")
def get_trace(trace_id: str):
    tree = tracer.get_trace_tree(trace_id)
    if "error" in tree:
        raise HTTPException(status_code=404, detail=tree["error"])
    return tree


@app.post("/traces/start")
def start_trace(operation: str):
    trace_id = tracer.start_trace(operation)
    return {"trace_id": trace_id}


@app.post("/traces/{trace_id}/span")
def add_span(trace_id: str, name: str, parent_span_id: str = ""):
    span_id = tracer.start_span(trace_id, name, parent_span_id)
    return {"span_id": span_id}


@app.post("/traces/spans/{span_id}/end")
def end_span(span_id: str, status: str = "ok"):
    try:
        s = TraceStatus(status)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
    tracer.end_span(span_id, s)
    return {"ended": span_id}


@app.get("/llm/calls")
def llm_calls(provider: str = None, model: str = None, limit: int = 50):
    return llm_tracer.list_calls(provider=provider, model=model, limit=limit)


@app.get("/llm/summary")
def llm_summary():
    return llm_tracer.get_summary()


@app.get("/llm/by-provider")
def llm_by_provider():
    return llm_tracer.get_by_provider()


@app.get("/llm/by-model")
def llm_by_model():
    return llm_tracer.get_by_model()


@app.get("/llm/tokens")
def llm_token_distribution():
    return llm_tracer.get_token_distribution()


@app.post("/llm/record")
def record_llm_call(provider: str, model: str, input_tokens: int,
                    output_tokens: int, latency_ms: float,
                    ttft_ms: float = 0.0, prompt: str = "",
                    response: str = "", trace_id: str = ""):
    call = llm_tracer.record_call(
        provider=provider, model=model, input_tokens=input_tokens,
        output_tokens=output_tokens, latency_ms=latency_ms, ttft_ms=ttft_ms,
        prompt=prompt, response=response, trace_id=trace_id
    )
    return {"trace_id": call.trace_id, "cost_usd": call.cost_usd}


@app.get("/rag/events")
def rag_events(limit: int = 50):
    return rag_monitor.list_events(limit)


@app.get("/rag/summary")
def rag_summary():
    return rag_monitor.get_summary()


@app.get("/rag/relevance")
def rag_relevance_distribution():
    return rag_monitor.get_relevance_distribution()


@app.get("/rag/latency")
def rag_latency_breakdown():
    return rag_monitor.get_latency_breakdown()


@app.post("/rag/record")
def record_rag_event(query: str, documents_retrieved: int,
                     retrieval_ms: float, top_relevance_score: float = 0.0,
                     avg_relevance_score: float = 0.0, context_tokens: int = 0,
                     trace_id: str = ""):
    event = rag_monitor.record_event(
        query=query, documents_retrieved=documents_retrieved,
        retrieval_ms=retrieval_ms, top_relevance_score=top_relevance_score,
        avg_relevance_score=avg_relevance_score, context_tokens=context_tokens,
        trace_id=trace_id
    )
    return {"trace_id": event.trace_id}


@app.get("/agents/runs")
def agent_runs(limit: int = 50):
    return agent_tracer.list_runs(limit)


@app.get("/agents/summary")
def agent_summary():
    return agent_tracer.get_summary()


@app.get("/agents/tools")
def agent_tool_usage():
    return agent_tracer.get_tool_usage()


@app.get("/agents/runs/{trace_id}")
def agent_run_detail(trace_id: str):
    detail = agent_tracer.get_run_detail(trace_id)
    if "error" in detail:
        raise HTTPException(status_code=404, detail=detail["error"])
    return detail


@app.post("/agents/start")
def start_agent_run(agent_name: str):
    trace_id = agent_tracer.start_run(agent_name)
    return {"trace_id": trace_id}


@app.post("/agents/{trace_id}/step")
def add_agent_step(trace_id: str, action: str, tool_name: str = "",
                   reasoning: str = "", duration_ms: float = 0.0,
                   tokens_used: int = 0):
    run = agent_tracer.get_run(trace_id)
    if not run:
        raise HTTPException(status_code=404, detail=f"Run {trace_id} not found")
    step = agent_tracer.add_step(
        action=action, tool_name=tool_name, reasoning=reasoning,
        duration_ms=duration_ms, tokens_used=tokens_used
    )
    return {"step": step.step_number}


@app.post("/agents/{trace_id}/end")
def end_agent_run(trace_id: str, status: str = "ok"):
    try:
        s = TraceStatus(status)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
    agent_tracer.end_run(s)
    return {"ended": trace_id}


@app.get("/slos")
def list_slos():
    return slo_manager.get_summary()


@app.get("/slos/errors")
def slo_error_budgets():
    return slo_manager.get_error_budgets()


@app.post("/slos/{slo_id}/sli")
def record_sli(slo_id: str, value: float):
    slo = slo_manager.get_slo(slo_id)
    if not slo:
        raise HTTPException(status_code=404, detail=f"SLO {slo_id} not found")
    slo_manager.record_sli(slo.name, value)
    return {"updated": slo.name, "value": value, "state": slo.state.value}


@app.get("/alerts")
def list_alerts(severity: str = None, limit: int = 50):
    sev = AlertSeverity(severity) if severity else None
    return alert_manager.list_alerts(severity=sev, limit=limit)


@app.get("/alerts/active")
def active_alerts():
    return alert_manager.get_active_alerts()


@app.get("/alerts/summary")
def alert_summary():
    return alert_manager.get_alert_summary()


@app.get("/alerts/rules")
def alert_rules():
    return alert_manager.list_rules()


@app.post("/alerts/evaluate")
def evaluate_alerts():
    ai_metrics = {
        "p95_latency_ms": metrics.get_histogram_stats("llm_latency_ms").get("p95", 0),
        "error_rate_pct": metrics.get_rate("errors_total") * 100,
        "retrieval_relevance": metrics.get_latest("retrieval_relevance") or 100,
        "daily_cost_usd": llm_tracer.get_summary().get("total_cost_usd", 0),
        "gpu_utilization": metrics.get_latest("gpu_utilization") or 0,
    }
    fired = alert_manager.evaluate(ai_metrics)
    return {
        "evaluated": len(alert_manager._rules),
        "fired": len(fired),
        "alerts": [
            {"name": a.name, "severity": a.severity.value, "message": a.message}
            for a in fired
        ]
    }


@app.get("/drift")
def drift_status():
    return drift_detector.get_summary()


@app.get("/drift/events")
def drift_events(limit: int = 50):
    return drift_detector.get_drift_events(limit)


@app.get("/drift/{metric_name}")
def drift_metric_detail(metric_name: str):
    return drift_detector.get_metric_stats(metric_name)


@app.post("/drift/record")
def record_drift_sample(metric_name: str, value: float):
    sample = drift_detector.add_sample(metric_name, value)
    if sample:
        return {
            "metric": metric_name,
            "value": value,
            "z_score": sample.z_score,
            "is_drift": sample.is_drift,
            "baseline_mean": sample.baseline_mean
        }
    return {"metric": metric_name, "value": value, "status": "insufficient_baseline"}


@app.get("/architecture/overview")
def architecture_overview():
    return {
        "observability_layers": {
            "infrastructure": {
                "description": "CPU, memory, GPU, network, pod health",
                "metrics_count": len([m for m in metrics.list_metrics() if "gpu" in m["name"] or "cpu" in m["name"]])
            },
            "application": {
                "description": "Request rate, latency, errors, throughput",
                "metrics_count": len([m for m in metrics.list_metrics() if "request" in m["name"] or "error" in m["name"]])
            },
            "ai_workflow": {
                "description": "LLM calls, token usage, model behavior",
                "llm_calls": llm_tracer.get_summary().get("total_calls", 0),
                "traces": tracer.get_trace_summary().get("total_traces", 0)
            },
            "retrieval": {
                "description": "RAG quality, relevance, context",
                "rag_events": rag_monitor.get_summary().get("total_events", 0)
            },
            "agents": {
                "description": "Agent workflows, tool calls, loops",
                "agent_runs": agent_tracer.get_summary().get("total_runs", 0)
            },
            "quality": {
                "description": "Evaluation scores, drift detection",
                "drifting_metrics": drift_detector.get_summary().get("drifting_metrics", 0)
            },
            "cost": {
                "description": "Token cost, provider spend, budget",
                "total_cost_usd": llm_tracer.get_summary().get("total_cost_usd", 0)
            }
        },
        "slo_health": slo_manager.get_summary().get("overall_health"),
        "active_alerts": alert_manager.get_alert_summary().get("firing", 0),
        "total_traces": tracer.get_trace_summary().get("total_traces", 0)
    }
