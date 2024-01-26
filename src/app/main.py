from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import (
    employer_route,
    job_route,
    seeker_route,
    resume_route,
    analytic_route,
)
import os
from app.middleware.error_handling_middleware import exception_handling_middleware


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
app.middleware("http")(exception_handling_middleware)


# Include routers from the routes module
app.include_router(employer_route.router)
app.include_router(job_route.router)
app.include_router(seeker_route.router)
app.include_router(resume_route.router)
app.include_router(analytic_route.router)
