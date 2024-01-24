from pydantic import BaseModel


class FieldBase(BaseModel):
    id: int
    name: str
