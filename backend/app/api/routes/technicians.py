"""Technician management API routes."""

import math
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import CurrentUser, DbSession, RequireManager
from app.models.technician import AvailabilityStatus, Technician
from app.repositories.technician_repository import TechnicianRepository
from app.schemas import PaginatedResponse, TechnicianCreate, TechnicianResponse, TechnicianUpdate

router = APIRouter(prefix="/technicians", tags=["Technicians"])


@router.get("", response_model=PaginatedResponse[TechnicianResponse])
def list_technicians(
    db: DbSession,
    _: CurrentUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    availability: Optional[AvailabilityStatus] = None,
):
    repo = TechnicianRepository(db)
    skip = (page - 1) * page_size
    items, total = repo.search(search=search, availability=availability, skip=skip, limit=page_size)
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=math.ceil(total / page_size) if total else 0,
    )


@router.get("/{technician_id}", response_model=TechnicianResponse)
def get_technician(technician_id: int, db: DbSession, _: CurrentUser):
    tech = TechnicianRepository(db).get(technician_id)
    if not tech:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Technician not found")
    return tech


@router.post("", response_model=TechnicianResponse, status_code=status.HTTP_201_CREATED)
def create_technician(data: TechnicianCreate, db: DbSession, _: RequireManager):
    tech = Technician(**data.model_dump())
    return TechnicianRepository(db).create(tech)


@router.put("/{technician_id}", response_model=TechnicianResponse)
def update_technician(technician_id: int, data: TechnicianUpdate, db: DbSession, _: RequireManager):
    repo = TechnicianRepository(db)
    tech = repo.get(technician_id)
    if not tech:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Technician not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(tech, field, value)
    return repo.update(tech)


@router.delete("/{technician_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_technician(technician_id: int, db: DbSession, _: RequireManager):
    repo = TechnicianRepository(db)
    tech = repo.get(technician_id)
    if not tech:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Technician not found")
    repo.delete(tech)
