"""Health check endpoints."""

from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["health"]
)


@router.get("/")
def health_check():
    """
    Health check endpoint.
    Returns the status of the API.
    """
    return {
        "status": "healthy"
    }


@router.get("/ready")
def readiness_check():
    """
    Readiness check endpoint.
    Returns True if the service is ready to handle requests.
    """
    return {
        "ready": True,
        "message": "Service is ready to accept requests"
    }
