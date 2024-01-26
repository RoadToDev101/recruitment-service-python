from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class SeekerBase(BaseModel):
    name: str
    birthday: date
    provinceId: int


class SeekerCreate(SeekerBase):
    name: str = Field(..., max_length=255)
    birthday: date = Field(..., example="2000-01-01")
    address: Optional[str]
    provinceId: int = Field(..., ge=1)


class SeekerUpdate(SeekerBase):
    name: str = Field(..., max_length=255)
    birthday: date = Field(..., example="2000-01-01")
    address: Optional[str]
    provinceId: int = Field(..., ge=1)


class SeekerOut(SeekerBase):
    id: int
    name: str
    birthday: str
    address: Optional[str]
    provinceId: Optional[int]
    provinceName: Optional[str]
