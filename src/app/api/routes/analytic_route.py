from app.common.api_response import ApiResponse
from app.common.pagination import Pagination
from app.dependencies import get_db
from app.api.controllers.analytic_controller import AnalyticController
from app.api.schemas.analytic_schema import (
    InputTimeFrame,
    OverallStatistic,
    SuitableSeekers,
)
from fastapi import APIRouter, Depends, Query, status
from datetime import date

router = APIRouter(
    prefix="/api/v1/analytic",
    tags=["Analytic"],
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
    return ApiResponse[OverallStatistic].success_with_object(
        object=AnalyticController.get_overall_statistic(db, fromDate, toDate)
    )


@router.get(
    "/suitable-seekers",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[SuitableSeekers],
)
async def get_suitable_seekers(
    job_id: int = Query(..., gt=0),
    page: int = Query(1, gt=0),
    pageSize: int = Query(10, gt=0),
    db=Depends(get_db),
):
    return ApiResponse[SuitableSeekers].success_with_object(
        object=AnalyticController.find_suitable_seekers(db, job_id, page, pageSize)
    )
