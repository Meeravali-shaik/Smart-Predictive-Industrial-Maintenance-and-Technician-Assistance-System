"""Prediction API routes."""

import math
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import CurrentUser, DbSession
from app.repositories.machine_repository import MachineRepository
from app.repositories.prediction_repository import PredictionRepository
from app.schemas import PaginatedResponse, PredictionResponse

router = APIRouter(prefix="/predictions", tags=["Predictions"])


@router.get("", response_model=PaginatedResponse[PredictionResponse])
def list_predictions(
    db: DbSession,
    _: CurrentUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    machine_id: Optional[int] = None,
):
    repo = PredictionRepository(db)
    if machine_id:
        items = repo.get_trends_for_machine(machine_id, limit=page_size)
        total = len(items)
    else:
        items = repo.get_recent(limit=page_size)
        total = repo.count()
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=math.ceil(total / page_size) if total else 0,
    )


@router.get("/latest/{machine_id}", response_model=PredictionResponse)
def get_latest_prediction(machine_id: int, db: DbSession, _: CurrentUser):
    if not MachineRepository(db).get(machine_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine not found")
    prediction = PredictionRepository(db).get_latest_for_machine(machine_id)
    if not prediction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No predictions found")
    return prediction
