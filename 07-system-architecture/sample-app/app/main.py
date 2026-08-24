"""FastAPI application for the AI System Architecture."""
import uuid
import time
from datetime import datetime
from fastapi import FastAPI, HTTPException, Header, Depends
from typing import Optional
from app.models import AIRequest, AIResponse, RequestStatus
from app.gateway import AIGateway
from app.rag import RAGService
from app.agents import AgentService
from app.model_router import ModelRouter
from app.context import ContextAssembler
from app.observability import ObservabilityService
from app.security import SecurityService

app = FastAPI(
    title="AI System Architecture API",
    description="Complete AI system with gateway, RAG, agents, model routing, and observability",
    version="0.1.0"
)

gateway = AIGateway()
rag = RAGService()
agents = AgentService()
model_router = ModelRouter()
context_assembler = ContextAssembler()
observability = ObservabilityService()
security = SecurityService()


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "gateway": "ok",
            "rag": "ok",
            "agents": "ok",
            "model_router": "ok",
            "observability": "ok",
            "security": "ok"
        }
    }


@app.post("/auth/login")
def login(email: str, password: str):
    result = security.authenticate(email, password)
    if not result["authenticated"]:
        raise HTTPException(status_code=401, detail=result["reason"])
    return result


@app.post("/ai/query")
def ai_query(request: AIRequest, authorization: str = Header(None)):
    start_time = time.time()
    request_id = f"req-{uuid.uuid4().hex[:8]}"

    user = security.identity_provider.get_user(request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    sec_ctx = security.get_security_context(request.user_id)

    gw_check = gateway.process_request(request, sec_ctx)
    if not gw_check["allowed"]:
        raise HTTPException(status_code=429, detail=gw_check.get("reason", "request denied"))

    trace = observability.tracer.start_trace(request_id, request.user_id)
    span = observability.tracer.add_span(request_id, "ai_query", attributes={"query": request.query[:100]})

    rag_result = rag.retrieve(
        query=request.query,
        user_roles=sec_ctx.roles,
        top_k=5
    )
    observability.tracer.add_span(request_id, "rag_retrieval", attributes={
        "chunks_found": rag_result["raw_count"],
        "tokens_used": rag_result["tokens_used"]
    })

    agent_result = None
    if request.use_agent:
        agent_result = agents.run(
            query=request.query,
            context=rag_result["context"],
            user_roles=sec_ctx.roles
        )
        observability.tracer.add_span(request_id, "agent_execution", attributes={
            "tools_used": len(agent_result.get("execution", {}).get("results", []))
        })

    assembled = context_assembler.assemble(
        query=request.query,
        rag_context=rag_result,
        agent_results=agent_result
    )

    selected_model = model_router.select_model()
    output_tokens = len(assembled["prompt"].split()) * 2
    input_tokens = assembled["estimated_tokens"]
    cost = model_router.estimate_cost(selected_model.model_name, input_tokens, output_tokens)

    latency_ms = (time.time() - start_time) * 1000

    observability.record_request(
        request_id=request_id,
        user_id=request.user_id,
        model=selected_model.model_name,
        provider=selected_model.provider.value,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        latency_ms=latency_ms,
        cost_usd=cost
    )

    observability.tracer.end_span(request_id, span.span_id if span else "unknown")
    observability.tracer.complete_trace(
        request_id,
        model_used=selected_model.model_name,
        total_tokens=input_tokens + output_tokens,
        total_cost=cost
    )

    security.audit_logger.log("ai_query", request.user_id, {
        "request_id": request_id,
        "model": selected_model.model_name,
        "tokens": input_tokens + output_tokens,
        "cost": cost
    })

    return AIResponse(
        request_id=request_id,
        answer=f"Based on {len(rag_result['sources'])} sources, here is the answer to your question.",
        sources=rag_result["sources"],
        model_used=selected_model.model_name,
        provider=selected_model.provider.value,
        tokens_used=input_tokens + output_tokens,
        latency_ms=round(latency_ms, 2),
        cost_usd=cost,
        status=RequestStatus.COMPLETED,
        metadata={
            "agent_used": request.use_agent,
            "rag_chunks": rag_result["raw_count"]
        }
    )


@app.get("/rag/stats")
def rag_stats():
    return rag.get_stats()


@app.post("/rag/ingest")
def rag_ingest(source: str, content: str, category: str = "general"):
    result = rag.ingest_document(content, source, category, ["all"])
    security.audit_logger.log("document_ingest", "system", {"source": source})
    return result


@app.get("/agents/tools")
def agent_tools():
    return agents.get_tools()


@app.get("/agents/stats")
def agent_stats():
    return agents.get_stats()


@app.get("/models/routes")
def model_routes():
    return model_router.list_routes()


@app.get("/models/stats")
def model_stats():
    return model_router.get_stats()


@app.get("/observability/dashboard")
def observability_dashboard():
    return observability.get_dashboard()


@app.get("/observability/traces")
def observability_traces(user_id: str = None, limit: int = 20):
    traces = observability.tracer.get_traces(user_id=user_id, limit=limit)
    return [{"request_id": t.request_id, "model": t.model_used,
             "tokens": t.total_tokens, "cost": t.total_cost_usd,
             "latency_ms": t.total_latency_ms, "status": t.status.value}
            for t in traces]


@app.get("/observability/costs")
def cost_report():
    return {
        "total_24h": observability.cost_tracker.get_total_cost(24),
        "by_model": observability.cost_tracker.get_cost_by_model(),
        "by_user": observability.cost_tracker.get_cost_by_user()
    }


@app.get("/security/audit")
def audit_log(event_type: str = None, limit: int = 50):
    return security.audit_logger.get_events(event_type=event_type, limit=limit)


@app.get("/security/audit/summary")
def audit_summary():
    return security.audit_logger.get_summary()


@app.get("/system/architecture")
def system_architecture():
    return {
        "layers": {
            "client": ["Web App", "Mobile", "Internal Tools", "API Clients"],
            "gateway": ["API Gateway", "AI Gateway"],
            "ai": ["RAG Service", "Agent Service", "Context Assembly"],
            "model": ["Model Router", "Managed Models", "Self-hosted Models", "Fallback"],
            "data": ["Vector DB", "Relational DB", "Object Storage", "Streaming"],
            "platform": ["MLOps", "Evaluation", "Registry", "CI/CD"],
            "infrastructure": ["Kubernetes", "GPU Pool", "Network", "Storage"],
            "cross_cutting": ["Security", "Observability", "Governance", "Reliability", "FinOps"]
        },
        "components": {
            "gateway": gateway.get_stats(),
            "rag": rag.get_stats(),
            "agents": agents.get_stats(),
            "model_router": model_router.get_stats(),
            "observability": {"traces": len(observability.tracer.get_traces(limit=10000))},
            "security": security.audit_logger.get_summary()
        }
    }
