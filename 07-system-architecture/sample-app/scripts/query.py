"""Script to test a complete AI query through all subsystems."""
import sys
sys.path.insert(0, ".")

from pipelines.request_pipeline import RequestPipeline


def main():
    pipeline = RequestPipeline()

    print("--- Synchronous Request ---")
    result = pipeline.process(
        query="What is our remote work policy?",
        user_id="user-001"
    )
    print(f"Request ID: {result['request_id']}")
    print(f"Model: {result['model']} ({result['provider']})")
    print(f"Tokens: {result['tokens']}")
    print(f"Cost: ${result['cost_usd']}")
    print(f"Latency: {result['latency_ms']}ms")
    print(f"RAG Chunks: {result['rag_chunks']}")
    print(f"Status: {result['status']}")

    print("\n--- Agent Request ---")
    result_agent = pipeline.process(
        query="search for expense policy and send me a summary",
        user_id="user-001",
        use_agent=True
    )
    print(f"Request ID: {result_agent['request_id']}")
    print(f"Agent Used: {result_agent['agent_used']}")
    print(f"Model: {result_agent['model']}")
    print(f"Status: {result_agent['status']}")


if __name__ == "__main__":
    main()
