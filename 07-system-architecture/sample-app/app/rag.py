"""RAG subsystem — retrieval, reranking, and context building."""
import uuid
import random
from datetime import datetime
from typing import Optional
from app.models import RetrievalResult


class VectorStore:
    """Simulated vector store with metadata filtering."""

    def __init__(self):
        self._documents: list[dict] = []
        self._seed_documents()

    def _seed_documents(self):
        sources = [
            {"source": "hr/policy-remote-work.md", "category": "hr", "access": ["all"]},
            {"source": "hr/policy-pto.md", "category": "hr", "access": ["all"]},
            {"source": "security/data-classification.md", "category": "security", "access": ["admin", "security"]},
            {"source": "engineering/architecture-guide.md", "category": "engineering", "access": ["engineering"]},
            {"source": "finance/expense-policy.md", "category": "finance", "access": ["all"]},
            {"source": "legal/data-privacy.md", "category": "legal", "access": ["legal", "admin"]},
            {"source": "engineering/api-standards.md", "category": "engineering", "access": ["engineering"]},
            {"source": "hr/benefits-overview.md", "category": "hr", "access": ["all"]},
        ]

        chunks_per_doc = 3
        for doc in sources:
            for i in range(chunks_per_doc):
                self._documents.append({
                    "chunk_id": f"{doc['source']}-{i}",
                    "content": f"Content from {doc['source']} chunk {i}. "
                              f"This covers important information about {doc['category']} policies.",
                    "source": doc["source"],
                    "category": doc["category"],
                    "access": doc["access"],
                    "embedding": [random.uniform(-1, 1) for _ in range(128)]
                })

    def search(self, query_embedding: list[float], top_k: int = 5,
               access_filter: list[str] = None, category_filter: str = None) -> list[dict]:
        results = []
        for doc in self._documents:
            if access_filter and not any(a in doc.get("access", []) for a in access_filter):
                if "all" not in doc.get("access", []):
                    continue

            if category_filter and doc.get("category") != category_filter:
                continue

            score = random.uniform(0.5, 0.99)
            results.append({
                "chunk_id": doc["chunk_id"],
                "content": doc["content"],
                "source": doc["source"],
                "score": round(score, 3),
                "metadata": {
                    "category": doc["category"],
                    "access": doc["access"]
                }
            })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def add_document(self, content: str, source: str, category: str,
                     access: list[str], embedding: list[float]):
        doc = {
            "chunk_id": f"{source}-{uuid.uuid4().hex[:6]}",
            "content": content,
            "source": source,
            "category": category,
            "access": access,
            "embedding": embedding
        }
        self._documents.append(doc)
        return doc

    def get_document_count(self) -> int:
        return len(self._documents)


class Reranker:
    """Simulated reranker for retrieval results."""

    def rerank(self, query: str, results: list[dict], top_k: int = 3) -> list[dict]:
        for r in results:
            r["score"] = round(r["score"] * random.uniform(0.9, 1.1), 3)
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]


class ContextBuilder:
    """Build context from retrieved chunks."""

    def __init__(self, max_tokens: int = 4096):
        self.max_tokens = max_tokens

    def build(self, query: str, chunks: list[dict]) -> dict:
        context_parts = []
        sources = []
        tokens_used = 0

        for chunk in chunks:
            estimated_tokens = len(chunk["content"].split()) * 1.3
            if tokens_used + estimated_tokens > self.max_tokens:
                break

            context_parts.append(chunk["content"])
            sources.append({
                "source": chunk["source"],
                "score": chunk["score"],
                "chunk_id": chunk["chunk_id"]
            })
            tokens_used += estimated_tokens

        return {
            "context": "\n\n".join(context_parts),
            "sources": sources,
            "tokens_used": int(tokens_used),
            "chunks_used": len(context_parts)
        }


class RAGService:
    """Complete RAG subsystem."""

    def __init__(self):
        self.vector_store = VectorStore()
        self.reranker = Reranker()
        self.context_builder = ContextBuilder()

    def retrieve(self, query: str, user_roles: list[str] = None,
                 top_k: int = 5, category: str = None) -> dict:
        query_embedding = [random.uniform(-1, 1) for _ in range(128)]

        access_filter = user_roles or ["all"]
        raw_results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            access_filter=access_filter,
            category_filter=category
        )

        reranked = self.reranker.rerank(query, raw_results, top_k=3)

        context = self.context_builder.build(query, reranked)

        return {
            "query": query,
            "raw_count": len(raw_results),
            "reranked_count": len(reranked),
            "context": context["context"],
            "sources": context["sources"],
            "tokens_used": context["tokens_used"]
        }

    def ingest_document(self, content: str, source: str, category: str,
                        access: list[str]) -> dict:
        embedding = [random.uniform(-1, 1) for _ in range(128)]
        doc = self.vector_store.add_document(content, source, category, access, embedding)
        return {
            "status": "ingested",
            "chunk_id": doc["chunk_id"],
            "source": source
        }

    def get_stats(self) -> dict:
        return {
            "total_documents": self.vector_store.get_document_count(),
            "vector_store": "simulated",
            "reranker": "simulated"
        }
