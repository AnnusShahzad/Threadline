"""Shared fixtures for the Threadline test suite."""

from __future__ import annotations

from pathlib import Path

import pytest

from threadline.config import Paths


@pytest.fixture
def paths(tmp_path: Path) -> Paths:
    return Paths(
        data_dir=tmp_path / "data",
        transforms_dir=tmp_path / "transforms",
        client_dist_dir=tmp_path / "client-dist",
    )
