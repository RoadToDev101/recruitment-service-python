from pydantic import BaseModel, Field
from typing import Optional
from app.api.models.user_model import UserRole


class TokenResponse(BaseModel):
    access_token: Optional[str] = Field(None, description="Access token for the user")
    token_type: Optional[str] = Field(None, description="Type of the access token")
    user_id: Optional[int] = Field(
        None, description="User ID of the authenticated user"
    )
    role: Optional[UserRole] = Field(None, description="Role of the authenticated user")

    @classmethod
    def token_response(
        cls,
        message: str = "Authentication successful",
        access_token: str = None,
        token_type: str = None,
        user_id: int = None,
        role: UserRole = None,
    ):
        return cls(
            success=True,
            message=message,
            access_token=access_token,
            token_type=token_type,
            user_id=user_id,
            role=role,
        )

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Authentication successful",
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
                "token_type": "bearer",
                "user_id": 1,
                "role": "USER",
            }
        }
