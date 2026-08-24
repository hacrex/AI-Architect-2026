"""Script to ingest documents into the system."""
import sys
sys.path.insert(0, ".")

from pipelines.request_pipeline import IngestionPipeline


def main():
    pipeline = IngestionPipeline()

    documents = [
        {"source": "hr/remote-work-2024.md", "content": "Updated remote work policy for 2024. Employees may work from home up to 3 days per week with manager approval.", "category": "hr"},
        {"source": "engineering/api-standards-v2.md", "content": "API standards v2. All new APIs must follow REST conventions with OpenAPI documentation.", "category": "engineering"},
        {"source": "security/data-handling.md", "content": "Data handling procedures. All sensitive data must be encrypted at rest and in transit.", "category": "security"},
    ]

    results = pipeline.batch_ingest(documents)
    for r in results:
        print(f"Ingested: {r['source']} ({r['status']})")


if __name__ == "__main__":
    main()
