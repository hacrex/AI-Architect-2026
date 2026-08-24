"""End-to-end request pipeline simulation."""
import time
import uuid
from datetime import datetime
from app.gateway import AIGateway
from app.rag import RAGService
from app.agents import AgentService
from app.model_router import ModelRouter
from app.context import ContextAssembler
from app.observability import ObservabilityService
from app.security import SecurityService
from app.models import AIRequest, SecurityContext


class RequestPipeline:
    """Simulate the complete request pipeline."""

    def __init__(self):
        self.gateway = AIGateway()
        self.rag = RAGService()
        self.agents = AgentService()
        self.model_router = ModelRouter()
        self.context_assembler = ContextAssembler()
        self.observability = ObservabilityService()
        self.security = SecurityService()

    def process(self, query: str, user_id: str, use_agent: bool = False) -> dict:
        start = time.time()
        request_id = f"pipe-{uuid.uuid4().hex[:8]}"

        sec_ctx = self.security.get_security_context(user_id)

        gw_result = self.gateway.process_request(
            AIRequest(query=query, user_id=user_id, use_agent=use_agent),
            sec_ctx
        )

        rag_result = self.rag.retrieve(query=query, user_roles=sec_ctx.roles)

        agent_result = None
        if use_agent:
            agent_result = self.agents.run(query=query, context=rag_result["context"], user_roles=sec_ctx.roles)

        assembled = self.context_assembler.assemble(query=query, rag_context=rag_result, agent_results=agent_result)

        model = self.model_router.select_model()
        tokens = assembled["estimated_tokens"]
        cost = self.model_router.estimate_cost(model.model_name, tokens, tokens * 2)
        latency = (time.time() - start) * 1000

        self.observability.record_request(request_id, user_id, model.model_name, model.provider.value, tokens, tokens * 2, latency, cost)

        return {
            "request_id": request_id,
            "query": query,
            "user_id": user_id,
            "model": model.model_name,
            "provider": model.provider.value,
            "tokens": tokens,
            "cost_usd": cost,
            "latency_ms": round(latency, 2),
            "rag_chunks": rag_result["raw_count"],
            "agent_used": use_agent,
            "status": "completed"
        }


class IngestionPipeline:
    """Simulate document ingestion pipeline."""

    def __init__(self):
        self.rag = RAGService()

    def ingest(self, source: str, content: str, category: str = "general") -> dict:
        result = self.rag.ingest_document(content, source, category, ["all"])
        return {
            "source": source,
            "category": category,
            "status": result["status"],
            "chunk_id": result["chunk_id"],
            "timestamp": datetime.utcnow().isoformat()
        }

    def batch_ingest(self, documents: list[dict]) -> list[dict]:
        results = []
        for doc in documents:
            result = self.ingest(
                source=doc.get("source", "unknown"),
                content=doc.get("content", ""),
                category=doc.get("category", "general")
            )
            results.append(result)
        return results
