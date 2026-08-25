"""RAG Monitor — observe retrieval quality, relevance, and context assembly."""
import uuid
from datetime import datetime
from app.models import RAGEvent
import config.settings as settings


class RAGMonitor:
    """Monitor RAG pipeline quality with retrieval and relevance tracking."""

    def __init__(self):
        self._events: list[RAGEvent] = []

    def record_event(self, query: str, documents_retrieved: int,
                     retrieval_ms: float, query_embedding_ms: float = 0.0,
                     reranking_ms: float = 0.0, documents_reranked: int = 0,
                     top_relevance_score: float = 0.0, avg_relevance_score: float = 0.0,
                     context_tokens: int = 0, authorized: bool = True,
                     filtered_count: int = 0, trace_id: str = "",
                     span_id: str = "") -> RAGEvent:
        event = RAGEvent(
            trace_id=trace_id or uuid.uuid4().hex[:16],
            span_id=span_id or uuid.uuid4().hex[:12],
            query=query,
            query_embedding_ms=query_embedding_ms,
            retrieval_ms=retrieval_ms,
            reranking_ms=reranking_ms,
            documents_retrieved=documents_retrieved,
            documents_reranked=documents_reranked,
            top_relevance_score=top_relevance_score,
            avg_relevance_score=avg_relevance_score,
            context_tokens=context_tokens,
            authorized=authorized,
            filtered_count=filtered_count
        )
        self._events.append(event)
        return event

    def get_summary(self) -> dict:
        if not self._events:
            return {"total_events": 0}
        retrieval_latencies = [e.retrieval_ms for e in self._events]
        relevance_scores = [e.top_relevance_score for e in self._events]
        doc_counts = [e.documents_retrieved for e in self._events]
        context_sizes = [e.context_tokens for e in self._events]
        authorized = sum(1 for e in self._events if e.authorized)
        return {
            "total_events": len(self._events),
            "avg_retrieval_ms": round(sum(retrieval_latencies) / len(retrieval_latencies), 1),
            "p95_retrieval_ms": round(sorted(retrieval_latencies)[int(len(retrieval_latencies) * 0.95)], 1) if retrieval_latencies else 0,
            "avg_relevance_score": round(sum(relevance_scores) / len(relevance_scores), 4) if relevance_scores else 0,
            "avg_documents_retrieved": round(sum(doc_counts) / len(doc_counts), 1) if doc_counts else 0,
            "avg_context_tokens": round(sum(context_sizes) / len(context_sizes), 0) if context_sizes else 0,
            "authorization_pass_rate": round(authorized / len(self._events) * 100, 1),
            "low_relevance_count": sum(1 for s in relevance_scores if s < settings.RAG_RELEVANCE_THRESHOLD),
        }

    def get_relevance_distribution(self) -> dict:
        scores = [e.top_relevance_score for e in self._events]
        if not scores:
            return {"bins": []}
        bins = {"0.0-0.2": 0, "0.2-0.4": 0, "0.4-0.6": 0, "0.6-0.8": 0, "0.8-1.0": 0}
        for s in scores:
            if s < 0.2: bins["0.0-0.2"] += 1
            elif s < 0.4: bins["0.2-0.4"] += 1
            elif s < 0.6: bins["0.4-0.6"] += 1
            elif s < 0.8: bins["0.6-0.8"] += 1
            else: bins["0.8-1.0"] += 1
        total = len(scores)
        return {
            "bins": {k: {"count": v, "pct": round(v / total * 100, 1)} for k, v in bins.items()},
            "below_threshold": sum(1 for s in scores if s < settings.RAG_RELEVANCE_THRESHOLD)
        }

    def get_latency_breakdown(self) -> dict:
        if not self._events:
            return {}
        embedding = [e.query_embedding_ms for e in self._events if e.query_embedding_ms > 0]
        retrieval = [e.retrieval_ms for e in self._events]
        reranking = [e.reranking_ms for e in self._events if e.reranking_ms > 0]
        return {
            "embedding": {
                "avg_ms": round(sum(embedding) / len(embedding), 1) if embedding else 0,
                "p95_ms": round(sorted(embedding)[int(len(embedding) * 0.95)], 1) if len(embedding) > 1 else 0,
            },
            "retrieval": {
                "avg_ms": round(sum(retrieval) / len(retrieval), 1) if retrieval else 0,
                "p95_ms": round(sorted(retrieval)[int(len(retrieval) * 0.95)], 1) if len(retrieval) > 1 else 0,
            },
            "reranking": {
                "avg_ms": round(sum(reranking) / len(reranking), 1) if reranking else 0,
                "p95_ms": round(sorted(reranking)[int(len(reranking) * 0.95)], 1) if len(reranking) > 1 else 0,
            }
        }

    def list_events(self, limit: int = 50) -> list[dict]:
        return [
            {
                "trace_id": e.trace_id,
                "query_preview": e.query[:80],
                "documents_retrieved": e.documents_retrieved,
                "retrieval_ms": e.retrieval_ms,
                "top_relevance": e.top_relevance_score,
                "context_tokens": e.context_tokens,
                "authorized": e.authorized,
                "timestamp": e.timestamp.isoformat()
            }
            for e in self._events[-limit:]
        ]
