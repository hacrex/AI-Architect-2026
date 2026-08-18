from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List
import time
import logging

from app.models import QueryRequest, QueryResponse, HealthResponse
from app.rag import RAGPipeline
from app.model_gateway import ModelGateway
from app.auth import get_current_user, User
from app.observability import MetricsCollector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Knowledge Assistant",
    description="Enterprise RAG-based knowledge assistant - Day 01 Sample",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_pipeline = RAGPipeline()
model_gateway = ModelGateway()
metrics = MetricsCollector()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(round(process_time, 4))
    metrics.record_request_latency(process_time)
    return response


@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        components={
            "rag": rag_pipeline.health_check(),
            "model_gateway": model_gateway.health_check(),
        },
    )


@app.post("/query", response_model=QueryResponse)
async def query_knowledge_base(
    request: QueryRequest,
    user: User = Depends(get_current_user),
):
    start_time = time.time()

    try:
        retrieval_results = await rag_pipeline.retrieve(
            query=request.query,
            top_k=request.top_k or 5,
            user_permissions=user.document_permissions,
        )

        context = rag_pipeline.build_context(retrieval_results)

        response = await model_gateway.generate(
            query=request.query,
            context=context,
            model=request.model or settings.default_model,
        )

        metrics.record_successful_query()

        return QueryResponse(
            answer=response.content,
            sources=[r.source for r in retrieval_results],
            model=response.model_used,
            tokens_used=response.tokens_used,
            latency_ms=round((time.time() - start_time) * 1000, 2),
        )

    except Exception as e:
        metrics.record_failed_query()
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query/stream")
async def query_knowledge_base_stream(
    request: QueryRequest,
    user: User = Depends(get_current_user),
):
    async def generate_stream():
        retrieval_results = await rag_pipeline.retrieve(
            query=request.query,
            top_k=request.top_k or 5,
            user_permissions=user.document_permissions,
        )

        context = rag_pipeline.build_context(retrieval_results)

        async for chunk in model_gateway.generate_stream(
            query=request.query,
            context=context,
            model=request.model or settings.default_model,
        ):
            yield chunk

    return StreamingResponse(generate_stream(), media_type="text/event-stream")


@app.post("/ingest")
async def ingest_document(
    content: str,
    metadata: dict,
    user: User = Depends(get_current_user),
):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    doc_id = await rag_pipeline.ingest_document(content, metadata)
    return {"document_id": doc_id, "status": "ingested"}


@app.get("/metrics")
async def get_metrics(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return metrics.get_summary()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
