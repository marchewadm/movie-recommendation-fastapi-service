from fastapi import APIRouter, status

from app.schemas.health import CheckHealthResponse
from app.dependencies.health import HealthControllerDependency


router = APIRouter(prefix="/api", tags=["API"])


@router.get(
    "/health", response_model=CheckHealthResponse, status_code=status.HTTP_200_OK
)
async def get_health(health_controller: HealthControllerDependency):
    """Health check endpoint to verify if the service is running."""

    response = await health_controller.check_health()

    return response
