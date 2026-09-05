"""Alert management API routes."""

import math
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import CurrentUser, DbSession
from app.models.alert import AlertSeverity, AlertStatus
from app.repositories.alert_repository import AlertRepository
from app.repositories.machine_repository import MachineRepository
from app.repositories.maintenance_repository import MaintenanceRepository
from app.repositories.technician_repository import TechnicianRepository
from app.schemas import (
    AlertResponse,
    AlertUpdate,
    PaginatedResponse,
    TechnicianAssistanceResponse,
)
from app.services.alert_service import AlertService

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("", response_model=PaginatedResponse[AlertResponse])
def list_alerts(
    db: DbSession,
    _: CurrentUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status_filter: Optional[AlertStatus] = Query(None, alias="status"),
    severity: Optional[AlertSeverity] = None,
    machine_id: Optional[int] = None,
):
    repo = AlertRepository(db)
    skip = (page - 1) * page_size
    items, total = repo.search(status=status_filter, severity=severity, machine_id=machine_id, skip=skip, limit=page_size)
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=math.ceil(total / page_size) if total else 0,
    )


@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: int, db: DbSession, _: CurrentUser):
    alert = AlertRepository(db).get(alert_id)
    if not alert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")
    return alert


@router.put("/{alert_id}", response_model=AlertResponse)
def update_alert(alert_id: int, data: AlertUpdate, db: DbSession, _: CurrentUser):
    repo = AlertRepository(db)
    alert = repo.get(alert_id)
    if not alert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")

    service = AlertService(db)
    if data.status == AlertStatus.RESOLVED:
        alert = service.resolve_alert(alert)
    elif data.status == AlertStatus.ACKNOWLEDGED:
        alert = service.acknowledge_alert(alert)
    else:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(alert, field, value)
        alert = repo.update(alert)
    return alert


@router.get("/{alert_id}/assistance", response_model=TechnicianAssistanceResponse)
def get_technician_assistance(alert_id: int, db: DbSession, _: CurrentUser):
    alert_repo = AlertRepository(db)
    alert = alert_repo.get(alert_id)
    if not alert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")

    machine = MachineRepository(db).get(alert.machine_id)
    technician = TechnicianRepository(db).get(alert.technician_id) if alert.technician_id else None
    maintenance = MaintenanceRepository(db).get_for_machine(alert.machine_id)

    return TechnicianAssistanceResponse(
        alert=alert,
        machine=machine,
        technician=technician,
        fault=alert.message,
        priority=alert.severity.value,
        recommended_action=alert.recommended_action or "Follow standard maintenance procedures.",
        maintenance_history=maintenance,
    )
