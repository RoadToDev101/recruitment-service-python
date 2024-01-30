from pydantic import BaseModel
from app.api.models.user_model import UserRole


class Token(BaseModel):
    access_token: str
    token_type: str


class Payload(Token):
    user_id: int
    role: UserRole
