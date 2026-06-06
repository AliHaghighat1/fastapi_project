"""Pydantic schemas for request/response validation."""

from typing import Optional

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    service: str
    environment: str


class ReadinessResponse(BaseModel):
    """Readiness check response model."""

    ready: bool
    message: str
    environment: str


class ErrorResponse(BaseModel):
    """Error response model."""

    detail: str
    code: Optional[str] = None
