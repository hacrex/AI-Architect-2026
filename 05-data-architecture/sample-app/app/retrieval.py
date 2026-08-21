"""Retrieval layer with hybrid search and permissions."""
import time
from typing import Optional

from .embeddings import get_embedding_provider
from .vectordb import VectorStore
from .auth import UserContext, PermissionChecker


class RetrievalEngine:
    """Hybrid retrieval with permission filtering."""
    
    def __init__(
        self,
        vector_store: VectorStore,
        embedding_provider=None,
        permission_checker: Optional[PermissionChecker] = None,
    ):
        self.vector_store = vector_store
        self.embedding_provider = embedding_provider or get_embedding_provider("mock")
        self.permission_checker = permission_checker or PermissionChecker()
    
    def hybrid_search(
        self,
        query: str,
        user_context: UserContext,
        top_k: int = 10,
        use_hybrid: bool = True,
        use_reranking: bool = True,
    ) -> dict:
        """
        Perform hybrid search with permission filtering.
        
        Args:
            query: Search query
            user_context: User context for permissions
            top_k: Number of results
            use_hybrid: Use hybrid search (keyword + vector)
            use_reranking: Apply reranking
            
        Returns:
            Search results
        """
        start_time = time.time()
        
        query_embedding = self.embedding_provider.embed(query)
        
        candidate_limit = top_k * 5 if use_reranking else top_k
        
        vector_results = self.vector_store.search(
            query_vector=query_embedding,
            top_k=candidate_limit,
        )
        
        if use_hybrid:
            keyword_results = self._keyword_search(query, candidate_limit)
            results = self._merge_results(vector_results, keyword_results)
        else:
            results = vector_results
        
        filtered_results = [
            r for r in results
            if self.permission_checker.has_permission(user_context, r["metadata"])
        ]
        
        if use_reranking and len(filtered_results) > top_k:
            filtered_results = self._rerank(query, filtered_results)
        
        final_results = filtered_results[:top_k]
        
        for i, result in enumerate(final_results):
            result["rank"] = i + 1
        
        latency_ms = (time.time() - start_time) * 1000
        
        return {
            "query": query,
            "results": final_results,
            "total_results": len(final_results),
            "latency_ms": latency_ms,
        }
    
    def _keyword_search(self, query: str, top_k: int) -> list[dict]:
        """
        Simple keyword search.
        
        Args:
            query: Search query
            top_k: Number of results
            
        Returns:
            Search results
        """
        query_words = set(query.lower().split())
        results = []
        
        for chunk_id, data in self.vector_store._vectors.items():
            text = data["metadata"].get("text", "").lower()
            text_words = set(text.split())
            
            overlap = len(query_words & text_words)
            if overlap > 0:
                score = overlap / len(query_words)
                results.append({
                    "chunk_id": chunk_id,
                    "score": score,
                    "metadata": data["metadata"],
                    "source": "keyword"
                })
        
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
    
    def _merge_results(
        self,
        vector_results: list[dict],
        keyword_results: list[dict],
        vector_weight: float = 0.7,
        keyword_weight: float = 0.3,
    ) -> list[dict]:
        """
        Merge vector and keyword results.
        
        Args:
            vector_results: Vector search results
            keyword_results: Keyword search results
            vector_weight: Weight for vector scores
            keyword_weight: Weight for keyword scores
            
        Returns:
            Merged results
        """
        scores = {}
        
        for result in vector_results:
            chunk_id = result["chunk_id"]
            scores[chunk_id] = {
                "vector_score": result["score"],
                "keyword_score": 0.0,
                "metadata": result["metadata"],
            }
        
        for result in keyword_results:
            chunk_id = result["chunk_id"]
            if chunk_id in scores:
                scores[chunk_id]["keyword_score"] = result["score"]
            else:
                scores[chunk_id] = {
                    "vector_score": 0.0,
                    "keyword_score": result["score"],
                    "metadata": result["metadata"],
                }
        
        merged = []
        for chunk_id, score_data in scores.items():
            combined_score = (
                vector_weight * score_data["vector_score"] +
                keyword_weight * score_data["keyword_score"]
            )
            merged.append({
                "chunk_id": chunk_id,
                "score": combined_score,
                "metadata": score_data["metadata"],
            })
        
        merged.sort(key=lambda x: x["score"], reverse=True)
        return merged
    
    def _rerank(self, query: str, results: list[dict]) -> list[dict]:
        """
        Rerank results based on query relevance.
        
        Args:
            query: Search query
            results: Initial results
            
        Returns:
            Reranked results
        """
        query_words = set(query.lower().split())
        
        for result in results:
            text = result["metadata"].get("text", "").lower()
            
            text_words = set(text.split())
            word_overlap = len(query_words & text_words) / max(len(query_words), 1)
            
            has_heading = "heading" in result["metadata"]
            heading_bonus = 0.1 if has_heading else 0.0
            
            result["rerank_score"] = result["score"] * 0.7 + word_overlap * 0.2 + heading_bonus
        
        results.sort(key=lambda x: x.get("rerank_score", x["score"]), reverse=True)
        return results
