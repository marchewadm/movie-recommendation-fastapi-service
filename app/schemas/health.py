from pydantic import BaseModel


class CheckHealthResponse(BaseModel):
    """Response model for health check endpoint."""

    message: str = "Application is running. HTTP request received."
