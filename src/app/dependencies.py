from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError
from typing import Annotated
from src.app.config.database.mysql import MySQLConnection
from src.app.api.controllers.user_controller import UserController
from src.app.utils.jwt import decode_access_token
from src.app.api.schemas.user_schema import UserOut, UserBase
from src.app.api.models.user_model import UserRole
from src.app.common.custom_exception import CredentialsException, ForbiddenException


def get_db():
    db = MySQLConnection().SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
) -> UserOut:
    try:
        payload = decode_access_token(token)
        user_id: int = payload.get("sub")

        if user_id is None:
            raise CredentialsException
    except JWTError:
        raise CredentialsException

    user = UserController.get_user_by_id(db, user_id=user_id)
    if user is None:
        raise CredentialsException
    return user


def identify_consumer(
    request: Request, current_user: Annotated[UserBase, Depends(get_current_user)]
):
    request.state.consumer_identifier = current_user.id


async def get_current_admin(
    current_user: Annotated[UserOut, Depends(get_current_user)]
):
    if current_user.role != UserRole.ADMIN:
        raise ForbiddenException()
    return current_user
