from fastapi import APIRouter
from app.api.routes.github_routes import router as github_routes

api_router = APIRouter()

api_router.include_router(github_routes, prefix="/github", tags=["GitHub"])