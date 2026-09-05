"""User management API routes."""

import math

from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import CurrentUser, DbSession, RequireAdmin
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas import PaginatedResponse, UserResponse, UserUpdate
from app.services.auth_service import AuthService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=PaginatedResponse[UserResponse])
def list_users(
    db: DbSession,
    _: RequireAdmin,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    repo = UserRepository(db)
    skip = (page - 1) * page_size
    items = repo.get_all(skip=skip, limit=page_size)
    total = repo.count()
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=math.ceil(total / page_size) if total else 0,
    )


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: DbSession, current_user: CurrentUser):
    if current_user.id != user_id and current_user.role.value != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    user = UserRepository(db).get(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, data: UserUpdate, db: DbSession, current_user: CurrentUser):
    if current_user.id != user_id and current_user.role.value != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    user = UserRepository(db).get(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return AuthService(db).update_user(user, data)
