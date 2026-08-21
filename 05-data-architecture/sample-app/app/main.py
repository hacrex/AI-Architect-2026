"""FastAPI application for Data Pipeline API."""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from .models import (
    IngestRequest, IngestBatchRequest, QueryRequest, QueryResponse,
    ChunkingCompareRequest, ChunkingCompareResponse, StatsResponse,
    HealthResponse, Document
)
from .vectordb import VectorStore, MetadataStore, DocumentStore
from .embeddings import get_embedding_provider
from .ingestion import IngestionPipeline
from .retrieval import RetrievalEngine
from .auth import get_user_context, PermissionChecker
from .chunker import chunk_document

app = FastAPI(
    title="Data Architecture Sample App",
    description="Day 05 - Data Pipeline with Ingestion, Chunking, and Retrieval",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vector_store = VectorStore(dimensions=384)
metadata_store = MetadataStore()
document_store = DocumentStore()
embedding_provider = get_embedding_provider("mock")
permission_checker = PermissionChecker()

ingestion_pipeline = IngestionPipeline(
    vector_store=vector_store,
    metadata_store=metadata_store,
    document_store=document_store,
    embedding_provider=embedding_provider,
    chunking_strategy="structure",
)

retrieval_engine = RetrievalEngine(
    vector_store=vector_store,
    embedding_provider=embedding_provider,
    permission_checker=permission_checker,
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        vectordb=f"{vector_store.count()} vectors",
        metadata_db=f"{metadata_store.count()} documents",
        embedding_model="mock-384d",
    )


@app.post("/ingest")
async def ingest_document(request: IngestRequest):
    result = ingestion_pipeline.ingest_document(
        document_id=request.document_id,
        title=request.title,
        content=request.content,
        department=request.department.value,
        classification=request.classification.value,
        owner=request.owner,
    )
    return result


@app.post("/ingest/batch")
async def ingest_batch(request: IngestBatchRequest):
    results = []
    for doc in request.documents:
        result = ingestion_pipeline.ingest_document(
            document_id=doc.document_id,
            title=doc.title,
            content=doc.content,
            department=doc.department.value,
            classification=doc.classification.value,
            owner=doc.owner,
        )
        results.append(result)
    return {"results": results, "total": len(results)}


@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    user_context = get_user_context(request.user_id)
    if not user_context:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = retrieval_engine.hybrid_search(
        query=request.query,
        user_context=user_context,
        top_k=request.top_k,
        use_hybrid=request.use_hybrid,
        use_reranking=request.use_reranking,
    )
    
    return QueryResponse(
        query=result["query"],
        results=result["results"],
        total_results=result["total_results"],
        latency_ms=result["latency_ms"],
    )


@app.post("/chunking/compare")
async def compare_chunking(request: ChunkingCompareRequest):
    doc = document_store.get(request.document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    results = []
    for strategy in request.strategies:
        chunks = chunk_document(
            text=doc["content"],
            strategy=strategy.value,
        )
        
        avg_size = sum(c["token_count"] for c in chunks) / len(chunks) if chunks else 0
        
        results.append({
            "strategy": strategy.value,
            "chunk_count": len(chunks),
            "avg_chunk_size": avg_size,
            "chunks": chunks[:3],
        })
    
    return ChunkingCompareResponse(
        document_id=request.document_id,
        results=results,
    )


@app.get("/documents")
async def list_documents():
    return metadata_store.list_all()


@app.get("/documents/{document_id}")
async def get_document(document_id: str):
    doc = metadata_store.get(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@app.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    result = ingestion_pipeline.delete_document(document_id)
    return result


@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    stats = ingestion_pipeline.get_stats()
    return StatsResponse(**stats)


@app.get("/users")
async def list_users():
    from .auth import USERS
    return [
        {
            "user_id": user.user_id,
            "department": user.department,
            "clearance": user.clearance,
            "roles": user.roles,
        }
        for user in USERS.values()
    ]
