"""Application configuration loaded from environment variables."""

import json
from functools import lru_cache
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for local, test and production environments."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # API settings
    api_title: str = Field(default="FastAPI Backend", alias="API_TITLE")
    api_description: str = Field(
        default="FastAPI backend application",
        alias="API_DESCRIPTION",
    )
    api_version: str = Field(default="1.0.0", alias="API_VERSION")

    # Runtime settings
    environment: str = Field(default="development", alias="APP_ENV")
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")
    debug: bool = Field(default=False, alias="DEBUG")

    # Security / integration settings
    cors_origins: list[str] = Field(default=["*"], alias="CORS_ORIGINS")
    cohere_api_token: str | None = Field(default=None, alias="COHERE_API_TOKEN")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: Any) -> list[str]:
        """Accept CORS origins as JSON list or comma-separated string."""
        if value is None or value == "":
            return ["*"]
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            value = value.strip()
            if value.startswith("["):
                parsed = json.loads(value)
                if not isinstance(parsed, list):
                    raise ValueError("CORS_ORIGINS JSON value must be a list")
                return [str(item).strip() for item in parsed if str(item).strip()]
            return [item.strip() for item in value.split(",") if item.strip()]
        raise ValueError("CORS_ORIGINS must be a list, JSON list, or comma-separated string")


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()


settings = get_settings()
