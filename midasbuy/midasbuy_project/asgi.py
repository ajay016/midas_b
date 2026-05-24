"""
ASGI entry-point that mounts both Django and FastAPI under one server.

    Django  →  handles everything at  /
    FastAPI →  handles everything at  /api/

Run:
    uvicorn midasbuy_project.asgi:application --reload --port 8000
"""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "midasbuy_project.settings")

# Django must be set up before any Django imports
from django.core.asgi import get_asgi_application
django_app = get_asgi_application()

# FastAPI (imported after Django setup to avoid app-registry issues)
from api.app import api_app  # noqa: E402
from starlette.routing import Mount
from starlette.applications import Starlette

application = Starlette(
    routes=[
        Mount("/api", app=api_app),
        Mount("/",    app=django_app),
    ]
)
