"""Machine management API routes."""

import math
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import CurrentUser, DbSession, RequireManager
from app.models.audit_log import AuditLog
from app.models.machine import Machine, MachineStatus
from app.repositories.machine_repository import MachineRepository
from app.schemas import MachineCreate, MachineResponse, MachineUpdate, PaginatedResponse

router = APIRouter(prefix="/machines", tags=["Machines"])


@router.get("", response_model=PaginatedResponse[MachineResponse])
def list_machines(
    db: DbSession,
    _: CurrentUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    status: Optional[MachineStatus] = None,
    factory: Optional[str] = None,
):
    repo = MachineRepository(db)
    skip = (page - 1) * page_size
    items, total = repo.search(search=search, status=status, factory=factory, skip=skip, limit=page_size)
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=math.ceil(total / page_size) if total else 0,
    )


@router.get("/{machine_id}", response_model=MachineResponse)
def get_machine(machine_id: int, db: DbSession, _: CurrentUser):
    machine = MachineRepository(db).get(machine_id)
    if not machine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine not found")
    return machine


@router.post("", response_model=MachineResponse, status_code=status.HTTP_201_CREATED)
def create_machine(data: MachineCreate, db: DbSession, current_user: RequireManager):
    repo = MachineRepository(db)
    if repo.get_by_machine_id(data.machine_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Machine ID already exists")
    machine = Machine(**data.model_dump())
    created = repo.create(machine)
    _log(db, current_user.id, "create", "machine", str(created.id))
    return created


@router.put("/{machine_id}", response_model=MachineResponse)
def update_machine(machine_id: int, data: MachineUpdate, db: DbSession, current_user: RequireManager):
    repo = MachineRepository(db)
    machine = repo.get(machine_id)
    if not machine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(machine, field, value)
    updated = repo.update(machine)
    _log(db, current_user.id, "update", "machine", str(updated.id))
    return updated


@router.delete("/{machine_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_machine(machine_id: int, db: DbSession, current_user: RequireManager):
    repo = MachineRepository(db)
    machine = repo.get(machine_id)
    if not machine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine not found")
    _log(db, current_user.id, "delete", "machine", str(machine.id))
    repo.delete(machine)


def _log(db, user_id: int, action: str, resource: str, resource_id: str) -> None:
    db.add(AuditLog(user_id=user_id, action=action, resource=resource, resource_id=resource_id))
    db.commit()
