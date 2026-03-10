from app.routers.member_routes import member_router
from app.routers.ieee_routes import ieee_router
from fastapi import FastAPI
def register_routers(app: FastAPI):
    """Import and register all API routers."""
    app.include_router(member_router, prefix="/members")
    app.include_router(ieee_router, prefix="/ieee")
    return app
