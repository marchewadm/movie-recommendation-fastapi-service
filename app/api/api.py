from fastapi import APIRouter

from .health.router import router as health_router
from .v1.api_v1 import router as v1_router


router = APIRouter(prefix="/api", tags=["API"])

router.include_router(health_router)
router.include_router(v1_router)
