from fastapi import APIRouter, Depends, status, Query
from src.app.api.controllers.employer_controller import EmployerController
from src.app.api.schemas.employer_schema import (
    EmployerCreate,
    EmployerUpdate,
    EmployerOut,
)
from src.app.common.api_response import ApiResponse
from src.app.common.pagination import Pagination
from src.app.dependencies import get_db
from src.app.config.cache.redis import get_redis_cache, set_redis_cache
import json
from sqlalchemy.orm import Session
from src.app.dependencies import get_current_user

router = APIRouter(
    prefix="/api/v1/employers",
    tags=["Employers"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse,
)
async def create_employer(
    employer: EmployerCreate,
    db: Session = Depends(get_db),
):
    return ApiResponse.success_message_only(
        message=EmployerController.create_employer(db, employer)
    )


@router.patch(
    "/{employer_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[EmployerOut],
)
async def update_employer(
    employer_id: int,
    employer: EmployerUpdate,
    db: Session = Depends(get_db),
):
    return ApiResponse.success_message_only(
        message=EmployerController.update_employer_by_id(db, employer_id, employer)
    )


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[Pagination[EmployerOut]],
)
async def get_all_employers(
    page: int = Query(1, ge=1),
    pageSize: int = Query(10, ge=1, le=500),
    db: Session = Depends(get_db),
):
    cache_key = f"employers_page_{page}_size_{pageSize}"
    cached_employers = await get_redis_cache(cache_key)

    if cached_employers is not None:
        cached_employers = json.loads(cached_employers)
        return ApiResponse[Pagination[EmployerOut]].success_with_object(
            object=cached_employers
        )

    employers = EmployerController.get_employers(db, page, pageSize)
    await set_redis_cache(cache_key, employers.model_dump_json())
    return ApiResponse[Pagination[EmployerOut]].success_with_object(object=employers)


@router.get(
    "/{employer_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[EmployerOut],
)
async def get_employer_by_employer_id(employer_id: int, db: Session = Depends(get_db)):
    cache_key = f"employer_{employer_id}"
    cached_employee = await get_redis_cache(cache_key)

    if cached_employee is not None:
        cached_employee = json.loads(cached_employee)
        return ApiResponse[EmployerOut].success_with_object(object=cached_employee)

    employer = EmployerController.get_employer_by_id(db, employer_id)
    await set_redis_cache(cache_key, employer.model_dump_json())
    return ApiResponse[EmployerOut].success_with_object(object=employer)


@router.delete(
    "/{employer_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse,
)
async def delete_employer_by_id(employer_id: int, db: Session = Depends(get_db)):
    return ApiResponse.success_message_only(
        message=EmployerController.delete_employer_by_id(db, employer_id)
    )
