"""Security Governance Demo — status report."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipelines.security_pipeline import SecurityPipeline


def main():
    print("=" * 60)
    print("AI Security Governance Demo — System Status")
    print("=" * 60)

    pipeline = SecurityPipeline()
    status = pipeline.get_system_status()

    print(f"\n1. AUTHENTICATION")
    print(f"   Users registered: {status['auth']['users']}")

    users = pipeline.authenticator.list_users()
    for u in users:
        roles = ", ".join(u["roles"])
        print(f"   - {u['id']:10s} {u['name']:20s} roles=[{roles}]")

    print(f"\n2. GOVERNANCE (AI System Inventory)")
    gov = status["governance"]
    print(f"   Total systems:   {gov['total_systems']}")
    print(f"   By risk level:   {gov['by_risk_level']}")
    print(f"   Reviews due:     {gov['reviews_due']}")
    print(f"   Total users:     {gov['total_users']:,}")

    for sys in pipeline.governance.list_systems():
        print(f"   - {sys.id}: {sys.name} (risk={sys.risk_level.value}, owner={sys.owner})")

    print(f"\n3. RISK ASSESSMENT")
    risk = status["risk"]
    print(f"   Total threats:   {risk['total_threats']}")
    print(f"   By category:     {risk['by_category']}")
    print(f"   By risk score:   {risk['by_risk_score']}")

    print(f"\n4. COMPLIANCE")
    comp = status["compliance"]
    print(f"   Requirements:    {comp['total_requirements']}")
    print(f"   Implemented:     {comp['implemented']}")
    print(f"   Compliance %:    {comp['compliance_pct']}%")
    print(f"   By category:     {comp['by_category']}")

    print(f"\n5. SECURITY CONTROLS")
    print(f"   Prompt Guard:    {status['prompt_guard']}")
    print(f"   Data Classifier: {status['data_classifier']}")
    print(f"   Agent Permissions: {status['agent_permissions']}")
    print(f"   Audit Log:       {status['audit']}")

    print(f"\n{'=' * 60}")
    print("Status report complete.")


if __name__ == "__main__":
    main()
