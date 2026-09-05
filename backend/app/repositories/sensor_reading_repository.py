"""Sensor reading repository."""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.sensor_reading import SensorReading
from app.repositories.base import BaseRepository


class SensorReadingRepository(BaseRepository[SensorReading]):
    def __init__(self, db: Session):
        super().__init__(SensorReading, db)

    def get_latest_for_machine(self, machine_id: int, limit: int = 50) -> List[SensorReading]:
        stmt = (
            select(SensorReading)
            .where(SensorReading.machine_id == machine_id)
            .order_by(SensorReading.recorded_at.desc())
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def get_recent(self, limit: int = 20) -> List[SensorReading]:
        stmt = select(SensorReading).order_by(SensorReading.recorded_at.desc()).limit(limit)
        return list(self.db.scalars(stmt).all())

    def get_trends(
        self, machine_id: int, since: datetime, limit: int = 100
    ) -> List[SensorReading]:
        stmt = (
            select(SensorReading)
            .where(SensorReading.machine_id == machine_id, SensorReading.recorded_at >= since)
            .order_by(SensorReading.recorded_at.asc())
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def get_averages_for_machine(self, machine_id: int) -> dict[str, float]:
        stmt = select(
            func.avg(SensorReading.temperature),
            func.avg(SensorReading.current),
            func.avg(SensorReading.vibration),
        ).where(SensorReading.machine_id == machine_id)
        result = self.db.execute(stmt).one()
        return {
            "average_temperature": float(result[0] or 0),
            "average_current": float(result[1] or 0),
            "average_vibration": float(result[2] or 0),
        }
