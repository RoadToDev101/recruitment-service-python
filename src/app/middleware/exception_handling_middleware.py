from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import traceback
import os
from app.common.custom_exception import ApiException
from app.common.api_response import ApiResponse  # Import ApiResponse
from app.common.error_code import ErrorCode  # Import ErrorCode
import json

# from sentry_sdk import capture_exception


async def exception_handling_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except ApiException as api_exc:
        return JSONResponse(
            status_code=api_exc.response.statusCode,
            content=json.loads(api_exc.response.model_dump_json()),
        )
    except HTTPException as http_exc:
        # Capture specific HTTP exceptions
        # capture_exception(http_exc)  # Sentry logging
        return JSONResponse(
            status_code=http_exc.status_code,
            content=json.loads(
                ApiResponse.error(
                    errorCode=ErrorCode(
                        http_exc.status_code
                    ),  # Map status code to ErrorCode
                    statusCode=http_exc.status_code,
                    message=http_exc.detail,
                ).model_dump_json()
            ),
        )
    except Exception as e:
        # Capture all other exceptions
        # capture_exception(e)  # Sentry logging
        if os.getenv("ENV") == "development":
            trace = traceback.format_exc()
            return JSONResponse(
                content=ApiResponse.error(
                    errorCode=ErrorCode.INTERNAL_ERR,
                    statusCode=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    message="Internal Server Error"
                    if os.getenv("ENV") != "development"
                    else f"Internal Server Error: {trace}",
                ).model_dump(),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        else:
            return JSONResponse(
                content=ApiResponse.error(
                    errorCode=ErrorCode.INTERNAL_ERR,
                    statusCode=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    message="Internal Server Error",
                ).model_dump(),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
