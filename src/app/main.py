import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from apitally.fastapi import ApitallyMiddleware
from src.app.api.routes import (
    employer_route,
    job_route,
    seeker_route,
    resume_route,
    analytic_route,
    user_route,
    auth_route,
)
from src.app.middleware.api_logging import api_logging_middleware
from src.app.middleware.exception import unified_exception_middleware
from src.app.config.logging.logging_config import logger

PORT = os.getenv("PORT", 8000)

# Create a FastAPI app
app = FastAPI(title="Recruitment Service", version="0.0.1")
Instrumentator().instrument(app).expose(app)
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
app.include_router(employer_route.router)
app.include_router(job_route.router)
app.include_router(seeker_route.router)
app.include_router(resume_route.router)
app.include_router(analytic_route.router)
app.include_router(user_route.router)
app.include_router(auth_route.router)

logger.info(f"FastApi server is running on http://127.0.0.1:{PORT}")
