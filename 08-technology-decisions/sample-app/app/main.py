"""FastAPI application for Technology Decisions."""
import time
from datetime import datetime
from fastapi import FastAPI, HTTPException
from typing import Optional
from app.models import TechnologyCategory, DecisionCriteria, DecisionStatus
from app.decision_engine import DecisionEngine
from app.adr_manager import ADRManager
from app.build_buy_analyzer import BuildBuyAnalyzer
from app.constraint_validator import ConstraintManager
from pipelines.decision_pipeline import DecisionPipeline

app = FastAPI(
    title="Technology Decisions API",
    description="Decision engine for technology selection, Build vs Buy analysis, and ADR management",
    version="0.1.0"
)

decision_engine = DecisionEngine()
adr_manager = ADRManager()
build_buy_analyzer = BuildBuyAnalyzer()
constraint_manager = ConstraintManager()
pipeline = DecisionPipeline()


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "decision_engine": "ok",
            "adr_manager": "ok",
            "build_buy_analyzer": "ok",
            "constraint_validator": "ok",
            "pipeline": "ok"
        }
    }


@app.get("/decisions/matrices")
def list_matrices():
    return decision_engine.get_summary()


@app.get("/decisions/matrices/{matrix_id}")
def get_matrix(matrix_id: str):
    matrix = decision_engine.get_matrix(matrix_id)
    if not matrix:
        raise HTTPException(status_code=404, detail=f"Matrix {matrix_id} not found")
    return {
        "id": matrix.id,
        "title": matrix.title,
        "category": matrix.category.value,
        "criteria": [{"name": c.name, "weight": c.weight, "description": c.description} for c in matrix.criteria],
        "options": [{"name": o.name, "description": o.description, "is_managed": o.is_managed} for o in matrix.options],
        "scores": [
            {"option": s.option_name, "weighted_score": s.weighted_score,
             "scores": s.scores, "disqualified": s.is_disqualified,
             "violations": s.hard_constraint_violations}
            for s in matrix.scores
        ],
        "selected_option": matrix.selected_option,
        "rationale": matrix.rationale
    }


@app.post("/decisions/matrices/{matrix_id}/score")
def score_option(matrix_id: str, option_name: str, scores: dict[str, float]):
    try:
        result = decision_engine.score_option(matrix_id, option_name, scores)
        return {
            "option": result.option_name,
            "weighted_score": result.weighted_score,
            "disqualified": result.is_disqualified,
            "violations": result.hard_constraint_violations
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/decisions/matrices/{matrix_id}/select")
def select_option(matrix_id: str):
    try:
        selected = decision_engine.select_option(matrix_id)
        return {"selected_option": selected}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/decisions/challenge/{matrix_id}")
def challenge_decision(matrix_id: str):
    return pipeline.challenge_decision(matrix_id)


@app.get("/adr")
def list_adrs():
    return adr_manager.get_adr_summary()


@app.get("/adr/{adr_id}")
def get_adr(adr_id: str):
    adr = adr_manager.get_adr(adr_id)
    if not adr:
        raise HTTPException(status_code=404, detail=f"ADR {adr_id} not found")
    return {
        "id": adr.id,
        "title": adr.title,
        "context": adr.context,
        "options": adr.options,
        "decision": adr.decision,
        "rationale": adr.rationale,
        "consequences": adr.consequences,
        "revisit_conditions": adr.revisit_conditions,
        "status": adr.status.value,
        "metrics_to_track": adr.metrics_to_track
    }


@app.get("/adr/{adr_id}/markdown")
def get_adr_markdown(adr_id: str):
    markdown = adr_manager.format_adr_markdown(adr_id)
    if "not found" in markdown:
        raise HTTPException(status_code=404, detail=markdown)
    return {"markdown": markdown}


@app.post("/adr")
def create_adr(title: str, context: str, options: list[str], decision: str,
               rationale: str = "", consequences: dict = None,
               revisit_conditions: list[str] = None):
    adr = adr_manager.create_adr(
        title=title, context=context, options=options,
        decision=decision, rationale=rationale,
        consequences=consequences,
        revisit_conditions=revisit_conditions
    )
    return {"id": adr.id, "title": adr.title, "status": adr.status.value}


@app.put("/adr/{adr_id}/status")
def update_adr_status(adr_id: str, status: str):
    try:
        new_status = DecisionStatus(status)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid status: {status}")

    adr = adr_manager.update_status(adr_id, new_status)
    if not adr:
        raise HTTPException(status_code=404, detail=f"ADR {adr_id} not found")
    return {"id": adr.id, "status": adr.status.value}


@app.get("/build-buy")
def list_build_buy():
    return build_buy_analyzer.get_summary()


@app.get("/build-buy/{analysis_id}")
def get_build_buy(analysis_id: str):
    analysis = build_buy_analyzer.get_analysis(analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail=f"Analysis {analysis_id} not found")
    comparisons = build_buy_analyzer.compare_options(analysis_id)
    return {
        "id": analysis.id,
        "component": analysis.component,
        "recommendation": analysis.recommendation,
        "rationale": analysis.rationale,
        "comparisons": comparisons
    }


@app.get("/constraints")
def list_constraints():
    return constraint_manager.get_constraints_summary()


@app.post("/constraints/validate")
def validate_option(option_name: str, option_description: str = ""):
    return constraint_manager.validate_option(option_name, option_description)


@app.get("/evaluation/summary")
def evaluation_summary():
    return pipeline.run_full_evaluation()


@app.get("/evaluation/model-hosting")
def evaluate_model_hosting():
    return pipeline.evaluate_model_hosting()


@app.get("/evaluation/vector-storage")
def evaluate_vector_storage():
    return pipeline.evaluate_vector_storage()


@app.get("/evaluation/inference-platform")
def evaluate_inference_platform():
    return pipeline.evaluate_inference_platform()


@app.get("/evaluation/build-buy")
def evaluate_build_buy():
    return pipeline.get_build_buy_summary()


@app.get("/architecture/overview")
def architecture_overview():
    return {
        "decision_framework": {
            "matrices": len(decision_engine.list_matrices()),
            "adrs": len(adr_manager.list_adrs()),
            "build_buy_analyses": len(build_buy_analyzer.list_analyses()),
            "constraints": len(constraint_manager.get_all_constraints())
        },
        "selected_architecture": {
            "model_hosting": "Hybrid (Managed + Self-hosted)",
            "vector_storage": "PostgreSQL + pgvector",
            "inference_platform": "Hybrid (Managed + vLLM)",
            "observability": "Open-Source Stack"
        },
        "decision_process": [
            "1. Define requirements and hard constraints",
            "2. Identify technology options",
            "3. Create decision matrix with weighted criteria",
            "4. Score options against criteria",
            "5. Validate against hard constraints",
            "6. Select highest-scoring valid option",
            "7. Document decision as ADR",
            "8. Define revisit conditions",
            "9. Challenge your own decision"
        ]
    }
