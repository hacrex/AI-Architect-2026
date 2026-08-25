"""Security Governance Demo — audit log viewer."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipelines.security_pipeline import SecurityPipeline
from app.models import RiskLevel


def main():
    print("=" * 60)
    print("AI Security Governance — Audit Log Viewer")
    print("=" * 60)

    pipeline = SecurityPipeline()

    print("\n--- Generating Sample Audit Events ---")
    pipeline.audit.log("alice", "document_read", "engineering_doc", "doc-001",
                       details={"source": "knowledge_base"})
    pipeline.audit.log("bob", "document_read", "hr_doc", "doc-002",
                       details={"source": "hr_policy"})
    pipeline.audit.log("alice", "prompt_check", "prompt", "p-001",
                       details={"injection_detected": False})
    pipeline.audit.log("eve", "prompt_check", "prompt", "p-002",
                       details={"injection_detected": True},
                       risk_level=RiskLevel.CRITICAL)
    pipeline.audit.log("carol", "data_access", "financial_report", "fin-001",
                       details={"classification": "confidential"})
    pipeline.audit.log("dave", "agent_action", "tool", "t-001",
                       details={"tool": "web_search", "decision": "allowed"})
    pipeline.audit.log("alice", "authentication", "auth", "a-001",
                       details={"method": "jwt"})
    pipeline.audit.log("eve", "authorization", "document", "doc-003",
                       details={"allowed": False, "reason": "no_policy"})

    print("\n--- All Audit Entries ---")
    entries = pipeline.audit.list_entries(limit=20)
    risk_symbols = {"low": "", "medium": "-", "high": "!", "critical": "!!"}
    for e in entries:
        risk_symbol = risk_symbols.get(e["risk_level"], "?")
        print(f"  [{e['timestamp'][:19]}] {e['user_id']:8s} "
              f"{e['action']:25s} {e['resource_type']:15s} "
              f"{e['result']:10s} {risk_symbol}")

    print("\n--- Summary ---")
    summary = pipeline.audit.get_summary()
    print(f"  Total entries:    {summary['total_entries']}")
    print(f"  By result:        {summary['by_result']}")
    print(f"  By risk level:    {summary['by_risk_level']}")
    print(f"  Unique users:     {summary['unique_users']}")

    print("\n--- User Activity: alice ---")
    alice_activity = pipeline.audit.get_user_activity("alice")
    print(f"  Total events:     {alice_activity['total_events']}")
    print(f"  Actions:          {alice_activity['actions']}")
    print(f"  Last event:       {alice_activity['last_event']}")

    print("\n--- User Activity: eve ---")
    eve_activity = pipeline.audit.get_user_activity("eve")
    print(f"  Total events:     {eve_activity['total_events']}")
    print(f"  Actions:          {eve_activity['actions']}")
    print(f"  Last event:       {eve_activity['last_event']}")

    print(f"\n{'=' * 60}")
    print("Audit log viewer complete.")


if __name__ == "__main__":
    main()
