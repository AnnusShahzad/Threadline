"""The backend must stay usable before the client has ever been built."""

from __future__ import annotations

from fastapi.testclient import TestClient

from threadline.config import Paths
from threadline.main import create_app


def test_root_explains_how_to_build_the_client(paths: Paths) -> None:
    with TestClient(create_app(paths)) as client:
        response = client.get("/")

    assert response.status_code == 503
    assert "npm run build" in response.text


def test_root_serves_the_built_client(paths: Paths) -> None:
    paths.client_dist_dir.mkdir(parents=True)
    (paths.client_dist_dir / "index.html").write_text(
        "<!doctype html><title>Threadline</title>", encoding="utf-8"
    )

    with TestClient(create_app(paths)) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert "Threadline" in response.text
