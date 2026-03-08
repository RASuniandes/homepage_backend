"""
Shared FastAPI dependencies.

Inject these into route handlers via `Depends(...)`.
"""

from collections.abc import Generator
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.config import Settings, get_settings


def get_db() -> Generator[Session, None, None]:
    """Yield a DB session and guarantee it's closed after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_settings() -> Settings:
    """Return the cached application settings."""
    return get_settings()
