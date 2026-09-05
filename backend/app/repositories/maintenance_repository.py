"""Maintenance history repository."""

from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.maintenance_history import MaintenanceHistory
from app.repositories.base import BaseRepository


class MaintenanceRepository(BaseRepository[MaintenanceHistory]):
    def __init__(self, db: Session):
        super().__init__(MaintenanceHistory, db)

    def get_for_machine(self, machine_id: int, limit: int = 20) -> List[MaintenanceHistory]:
        stmt = (
            select(MaintenanceHistory)
            .where(MaintenanceHistory.machine_id == machine_id)
            .order_by(MaintenanceHistory.repair_date.desc())
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def get_recent(self, limit: int = 20) -> List[MaintenanceHistory]:
        stmt = select(MaintenanceHistory).order_by(MaintenanceHistory.repair_date.desc()).limit(limit)
        return list(self.db.scalars(stmt).all())

    def search(
        self,
        machine_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[List[MaintenanceHistory], int]:
        stmt = select(MaintenanceHistory)
        count_stmt = select(func.count()).select_from(MaintenanceHistory)

        if machine_id:
            stmt = stmt.where(MaintenanceHistory.machine_id == machine_id)
            count_stmt = count_stmt.where(MaintenanceHistory.machine_id == machine_id)

        total = self.db.scalar(count_stmt) or 0
        items = list(
            self.db.scalars(stmt.order_by(MaintenanceHistory.repair_date.desc()).offset(skip).limit(limit)).all()
        )
        return items, total

    def get_total_downtime(self) -> float:
        stmt = select(func.sum(MaintenanceHistory.downtime_hours))
        return float(self.db.scalar(stmt) or 0)

    def get_monthly_failures(self) -> int:
        return self.count()
