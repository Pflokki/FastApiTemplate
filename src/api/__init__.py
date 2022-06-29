from fastapi import APIRouter

from api.healthcheck.healthcheck import api_router as healthcheck_api_router

api_router = APIRouter()

api_router.include_router(healthcheck_api_router, tags=['healthcheck'])
