from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

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


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Include routers from the routes module
# app.include_router(user_route.router)
