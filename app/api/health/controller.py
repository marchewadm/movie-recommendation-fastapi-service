from .schemas import CheckHealthResponse


class HealthController:
    """Controller for health check endpoints."""

    @staticmethod
    async def check_health() -> CheckHealthResponse:
        """Verify if the app is running.

        Returns:
            CheckHealthResponse:
                A response model indicating the app status.
        """

        return CheckHealthResponse()
