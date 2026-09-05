"""Authentication API routes."""

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import CurrentUser, DbSession
from app.schemas import Token, UserCreate, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: DbSession):
    return AuthService(db).register(user_data)


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: DbSession = None):
    result = AuthService(db).login(form_data.username, form_data.password)
    return {"access_token": result["access_token"], "token_type": result["token_type"]}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: CurrentUser):
    return current_user
