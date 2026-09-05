"""Maintenance history API routes."""

import math
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import CurrentUser, DbSession
from app.models.maintenance_history import MaintenanceHistory
from app.repositories.maintenance_repository import MaintenanceRepository
from app.schemas import MaintenanceCreate, MaintenanceResponse, MaintenanceUpdate, PaginatedResponse

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])


@router.get("", response_model=PaginatedResponse[MaintenanceResponse])
def list_maintenance(
    db: DbSession,
    _: CurrentUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    machine_id: Optional[int] = None,
):
    repo = MaintenanceRepository(db)
    skip = (page - 1) * page_size
    items, total = repo.search(machine_id=machine_id, skip=skip, limit=page_size)
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=math.ceil(total / page_size) if total else 0,
    )


@router.get("/{record_id}", response_model=MaintenanceResponse)
def get_maintenance(record_id: int, db: DbSession, _: CurrentUser):
    record = MaintenanceRepository(db).get(record_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Maintenance record not found")
    return record


@router.post("", response_model=MaintenanceResponse, status_code=status.HTTP_201_CREATED)
def create_maintenance(data: MaintenanceCreate, db: DbSession, _: CurrentUser):
    record = MaintenanceHistory(**data.model_dump())
    return MaintenanceRepository(db).create(record)


@router.put("/{record_id}", response_model=MaintenanceResponse)
def update_maintenance(record_id: int, data: MaintenanceUpdate, db: DbSession, _: CurrentUser):
    repo = MaintenanceRepository(db)
    record = repo.get(record_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Maintenance record not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(record, field, value)
    return repo.update(record)
