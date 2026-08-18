import chromadb
from typing import List, Optional
from app.models import RetrievalResult
from config.settings import settings
import hashlib
import logging

logger = logging.getLogger(__name__)


class RAGPipeline:
    """RAG pipeline handling retrieval and context assembly."""

    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
        self.collection = self.client.get_or_create_collection(
            name="knowledge_base",
            metadata={"hnsw:space": "cosine"},
        )
        logger.info("RAG Pipeline initialized")

    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
        user_permissions: Optional[List[str]] = None,
    ) -> List[RetrievalResult]:
        where_filter = None
        if user_permissions:
            where_filter = {"department": {"$in": user_permissions}}

        results = self.collection.query(
            query_texts=[query],
            n_results=top_k,
            where=where_filter,
            include=["documents", "metadatas", "distances"],
        )

        retrieval_results = []
        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                retrieval_results.append(
                    RetrievalResult(
                        content=doc,
                        source=results["metadatas"][0][i].get("source", "unknown"),
                        score=1 - results["distances"][0][i],
                        metadata=results["metadatas"][0][i],
                    )
                )

        return retrieval_results

    def build_context(self, results: List[RetrievalResult]) -> str:
        if not results:
            return "No relevant documents found."

        context_parts = ["Relevant documents:\n"]
        for i, result in enumerate(results, 1):
            context_parts.append(
                f"[Document {i}] (Source: {result.source}, Relevance: {result.score:.2f})\n"
                f"{result.content}\n"
            )

        return "\n".join(context_parts)

    async def ingest_document(self, content: str, metadata: dict) -> str:
        doc_id = hashlib.md5(content.encode()).hexdigest()

        self.collection.add(
            documents=[content],
            metadatas=[metadata],
            ids=[doc_id],
        )

        logger.info(f"Document ingested: {doc_id}")
        return doc_id

    def health_check(self) -> dict:
        try:
            count = self.collection.count()
            return {"status": "healthy", "document_count": count}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
