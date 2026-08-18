from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import time
import logging

from app.models import (
    QueryRequest,
    QueryResponse,
    AutoQueryRequest,
    CompareRequest,
    ComparisonResult,
    BenchmarkRequest,
    BenchmarkResult,
    ModelInfo,
    MetricsResponse,
)
from app.model_router import router
from app.model_gateway import model_gateway
from app.model_comparator import comparator
from config.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI/ML Model Comparison & Routing",
    description="Day 02 - Model comparison, routing, and architecture trade-offs",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check with model status."""
    return {
        "status": "healthy",
        "version": "0.2.0",
        "gateway": model_gateway.health_check(),
    }


@app.post("/query", response_model=QueryResponse)
async def query_single_model(request: QueryRequest):
    """Query a specific model."""
    start_time = time.time()

    try:
        model = request.model or settings.default_model

        response = await model_gateway.generate(
            query=request.query,
            context="",
            model=model,
        )

        # Get routing decision for reference
        complexity, _, reason = router.get_routing_info(request.query)

        return QueryResponse(
            answer=response.content,
            model_used=response.model_used,
            routing_decision=complexity,
            tokens_used=response.tokens_used,
            latency_ms=response.latency_ms,
            cost_estimate=response.cost_estimate,
        )

    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query/auto", response_model=QueryResponse)
async def query_auto_routed(request: AutoQueryRequest):
    """Auto-route query based on complexity."""
    start_time = time.time()

    try:
        # Get routing decision
        complexity, model, reason = router.get_routing_info(request.query)

        # Override model if forced
        if request.force_model:
            model = request.force_model

        logger.info(
            f"Routing: {request.query[:50]}... -> {model} ({complexity.value})"
        )

        response = await model_gateway.generate(
            query=request.query,
            context="",
            model=model,
        )

        return QueryResponse(
            answer=response.content,
            model_used=response.model_used,
            routing_decision=complexity,
            tokens_used=response.tokens_used,
            latency_ms=response.latency_ms,
            cost_estimate=response.cost_estimate,
        )

    except Exception as e:
        logger.error(f"Auto query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/compare", response_model=ComparisonResult)
async def compare_models(request: CompareRequest):
    """Compare response from multiple models."""
    try:
        result = await comparator.compare(
            query=request.query,
            models=request.models,
            metrics=request.metrics,
        )
        return result

    except Exception as e:
        logger.error(f"Comparison failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/models")
async def list_models():
    """List available models and their characteristics."""
    models = []
    for model_id, info in settings.model_info.items():
        models.append(
            ModelInfo(
                id=model_id,
                name=info["name"],
                provider=info["provider"],
                context_window=info["context_window"],
                input_cost_per_1k=info["input_cost"],
                output_cost_per_1k=info["output_cost"],
                estimated_latency_ms=info["latency_ms"],
                tier=info["tier"],
            )
        )
    return models


@app.post("/benchmark")
async def run_benchmark(request: BenchmarkRequest):
    """Run benchmark against test prompts."""
    try:
        results = await comparator.run_benchmark(
            models=request.models,
            category=request.category,
            iterations=request.iterations,
        )

        # Calculate summaries
        summaries = []
        for model in request.models:
            summary = comparator.calculate_benchmark_summary(results, model)
            summaries.append(summary)

        return {
            "results": results,
            "summaries": summaries,
        }

    except Exception as e:
        logger.error(f"Benchmark failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics", response_model=MetricsResponse)
async def get_metrics():
    """Get usage metrics."""
    usage = model_gateway.get_usage_summary()

    return MetricsResponse(
        total_requests=sum(model_gateway.token_usage.values()),
        total_tokens=usage["total_tokens"],
        total_cost=usage["total_cost"],
        avg_latency_ms=0,  # Would need to track this
        requests_by_model={},
        cost_by_model=usage["cost_by_model"],
    )


@app.get("/classify")
async def classify_query(query: str):
    """Classify a query's complexity (for debugging/testing)."""
    complexity, model, reason = router.get_routing_info(query)
    return {
        "query": query,
        "complexity": complexity.value,
        "selected_model": model,
        "reason": reason,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
