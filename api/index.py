"""
Vercel serverless entrypoint.

Exposes the FastAPI app instance for Vercel's Python runtime.
"""

from app.main import app

