from fastapi import APIRouter, Depends, status, Query
from app.api.controllers.employer_controller import EmployerController
from app.api.models.employer_model import EmployerCreate, EmployerOut, EmployerUpdate
from app.common.api_response import ApiResponse
from app.common.pagination import Pagination
from app.dependencies import get_db

router = APIRouter(
    prefix="/api/v1/employers",
    tags=["Employers"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse,
)
async def create_employer(employer: EmployerCreate, db=Depends(get_db)):
    return ApiResponse.success_message_only(
        message=EmployerController.create_employer(db, employer)
    )


@router.patch(
    "/{employer_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse,
)
async def update_employer(
    employer_id: int, employer: EmployerUpdate, db=Depends(get_db)
):
    return ApiResponse.success_message_only(
        message=EmployerController.update_employer_by_id(db, employer_id, employer)
    )


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[Pagination[EmployerOut]],
)
async def get_employers(
    page: int = Query(1, ge=1),
    pageSize: int = Query(10, ge=1, le=500),
    db=Depends(get_db),
):
    employers = EmployerController.get_employers(db, page, pageSize)
    return ApiResponse[Pagination[EmployerOut]].success_with_object(object=employers)


@router.get(
    "/{employer_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[EmployerOut],
)
async def get_employer_by_id(employer_id: int, db=Depends(get_db)):
    employer = EmployerController.get_employer_by_id(db, employer_id)
    return ApiResponse[EmployerOut].success_with_object(object=employer)


@router.delete(
    "/{employer_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse,
)
async def delete_employer_by_id(employer_id: int, db=Depends(get_db)):
    return ApiResponse.success_message_only(
        message=EmployerController.delete_employer_by_id(db, employer_id)
    )
