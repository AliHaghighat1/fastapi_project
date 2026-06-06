"""Application configuration loaded from environment variables."""

import json
from functools import lru_cache
from typing import Any

from pydantic import Field
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
    cors_origins: str = Field(default="*", alias="CORS_ORIGINS")
    cohere_api_token: str | None = Field(default=None, alias="COHERE_API_TOKEN")

    @property
    def cors_origins_list(self) -> list[str]:
        """Return CORS origins from JSON list, comma-separated string, or wildcard."""
        value: Any = self.cors_origins
        if value is None or value == "":
            return ["*"]

        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]

        value = str(value).strip()
        if (value.startswith("'") and value.endswith("'")) or (
            value.startswith('"') and value.endswith('"')
        ):
            value = value[1:-1].strip()

        if value.startswith("["):
            parsed = json.loads(value)
            if not isinstance(parsed, list):
                raise ValueError("CORS_ORIGINS JSON value must be a list")
            return [str(item).strip() for item in parsed if str(item).strip()]

        return [item.strip() for item in value.split(",") if item.strip()] or ["*"]


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()


settings = get_settings()
