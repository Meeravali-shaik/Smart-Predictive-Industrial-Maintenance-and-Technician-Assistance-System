"""Sensor reading API routes."""

import math
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import CurrentUser, DbSession
from app.repositories.machine_repository import MachineRepository
from app.repositories.sensor_reading_repository import SensorReadingRepository
from app.schemas import PaginatedResponse, SensorReadingResponse

router = APIRouter(prefix="/sensor-readings", tags=["Sensor Readings"])


@router.get("", response_model=PaginatedResponse[SensorReadingResponse])
def list_readings(
    db: DbSession,
    _: CurrentUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    machine_id: Optional[int] = None,
):
    repo = SensorReadingRepository(db)
    if machine_id:
        items = repo.get_latest_for_machine(machine_id, limit=page_size)
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


@router.get("/latest/{machine_id}", response_model=list[SensorReadingResponse])
def get_latest_readings(machine_id: int, db: DbSession, _: CurrentUser, limit: int = Query(50, ge=1, le=200)):
    if not MachineRepository(db).get(machine_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine not found")
    return SensorReadingRepository(db).get_latest_for_machine(machine_id, limit=limit)
