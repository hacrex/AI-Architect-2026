"""Bulk ingestion script for sample documents."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.vectordb import VectorStore, MetadataStore, DocumentStore
from app.embeddings import get_embedding_provider
from app.ingestion import IngestionPipeline


SAMPLE_DOCUMENTS = [
    {
        "document_id": "eng-001",
        "title": "Kubernetes Deployment Guide",
        "department": "engineering",
        "classification": "internal",
        "file": "docs/engineering/kubernetes-guide.md"
    },
    {
        "document_id": "hr-001",
        "title": "Leave Policy 2026",
        "department": "hr",
        "classification": "internal",
        "file": "docs/hr/leave-policy.md"
    },
    {
        "document_id": "sec-001",
        "title": "Security Policy",
        "department": "security",
        "classification": "confidential",
        "file": "docs/security/security-policy.md"
    },
]


def main():
    print("=== Document Ingestion ===\n")
    
    vector_store = VectorStore(dimensions=384)
    metadata_store = MetadataStore()
    document_store = DocumentStore()
    embedding_provider = get_embedding_provider("mock")
    
    pipeline = IngestionPipeline(
        vector_store=vector_store,
        metadata_store=metadata_store,
        document_store=document_store,
        embedding_provider=embedding_provider,
        chunking_strategy="structure",
    )
    
    for doc_info in SAMPLE_DOCUMENTS:
        file_path = Path(__file__).parent.parent / doc_info["file"]
        
        if not file_path.exists():
            print(f"Warning: {file_path} not found, skipping")
            continue
        
        content = file_path.read_text()
        
        result = pipeline.ingest_document(
            document_id=doc_info["document_id"],
            title=doc_info["title"],
            content=content,
            department=doc_info["department"],
            classification=doc_info["classification"],
        )
        
        print(f"Ingested: {result['title']}")
        print(f"  Department: {result['department']}")
        print(f"  Classification: {result['classification']}")
        print(f"  Chunks: {result['chunk_count']}")
        print()
    
    stats = pipeline.get_stats()
    print("=== Ingestion Complete ===")
    print(f"Total documents: {stats['total_documents']}")
    print(f"Total chunks: {stats['total_chunks']}")
    print(f"Chunks by department: {stats['chunks_by_department']}")
    print(f"Avg chunk size: {stats['avg_chunk_size']:.1f} tokens")


if __name__ == "__main__":
    main()
