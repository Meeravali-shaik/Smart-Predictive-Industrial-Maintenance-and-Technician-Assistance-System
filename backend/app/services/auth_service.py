"""Authentication and user management service."""

from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.audit_log import AuditLog
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas import UserCreate, UserUpdate


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def register(self, user_data: UserCreate) -> User:
        if self.user_repo.get_by_email(user_data.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        if self.user_repo.get_by_username(user_data.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

        user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            role=user_data.role,
            hashed_password=get_password_hash(user_data.password),
        )
        return self.user_repo.create(user)

    def authenticate(self, username: str, password: str) -> Optional[User]:
        user = self.user_repo.get_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is inactive")
        return user

    def login(self, username: str, password: str) -> dict:
        user = self.authenticate(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        token = create_access_token({"sub": str(user.id), "role": user.role.value})
        self._log_action(user.id, "login", "auth", str(user.id))
        return {"access_token": token, "token_type": "bearer", "user": user}

    def update_user(self, user: User, data: UserUpdate) -> User:
        update_data = data.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        for field, value in update_data.items():
            setattr(user, field, value)
        return self.user_repo.update(user)

    def _log_action(self, user_id: int, action: str, resource: str, resource_id: str) -> None:
        log = AuditLog(user_id=user_id, action=action, resource=resource, resource_id=resource_id)
        self.db.add(log)
        self.db.commit()
