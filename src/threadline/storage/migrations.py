"""Apply numbered SQL migrations, tracked in SQLite's own ``user_version``."""

from __future__ import annotations

import re
from pathlib import Path

import aiosqlite

MIGRATION_FILE_PATTERN = re.compile(r"^(\d+)_[a-z0-9_]+\.sql$")


class MigrationError(RuntimeError):
    """A migration folder or file could not be applied."""


async def apply_migrations(connection: aiosqlite.Connection, migrations_dir: Path) -> int:
    """Apply every migration newer than the database reports, returning the new version."""
    if not migrations_dir.is_dir():
        raise MigrationError(f"migration directory {migrations_dir} does not exist")

    current_version = await _schema_version(connection)
    for version, migration_file in _numbered_migrations(migrations_dir):
        if version <= current_version:
            continue
        await _apply_one(connection, version, migration_file)
        current_version = version
    return current_version


async def _schema_version(connection: aiosqlite.Connection) -> int:
    cursor = await connection.execute("PRAGMA user_version")
    try:
        row = await cursor.fetchone()
    finally:
        await cursor.close()
    if row is None:
        raise MigrationError("SQLite did not report a user_version")
    return int(row[0])


async def _apply_one(connection: aiosqlite.Connection, version: int, migration_file: Path) -> None:
    try:
        await connection.executescript(migration_file.read_text(encoding="utf-8"))
        # PRAGMA values cannot be bound as parameters; ``version`` is an int parsed from the
        # filename, so interpolating it cannot carry foreign SQL.
        await connection.execute(f"PRAGMA user_version = {version}")
        await connection.commit()
    except aiosqlite.Error as error:
        raise MigrationError(f"migration {migration_file.name} failed: {error}") from error


def _numbered_migrations(migrations_dir: Path) -> list[tuple[int, Path]]:
    migrations: list[tuple[int, Path]] = []
    for migration_file in migrations_dir.glob("*.sql"):
        match = MIGRATION_FILE_PATTERN.match(migration_file.name)
        if match is None:
            raise MigrationError(
                f"migration {migration_file.name} is not named NNNN_description.sql"
            )
        migrations.append((int(match.group(1)), migration_file))
    return sorted(migrations)
