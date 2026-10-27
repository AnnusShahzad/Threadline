"""Liveness endpoint that proves the database is reachable."""

from __future__ import annotations

import logging

import aiosqlite
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/api/health")
async def health(request: Request) -> JSONResponse:
    database: aiosqlite.Connection = request.app.state.database
    try:
        cursor = await database.execute("SELECT 1")
        await cursor.close()
    except aiosqlite.Error:
        # The response stays free of local paths; the log carries the detail.
        logger.exception("health check could not query SQLite")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "degraded", "database": "unavailable"},
        )
    return JSONResponse(content={"status": "ok", "database": "ok"})
