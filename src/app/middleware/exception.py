import json
from fastapi import Request, status
from fastapi.responses import JSONResponse
from src.app.common.api_response import ApiResponse
from src.app.common.custom_exception import ApiException
from src.app.common.error_code import ErrorCode
from src.app.config.logging.logging_config import logger


async def unified_exception_middleware(request: Request, call_next):
    # Create log context and default error response
    log_context = {
        "method": request.method,
        "path": request.url.path,
        "query_params": dict(request.query_params),
    }
    default_error_response = JSONResponse(
        content=json.loads(
            ApiResponse.error(
                errorCode=ErrorCode.INTERNAL_ERR,
                statusCode=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Internal Server Error",
            ).model_dump_json()
        ),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

    try:
        # Proceed with the next middleware or route handler
        response = await call_next(request)
    except ApiException as exc:
        # Handle custom ApiException
        logger.error(f"ApiException ({type(exc).__name__})", extra=log_context)
        if exc.response:
            content = json.loads(exc.response.model_dump_json())
            status_code = exc.response.statusCode
            response = JSONResponse(content=content, status_code=status_code)
        else:
            response = default_error_response
    except Exception:
        # Handle generic exceptions
        logger.exception(
            f"Unhandled exception occurred during request processing", extra=log_context
        )
        response = default_error_response

    return response
