"""FastAPI application — AI Business Architecture Portfolio."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="AI Business Architecture Portfolio",
    description="Business alignment, cost modeling, and architecture decision management",
    version="1.0.0"
)

orchestrator = None


def get_orchestrator():
    global orchestrator
    if orchestrator is None:
        from app.orchestrator import PortfolioOrchestrator
        orchestrator = PortfolioOrchestrator()
    return orchestrator


@app.get("/")
def root():
    return {"status": "running", "service": "ai-business-architecture"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/portfolio/summary")
def portfolio_summary():
    return get_orchestrator().portfolio.get_summary()


@app.get("/portfolio/projects")
def list_projects():
    return [
        {"id": p.id, "name": p.name, "demonstrates": p.demonstrates}
        for p in get_orchestrator().portfolio.list_projects()
    ]


@app.get("/portfolio/use-cases")
def list_use_cases():
    return [
        {"id": uc.id, "name": uc.name, "score": uc.weighted_score(),
         "status": uc.status.value}
        for uc in get_orchestrator().portfolio.list_use_cases()
    ]


@app.get("/portfolio/prioritize")
def prioritize_use_cases():
    return get_orchestrator().prioritize_use_cases()


@app.get("/portfolio/project/{project_id}/cost-analysis")
def project_cost_analysis(project_id: str):
    result = get_orchestrator().get_project_cost_analysis(project_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@app.get("/portfolio/report")
def portfolio_report():
    return get_orchestrator().generate_portfolio_report()


@app.get("/adrs")
def list_adrs():
    return [
        {"id": a.id, "title": a.title, "status": a.status.value}
        for a in get_orchestrator().adrs.list_adrs()
    ]


@app.get("/adrs/{adr_id}")
def get_adr(adr_id: str):
    adr = get_orchestrator().adrs.get_adr(adr_id)
    if not adr:
        raise HTTPException(status_code=404, detail=f"ADR {adr_id} not found")
    return adr


@app.get("/adrs/{adr_id}/formatted")
def format_adr(adr_id: str):
    return get_orchestrator().adrs.format_adr(adr_id)


@app.get("/costs/summary")
def cost_summary():
    return get_orchestrator().costs.get_summary()


@app.get("/costs/model/{model_id}")
def get_cost_model(model_id: str):
    model = get_orchestrator().costs.get_cost_model(model_id)
    if not model:
        raise HTTPException(status_code=404, detail=f"Cost model {model_id} not found")
    return {
        "id": model.id, "name": model.name,
        "total": model.total_cost(), "breakdown": model.by_category(),
        "items": [{"name": i.name, "category": i.category, "cost": i.annual_cost}
                  for i in model.items]
    }


@app.get("/metrics/summary")
def metrics_summary():
    return get_orchestrator().metrics.get_summary()


@app.get("/metrics/value/{bv_id}")
def get_business_value(bv_id: str):
    result = get_orchestrator().metrics.get_value_summary(bv_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@app.get("/trade-offs")
def list_trade_offs():
    return [
        {"id": t.id, "title": t.title, "winner": t.winner}
        for t in get_orchestrator().trade_offs.list_trade_offs()
    ]


@app.get("/trade-offs/{to_id}")
def get_trade_off(to_id: str):
    to = get_orchestrator().trade_offs.get_trade_off(to_id)
    if not to:
        raise HTTPException(status_code=404, detail=f"Trade-off {to_id} not found")
    return to


@app.get("/trade-offs/{to_id}/evaluate")
def evaluate_trade_off(to_id: str):
    result = get_orchestrator().trade_offs.evaluate(to_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@app.get("/reviews/checklist")
def review_checklist():
    return get_orchestrator().reviews.get_checklist()


@app.get("/reviews/summary")
def review_summary():
    return get_orchestrator().reviews.get_summary()


@app.get("/briefs")
def list_briefs():
    return [
        {"project": b.project_name, "requirements": len(b.requirements)}
        for b in get_orchestrator().briefs.list_briefs()
    ]


@app.get("/briefs/{project_name}")
def get_brief(project_name: str):
    brief = get_orchestrator().briefs.get_brief(project_name)
    if not brief:
        raise HTTPException(status_code=404, detail=f"Brief for {project_name} not found")
    return brief


@app.get("/briefs/{project_name}/formatted")
def format_brief(project_name: str):
    return get_orchestrator().briefs.format_brief(project_name)


@app.get("/status")
def full_status():
    return get_orchestrator().get_full_status()
