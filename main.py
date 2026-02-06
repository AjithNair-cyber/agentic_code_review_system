from fastapi import FastAPI
from app.api.router_handler import api_router

app = FastAPI(title="Code Validator")

app.include_router(api_router, prefix="/api/v1")
