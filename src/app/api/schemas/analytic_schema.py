from pydantic import BaseModel, Field
from typing import List
from datetime import date
from app.api.schemas.job_schema import JobOut
from app.api.schemas.seeker_schema import SeekerOut


class InputTimeFrame(BaseModel):
    fromDate: date = Field(..., example="2000-01-01")
    toDate: date = Field(..., example="2000-01-01")


class ChartElement(BaseModel):
    date: date
    numEmployer: int
    numJob: int
    numSeeker: int
    numResume: int


class OverallStatistic(BaseModel):
    numEmployer: int
    numJob: int
    numSeeker: int
    numResume: int
    chart: List[ChartElement]


class SuitableSeekers(JobOut):
    seekers: List[SeekerOut]
