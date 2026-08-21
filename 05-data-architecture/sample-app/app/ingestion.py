"""Document ingestion pipeline."""
import uuid
from datetime import datetime
from typing import Optional

from .chunker import chunk_document
from .metadata import extract_metadata
from .embeddings import get_embedding_provider
from .vectordb import VectorStore, MetadataStore, DocumentStore


class IngestionPipeline:
    """Complete ingestion pipeline for documents."""
    
    def __init__(
        self,
        vector_store: VectorStore,
        metadata_store: MetadataStore,
        document_store: DocumentStore,
        embedding_provider=None,
        chunking_strategy: str = "structure",
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ):
        self.vector_store = vector_store
        self.metadata_store = metadata_store
        self.document_store = document_store
        self.embedding_provider = embedding_provider or get_embedding_provider("mock")
        self.chunking_strategy = chunking_strategy
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def ingest_document(
        self,
        document_id: str,
        title: str,
        content: str,
        department: Optional[str] = None,
        classification: Optional[str] = None,
        owner: Optional[str] = None,
    ) -> dict:
        """
        Ingest a document through the complete pipeline.
        
        Args:
            document_id: Document identifier
            title: Document title
            content: Document content
            department: Override department
            classification: Override classification
            owner: Document owner
            
        Returns:
            Ingestion result
        """
        metadata = extract_metadata(
            document_id=document_id,
            title=title,
            content=content,
            department=department,
            classification=classification,
            owner=owner,
        )
        
        self.document_store.store(document_id, content, metadata)
        self.metadata_store.upsert(document_id, metadata)
        
        chunks = chunk_document(
            text=content,
            strategy=self.chunking_strategy,
            chunk_size=self.chunk_size,
            overlap=self.chunk_overlap,
        )
        
        chunk_ids = []
        for chunk in chunks:
            chunk_id = f"{document_id}_chunk_{chunk['chunk_index']}"
            
            chunk_metadata = {
                "document_id": document_id,
                "title": title,
                "text": chunk["text"],
                "chunk_index": chunk["chunk_index"],
                "token_count": chunk["token_count"],
                "department": metadata["department"],
                "classification": metadata["classification"],
                "source": f"{title} (chunk {chunk['chunk_index'] + 1})",
                "version": metadata["version"],
                "strategy": chunk.get("strategy", self.chunking_strategy),
            }
            
            embedding = self.embedding_provider.embed(chunk["text"])
            
            self.vector_store.upsert(chunk_id, embedding, chunk_metadata)
            chunk_ids.append(chunk_id)
        
        return {
            "document_id": document_id,
            "title": title,
            "department": metadata["department"],
            "classification": metadata["classification"],
            "chunk_count": len(chunks),
            "chunk_ids": chunk_ids,
            "ingested_at": datetime.now().isoformat(),
        }
    
    def delete_document(self, document_id: str) -> dict:
        """
        Delete a document and all its chunks.
        
        Args:
            document_id: Document identifier
            
        Returns:
            Deletion result
        """
        chunks_deleted = self.vector_store.delete_by_document(document_id)
        metadata_deleted = self.metadata_store.delete(document_id)
        document_deleted = self.document_store.delete(document_id)
        
        return {
            "document_id": document_id,
            "chunks_deleted": chunks_deleted,
            "metadata_deleted": metadata_deleted,
            "document_deleted": document_deleted,
        }
    
    def get_stats(self) -> dict:
        """Get ingestion statistics."""
        return {
            "total_documents": self.metadata_store.count(),
            "total_chunks": self.vector_store.count(),
            "chunks_by_department": self.vector_store.count_by_department(),
            "chunks_by_classification": self.vector_store.count_by_classification(),
            "avg_chunk_size": self._calculate_avg_chunk_size(),
            "embedding_dimensions": self.vector_store.dimensions,
        }
    
    def _calculate_avg_chunk_size(self) -> float:
        """Calculate average chunk size."""
        count = self.vector_store.count()
        if count == 0:
            return 0.0
        
        total_tokens = sum(
            data["metadata"].get("token_count", 0)
            for data in self.vector_store._vectors.values()
        )
        
        return total_tokens / count
