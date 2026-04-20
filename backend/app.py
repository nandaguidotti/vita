"""
VITA Platform - Main Application

Description:
Entry point of the VITA (Visionary Industrial Technology Architecture) platform.
Responsible for initializing services, middleware, security, and documentation.
"""

from pathlib import Path
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from backend import config
from backend.common.logger import logger
from backend.common.security import login_handler
from backend.services._index_ import init_services

from backend.services.custom_documentation import customize_documentation

# ------------------------------------------------------------------------------
# App initialization
# ------------------------------------------------------------------------------

app = FastAPI(
    title="VITA: Visionary Industrial Technology Architecture"
)

# ------------------------------------------------------------------------------
# Service registration
# ------------------------------------------------------------------------------

init_services(app)
customize_documentation(app)

# ------------------------------------------------------------------------------
# Authentication
# ------------------------------------------------------------------------------

app.post("/auth/login", tags=["Auth"])(login_handler)


# ------------------------------------------------------------------------------
# Static documentation (Sphinx)
# ------------------------------------------------------------------------------

DOCS_DIR = Path(__file__).resolve().parent / "docs" / "build" / "html"

if not DOCS_DIR.exists():
    logger.log.warning(f"Sphinx HTML not found at: {DOCS_DIR}. Run: cd docs && make html")

app.mount(
    "/html/docs",
    StaticFiles(directory=str(DOCS_DIR), html=True),
    name="html_docs"
)

# ------------------------------------------------------------------------------
# CORS configuration
# ------------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------------------
# Health & test endpoints
# ------------------------------------------------------------------------------

@app.get("/ping", tags=["Test"])
def ping():
    return {"pong": True}


@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}


# ------------------------------------------------------------------------------
# Run application
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    logger.log.debug("--- Application starts ---")

    uvicorn.run(
        "app:app",
        host=config.api["SERVER_HOST"],
        port=config.api["SERVER_PORT"],
        reload=False
    )

    logger.log.debug("--- Application ends ---")