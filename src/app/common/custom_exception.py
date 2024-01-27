from .api_response import ApiResponse
from .error_code import ErrorCode


class ApiException(Exception):
    response: ApiResponse

    def __init__(self, status_code: int, detail: str, errorCode: ErrorCode):
        self.response = ApiResponse.error(
            errorCode=errorCode,
            statusCode=status_code,
            message=detail,
        )


class CredentialsException(ApiException):
    def __init__(self, detail: str = "Access denied. Invalid credentials"):
        super().__init__(
            status_code=ErrorCode.UNAUTHORIZED.value,
            detail=detail,
            errorCode=ErrorCode.UNAUTHORIZED,
        )


class ForbiddenException(ApiException):
    def __init__(self, detail: str = "Not enough permissions."):
        super().__init__(
            status_code=ErrorCode.FORBIDDEN.value,
            detail=detail,
            errorCode=ErrorCode.FORBIDDEN,
        )


class NotFoundException(ApiException):
    def __init__(self, detail: str = "Not found."):
        super().__init__(
            status_code=ErrorCode.NOT_FOUND.value,
            detail=detail,
            errorCode=ErrorCode.NOT_FOUND,
        )


class BadRequestException(ApiException):
    def __init__(self, detail: str = "Bad request. Try again."):
        super().__init__(
            status_code=ErrorCode.BAD_REQUEST.value,
            detail=detail,
            errorCode=ErrorCode.BAD_REQUEST,
        )


class UnprocessableEntityException(ApiException):
    def __init__(self, detail: str = "Unprocessable entity"):
        super().__init__(
            status_code=ErrorCode.UNPROCESSABLE_ENTITY.value,
            detail=detail,
            errorCode=ErrorCode.UNPROCESSABLE_ENTITY,
        )


class ValidationException(ApiException):
    def __init__(self, detail: str = "Validation error"):
        super().__init__(
            status_code=ErrorCode.UNPROCESSABLE_ENTITY.value,
            detail=detail,
            errorCode=ErrorCode.UNPROCESSABLE_ENTITY,
        )
