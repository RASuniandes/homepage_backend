"""
FastAPI application factory.

Equivalent to Flask's `create_app()`.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import get_settings
from app.database import init_db
from app.routers import register_routers
import logging
from fastapi import Request
import time


# ── Lifespan (startup / shutdown) ────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Runs once on startup and once on shutdown."""
    settings = get_settings()
    print("=" * 60)
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"   ENV : {settings.ENV}")
    print(f"   PORT: {settings.PORT}")
    print(f"   DB  : {settings.DATABASE_URL}")
    print("=" * 60)

    # Create tables (safe for SQLite first-run)
    init_db()
    print("✓ Database initialised")

    yield  # ← app is running

    print("⏹  Shutting down …")


# ── Factory ──────────────────────────────────────────────────────────
def create_app() -> FastAPI:
    """Build and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # ── CORS ─────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # ── Logging Middleware ───────────────────────────────────
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
    
    logger = logging.getLogger(__name__)

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(
            f"{request.method} {request.url.path} - {response.status_code} ({process_time:.3f}s)"
        )
        return response
    # ── Routers ──────────────────────────────────────
    app.get("/")(lambda: {"message": "Welcome to the Homepage Backend API!"})
    app.get("/health")(lambda: {"status": "ok"})
    # Image uploads 

    register_routers(app)
    print(app.routes)
    return app
