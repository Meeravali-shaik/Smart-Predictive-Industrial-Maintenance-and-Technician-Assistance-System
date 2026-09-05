"""Machine repository."""

from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.machine import Machine, MachineStatus
from app.repositories.base import BaseRepository


class MachineRepository(BaseRepository[Machine]):
    def __init__(self, db: Session):
        super().__init__(Machine, db)

    def get_by_machine_id(self, machine_id: str) -> Optional[Machine]:
        stmt = select(Machine).where(Machine.machine_id == machine_id)
        return self.db.scalar(stmt)

    def search(
        self,
        search: Optional[str] = None,
        status: Optional[MachineStatus] = None,
        factory: Optional[str] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[List[Machine], int]:
        stmt = select(Machine)
        count_stmt = select(func.count()).select_from(Machine)

        if search:
            pattern = f"%{search}%"
            condition = (
                Machine.name.ilike(pattern)
                | Machine.machine_id.ilike(pattern)
                | Machine.location.ilike(pattern)
            )
            stmt = stmt.where(condition)
            count_stmt = count_stmt.where(condition)

        if status:
            stmt = stmt.where(Machine.status == status)
            count_stmt = count_stmt.where(Machine.status == status)

        if factory:
            stmt = stmt.where(Machine.factory == factory)
            count_stmt = count_stmt.where(Machine.factory == factory)

        total = self.db.scalar(count_stmt) or 0
        items = list(self.db.scalars(stmt.order_by(Machine.id.desc()).offset(skip).limit(limit)).all())
        return items, total

    def count_by_status(self, status: MachineStatus) -> int:
        stmt = select(func.count()).select_from(Machine).where(Machine.status == status)
        return self.db.scalar(stmt) or 0
