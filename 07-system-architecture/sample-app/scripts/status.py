"""Script to view architecture and system status."""
import sys
sys.path.insert(0, ".")

from app.gateway import AIGateway
from app.rag import RAGService
from app.agents import AgentService
from app.model_router import ModelRouter
from app.observability import ObservabilityService
from app.security import SecurityService
from pipelines.adr_manager import ADRManager


def main():
    print("=== AI System Architecture Status ===\n")

    gw = AIGateway()
    print("Gateway:")
    for k, v in gw.get_stats().items():
        print(f"  {k}: {v}")

    rag = RAGService()
    print("\nRAG:")
    for k, v in rag.get_stats().items():
        print(f"  {k}: {v}")

    agent = AgentService()
    print("\nAgents:")
    for k, v in agent.get_stats().items():
        print(f"  {k}: {v}")

    router = ModelRouter()
    print("\nModel Router:")
    for route in router.list_routes():
        print(f"  {route['model']} ({route['provider']}): priority={route['priority']}, circuit_open={route['circuit_open']}")

    obs = ObservabilityService()
    print("\nObservability:")
    dashboard = obs.get_dashboard()
    print(f"  Traces: {dashboard['active_traces']}")

    sec = SecurityService()
    print("\nSecurity Audit:")
    summary = sec.audit_logger.get_summary()
    print(f"  Total events: {summary['total_events']}")

    adr_mgr = ADRManager()
    print("\nArchitecture Decision Records:")
    for adr in adr_mgr.list_adrs():
        print(f"  {adr.id}: {adr.title}")
        print(f"    Decision: {adr.decision}")


if __name__ == "__main__":
    main()
