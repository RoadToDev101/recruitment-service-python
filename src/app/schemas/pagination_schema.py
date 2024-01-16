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
    def total_pages(cls, totalElements: int, pageSize: int) -> int:
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
            total_pages=cls.total_pages(totalElements, pageSize),
        )
        return cls(data=data, pagination=pagination)
