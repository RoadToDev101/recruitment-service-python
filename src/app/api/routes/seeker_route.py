import json
from fastapi import APIRouter, Depends, status, Query
from src.app.api.controllers.seeker_controller import SeekerController
from src.app.api.schemas.seeker_schema import SeekerCreate, SeekerOut, SeekerUpdate
from src.app.common.api_response import ApiResponse
from src.app.common.pagination import Pagination
from src.app.dependencies import get_db, get_current_user, identify_consumer
from src.app.config.cache.redis import get_redis_cache, set_redis_cache

router = APIRouter(
    prefix="/api/v1/seekers",
    tags=["Seekers"],
    dependencies=[Depends(get_current_user), Depends(identify_consumer)],
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
    cache_key = f"seeker_{seeker_id}"
    cached_seeker = await get_redis_cache(cache_key)

    if cached_seeker is not None:
        cached_seeker = json.loads(cached_seeker)
        return ApiResponse[SeekerOut].success_with_object(object=cached_seeker)

    seeker = SeekerController.get_seeker_by_id(db, seeker_id)
    await set_redis_cache(cache_key, seeker.model_dump_json())
    return ApiResponse[SeekerOut].success_with_object(object=seeker)


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
    cache_key = f"seekers_page_{page}_size_{pageSize}"
    cached_seekers = await get_redis_cache(cache_key)

    if cached_seekers is not None:
        cached_seekers = json.loads(cached_seekers)
        return ApiResponse[Pagination[SeekerOut]].success_with_object(
            object=cached_seekers
        )

    seekers = SeekerController.get_seekers(db, page, pageSize)
    await set_redis_cache(cache_key, seekers.model_dump_json())
    return ApiResponse[Pagination[SeekerOut]].success_with_object(object=seekers)


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
