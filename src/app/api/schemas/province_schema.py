from pydantic import BaseModel


class ProvinceBase(BaseModel):
    id: int
    name: str
