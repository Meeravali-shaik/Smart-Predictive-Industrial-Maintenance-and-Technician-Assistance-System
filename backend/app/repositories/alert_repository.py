"""Alert repository."""

from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.alert import Alert, AlertSeverity, AlertStatus
from app.repositories.base import BaseRepository


class AlertRepository(BaseRepository[Alert]):
    def __init__(self, db: Session):
        super().__init__(Alert, db)

    def get_active_count(self) -> int:
        stmt = select(func.count()).select_from(Alert).where(Alert.status == AlertStatus.ACTIVE)
        return self.db.scalar(stmt) or 0

    def get_recent(self, limit: int = 20) -> List[Alert]:
        stmt = select(Alert).order_by(Alert.created_at.desc()).limit(limit)
        return list(self.db.scalars(stmt).all())

    def search(
        self,
        status: Optional[AlertStatus] = None,
        severity: Optional[AlertSeverity] = None,
        machine_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[List[Alert], int]:
        stmt = select(Alert)
        count_stmt = select(func.count()).select_from(Alert)

        if status:
            stmt = stmt.where(Alert.status == status)
            count_stmt = count_stmt.where(Alert.status == status)
        if severity:
            stmt = stmt.where(Alert.severity == severity)
            count_stmt = count_stmt.where(Alert.severity == severity)
        if machine_id:
            stmt = stmt.where(Alert.machine_id == machine_id)
            count_stmt = count_stmt.where(Alert.machine_id == machine_id)

        total = self.db.scalar(count_stmt) or 0
        items = list(self.db.scalars(stmt.order_by(Alert.created_at.desc()).offset(skip).limit(limit)).all())
        return items, total

    def get_active_for_machine(self, machine_id: int, alert_type: str) -> Optional[Alert]:
        stmt = select(Alert).where(
            Alert.machine_id == machine_id,
            Alert.alert_type == alert_type,
            Alert.status == AlertStatus.ACTIVE,
        )
        return self.db.scalar(stmt)
