from sqlalchemy import Column, String, Integer, BigInteger, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.config.database.mysql import Base
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


# MODEL
class Seeker(Base):
    __tablename__ = "seeker"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)
    birthday = Column(String, nullable=False)  # yyyy-MM-dd
    address = Column(String, nullable=False)
    province = Column(Integer, ForeignKey("job_province.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    province_data = relationship("Province", back_populates="seekers")


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
