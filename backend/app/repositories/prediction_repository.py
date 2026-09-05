"""Prediction repository."""

from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.prediction import Prediction
from app.repositories.base import BaseRepository


class PredictionRepository(BaseRepository[Prediction]):
    def __init__(self, db: Session):
        super().__init__(Prediction, db)

    def get_latest_for_machine(self, machine_id: int) -> Prediction | None:
        stmt = (
            select(Prediction)
            .where(Prediction.machine_id == machine_id)
            .order_by(Prediction.created_at.desc())
            .limit(1)
        )
        return self.db.scalar(stmt)

    def get_recent(self, limit: int = 20) -> List[Prediction]:
        stmt = select(Prediction).order_by(Prediction.created_at.desc()).limit(limit)
        return list(self.db.scalars(stmt).all())

    def get_trends_for_machine(self, machine_id: int, limit: int = 100) -> List[Prediction]:
        stmt = (
            select(Prediction)
            .where(Prediction.machine_id == machine_id)
            .order_by(Prediction.created_at.asc())
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())
