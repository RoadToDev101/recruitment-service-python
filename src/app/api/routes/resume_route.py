from fastapi import APIRouter, Depends, status, Query
from app.api.controllers.resume_controller import ResumeController
from app.api.schemas.resume_schema import ResumeCreate, ResumeOut, ResumeUpdate
from app.common.api_response import ApiResponse
from app.common.pagination import Pagination
from app.dependencies import get_db
from app.config.cache.redis import get_redis_cache, set_redis_cache
import json

router = APIRouter(
    prefix="/api/v1/resumes",
    tags=["Resumes"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse,
)
async def create_resume(resume: ResumeCreate, db=Depends(get_db)):
    return ApiResponse.success_message_only(
        message=ResumeController.create_resume(db, resume)
    )


@router.get(
    "/{resume_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse,
)
async def get_resume_by_id(resume_id: int, db=Depends(get_db)):
    cache_key = f"resume_{resume_id}"
    cached_resume = await get_redis_cache(cache_key)

    if cached_resume is not None:
        cached_resume = json.loads(cached_resume)
        return ApiResponse.success_with_object(object=cached_resume)

    resume = ResumeController.get_resume_by_id(db, resume_id)
    await set_redis_cache(cache_key, resume.model_dump_json())
    return ApiResponse.success_with_object(object=resume)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[Pagination[ResumeOut]],
)
async def get_resumes(
    page: int = Query(1, gt=0),
    limit: int = Query(10, gt=0),
    db=Depends(get_db),
):
    cache_key = f"resumes_page_{page}_limit_{limit}"
    cached_resumes = await get_redis_cache(cache_key)

    if cached_resumes is not None:
        cached_resumes = json.loads(cached_resumes)
        return ApiResponse[Pagination[ResumeOut]].success_with_object(
            object=cached_resumes
        )

    resumes = ResumeController.get_resumes(db, page, limit)
    await set_redis_cache(cache_key, resumes.model_dump_json())
    return ApiResponse[Pagination[ResumeOut]].success_with_object(object=resumes)


@router.patch(
    "/{resume_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse,
)
async def update_resume(resume_id: int, resume: ResumeUpdate, db=Depends(get_db)):
    return ApiResponse.success_message_only(
        message=ResumeController.update_resume_by_id(db, resume_id, resume)
    )


@router.delete(
    "/{resume_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse,
)
async def delete_resume(resume_id: int, db=Depends(get_db)):
    return ApiResponse.success_message_only(
        message=ResumeController.delete_resume_by_id(db, resume_id)
    )
