"""
Database engine, session factory, and declarative Base.

- Uses SQLAlchemy 2.0 style.
- Creates a local SQLite file (data/app.db) by default; switch to
  MySQL/PostgreSQL via the DATABASE_URL env var.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config import get_settings

settings = get_settings()

# ── Ensure data/ directory exists for SQLite ────────────────────────
if settings.DATABASE_URL.startswith("sqlite"):
    os.makedirs("data", exist_ok=True)

# ── Engine ──────────────────────────────────────────────────────────
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    connect_args=connect_args,
    pool_pre_ping=True,
)

# ── Session ─────────────────────────────────────────────────────────
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ── Declarative Base ────────────────────────────────────────────────
class Base(DeclarativeBase):
    """All models inherit from this class."""
    pass


def init_db() -> None:
    """
    Create all tables that don't exist yet.

    Call this on startup so the SQLite file is ready
    without needing Alembic for the initial schema.
    """
    import app.models  # noqa: F401  — ensure every model is imported
    Base.metadata.create_all(bind=engine)
