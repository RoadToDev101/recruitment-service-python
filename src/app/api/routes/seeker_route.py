from fastapi import APIRouter, Depends, status, Query
from app.api.controllers.seeker_controller import SeekerController
from app.api.schemas.seeker_schema import SeekerCreate, SeekerOut, SeekerUpdate
from app.common.api_response import ApiResponse
from app.common.pagination import Pagination
from app.dependencies import get_db

router = APIRouter(
    prefix="/api/v1/seekers",
    tags=["Seekers"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse,
)
async def create_seeker(seeker: SeekerCreate, db=Depends(get_db)):
    return ApiResponse.success_message_only(
        message=SeekerController.create_seeker(db, seeker)
    )


@router.get(
    "/{seeker_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[SeekerOut],
)
async def get_seeker_by_id(seeker_id: int, db=Depends(get_db)):
    return ApiResponse.success_with_object(
        object=SeekerController.get_seeker_by_id(db, seeker_id)
    )


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[Pagination[SeekerOut]],
)
async def get_seekers(
    page: int = Query(1, ge=1),
    pageSize: int = Query(10, ge=1, le=500),
    db=Depends(get_db),
):
    return ApiResponse[Pagination[SeekerOut]].success_with_object(
        object=SeekerController.get_seekers(db, page, pageSize)
    )


@router.patch(
    "/{seeker_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse,
)
async def update_seeker(seeker_id: int, seeker: SeekerUpdate, db=Depends(get_db)):
    return ApiResponse.success_message_only(
        message=SeekerController.update_seeker_by_id(db, seeker_id, seeker)
    )


@router.delete(
    "/{seeker_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse,
)
async def delete_seeker(seeker_id: int, db=Depends(get_db)):
    return ApiResponse.success_message_only(
        message=SeekerController.delete_seeker_by_id(db, seeker_id)
    )
