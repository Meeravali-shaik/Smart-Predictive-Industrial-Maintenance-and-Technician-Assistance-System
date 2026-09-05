"""Technician repository."""

from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.technician import AvailabilityStatus, Technician
from app.repositories.base import BaseRepository


class TechnicianRepository(BaseRepository[Technician]):
    def __init__(self, db: Session):
        super().__init__(Technician, db)

    def get_available_count(self) -> int:
        stmt = (
            select(func.count())
            .select_from(Technician)
            .where(
                Technician.availability == AvailabilityStatus.AVAILABLE,
                Technician.is_active.is_(True),
            )
        )
        return self.db.scalar(stmt) or 0

    def get_available_technician(self, skills_keyword: Optional[str] = None, specialization: Optional[str] = None) -> Optional[Technician]:
        stmt = select(Technician).where(
            Technician.availability == AvailabilityStatus.AVAILABLE,
            Technician.is_active.is_(True),
        )
        if skills_keyword:
            stmt = stmt.where(Technician.skills.ilike(f"%{skills_keyword}%"))
        if specialization:
            stmt = stmt.where(
                (Technician.specialization.is_(None)) | Technician.specialization.ilike(f"%{specialization}%")
            )
        stmt = stmt.order_by(Technician.current_workload.asc(), Technician.assignment_count.asc(), Technician.id.asc()).limit(1)
        return self.db.scalar(stmt)

    def search(
        self,
        search: Optional[str] = None,
        availability: Optional[AvailabilityStatus] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[List[Technician], int]:
        stmt = select(Technician)
        count_stmt = select(func.count()).select_from(Technician)

        if search:
            pattern = f"%{search}%"
            condition = Technician.name.ilike(pattern) | Technician.skills.ilike(pattern)
            stmt = stmt.where(condition)
            count_stmt = count_stmt.where(condition)

        if availability:
            stmt = stmt.where(Technician.availability == availability)
            count_stmt = count_stmt.where(Technician.availability == availability)

        total = self.db.scalar(count_stmt) or 0
        items = list(self.db.scalars(stmt.order_by(Technician.id.desc()).offset(skip).limit(limit)).all())
        return items, total
