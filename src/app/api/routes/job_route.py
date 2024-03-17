from fastapi import APIRouter, Depends, status, Query
import json
from src.app.api.controllers.job_controller import JobController
from src.app.api.schemas.job_schema import JobCreate, JobOut, JobUpdate
from src.app.common.api_response import ApiResponse
from src.app.common.pagination import Pagination
from src.app.dependencies import get_db, get_current_user, identify_consumer
from src.app.config.cache.redis import get_redis_cache, set_redis_cache

router = APIRouter(
    prefix="/api/v1/jobs",
    tags=["Jobs"],
    dependencies=[Depends(get_current_user), Depends(identify_consumer)],
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
    cache_key = f"job_{job_id}"
    cached_job = await get_redis_cache(cache_key)

    if cached_job is not None:
        cached_job = json.loads(cached_job)
        return ApiResponse[JobOut].success_with_object(object=cached_job)

    job = JobController.get_job_by_id(db, job_id)
    await set_redis_cache(cache_key, job.model_dump_json())
    return ApiResponse[JobOut].success_with_object(object=job)


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
    cache_key = f"jobs_page_{page}_limit_{limit}"
    cached_jobs = await get_redis_cache(cache_key)

    if cached_jobs is not None:
        cached_jobs = json.loads(cached_jobs)
        return ApiResponse[Pagination[JobOut]].success_with_object(object=cached_jobs)

    jobs = JobController.get_jobs(db, page, limit)
    await set_redis_cache(cache_key, jobs.model_dump_json())
    return ApiResponse[Pagination[JobOut]].success_with_object(object=jobs)


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
