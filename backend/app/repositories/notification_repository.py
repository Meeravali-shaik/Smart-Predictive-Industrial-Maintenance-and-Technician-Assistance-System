"""Notification repository."""

from typing import List

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.repositories.base import BaseRepository


class NotificationRepository(BaseRepository[Notification]):
    def __init__(self, db: Session):
        super().__init__(Notification, db)

    def get_for_user(self, user_id: int, skip: int = 0, limit: int = 20) -> tuple[List[Notification], int]:
        stmt = select(Notification).where(Notification.user_id == user_id)
        count_stmt = select(func.count()).select_from(Notification).where(Notification.user_id == user_id)
        total = self.db.scalar(count_stmt) or 0
        items = list(
            self.db.scalars(stmt.order_by(Notification.created_at.desc()).offset(skip).limit(limit)).all()
        )
        return items, total

    def get_unread_count(self, user_id: int) -> int:
        stmt = (
            select(func.count())
            .select_from(Notification)
            .where(Notification.user_id == user_id, Notification.is_read.is_(False))
        )
        return self.db.scalar(stmt) or 0
