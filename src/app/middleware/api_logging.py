import os
from dotenv import load_dotenv
import json
from time import time
from fastapi import Request
from fastapi.responses import JSONResponse
from pymongo.errors import PyMongoError
from src.app.config.database.mongodb import mongo_db
from src.app.config.logging.logging_config import logger

load_dotenv()

MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")


async def api_logging_middleware(request: Request, call_next):
    # Only log requests to the specified API routes
    log_routes = ["/api/v1"]
    if not request.url.path.startswith(tuple(log_routes)):
        return await call_next(request)

    start = time()

    # Create log_dict
    log_dict = {
        "timestamp": f"{start:.3f}",
        "method": request.method,
        "path": request.url.path,
        "query_params": dict(request.query_params),
    }

    # Attempt to log request body
    if request.method in ["POST", "PUT", "PATCH"]:
        try:
            log_dict["request_body"] = await request.json()
        except json.JSONDecodeError as e:
            log_dict["request_body"] = f"Unable to decode JSON: {e}"

    # Process request and measure time
    response = await call_next(request)
    log_dict["process_time"] = f"{time() - start:.3f}"
    log_dict["status_code"] = (
        response.status_code
    )  # Capture status code of the response

    # Attempt to log response body if needed (for certain status codes)
    if response.status_code in [200, 201]:
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        response_body_str = response_body.decode()
        response_data = json.loads(response_body_str)
        # logger.debug(f"Response body: {response_body.decode()}")

        # Create a new response with the same data
        response = JSONResponse(content=response_data, status_code=response.status_code)

        # Log response body
        try:
            log_dict["response_body"] = response_data
        except Exception as e:
            log_dict["response_body"] = f"Unable to decode response body: {e}"

    # Determine log level based on status code
    try:
        if 400 <= log_dict["status_code"] < 500:
            logger.warning(f"Client error occurred", extra=log_dict)
            mongo_db.client[MONGODB_DATABASE]["client_error_logs"].insert_one(log_dict)
        elif 500 <= log_dict["status_code"]:
            logger.error(f"Server error occurred", extra=log_dict)
            mongo_db.client[MONGODB_DATABASE]["server_error_logs"].insert_one(log_dict)
        else:
            logger.info(
                f"{log_dict['method']} {log_dict['path']} {log_dict['status_code']}",
                extra=log_dict,
            )
            mongo_db.client[MONGODB_DATABASE]["info_logs"].insert_one(log_dict)
    except PyMongoError as e:
        logger.error(f"Error inserting log into MongoDB: {e}")

    return response
