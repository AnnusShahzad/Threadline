"""Health has to prove something, so it queries the database it reports on."""

from __future__ import annotations

from fastapi.testclient import TestClient

from threadline.config import Paths
from threadline.main import create_app


def test_health_reports_database_ok(paths: Paths) -> None:
    with TestClient(create_app(paths)) as client:
        response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}
