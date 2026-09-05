"""Notification API routes."""

import math

from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import CurrentUser, DbSession
from app.repositories.notification_repository import NotificationRepository
from app.schemas import MessageResponse, NotificationResponse, PaginatedResponse

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("", response_model=PaginatedResponse[NotificationResponse])
def list_notifications(
    db: DbSession,
    current_user: CurrentUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    repo = NotificationRepository(db)
    skip = (page - 1) * page_size
    items, total = repo.get_for_user(current_user.id, skip=skip, limit=page_size)
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=math.ceil(total / page_size) if total else 0,
    )


@router.put("/{notification_id}/read", response_model=NotificationResponse)
def mark_as_read(notification_id: int, db: DbSession, current_user: CurrentUser):
    repo = NotificationRepository(db)
    notification = repo.get(notification_id)
    if not notification or notification.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    notification.is_read = True
    notification.status = "read"
    return repo.update(notification)


@router.put("/{notification_id}/archive", response_model=NotificationResponse)
def archive_notification(notification_id: int, db: DbSession, current_user: CurrentUser):
    repo = NotificationRepository(db)
    notification = repo.get(notification_id)
    if not notification or notification.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    notification.status = "archived"
    return repo.update(notification)


@router.put("/read-all", response_model=MessageResponse)
def mark_all_read(db: DbSession, current_user: CurrentUser):
    repo = NotificationRepository(db)
    items, _ = repo.get_for_user(current_user.id, skip=0, limit=1000)
    for notification in items:
        notification.is_read = True
        notification.status = "read"
    db.commit()
    return MessageResponse(message="All notifications marked as read")
