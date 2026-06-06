"""Health check endpoints."""

from fastapi import APIRouter

from app.config import settings
from app.models.schemas import HealthResponse, ReadinessResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
@router.get("/", response_model=HealthResponse, include_in_schema=False)
def health_check() -> HealthResponse:
    """Return the basic application health status."""
    return HealthResponse(
        status="healthy",
        service=settings.api_title,
        environment=settings.environment,
    )


@router.get("/ready", response_model=ReadinessResponse)
def readiness_check() -> ReadinessResponse:
    """Return whether the service is ready to accept requests."""
    return ReadinessResponse(
        ready=True,
        message="Service is ready to accept requests",
        environment=settings.environment,
    )
