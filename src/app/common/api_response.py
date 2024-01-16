from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional
from fastapi import status
from .error_code import ErrorCode

DataT = TypeVar("DataT")


class ApiResponse(BaseModel, Generic[DataT]):
    errorCode: Optional[ErrorCode] = Field(
        ErrorCode.SUCCESS, description="Error code, 0 means no error"
    )
    statusCode: Optional[int] = Field(
        status.HTTP_200_OK, description="HTTP status code"
    )
    message: Optional[str] = Field(None, description="Response message")
    object: Optional[DataT] = Field(None, description="Response data")

    @classmethod
    def success_message_only(cls, message: str):
        return cls(
            errorCode=ErrorCode.SUCCESS,
            statusCode=status.HTTP_200_OK,
            message=message,
            object={},
        )

    @classmethod
    def success_with_object(cls, object: DataT):
        return cls(
            errorCode=ErrorCode.SUCCESS,
            statusCode=status.HTTP_200_OK,
            object=object,
        )

    @classmethod
    def error(cls, errorCode: ErrorCode, statusCode: int, message: str):
        return cls(
            errorCode=errorCode,
            statusCode=statusCode,
            message=message,
        )
