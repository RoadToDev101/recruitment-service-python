from app.config.database.mysql import SessionLocal
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from sqlalchemy.orm import Session
from app.common.custom_exception import CredentialsException
from app.utils.jwt import decode_access_token
from app.common.custom_exception import ForbiddenException
from jose import JWTError
from typing import Annotated
from app.api.schemas.user_schema import UserOut
from app.api.models.user_model import UserRole
from app.api.controllers.user_controller import UserController


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


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


async def get_current_admin(
    current_user: Annotated[UserOut, Depends(get_current_user)]
):
    if current_user.role != UserRole.ADMIN:
        raise ForbiddenException()
    return current_user
