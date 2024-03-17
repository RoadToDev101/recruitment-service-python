import os
from dotenv import load_dotenv
from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session
from src.app.utils.jwt import create_access_token
from src.app.dependencies import get_db
from src.app.api.controllers.user_controller import UserController
from src.app.api.schemas.user_schema import UserCreate
from src.app.common.token_response import TokenResponse

load_dotenv()

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=TokenResponse,
)
async def register(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = UserCreate(username=form_data.username, password=form_data.password)
    new_user = UserController.create_user(db, user=user)

    expires_delta = timedelta(days=float(os.getenv("JWT_LIFETIME_DAYS")))

    access_token = create_access_token(
        data={"sub": new_user.id},
        expires_delta=expires_delta,
    )

    return TokenResponse.token_response(
        access_token=access_token,
        token_type="bearer",
        user_id=new_user.id,
        role=new_user.role,
        message="User registered successfully",
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    authenticated_user = UserController.authenticate_user(
        db, form_data.username, form_data.password
    )

    access_token_lifespan = timedelta(days=float(os.getenv("JWT_LIFETIME_DAYS")))
    access_token = create_access_token(
        data={"sub": authenticated_user.user_id},
        expires_delta=access_token_lifespan,
    )

    return TokenResponse.token_response(
        access_token=access_token,
        token_type="bearer",
        user_id=authenticated_user.user_id,
        role=authenticated_user.role,
        message="User logged in successfully",
    )
