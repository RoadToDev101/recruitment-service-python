from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional
from fastapi import status

DataT = TypeVar("DataT")


class ApiResponse(BaseModel, Generic[DataT]):
    errorCode: Optional[int] = Field(0, description="Error code, 0 means no error")
    statusCode: Optional[int] = Field(
        status.HTTP_200_OK, description="HTTP status code"
    )
    message: Optional[str] = Field(None, description="Response message")
    object: Optional[DataT] = Field(None, description="Response data")

    @classmethod
    def success_with_message(cls, message: str, object: DataT = None):
        return cls(
            errorCode=0,
            statusCode=status.HTTP_200_OK,
            message=message,
            object=object,
        )

    @classmethod
    def success_without_message(cls, object: DataT = None):
        return cls(
            errorCode=0,
            statusCode=status.HTTP_200_OK,
            message=None,
            object=object,
        )

    @classmethod
    def error(cls, errorCode: int, statusCode: int, message: str):
        return cls(
            errorCode=errorCode,
            statusCode=statusCode,
            message=message,
        )
