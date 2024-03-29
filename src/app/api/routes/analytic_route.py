import json
from fastapi import APIRouter, Depends, Query, status
from datetime import date
from src.app.common.api_response import ApiResponse
from src.app.api.controllers.analytic_controller import AnalyticController
from src.app.api.schemas.analytic_schema import (
    InputTimeFrame,
    OverallStatistic,
    SuitableSeekers,
)
from src.app.config.cache.redis import get_redis_cache, set_redis_cache
from src.app.dependencies import get_current_admin, identify_consumer, get_db


router = APIRouter(
    prefix="/api/v1/analytic",
    tags=["Analytic"],
    dependencies=[Depends(get_current_admin), Depends(identify_consumer)],
)

input_time_frame = InputTimeFrame(fromDate=date(2022, 1, 1), toDate=date(2022, 12, 31))


@router.get(
    "/overall-statistic",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[OverallStatistic],
)
async def get_overall_statistic(
    fromDate: date = input_time_frame.fromDate,
    toDate: date = input_time_frame.toDate,
    db=Depends(get_db),
):
    """
    Retrieve the overall statistic within a specified time frame.

    Args:
        fromDate (date): The start date of the time frame.
        toDate (date): The end date of the time frame.
        db: The database dependency.

    Returns:
        ApiResponse[OverallStatistic]: The API response containing the overall statistic.
    """
    cache_key = f"overall_statistic_{fromDate}_{toDate}"
    cached_statistic = await get_redis_cache(cache_key)

    if cached_statistic is not None:
        cached_statistic = json.loads(cached_statistic)
        return ApiResponse[OverallStatistic].success_with_object(
            object=cached_statistic
        )

    statistic = AnalyticController.get_overall_statistic(db, fromDate, toDate)
    await set_redis_cache(cache_key, statistic.model_dump_json())
    return ApiResponse[OverallStatistic].success_with_object(object=statistic)


@router.get(
    "/suitable-seekers",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[SuitableSeekers],
)
async def get_suitable_seekers(
    job_id: int = Query(..., gt=0),
    db=Depends(get_db),
):
    cache_key = f"suitable_seekers_{job_id}"
    cached_seekers = await get_redis_cache(cache_key)

    if cached_seekers is not None:
        cached_seekers = json.loads(cached_seekers)
        return ApiResponse[SuitableSeekers].success_with_object(object=cached_seekers)

    seekers = AnalyticController.find_suitable_seekers(db, job_id)
    await set_redis_cache(cache_key, seekers.model_dump_json())
    return ApiResponse[SuitableSeekers].success_with_object(object=seekers)
