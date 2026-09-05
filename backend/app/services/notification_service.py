"""Notification generation service for alerts, predictions, and maintenance events."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.notification import Notification, NotificationType
from app.models.user import User, UserRole


class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    def create_for_users(self, title: str, message: str, notification_type: NotificationType, reference_id: int | None = None) -> list[Notification]:
        users = self.db.query(User).filter(User.is_active.is_(True)).all()
        notifications = []
        for user in users:
            notification = Notification(
                user_id=user.id,
                title=title,
                message=message,
                notification_type=notification_type,
                reference_id=reference_id,
            )
            self.db.add(notification)
            notifications.append(notification)
        self.db.commit()
        return notifications

    def create_for_roles(self, title: str, message: str, notification_type: NotificationType, roles: list[UserRole], reference_id: int | None = None) -> list[Notification]:
        users = self.db.query(User).filter(User.is_active.is_(True), User.role.in_(roles)).all()
        notifications = []
        for user in users:
            notification = Notification(
                user_id=user.id,
                title=title,
                message=message,
                notification_type=notification_type,
                reference_id=reference_id,
            )
            self.db.add(notification)
            notifications.append(notification)
        self.db.commit()
        return notifications
