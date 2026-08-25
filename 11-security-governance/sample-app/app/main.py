"""FastAPI application — security governance demo."""
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from app.models import User

app = FastAPI(
    title="AI Security Governance Demo",
    description="Secure AI architecture with authentication, authorization, and audit",
    version="1.0.0"
)

pipeline = None


def get_pipeline():
    global pipeline
    if pipeline is None:
        from pipelines.security_pipeline import SecurityPipeline
        pipeline = SecurityPipeline()
    return pipeline


class LoginRequest(BaseModel):
    user_id: str


class PromptRequest(BaseModel):
    user_id: str
    prompt: str
    departments: list[str] = []


class AgentActionRequest(BaseModel):
    user_id: str
    agent_name: str
    tool_name: str
    action: str
    resource_department: str = "public"


@app.get("/")
def root():
    return {"status": "running", "service": "security-governance-demo"}


@app.get("/health")
def health(pipeline=Depends(get_pipeline)):
    return {"status": "healthy", "controls": len(pipeline.get_system_status())}


@app.post("/auth/login")
def login(req: LoginRequest, pipeline=Depends(get_pipeline)):
    result = pipeline.authenticator.authenticate(req.user_id)
    if not result["authenticated"]:
        raise HTTPException(status_code=401, detail=result["reason"])
    return result


@app.post("/prompt/check")
def check_prompt(req: PromptRequest, pipeline=Depends(get_pipeline)):
    result = pipeline.process_request(req.user_id, req.prompt, req.departments)
    if "error" in result and not result.get("allowed"):
        raise HTTPException(status_code=403, detail=result["error"])
    return result


@app.post("/agent/action")
def check_agent_action(req: AgentActionRequest, pipeline=Depends(get_pipeline)):
    return pipeline.process_agent_action(
        req.user_id, req.agent_name, req.tool_name,
        req.action, req.resource_department
    )


@app.get("/governance/systems")
def list_systems(pipeline=Depends(get_pipeline)):
    return [s.name for s in pipeline.governance.list_systems()]


@app.get("/governance/summary")
def governance_summary(pipeline=Depends(get_pipeline)):
    return pipeline.governance.get_summary()


@app.get("/risk/threats")
def list_threats(pipeline=Depends(get_pipeline)):
    return pipeline.risk_engine.list_threats()


@app.get("/risk/matrix")
def risk_matrix(pipeline=Depends(get_pipeline)):
    return pipeline.risk_engine.get_risk_matrix()


@app.get("/compliance/checklist")
def compliance_checklist(pipeline=Depends(get_pipeline)):
    return pipeline.compliance.get_checklist()


@app.get("/compliance/summary")
def compliance_summary(pipeline=Depends(get_pipeline)):
    return pipeline.compliance.get_summary()


@app.get("/audit/logs")
def audit_logs(limit: int = 50, pipeline=Depends(get_pipeline)):
    return pipeline.audit.list_entries(limit)


@app.get("/audit/summary")
def audit_summary(pipeline=Depends(get_pipeline)):
    return pipeline.audit.get_summary()


@app.get("/status")
def system_status(pipeline=Depends(get_pipeline)):
    return pipeline.get_system_status()
