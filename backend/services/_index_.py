"""
Service Initializer

Description:
Registers all service routes into the main FastAPI application.
"""

from fastapi import FastAPI

from backend.services import root_services
from backend.services.vision.routes import router as vision_router
from backend.common.security import secure_write


def init_services(app: FastAPI):
    """
    Register all service routes.
    """
    app.include_router(root_services.root_api)
    app.include_router(vision_router, prefix="/api", dependencies=[secure_write]
    # Add other services
    )