from app.api.schemas.province_schema import ProvinceBase
from app.api.schemas.job_field_schema import FieldBase
from pydantic import BaseModel, Field
from typing import List, Optional


class ResumeBase(BaseModel):
    title: str
    salary: int


class ResumeCreate(ResumeBase):
    seekerId: int = Field(...)
    careerObj: str = Field(...)
    title: str = Field(...)
    salary: int = Field(...)
    fieldIds: List[int] = Field(...)
    provinceIds: List[int] = Field(...)


class ResumeUpdate(ResumeBase):
    careerObj: str = Field(...)
    title: str = Field(...)
    salary: int = Field(...)
    fieldIds: List[int] = Field(...)
    provinceIds: List[int] = Field(...)


class ResumeOut(ResumeBase):
    id: int
    seekerId: Optional[int] = None
    seekerName: Optional[str] = None
    careerObj: str
    title: str
    salary: int
    fields: List[FieldBase]
    provinces: List[ProvinceBase]
