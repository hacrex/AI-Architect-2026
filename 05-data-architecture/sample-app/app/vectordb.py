"""Vector database operations."""
import uuid
from typing import Optional
from datetime import datetime


class VectorStore:
    """In-memory vector store for demonstration."""
    
    def __init__(self, dimensions: int = 384):
        self.dimensions = dimensions
        self._vectors: dict[str, dict] = {}
        self._index: dict[str, list[float]] = {}
    
    def upsert(
        self,
        chunk_id: str,
        vector: list[float],
        metadata: dict
    ) -> str:
        """
        Insert or update a vector.
        
        Args:
            chunk_id: Unique identifier
            vector: Embedding vector
            metadata: Associated metadata
            
        Returns:
            Chunk ID
        """
        self._vectors[chunk_id] = {
            "id": chunk_id,
            "metadata": metadata,
            "created_at": datetime.now().isoformat()
        }
        self._index[chunk_id] = vector
        return chunk_id
    
    def search(
        self,
        query_vector: list[float],
        top_k: int = 10,
        filters: Optional[dict] = None
    ) -> list[dict]:
        """
        Search for similar vectors.
        
        Args:
            query_vector: Query embedding
            top_k: Number of results
            filters: Metadata filters
            
        Returns:
            List of search results
        """
        scores = []
        
        for chunk_id, vector in self._index.items():
            if filters:
                metadata = self._vectors[chunk_id]["metadata"]
                if not self._apply_filters(metadata, filters):
                    continue
            
            score = self._cosine_similarity(query_vector, vector)
            scores.append({
                "chunk_id": chunk_id,
                "score": score,
                "metadata": self._vectors[chunk_id]["metadata"]
            })
        
        scores.sort(key=lambda x: x["score"], reverse=True)
        return scores[:top_k]
    
    def delete(self, chunk_id: str) -> bool:
        """
        Delete a vector.
        
        Args:
            chunk_id: Chunk identifier
            
        Returns:
            True if deleted, False if not found
        """
        if chunk_id in self._vectors:
            del self._vectors[chunk_id]
            del self._index[chunk_id]
            return True
        return False
    
    def delete_by_document(self, document_id: str) -> int:
        """
        Delete all vectors for a document.
        
        Args:
            document_id: Document identifier
            
        Returns:
            Number of vectors deleted
        """
        to_delete = [
            chunk_id for chunk_id, data in self._vectors.items()
            if data["metadata"].get("document_id") == document_id
        ]
        
        for chunk_id in to_delete:
            del self._vectors[chunk_id]
            del self._index[chunk_id]
        
        return len(to_delete)
    
    def get(self, chunk_id: str) -> Optional[dict]:
        """
        Get a vector by ID.
        
        Args:
            chunk_id: Chunk identifier
            
        Returns:
            Vector data or None
        """
        return self._vectors.get(chunk_id)
    
    def count(self) -> int:
        """Get total number of vectors."""
        return len(self._vectors)
    
    def count_by_department(self) -> dict[str, int]:
        """Count vectors by department."""
        counts = {}
        for data in self._vectors.values():
            dept = data["metadata"].get("department", "unknown")
            counts[dept] = counts.get(dept, 0) + 1
        return counts
    
    def count_by_classification(self) -> dict[str, int]:
        """Count vectors by classification."""
        counts = {}
        for data in self._vectors.values():
            classification = data["metadata"].get("classification", "unknown")
            counts[classification] = counts.get(classification, 0) + 1
        return counts
    
    def _cosine_similarity(self, a: list[float], b: list[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return dot_product / (norm_a * norm_b)
    
    def _apply_filters(self, metadata: dict, filters: dict) -> bool:
        """Apply metadata filters."""
        for key, value in filters.items():
            if key not in metadata:
                return False
            
            if isinstance(value, list):
                if metadata[key] not in value:
                    return False
            elif metadata[key] != value:
                return False
        
        return True


class MetadataStore:
    """Metadata store for documents."""
    
    def __init__(self):
        self._documents: dict[str, dict] = {}
    
    def upsert(self, document_id: str, metadata: dict) -> str:
        """Insert or update document metadata."""
        self._documents[document_id] = metadata
        return document_id
    
    def get(self, document_id: str) -> Optional[dict]:
        """Get document metadata."""
        return self._documents.get(document_id)
    
    def delete(self, document_id: str) -> bool:
        """Delete document metadata."""
        if document_id in self._documents:
            del self._documents[document_id]
            return True
        return False
    
    def list_all(self) -> list[dict]:
        """List all documents."""
        return list(self._documents.values())
    
    def count(self) -> int:
        """Get total number of documents."""
        return len(self._documents)
    
    def count_by_department(self) -> dict[str, int]:
        """Count documents by department."""
        counts = {}
        for metadata in self._documents.values():
            dept = metadata.get("department", "unknown")
            counts[dept] = counts.get(dept, 0) + 1
        return counts


class DocumentStore:
    """Document content store."""
    
    def __init__(self):
        self._documents: dict[str, dict] = {}
    
    def store(self, document_id: str, content: str, metadata: dict) -> str:
        """Store document content."""
        self._documents[document_id] = {
            "content": content,
            "metadata": metadata
        }
        return document_id
    
    def get(self, document_id: str) -> Optional[dict]:
        """Get document content."""
        return self._documents.get(document_id)
    
    def delete(self, document_id: str) -> bool:
        """Delete document."""
        if document_id in self._documents:
            del self._documents[document_id]
            return True
        return False
    
    def exists(self, document_id: str) -> bool:
        """Check if document exists."""
        return document_id in self._documents
