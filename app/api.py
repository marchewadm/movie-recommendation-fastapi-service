from fastapi import APIRouter

from .health.router import router as health_router


router = APIRouter(prefix="/api", tags=["API"])

router.include_router(health_router)
