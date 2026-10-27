"""Application factory and the static surface the canvas is served from."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles

from threadline.api import health
from threadline.config import Paths
from threadline.storage.database import open_database

CLIENT_BUILD_HINT = "Client bundle missing: run `npm run build` in client/"


def create_app(paths: Paths) -> FastAPI:
    """Build the application; tests pass their own paths so no real database is touched."""

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        paths.ensure_directories()
        app.state.database = await open_database(paths.database_file)
        try:
            yield
        finally:
            await app.state.database.close()

    app = FastAPI(title="Threadline", lifespan=lifespan)
    app.include_router(health.router)
    _serve_client(app, paths.client_dist_dir)
    return app


def _serve_client(app: FastAPI, client_dist_dir: Path) -> None:
    """Serve the built canvas, or say how to build it.

    A missing build is an ordinary state while developing, so it becomes a readable 503
    rather than a mount error that would stop the backend from starting at all.
    """
    if (client_dist_dir / "index.html").is_file():
        app.mount("/", StaticFiles(directory=client_dist_dir, html=True), name="client")
        return

    @app.get("/", response_class=PlainTextResponse, status_code=503)
    async def client_build_missing() -> str:
        return CLIENT_BUILD_HINT


app = create_app(Paths.from_environment())
