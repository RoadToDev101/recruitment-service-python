from fastapi import Request, status
from fastapi.responses import JSONResponse
import traceback
from app.common.custom_exception import ApiException
from app.common.api_response import ApiResponse
from app.common.error_code import ErrorCode
import json
from app.config.logging.logging_config import db_logger

# from sentry_sdk import capture_exception


async def api_exception_handler(request: Request, exc: ApiException):
    if exc.response is None:
        db_logger.error(f"ApiException: {exc.message}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=json.loads(
                ApiResponse.error(
                    errorCode=ErrorCode.INTERNAL_ERR,
                    statusCode=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    message="Internal Server Error",
                ).model_dump_json()
            ),
        )
    else:
        if 400 <= exc.response.statusCode < 500:
            db_logger.debug(f"ApiException: {exc.response.message}", exc_info=True)
        elif 500 <= exc.response.statusCode < 600:
            db_logger.error(f"ApiException: {exc.response.message}", exc_info=True)
        return JSONResponse(
            status_code=exc.response.statusCode,
            content=json.loads(exc.response.model_dump_json()),
        )


async def exception_handler(request: Request, e: Exception):
    trace = traceback.format_exc()
    db_logger.error(f"Exception: {e}\nTrace: {trace}")

    return JSONResponse(
        content=json.loads(
            ApiResponse.error(
                errorCode=ErrorCode.INTERNAL_ERR,
                statusCode=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Internal Server Error",
            ).model_dump_json()
        ),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
