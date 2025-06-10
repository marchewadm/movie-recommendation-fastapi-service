from .schemas import CheckHealthResponse


class HealthController:
    """Controller for health check endpoints."""

    @staticmethod
    async def check_health() -> CheckHealthResponse:
        """Verify if the service is running.

        :returns: A response model indicating the service status.
        :rtype: CheckHealthResponse
        """

        return CheckHealthResponse()
