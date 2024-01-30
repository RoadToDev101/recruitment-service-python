from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import (
    employer_route,
    job_route,
    seeker_route,
    resume_route,
    analytic_route,
    user_route,
    auth_route,
)
import os
from app.middleware.exception_handling_middleware import (
    api_exception_handler,
    exception_handler,
)
from app.common.custom_exception import ApiException


# Create a FastAPI app
app = FastAPI(title="Recruitment Service", version="0.0.1")

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_DOMAIN"), "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Set up error handling middleware
app.exception_handler(ApiException)(api_exception_handler)
app.exception_handler(Exception)(exception_handler)


# Include routers from the routes module
app.include_router(employer_route.router)
app.include_router(job_route.router)
app.include_router(seeker_route.router)
app.include_router(resume_route.router)
app.include_router(analytic_route.router)
app.include_router(user_route.router)
app.include_router(auth_route.router)
