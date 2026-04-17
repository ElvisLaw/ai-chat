"""FastAPI application entry point.

This file enables:
- fastapi dev (auto-discovers main.py)
- fastapi run

Usage:
    fastapi dev
    fastapi run
"""

from app.api import app

__all__ = ["app"]
