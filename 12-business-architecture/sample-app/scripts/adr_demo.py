"""Business Architecture Demo — ADR viewer."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.orchestrator import PortfolioOrchestrator


def main():
    print("=" * 60)
    print("AI Business Architecture — ADR Viewer")
    print("=" * 60)

    orch = PortfolioOrchestrator()

    print("\n--- All ADRs ---")
    for adr in orch.adrs.list_adrs():
        print(f"\n  {adr.id}: {adr.title} [{adr.status.value}]")
        print(f"    Context: {adr.context[:80]}...")
        print(f"    Options: {len(adr.options)}")
        print(f"    Decision: {adr.decision[:80]}...")
        print(f"    Consequences: {len(adr.consequences)}")
        print(f"    Revisit: {len(adr.revisit_conditions)}")

    print("\n--- Full ADR: ADR-001 ---")
    print(orch.adrs.format_adr("ADR-001"))

    print("\n--- ADR Summary ---")
    summary = orch.adrs.get_summary()
    print(f"  Total: {summary['total_adrs']}")
    print(f"  By Status: {summary['by_status']}")

    print(f"\n{'=' * 60}")
    print("ADR viewer complete.")


if __name__ == "__main__":
    main()
