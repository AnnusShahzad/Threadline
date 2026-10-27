"""Paths follow the environment so a test run or a second install cannot share state."""

from __future__ import annotations

from pathlib import Path

import pytest

from threadline.config import Paths

ENVIRONMENT_VARIABLES = (
    "THREADLINE_DATA_DIR",
    "THREADLINE_TRANSFORMS_DIR",
    "THREADLINE_CLIENT_DIST",
)


def test_environment_variables_override_defaults(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("THREADLINE_DATA_DIR", str(tmp_path / "state"))
    monkeypatch.setenv("THREADLINE_TRANSFORMS_DIR", str(tmp_path / "plugins"))
    monkeypatch.setenv("THREADLINE_CLIENT_DIST", str(tmp_path / "web"))

    paths = Paths.from_environment()

    assert paths.data_dir == tmp_path / "state"
    assert paths.transforms_dir == tmp_path / "plugins"
    assert paths.client_dist_dir == tmp_path / "web"


def test_defaults_are_relative_to_the_working_directory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for variable in ENVIRONMENT_VARIABLES:
        monkeypatch.delenv(variable, raising=False)

    paths = Paths.from_environment()

    assert paths.data_dir == Path("data")
    assert paths.database_file == Path("data/threadline.db")


def test_ensure_directories_creates_data_and_transforms_only(paths: Paths) -> None:
    paths.ensure_directories()

    assert paths.data_dir.is_dir()
    assert paths.transforms_dir.is_dir()
    # A missing client build is reported by the server, never invented here.
    assert not paths.client_dist_dir.exists()
