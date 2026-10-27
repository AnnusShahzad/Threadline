"""The migration stepper is the only thing allowed to shape a database."""

from __future__ import annotations

from pathlib import Path

import aiosqlite
import pytest

from threadline.config import Paths
from threadline.storage.database import MIGRATIONS_DIR, open_database
from threadline.storage.migrations import MigrationError, apply_migrations


async def _pragma_value(connection: aiosqlite.Connection, pragma: str) -> object:
    cursor = await connection.execute(pragma)
    try:
        row = await cursor.fetchone()
    finally:
        await cursor.close()
    assert row is not None, f"{pragma} returned no row"
    return row[0]


async def _table_names(connection: aiosqlite.Connection) -> set[str]:
    cursor = await connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    try:
        rows = await cursor.fetchall()
    finally:
        await cursor.close()
    return {str(row[0]) for row in rows}


async def test_migrations_create_schema(paths: Paths) -> None:
    paths.ensure_directories()

    connection = await open_database(paths.database_file)
    try:
        assert await _pragma_value(connection, "PRAGMA user_version") == 1
        assert {"investigations", "entities", "edges"} <= await _table_names(connection)
        assert await _pragma_value(connection, "PRAGMA journal_mode") == "wal"
        assert await _pragma_value(connection, "PRAGMA foreign_keys") == 1
    finally:
        await connection.close()


async def test_reapplying_migrations_leaves_the_version_alone(paths: Paths) -> None:
    paths.ensure_directories()
    connection = await open_database(paths.database_file)
    try:
        assert await apply_migrations(connection, MIGRATIONS_DIR) == 1
        assert await _pragma_value(connection, "PRAGMA user_version") == 1
    finally:
        await connection.close()


async def test_misnamed_migration_is_rejected(tmp_path: Path) -> None:
    migrations_dir = tmp_path / "migrations"
    migrations_dir.mkdir()
    (migrations_dir / "initial.sql").write_text("SELECT 1;", encoding="utf-8")

    connection = await aiosqlite.connect(tmp_path / "threadline.db")
    try:
        with pytest.raises(MigrationError, match="NNNN_description"):
            await apply_migrations(connection, migrations_dir)
    finally:
        await connection.close()


async def test_missing_migration_directory_is_reported(tmp_path: Path) -> None:
    connection = await aiosqlite.connect(tmp_path / "threadline.db")
    try:
        with pytest.raises(MigrationError, match="does not exist"):
            await apply_migrations(connection, tmp_path / "absent")
    finally:
        await connection.close()
