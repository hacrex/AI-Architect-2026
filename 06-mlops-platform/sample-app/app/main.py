"""FastAPI application for the MLOps platform."""
from datetime import datetime
from fastapi import FastAPI, HTTPException
from app.models import (
    ExperimentCreate, ModelRegister, ModelPromote, ModelRollback,
    EvaluationRun, DeploymentRequest, CanaryRequest
)
from app.experiment import ExperimentTracker
from app.registry import ModelRegistry
from app.evaluation import EvaluationPipeline
from app.deployment import DeploymentEngine
from app.monitoring import Monitor

app = FastAPI(
    title="MLOps Platform API",
    description="AI Platform for model lifecycle management",
    version="0.1.0"
)

tracker = ExperimentTracker()
registry = ModelRegistry()
evaluator = EvaluationPipeline()
deployer = DeploymentEngine()
monitor = Monitor()


@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.post("/experiments")
def create_experiment(request: ExperimentCreate):
    return tracker.create_experiment(
        name=request.name,
        dataset_version=request.dataset_version,
        model=request.model,
        prompt_template=request.prompt_template,
        parameters=request.parameters
    )


@app.get("/experiments")
def list_experiments(name: str = None):
    return tracker.list_experiments(name)


@app.get("/experiments/{experiment_id}")
def get_experiment(experiment_id: str):
    exp = tracker.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp


@app.post("/experiments/{experiment_id}/metrics")
def log_metrics(experiment_id: str, metrics: dict):
    try:
        return tracker.log_results(experiment_id, metrics)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/registry/register")
def register_model(request: ModelRegister):
    try:
        return registry.register(
            name=request.name,
            version=request.version,
            source_experiment=request.source_experiment,
            metrics=request.metrics,
            artifacts=request.artifacts,
            description=request.description
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/registry/models")
def list_models():
    return registry.list_models()


@app.get("/registry/models/{name}")
def list_model_versions(name: str):
    return registry.list_versions(name)


@app.get("/registry/models/{name}/{version}")
def get_model(name: str, version: str):
    model = registry.get_model(name, version)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model


@app.post("/registry/promote")
def promote_model(request: ModelPromote):
    try:
        return registry.promote(
            name=request.name,
            version=request.version,
            stage=request.stage,
            approved_by=request.approved_by
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/registry/rollback")
def rollback_model(request: ModelRollback):
    try:
        return registry.rollback(request.name, request.reason)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/registry/lineage/{name}")
def get_lineage(name: str):
    return registry.get_model_lineage(name)


@app.post("/evaluate")
def run_evaluation(request: EvaluationRun):
    return evaluator.evaluate(
        model=request.model,
        version=request.version,
        test_dataset=request.test_dataset,
        metrics=request.metrics
    )


@app.get("/evaluations")
def list_evaluations(model: str = None):
    return evaluator.list_evaluations(model)


@app.get("/evaluations/{eval_id}")
def get_evaluation(eval_id: str):
    result = evaluator.get_evaluation(eval_id)
    if not result:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return result


@app.get("/evaluations/{eval_id}/summary")
def get_eval_summary(eval_id: str):
    return evaluator.get_gate_summary(eval_id)


@app.post("/deploy")
def deploy_model(request: DeploymentRequest):
    return deployer.deploy(
        model=request.model,
        version=request.version,
        environment=request.environment
    )


@app.post("/deploy/canary")
def canary_deploy(request: CanaryRequest):
    return deployer.canary(
        model=request.model,
        version=request.version,
        initial_percentage=request.initial_percentage,
        increment=request.increment,
        observation_period_seconds=request.observation_period_seconds
    )


@app.get("/deployments")
def list_deployments(model: str = None, environment: str = None):
    return deployer.list_deployments(model, environment)


@app.get("/deployments/{deploy_id}")
def get_deployment(deploy_id: str):
    deployment = deployer.get_deployment(deploy_id)
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")
    return deployment


@app.post("/deployments/{deploy_id}/pause")
def pause_deployment(deploy_id: str):
    return deployer.pause(deploy_id)


@app.post("/deployments/{deploy_id}/resume")
def resume_deployment(deploy_id: str):
    return deployer.resume(deploy_id)


@app.post("/rollback")
def rollback(request: ModelRollback):
    return deployer.rollback(request.name, request.reason)


@app.get("/monitor/{model}")
def check_health(model: str):
    return monitor.check_health(model)


@app.get("/monitor/{model}/history")
def get_health_history(model: str, hours: int = 24):
    return monitor.get_health_history(model, hours)


@app.get("/drift/{model}")
def get_drift_report(model: str, time_range: str = "7d"):
    return monitor.get_drift_report(model, time_range)


@app.get("/monitor/{model}/metrics")
def get_metrics_summary(model: str):
    return monitor.get_metrics_summary(model)


@app.get("/alerts")
def get_alerts(model: str = None, limit: int = 10):
    return monitor.get_alerts(model, limit)
