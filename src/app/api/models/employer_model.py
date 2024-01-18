from sqlalchemy import Column, Integer, BigInteger, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.config.database.mysql import Base
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# MODEL
class Employer(Base):
    __tablename__ = "employer"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    province = Column(Integer, ForeignKey("job_province.id"), nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    jobs_data = relationship(
        "Job", back_populates="employer_data", cascade="all, delete-orphan"
    )
    province_data = relationship("Province", back_populates="employers")


# SCHEMA
class EmployerBase(BaseModel):
    name: str
    provinceId: int
    description: Optional[str]


class EmployerCreate(EmployerBase):
    email: EmailStr = Field(..., max_length=255)
    name: str = Field(..., max_length=255)
    provinceId: int = Field(..., ge=1)
    description: Optional[str] = Field(None)


class EmployerUpdate(EmployerBase):
    name: str = Field(..., max_length=255)
    provinceId: int = Field(..., ge=1)
    description: Optional[str] = Field(None)


class EmployerOut(EmployerBase):
    id: int
    email: EmailStr
    name: str
    provinceId: int
    provinceName: str
    description: Optional[str]

    class ConfigDict:
        orm_mode = True
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "employer@example.com",
                "name": "Employer",
                "provinceId": 1,
                "provinceName": "Province",
                "description": "Employer description",
            }
        }
