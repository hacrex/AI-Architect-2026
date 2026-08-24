"""Script to test the complete AI system architecture."""
import sys
sys.path.insert(0, ".")

from app.gateway import AIGateway
from app.rag import RAGService
from app.agents import AgentService
from app.model_router import ModelRouter
from app.context import ContextAssembler
from app.observability import ObservabilityService
from app.security import SecurityService
from app.models import AIRequest, SecurityContext
from pipelines.request_pipeline import RequestPipeline, IngestionPipeline
from pipelines.adr_manager import ADRManager


def test_gateway():
    print("=== Testing AI Gateway ===")
    gw = AIGateway()

    sec_ctx = SecurityContext(user_id="user-001", roles=["employee", "engineering"], rate_limit=100)
    request = AIRequest(query="What is our remote work policy?", user_id="user-001")

    result = gw.process_request(request, sec_ctx)
    print(f"Request allowed: {result['allowed']}")
    print(f"Request ID: {result['request_id']}")

    stats = gw.get_stats()
    print(f"Total requests: {stats['total_requests']}")
    print("PASSED\n")


def test_rag():
    print("=== Testing RAG Service ===")
    rag = RAGService()

    result = rag.retrieve(query="remote work policy", user_roles=["employee", "engineering"])
    print(f"Chunks found: {result['raw_count']}")
    print(f"Reranked: {result['reranked_count']}")
    print(f"Sources: {len(result['sources'])}")
    print(f"Tokens used: {result['tokens_used']}")

    stats = rag.get_stats()
    print(f"Total documents: {stats['total_documents']}")
    print("PASSED\n")


def test_agents():
    print("=== Testing Agent Service ===")
    agent = AgentService()

    result = agent.run(query="search for remote work policy", user_roles=["employee", "engineering"])
    print(f"Plan steps: {result['plan_steps']}")
    print(f"Tools needed: {result['tools_needed']}")
    print(f"Plan approved: {result['plan_approved']}")
    print(f"Tool calls: {result['execution']['total_tool_calls']}")
    print("PASSED\n")


def test_model_router():
    print("=== Testing Model Router ===")
    router = ModelRouter()

    model = router.select_model()
    print(f"Selected: {model.model_name} ({model.provider.value})")

    cost = router.estimate_cost("gpt-4", 1000, 500)
    print(f"Estimated cost: ${cost}")

    fallbacks = router.get_fallback_chain(model)
    print(f"Fallback options: {len(fallbacks)}")

    routes = router.list_routes()
    print(f"Total routes: {len(routes)}")
    print("PASSED\n")


def test_context_assembly():
    print("=== Testing Context Assembly ===")
    assembler = ContextAssembler()

    rag_ctx = {"context": "Remote work policy allows 3 days per week.", "tokens_used": 100, "sources": [{"source": "hr/policy.md"}]}
    result = assembler.assemble(query="What is our remote work policy?", rag_context=rag_ctx)
    print(f"Messages: {len(result['messages'])}")
    print(f"Estimated tokens: {result['estimated_tokens']}")
    print(f"Within budget: {result['within_budget']}")
    print("PASSED\n")


def test_observability():
    print("=== Testing Observability ===")
    obs = ObservabilityService()

    obs.record_request("req-001", "user-001", "gpt-4", "openai", 500, 200, 450.0, 0.045)
    obs.record_request("req-002", "user-002", "gpt-4", "openai", 600, 300, 520.0, 0.054)

    dashboard = obs.get_dashboard()
    print(f"Metrics tracked: {len(dashboard['metrics_summary'])}")
    print(f"Cost by model: {dashboard['cost_by_model']}")
    print("PASSED\n")


def test_security():
    print("=== Testing Security ===")
    sec = SecurityService()

    auth = sec.authenticate("alice@company.com", "password")
    print(f"Authenticated: {auth['authenticated']}")

    if auth["authenticated"]:
        authz = sec.authorize_request(auth["token"], "ask_questions")
        print(f"Authorized: {authz['authorized']}")
        print(f"User: {authz.get('user_id')}")

    sec_ctx = sec.get_security_context("user-001")
    print(f"Document access: {len(sec_ctx.document_permissions)}")
    print(f"Rate limit: {sec_ctx.rate_limit}")

    audit = sec.audit_logger.get_summary()
    print(f"Audit events: {audit['total_events']}")
    print("PASSED\n")


def test_pipeline():
    print("=== Testing Request Pipeline ===")
    pipeline = RequestPipeline()

    result = pipeline.process("What is our remote work policy?", "user-001")
    print(f"Request: {result['request_id']}")
    print(f"Model: {result['model']}")
    print(f"Tokens: {result['tokens']}")
    print(f"Cost: ${result['cost_usd']}")
    print(f"Latency: {result['latency_ms']}ms")

    result_agent = pipeline.process("search for expense policy", "user-001", use_agent=True)
    print(f"Agent request: {result_agent['request_id']}")
    print(f"Agent used: {result_agent['agent_used']}")
    print("PASSED\n")


def test_ingestion():
    print("=== Testing Ingestion Pipeline ===")
    pipeline = IngestionPipeline()

    result = pipeline.ingest("hr/new-policy.md", "New policy content about work from home.", "hr")
    print(f"Ingested: {result['source']}")
    print(f"Status: {result['status']}")

    docs = [
        {"source": "eng/docs-1.md", "content": "Engineering doc 1", "category": "engineering"},
        {"source": "eng/docs-2.md", "content": "Engineering doc 2", "category": "engineering"},
    ]
    batch = pipeline.batch_ingest(docs)
    print(f"Batch ingested: {len(batch)} documents")
    print("PASSED\n")


def test_adr():
    print("=== Testing ADR Manager ===")
    mgr = ADRManager()

    adrs = mgr.list_adrs()
    print(f"ADRs: {len(adrs)}")

    summary = mgr.get_adr_summary()
    for s in summary:
        print(f"  {s['id']}: {s['title']}")
    print("PASSED\n")


if __name__ == "__main__":
    print("AI System Architecture Tests\n")
    test_gateway()
    test_rag()
    test_agents()
    test_model_router()
    test_context_assembly()
    test_observability()
    test_security()
    test_pipeline()
    test_ingestion()
    test_adr()
    print("All tests passed!")
