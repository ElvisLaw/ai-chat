"""API server entry point.

Usage:
    fastapi dev -m app.api
    uvicorn app.api:app
"""

from app.api.server import app

__all__ = ["app"]
