"""Script to run a complete technology decision workflow."""
import sys
sys.path.insert(0, ".")

from pipelines.decision_pipeline import DecisionPipeline


def main():
    pipeline = DecisionPipeline()

    print("--- Full Technology Evaluation ---")
    summary = pipeline.run_full_evaluation()
    print(f"Matrices: {len(summary['matrices'])}")
    for m in summary["matrices"]:
        print(f"  {m['id']}: {m['title']} -> {m['selected']}")

    print(f"\nADRs: {len(summary['adrs'])}")
    for a in summary["adrs"]:
        print(f"  {a['id']}: {a['title']} ({a['status']})")

    print(f"\nBuild vs Buy: {len(summary['build_buy_analyses'])}")
    for b in summary["build_buy_analyses"]:
        print(f"  {b['component']}: {b['recommendation']}")

    print(f"\nConstraints: {len(summary['constraints'])}")
    for c in summary["constraints"]:
        print(f"  {c['name']} ({c['type']})")

    print("\n--- Model Hosting Evaluation ---")
    mh = pipeline.evaluate_model_hosting()
    print(f"  Matrix: {mh['matrix']['title']}")
    print(f"  Selected: {mh['matrix']['selected']}")
    for s in mh["matrix"]["scores"]:
        print(f"    {s['option']}: {s['score']}")
    if mh.get("adr"):
        print(f"  ADR: {mh['adr']['decision'][:80]}...")
        print(f"  Revisit conditions: {len(mh['adr']['revisit_conditions'])}")

    print("\n--- Challenge: Model Hosting ---")
    challenge = pipeline.challenge_decision("matrix-001")
    print(f"  Selected: {challenge['selected_option']}")
    for ch in challenge["challenges"]:
        if "question" in ch:
            print(f"  Challenge: {ch['question']}")
            print(f"    Gap: {ch['gap']}")
        if "criteria_where_alternative_wins" in ch:
            wins = ch["criteria_where_alternative_wins"]
            if wins:
                print(f"    Alternative wins on: {', '.join(w['criterion'] for w in wins)}")

    print("\n--- Build vs Buy Summary ---")
    bb = pipeline.get_build_buy_summary()
    for a in bb["analyses"]:
        print(f"  {a['component']}: {a['recommendation']}")
        print(f"    Cheapest: {a['cheapest_option']} (${a['cheapest_cost']:,.0f} over 5 years)")


if __name__ == "__main__":
    main()
