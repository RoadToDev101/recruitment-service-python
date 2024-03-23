import os
import socket
import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from apitally.fastapi import ApitallyMiddleware
from src.app.api.routes.employer_route import router as employer_route
from src.app.api.routes.job_route import router as job_route
from src.app.api.routes.seeker_route import router as seeker_route
from src.app.api.routes.resume_route import router as resume_route
from src.app.api.routes.analytic_route import router as analytic_route
from src.app.api.routes.user_route import router as user_route
from src.app.api.routes.auth_route import router as auth_route
from src.app.middleware.api_logging import api_logging_middleware
from src.app.middleware.exception import unified_exception_middleware
from src.app.config.logging.logging_config import logger

HOST_NAME = socket.gethostname()
PORT = os.getenv("PORT", 8000)

# Set up Sentry for error tracking
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    environment=os.getenv("ENV", "production"),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

# Create a FastAPI app
app = FastAPI(title="Recruitment Service", version="0.0.1")

# Prometheus Instrumentator
Instrumentator().instrument(app).expose(app)

# Set up Apitally middleware for tracking API usage and service health
app.add_middleware(
    ApitallyMiddleware,
    client_id=os.getenv("APITALLY_CLIENT_ID"),
    env=os.getenv("ENV", "production"),
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_DOMAIN"), "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up error handling middleware
app.middleware("http")(unified_exception_middleware)
app.middleware("http")(api_logging_middleware)


# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Recruitment Service!"}


# Include routers from the routes module
app.include_router(employer_route)
app.include_router(job_route)
app.include_router(seeker_route)
app.include_router(resume_route)
app.include_router(analytic_route)
app.include_router(user_route)
app.include_router(auth_route)

logger.info(f"FastApi server is running on {HOST_NAME}:{PORT}")
