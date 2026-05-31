"""
Pydantic schemas for request/response validation.
Add your data models here.
"""

from pydantic import BaseModel
from typing import Optional


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    service: str


class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str
    code: Optional[str] = None
