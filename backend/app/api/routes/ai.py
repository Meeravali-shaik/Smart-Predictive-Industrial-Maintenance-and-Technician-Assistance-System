"""AI/ML API routes."""

from fastapi import APIRouter

from app.ai.ml_pipeline import MLPredictorPipeline
from app.api.deps import CurrentUser, RequireAdmin

router = APIRouter(prefix="/ai", tags=["AI/ML"])


@router.post("/train")
def train_ml_model(_: RequireAdmin, model_name: str = "random_forest"):
    pipeline = MLPredictorPipeline()
    result = pipeline.train(model_name=model_name)
    return {"message": "Model trained successfully", **result}


@router.get("/models")
def list_models(_: CurrentUser):
    return {
        "available_models": ["random_forest", "gradient_boosting", "logistic_regression"],
        "active_method": "rule_based",
        "note": "Rule-based prediction is active. ML models can replace it via the prediction service factory.",
    }
