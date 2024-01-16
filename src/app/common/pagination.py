from math import ceil
from typing import Type, TypeVar, Generic, List
from pydantic import BaseModel

DataT = TypeVar("DataT")


class PaginationMeta(BaseModel):
    page: int
    pageSize: int
    totalElements: int
    totalPages: int


class Pagination(BaseModel, Generic[DataT]):
    data: List[DataT]
    pagination: PaginationMeta

    @classmethod
    def totalPages(cls, totalElements: int, pageSize: int) -> int:
        # Calculate total pages and use ceil to round up
        return ceil(totalElements / pageSize)

    @classmethod
    def create(
        cls: Type["Pagination[DataT]"],
        data: List[DataT],
        page: int,
        pageSize: int,
        totalElements: int,
    ) -> "Pagination[DataT]":
        pagination = PaginationMeta(
            page=page,
            pageSize=pageSize,
            totalElements=totalElements,
            totalPages=cls.totalPages(totalElements, pageSize),
        )
        return cls(data=data, pagination=pagination)

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "data": [
                    {
                        "id": 1,
                        "email": "example@example.com",
                    }
                ],
                "pagination": {
                    "page": 1,
                    "pageSize": 10,
                    "totalElements": 1,
                    "totalPages": 1,
                },
            }
        }
