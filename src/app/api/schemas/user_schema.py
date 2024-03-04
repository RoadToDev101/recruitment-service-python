# from pydantic import EmailStr
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.api.models.user_model import UserRole


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    # email: EmailStr = Field(..., max_length=254)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(UserBase):
    username: Optional[str] = Field(min_length=3, max_length=50)
    # email: Optional[EmailStr] = Field(max_length=254)
    role: Optional[UserRole]


class UserOut(BaseModel):
    id: int
    role: UserRole
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        orm_mode = True
        from_attributes = True
