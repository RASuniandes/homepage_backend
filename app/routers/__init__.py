from app.routers.member_routes import member_router
from fastapi import FastAPI
def register_routers(app: FastAPI):
    """Import and register all API routers."""
    app.include_router(member_router, prefix="/members")
    return app
  
  