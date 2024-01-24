from fastapi import APIRouter, Depends, status, Query
from app.api.controllers.job_controller import JobController
from app.api.schemas.job_schema import JobCreate, JobOut, JobUpdate
from app.common.api_response import ApiResponse
from app.common.pagination import Pagination
from app.dependencies import get_db

router = APIRouter(
    prefix="/api/v1/jobs",
    tags=["Jobs"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse,
)
async def create_job(job: JobCreate, db=Depends(get_db)):
    return ApiResponse.success_message_only(message=JobController.create_job(db, job))


@router.get(
    "/{job_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[JobOut],
)
async def get_job_by_id(job_id: int, db=Depends(get_db)):
    return ApiResponse.success_with_object(
        object=JobController.get_job_by_id(db, job_id)
    )


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[Pagination[JobOut]],
)
async def get_jobs(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db=Depends(get_db),
):
    return ApiResponse.success_with_object(
        object=JobController.get_jobs(db, page, limit)
    )


@router.patch(
    "/{job_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse,
)
async def update_job(job_id: int, job: JobUpdate, db=Depends(get_db)):
    return ApiResponse.success_message_only(
        message=JobController.update_job_by_id(db, job_id, job)
    )


@router.delete(
    "/{job_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse,
)
async def delete_job(job_id: int, db=Depends(get_db)):
    return ApiResponse.success_message_only(
        message=JobController.delete_job_by_id(db, job_id)
    )
