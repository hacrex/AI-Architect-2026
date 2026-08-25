"""Security Governance Demo — threat modeling demonstration."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipelines.security_pipeline import SecurityPipeline


def main():
    print("=" * 60)
    print("AI Security Governance — Threat Modeling Demo")
    print("=" * 60)

    pipeline = SecurityPipeline()

    print("\n--- Threat Catalog ---")
    threats = pipeline.risk_engine.list_threats()
    for t in threats:
        print(f"  {t['id']}: {t['name']}")
        print(f"    Category: {t['category']}, Impact: {t['impact']}, "
              f"Likelihood: {t['likelihood']}, Risk: {t['risk_score']}")

    print("\n--- Risk Assessment Scenarios ---")
    scenarios = [
        ("Internal Knowledge Bot", ["internal", "engineering"], 500, False),
        ("Customer Support Bot", ["public", "internal"], 50000, True),
        ("Financial Analysis Tool", ["financial", "confidential"], 100, False),
        ("Medical Records AI", ["medical", "restricted"], 50, False),
    ]
    for name, dtypes, users, external in scenarios:
        result = pipeline.risk_engine.assess_risk(name, dtypes, users, external)
        print(f"\n  {name}:")
        print(f"    Risk Level: {result['risk_level']}")
        print(f"    Factors: {result['risk_factors']}")
        print(f"    Applicable Threats: {result['applicable_threats']}")
        print(f"    Top Threat: {result['top_threats'][0]['name'] if result['top_threats'] else 'None'}")
        print(f"    Controls: {result['recommended_controls'][:3]}")

    print("\n--- Risk Matrix ---")
    matrix = pipeline.risk_engine.get_risk_matrix()
    for level, threat_names in matrix.items():
        print(f"  {level}: {', '.join(threat_names)}")

    print("\n--- Governance Summary ---")
    print(pipeline.governance.get_summary())

    print(f"\n{'=' * 60}")
    print("Threat modeling demo complete.")


if __name__ == "__main__":
    main()
