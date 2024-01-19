from sqlalchemy import Column, String, Integer, BigInteger, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.config.database.mysql import Base
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


# MODEL
class Job(Base):
    __tablename__ = "jobs"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    employer_id = Column(BigInteger, ForeignKey("employer.id"), nullable=False)
    title = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    salary = Column(Integer, nullable=False)
    fields = Column(String, nullable=False)
    provinces = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    expired_at = Column(DateTime, nullable=False)

    employer_data = relationship("Employer", back_populates="jobs_data")


# SCHEMA
class JobBase(BaseModel):
    title: str
    quantity: int
    description: str
    salary: int
    expiredAt: datetime


class FieldBase(BaseModel):
    id: int
    name: str


class ProvinceBase(BaseModel):
    id: int
    name: str


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
