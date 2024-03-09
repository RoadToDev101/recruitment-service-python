from src.app.api.schemas.province_schema import ProvinceBase
from src.app.api.schemas.job_field_schema import FieldBase
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class JobBase(BaseModel):
    title: str
    quantity: int
    description: str
    salary: int
    expiredAt: datetime


class JobCreate(JobBase):
    title: str = Field(..., max_length=255)
    employerId: int = Field(..., ge=1)
    quantity: int = Field(..., ge=1)
    description: str = Field(...)
    fieldIds: List[int] = Field(...)
    provinceIds: List[int] = Field(...)
    salary: int = Field(..., ge=1)
    expiredAt: datetime = Field(...)


class JobUpdate(JobBase):
    title: str = Field(..., max_length=255)
    quantity: int = Field(..., ge=1)
    description: str = Field(...)
    salary: int = Field(..., ge=1)
    fieldIds: List[int] = Field(...)
    provinceIds: List[int] = Field(...)
    expiredAt: datetime = Field(...)


class JobOut(JobBase):
    id: int
    title: str
    quantity: int
    description: str
    fields: List[FieldBase]
    provinces: List[ProvinceBase]
    salary: int
    expiredAt: Optional[datetime] = None
    employerId: Optional[int] = None
    employerName: Optional[str] = None
