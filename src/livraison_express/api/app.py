"""Assemblage de l'application FastAPI.

`create_app()` est, avec `bootstrap.py`, la racine de composition : le conteneur d'objets
est posé sur `app.state`, les routeurs le lisent via `dependencies.py`.

Le modèle est chargé une seule fois, au démarrage (lifespan), jamais dans un handler. Son
absence n'empêche pas l'API de démarrer : `/health/ready` répond 503.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from ..bootstrap import Container, get_container
from .errors import register_exception_handlers
from .metadata import API_DESCRIPTION, API_VERSION, SERVICE_NAME
from .routers import health, orders, predictions


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Load the model once at startup (unless the container already has one)."""
    container: Container = app.state.container
    if not container.model_ready:
        container.load_model()
    yield


def create_app(container: Container | None = None) -> FastAPI:
    """Build the FastAPI application.

    Tests pass their own `container` (fake model, in-memory store); in production the
    container is built from the environment.
    """
    app = FastAPI(
        title=SERVICE_NAME, version=API_VERSION, description=API_DESCRIPTION, lifespan=lifespan
    )
    app.state.container = container or get_container()
    register_exception_handlers(app)
    app.include_router(health.router)
    app.include_router(orders.router)
    app.include_router(predictions.router)
    return app
