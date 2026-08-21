from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import time
import logging
import asyncio

from app.models import (
    InferenceRequest,
    InferenceResponse,
    BatchInferenceRequest,
    BatchInferenceResponse,
    HealthResponse,
    ModelInfoResponse,
    MetricsResponse,
)
from app.inference import InferenceEngine, BatchScheduler
from app.health import MetricsCollector
from config.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Infrastructure — Inference Server",
    description="Day 04 - Inference serving, batching, and monitoring",
    version="0.4.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
engine = InferenceEngine(
    model_name=settings.model_name,
    device=settings.model_device,
)
batch_scheduler = BatchScheduler(
    max_batch_size=settings.batch_size,
    timeout_ms=settings.batch_timeout_ms,
)
metrics = MetricsCollector()


@app.on_event("startup")
async def startup():
    """Load model on startup."""
    logger.info("Starting inference server...")
    await engine.load_model()
    logger.info("Inference server ready")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check with GPU status."""
    return HealthResponse(
        status="healthy",
        version="0.4.0",
        model_loaded=engine.is_loaded(),
        gpu_available=settings.model_device == "cuda",
        gpu_memory_used=None,  # Would query actual GPU in production
        gpu_memory_total=None,
        uptime_seconds=round(time.time() - engine._start_time, 2),
    )


@app.post("/inference", response_model=InferenceResponse)
async def inference(request: InferenceRequest):
    """Single prompt inference."""
    start_time = time.time()

    try:
        result = await engine.generate(
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )

        latency_ms = (time.time() - start_time) * 1000

        metrics.record_request(
            latency_ms=latency_ms,
            tokens_generated=result["tokens_generated"],
        )

        return InferenceResponse(
            generated_text=result["generated_text"],
            tokens_generated=result["tokens_generated"],
            latency_ms=round(latency_ms, 2),
            model_used=result["model_used"],
            batch_size=1,
        )

    except Exception as e:
        logger.error(f"Inference failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/inference/stream")
async def inference_stream(request: InferenceRequest):
    """Streaming inference."""
    async def generate():
        async for chunk in engine.generate_stream(
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        ):
            yield chunk

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.post("/inference/batch", response_model=BatchInferenceResponse)
async def inference_batch(request: BatchInferenceRequest):
    """Batch inference (multiple prompts)."""
    start_time = time.time()

    try:
        results = await engine.batch_generate(
            prompts=request.prompts,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )

        total_latency_ms = (time.time() - start_time) * 1000
        avg_latency_ms = total_latency_ms / len(results)

        # Record metrics for each item
        for result in results:
            metrics.record_request(
                latency_ms=result["latency_ms"],
                tokens_generated=result["tokens_generated"],
                batch_size=len(results),
            )

        throughput = len(results) / (total_latency_ms / 1000) if total_latency_ms > 0 else 0

        return BatchInferenceResponse(
            results=[InferenceResponse(**r) for r in results],
            total_latency_ms=round(total_latency_ms, 2),
            avg_latency_ms=round(avg_latency_ms, 2),
            throughput_per_second=round(throughput, 2),
        )

    except Exception as e:
        logger.error(f"Batch inference failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
async def get_metrics():
    """Get performance metrics (Prometheus format)."""
    return metrics.get_prometheus_metrics()


@app.get("/metrics/json", response_model=MetricsResponse)
async def get_metrics_json():
    """Get performance metrics (JSON format)."""
    summary = metrics.get_summary()
    return MetricsResponse(**summary)


@app.get("/model/info", response_model=ModelInfoResponse)
async def model_info():
    """Get model information."""
    info = engine.get_info()
    return ModelInfoResponse(
        model_name=info["model_name"],
        model_device=info["device"],
        max_tokens=settings.max_tokens,
        batch_size=settings.batch_size,
    )


@app.post("/model/reload")
async def model_reload():
    """Hot-reload model (admin)."""
    await engine.unload_model()
    await engine.load_model()
    return {"status": "reloaded", "model": settings.model_name}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
