"""Observability Pipeline — end-to-end observability workflow with simulated data."""
from app.metrics import MetricsCollector
from app.logger import StructuredLogger
from app.tracer import DistributedTracer
from app.llm_trace import LLMTracer
from app.rag_monitor import RAGMonitor
from app.agent_trace import AgentTracer
from app.slo_manager import SLOManager
from app.alert_manager import AlertManager
from app.drift_detector import DriftDetector
from app.models import TraceStatus
import random
import config.settings as settings


class ObservabilityPipeline:
    """Complete observability pipeline with simulation and analysis."""

    def __init__(self):
        self.metrics = MetricsCollector()
        self.logger = StructuredLogger(level="INFO")
        self.tracer = DistributedTracer()
        self.llm_tracer = LLMTracer()
        self.rag_monitor = RAGMonitor()
        self.agent_tracer = AgentTracer()
        self.slo_manager = SLOManager()
        self.alert_manager = AlertManager()
        self.drift_detector = DriftDetector()
        self.drift_detector.seed_baselines()

    def simulate_infrastructure_metrics(self):
        self.metrics.gauge("gpu_utilization", random.uniform(40, 85))
        self.metrics.gauge("gpu_memory_used_gb", random.uniform(8, 20))
        self.metrics.gauge("cpu_utilization", random.uniform(20, 60))
        self.metrics.gauge("memory_utilization", random.uniform(40, 75))
        self.metrics.gauge("queue_depth", random.randint(0, 20))
        self.metrics.increment("requests_total")
        if random.random() < 0.02:
            self.metrics.increment("errors_total")

    def simulate_llm_call(self, provider: str = "openai", model: str = "gpt-4o") -> dict:
        input_tokens = random.randint(500, 4000)
        output_tokens = random.randint(100, 1500)
        latency_ms = random.uniform(800, 3500)
        ttft_ms = random.uniform(200, 800)
        self.metrics.histogram("llm_latency_ms", latency_ms)
        self.metrics.histogram("ttft_ms", ttft_ms)
        self.metrics.increment("llm_calls_total")
        self.metrics.increment("tokens_total", input_tokens + output_tokens)
        self.metrics.gauge("tokens_per_second",
                           (input_tokens + output_tokens) / (latency_ms / 1000))
        return self.llm_tracer.record_call(
            provider=provider, model=model,
            input_tokens=input_tokens, output_tokens=output_tokens,
            latency_ms=latency_ms, ttft_ms=ttft_ms
        )

    def simulate_rag_event(self, query: str = "test query") -> dict:
        docs = random.randint(2, 8)
        retrieval_ms = random.uniform(50, 400)
        relevance = random.uniform(0.5, 0.98)
        self.metrics.gauge("retrieval_relevance", relevance * 100)
        return self.rag_monitor.record_event(
            query=query, documents_retrieved=docs,
            retrieval_ms=retrieval_ms, top_relevance_score=relevance,
            avg_relevance_score=relevance * 0.85,
            context_tokens=docs * 250
        )

    def simulate_agent_run(self, agent_name: str = "research-agent") -> dict:
        trace_id = self.agent_tracer.start_run(agent_name)
        steps = [
            ("reason", "", "Analyzing query intent", 150, 50),
            ("search", "web_search", "Searching knowledge base", 300, 0),
            ("retrieve", "vector_db", "Retrieving relevant documents", 200, 0),
            ("reason", "", "Evaluating document relevance", 180, 80),
            ("respond", "llm", "Generating final response", 1200, 200),
        ]
        for action, tool, reasoning, duration, tokens in steps:
            self.agent_tracer.add_step(
                action=action, tool_name=tool, reasoning=reasoning,
                duration_ms=duration, tokens_used=tokens
            )
        self.agent_tracer.end_run(TraceStatus.OK)
        return {"trace_id": trace_id, "steps": len(steps)}

    def simulate_full_request(self, query: str = "Explain our incident policy") -> dict:
        trace_id = self.tracer.start_trace("ai_request")
        span_api = self.tracer.start_span(trace_id, "api_gateway")
        self.tracer.end_span(span_api, TraceStatus.OK, {"http.method": "POST"})

        span_query = self.tracer.start_span(trace_id, "query_processing", span_api)
        self.tracer.end_span(span_query, TraceStatus.OK)

        span_embed = self.tracer.start_span(trace_id, "embedding", span_query)
        self.tracer.end_span(span_embed, TraceStatus.OK, {"tokens": 15})

        span_retrieve = self.tracer.start_span(trace_id, "vector_search", span_embed)
        self.simulate_rag_event(query)
        self.tracer.end_span(span_retrieve, TraceStatus.OK, {"documents": 5})

        span_rerank = self.tracer.start_span(trace_id, "reranking", span_retrieve)
        self.tracer.end_span(span_rerank, TraceStatus.OK)

        span_llm = self.tracer.start_span(trace_id, "llm_call", span_rerank)
        call = self.simulate_llm_call()
        self.tracer.end_span(span_llm, TraceStatus.OK, {
            "model": call.provider + "/" + call.model,
            "tokens": call.total_tokens
        })

        self.tracer.end_span(span_api, TraceStatus.OK)
        return {"trace_id": trace_id, "spans": 6}

    def simulate_traffic(self, num_requests: int = 100) -> dict:
        results = {"requests": 0, "errors": 0, "traces": 0, "llm_calls": 0, "rag_events": 0}
        for i in range(num_requests):
            self.simulate_infrastructure_metrics()
            self.simulate_full_request(f"query-{i}")
            results["requests"] += 1
            results["traces"] += 1
            self.simulate_llm_call()
            results["llm_calls"] += 1
            if random.random() < 0.3:
                self.simulate_rag_event(f"rag-query-{i}")
                results["rag_events"] += 1
        return results

    def run_incident_investigation(self) -> dict:
        steps = []
        steps.append({"step": 1, "check": "availability", "result": "healthy",
                       "detail": "99.95% uptime"})
        steps.append({"step": 2, "check": "latency", "result": "healthy",
                       "detail": f"P95: {self.metrics.get_histogram_stats('llm_latency_ms').get('p95', 0):.0f}ms"})
        steps.append({"step": 3, "check": "model_errors", "result": "healthy",
                       "detail": "Error rate < 1%"})

        relevance = self.metrics.get_latest("retrieval_relevance") or 100
        if relevance < 70:
            steps.append({"step": 4, "check": "retrieval", "result": "DEGRADED",
                           "detail": f"Relevance: {relevance:.1f}%"})
            steps.append({"step": 5, "check": "data_pipeline", "result": "ROOT CAUSE",
                           "detail": "New document parser deployed 2 hours ago"})
            steps.append({"step": 6, "check": "mitigation", "result": "ACTION",
                           "detail": "Roll back document parser, re-index affected documents"})
        else:
            steps.append({"step": 4, "check": "retrieval", "result": "healthy",
                           "detail": f"Relevance: {relevance:.1f}%"})
            steps.append({"step": 5, "check": "model_version", "result": "healthy",
                           "detail": "No model changes in last 24h"})

        return {
            "incident": "AI response quality degradation reported",
            "investigation_steps": steps,
            "conclusion": steps[-1]["detail"]
        }

    def get_full_status(self) -> dict:
        return {
            "infrastructure": self.metrics.get_infrastructure_summary(),
            "ai_metrics": self.metrics.get_ai_summary(),
            "logs": self.logger.get_summary(),
            "traces": self.tracer.get_trace_summary(),
            "llm": self.llm_tracer.get_summary(),
            "rag": self.rag_monitor.get_summary(),
            "agents": self.agent_tracer.get_summary(),
            "slos": self.slo_manager.get_summary(),
            "alerts": self.alert_manager.get_alert_summary(),
            "drift": self.drift_detector.get_summary()
        }
