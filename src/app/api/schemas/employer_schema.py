from pydantic import BaseModel, EmailStr, Field
from typing import Optional


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
