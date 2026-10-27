"""Filesystem locations Threadline reads and writes while it runs."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

DATA_DIR_VARIABLE = "THREADLINE_DATA_DIR"
TRANSFORMS_DIR_VARIABLE = "THREADLINE_TRANSFORMS_DIR"
CLIENT_DIST_VARIABLE = "THREADLINE_CLIENT_DIST"

DATABASE_FILE_NAME = "threadline.db"


@dataclass(frozen=True)
class Paths:
    """Every directory the application touches, resolved once at startup.

    Defaults are relative to the working directory because Threadline is started from the
    repository root; a packaged build would need a per-platform data directory instead.
    """

    data_dir: Path
    transforms_dir: Path
    client_dist_dir: Path

    @classmethod
    def from_environment(cls) -> Paths:
        return cls(
            data_dir=Path(os.environ.get(DATA_DIR_VARIABLE, "data")),
            transforms_dir=Path(os.environ.get(TRANSFORMS_DIR_VARIABLE, "transforms")),
            client_dist_dir=Path(os.environ.get(CLIENT_DIST_VARIABLE, "client/dist")),
        )

    @property
    def database_file(self) -> Path:
        return self.data_dir / DATABASE_FILE_NAME

    def ensure_directories(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.transforms_dir.mkdir(parents=True, exist_ok=True)
