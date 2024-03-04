from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.api.controllers.user_controller import UserController
from app.api.schemas.user_schema import UserUpdate, UserOut
from app.common.pagination import Pagination
from app.dependencies import get_current_user, get_current_admin
from app.common.api_response import ApiResponse
from app.common.custom_exception import ForbiddenException

router = APIRouter(
    prefix="/api/v1/users", tags=["Users"], dependencies=[Depends(get_current_user)]
)


@router.get(
    "/{user_id}", status_code=status.HTTP_200_OK, response_model=ApiResponse[UserOut]
)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
):
    if current_user.role != "admin" and current_user.id != user_id:
        raise ForbiddenException
    user = UserController.get_user_by_id(db, user_id=user_id)
    return ApiResponse[UserOut].success_with_object(object=user)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[Pagination[UserOut]],
    dependencies=[Depends(get_current_admin)],
)
async def get_all_users(
    page: int = Query(1, ge=1),
    pageSize: int = Query(10, ge=1, le=500),
    db: Session = Depends(get_db),
):
    users = UserController.get_users(db, page, pageSize)
    return ApiResponse[Pagination[UserOut]].success_with_object(object=users)


@router.patch(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[UserOut],
)
async def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise ForbiddenException

    return ApiResponse[UserOut].success_message_only(
        message=UserController.update_user_by_id(db, user_id=user_id, user=user)
    )


@router.delete(
    "/{user_id}", status_code=status.HTTP_200_OK, response_model=ApiResponse[str]
)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
):
    if current_user.id != user_id and current_user.role != "admin":
        raise ForbiddenException

    return ApiResponse[str].success_message_only(
        message=UserController.delete_user_by_id(db, user_id=user_id)
    )
