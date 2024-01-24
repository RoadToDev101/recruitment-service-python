from pydantic import BaseModel, Field
from typing import Optional


class SeekerBase(BaseModel):
    name: str
    birthday: str
    provinceId: int


class SeekerCreate(SeekerBase):
    name: str = Field(..., max_length=255)
    birthday: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    address: Optional[str]
    provinceId: int = Field(..., ge=1)


class SeekerUpdate(SeekerBase):
    name: str = Field(..., max_length=255)
    birthday: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    address: Optional[str]
    provinceId: int = Field(..., ge=1)


class SeekerOut(SeekerBase):
    id: int
    name: str
    birthday: str
    address: Optional[str]
    provinceId: Optional[int]
    provinceName: Optional[str]
