"""Seed script to populate the vector database with sample documents."""

import json
import asyncio
import chromadb
from pathlib import Path


def seed_documents():
    client = chromadb.PersistentClient(path="./data/chroma")

    collection = client.get_or_create_collection(
        name="knowledge_base",
        metadata={"hnsw:space": "cosine"},
    )

    docs_path = Path("docs/sample-documents.json")
    with open(docs_path) as f:
        data = json.load(f)

    for doc in data["documents"]:
        collection.add(
            documents=[doc["content"]],
            metadatas=[doc["metadata"]],
            ids=[doc["id"]],
        )
        print(f"  Added: {doc['id']} - {doc['metadata']['category']}")

    print(f"\nSeeded {len(data['documents'])} documents into knowledge_base collection")


if __name__ == "__main__":
    print("Seeding knowledge base...\n")
    seed_documents()
