"""Decision Pipeline — end-to-end technology decision workflow."""
import uuid
from datetime import datetime
from app.decision_engine import DecisionEngine
from app.adr_manager import ADRManager
from app.build_buy_analyzer import BuildBuyAnalyzer
from app.constraint_validator import ConstraintManager
from app.models import TechnologyCategory, DecisionCriteria


class DecisionPipeline:
    """Complete technology decision pipeline."""

    def __init__(self):
        self.decision_engine = DecisionEngine()
        self.adr_manager = ADRManager()
        self.build_buy_analyzer = BuildBuyAnalyzer()
        self.constraint_manager = ConstraintManager()

    def run_full_evaluation(self) -> dict:
        matrices = self.decision_engine.list_matrices()
        adrs = self.adr_manager.list_adrs()
        analyses = self.build_buy_analyzer.list_analyses()
        constraints = self.constraint_manager.get_all_constraints()

        return {
            "matrices": [
                {
                    "id": m.id,
                    "title": m.title,
                    "selected": m.selected_option,
                    "options_scored": len(m.scores)
                }
                for m in matrices
            ],
            "adrs": [
                {
                    "id": a.id,
                    "title": a.title,
                    "status": a.status.value
                }
                for a in adrs
            ],
            "build_buy_analyses": [
                {
                    "id": a.id,
                    "component": a.component,
                    "recommendation": a.recommendation
                }
                for a in analyses
            ],
            "constraints": [
                {
                    "name": c.name,
                    "type": c.constraint_type.value
                }
                for c in constraints
            ]
        }

    def evaluate_model_hosting(self) -> dict:
        matrix = self.decision_engine.get_matrix("matrix-001")
        if not matrix:
            return {"error": "Model hosting matrix not found"}

        adr = None
        for a in self.adr_manager.list_adrs():
            if "Model Hosting" in a.title:
                adr = a
                break

        return {
            "matrix": {
                "id": matrix.id,
                "title": matrix.title,
                "selected": matrix.selected_option,
                "scores": [
                    {"option": s.option_name, "score": s.weighted_score, "disqualified": s.is_disqualified}
                    for s in matrix.scores
                ]
            },
            "adr": {
                "id": adr.id if adr else None,
                "decision": adr.decision if adr else None,
                "revisit_conditions": adr.revisit_conditions if adr else []
            } if adr else None
        }

    def evaluate_vector_storage(self) -> dict:
        matrix = self.decision_engine.get_matrix("matrix-002")
        if not matrix:
            return {"error": "Vector storage matrix not found"}

        adr = None
        for a in self.adr_manager.list_adrs():
            if "Vector Storage" in a.title:
                adr = a
                break

        return {
            "matrix": {
                "id": matrix.id,
                "title": matrix.title,
                "selected": matrix.selected_option,
                "scores": [
                    {"option": s.option_name, "score": s.weighted_score, "disqualified": s.is_disqualified}
                    for s in matrix.scores
                ]
            },
            "adr": {
                "id": adr.id if adr else None,
                "decision": adr.decision if adr else None,
                "revisit_conditions": adr.revisit_conditions if adr else []
            } if adr else None
        }

    def evaluate_inference_platform(self) -> dict:
        matrix = self.decision_engine.get_matrix("matrix-003")
        if not matrix:
            return {"error": "Inference platform matrix not found"}

        adr = None
        for a in self.adr_manager.list_adrs():
            if "Inference Platform" in a.title:
                adr = a
                break

        return {
            "matrix": {
                "id": matrix.id,
                "title": matrix.title,
                "selected": matrix.selected_option,
                "scores": [
                    {"option": s.option_name, "score": s.weighted_score, "disqualified": s.is_disqualified}
                    for s in matrix.scores
                ]
            },
            "adr": {
                "id": adr.id if adr else None,
                "decision": adr.decision if adr else None,
                "revisit_conditions": adr.revisit_conditions if adr else []
            } if adr else None
        }

    def get_build_buy_summary(self) -> dict:
        analyses = self.build_buy_analyzer.list_analyses()
        summary = []

        for analysis in analyses:
            comparisons = self.build_buy_analyzer.compare_options(analysis.id)
            summary.append({
                "component": analysis.component,
                "recommendation": analysis.recommendation,
                "rationale": analysis.rationale,
                "options_compared": len(comparisons),
                "cheapest_option": comparisons[0]["name"] if comparisons else None,
                "cheapest_cost": comparisons[0]["total_5yr_cost"] if comparisons else 0
            })

        return {"analyses": summary}

    def challenge_decision(self, matrix_id: str) -> dict:
        matrix = self.decision_engine.get_matrix(matrix_id)
        if not matrix:
            return {"error": f"Matrix {matrix_id} not found"}

        selected = matrix.selected_option
        alternatives = [s for s in matrix.scores if s.option_name != selected and not s.is_disqualified]

        challenges = []
        if alternatives:
            best_alternative = alternatives[0]
            challenges.append({
                "question": f"Why not use {best_alternative.option_name} instead of {selected}?",
                "alternative_score": best_alternative.weighted_score,
                "selected_score": next((s.weighted_score for s in matrix.scores if s.option_name == selected), 0),
                "gap": round(
                    next((s.weighted_score for s in matrix.scores if s.option_name == selected), 0) -
                    best_alternative.weighted_score, 4
                )
            })

            criteria_analysis = []
            for c in matrix.criteria:
                selected_val = next((s.scores.get(c.name, 0) for s in matrix.scores if s.option_name == selected), 0)
                alt_val = best_alternative.scores.get(c.name, 0)
                if alt_val > selected_val:
                    criteria_analysis.append({
                        "criterion": c.name,
                        "selected": selected_val,
                        "alternative": alt_val,
                        "advantage": "alternative"
                    })
            challenges.append({
                "criteria_where_alternative_wins": criteria_analysis
            })

        return {
            "matrix_id": matrix_id,
            "selected_option": selected,
            "challenges": challenges,
            "recommendation": "Review the criteria where the alternative scores higher. "
                            "If those criteria become more important, reconsider the decision."
        }
