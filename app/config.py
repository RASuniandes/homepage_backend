"""
Application configuration using Pydantic BaseSettings.

Loads from environment variables / .env file.
Supports: development, testing, production profiles.
"""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Base application settings — all values can be overridden via env vars."""

    # ── App ────────────────────────────────────────────
    APP_NAME: str = "Homepage Backend API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("ENV", "development") != "production"
    ENV: str = Field(default="development", alias="APP_ENV")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "your-secure-password")
    # ── Server ─────────────────────────────────────────
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ── Database ───────────────────────────────────────
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///data/app.db",
    )

    # ── JWT / Auth ─────────────────────────────────────
    SECRET_KEY: str = "change-me-in-production"
    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 360  # 6 h

    # ── CORS ───────────────────────────────────────────
    CORS_ORIGINS: list[str] = [
        "https://rasuniandes.org",
        "http://rasuniandes.org",
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    # ── Redis ──────────────────────────────────────────
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # ── Logging ────────────────────────────────────────
    LOG_LEVEL: str = "INFO"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


@lru_cache()
def get_settings() -> Settings:
    """Cached singleton — call this wherever you need settings."""
    return Settings()
