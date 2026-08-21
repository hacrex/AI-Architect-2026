"""Permission verification script."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.vectordb import VectorStore, MetadataStore, DocumentStore
from app.embeddings import get_embedding_provider
from app.ingestion import IngestionPipeline
from app.retrieval import RetrievalEngine
from app.auth import get_user_context, PermissionChecker


def main():
    print("=== Permission Verification ===\n")
    
    vector_store = VectorStore(dimensions=384)
    metadata_store = MetadataStore()
    document_store = DocumentStore()
    embedding_provider = get_embedding_provider("mock")
    permission_checker = PermissionChecker()
    
    pipeline = IngestionPipeline(
        vector_store=vector_store,
        metadata_store=metadata_store,
        document_store=document_store,
        embedding_provider=embedding_provider,
    )
    
    pipeline.ingest_document(
        document_id="eng-001",
        title="Kubernetes Guide",
        content="# Kubernetes\n\nThis guide covers Kubernetes deployment.",
        department="engineering",
        classification="internal",
    )
    
    pipeline.ingest_document(
        document_id="hr-001",
        title="Leave Policy",
        content="# Leave Policy\n\nAnnual leave is 20 days.",
        department="hr",
        classification="internal",
    )
    
    retrieval = RetrievalEngine(
        vector_store=vector_store,
        embedding_provider=embedding_provider,
        permission_checker=permission_checker,
    )
    
    test_cases = [
        ("alice@company.com", "How do I deploy?"),
        ("alice@company.com", "What is the leave policy?"),
        ("bob@company.com", "How do I deploy?"),
        ("bob@company.com", "What is the leave policy?"),
        ("admin@company.com", "How do I deploy?"),
        ("admin@company.com", "What is the leave policy?"),
    ]
    
    print("Testing permission filtering:\n")
    
    for user_id, query in test_cases:
        user_context = get_user_context(user_id)
        result = retrieval.hybrid_search(
            query=query,
            user_context=user_context,
            top_k=5,
            use_reranking=False,
        )
        
        user_dept = user_context.department if user_context else "unknown"
        docs_found = set(r["metadata"].get("document_id") for r in result["results"])
        
        print(f"User: {user_id} ({user_dept})")
        print(f"Query: {query}")
        print(f"Results: {len(result['results'])} chunks from {docs_found}")
        print()
    
    print("=== Permission Verification Complete ===")


if __name__ == "__main__":
    main()
