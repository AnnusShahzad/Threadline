"""Open the SQLite database with the pragmas and schema Threadline depends on."""

from __future__ import annotations

from pathlib import Path

import aiosqlite

from threadline.storage.migrations import apply_migrations

MIGRATIONS_DIR = Path(__file__).with_name("migrations")

# WAL lets the canvas read while a transform writes; cascades keep a deleted investigation
# from stranding its entities; the busy timeout absorbs a second connection during tests.
PRAGMAS = (
    "PRAGMA journal_mode = WAL",
    "PRAGMA foreign_keys = ON",
    "PRAGMA busy_timeout = 5000",
)


async def open_database(database_file: Path) -> aiosqlite.Connection:
    """Return an open connection whose schema is at the latest migration."""
    database_file.parent.mkdir(parents=True, exist_ok=True)
    connection = await aiosqlite.connect(database_file)
    try:
        for pragma in PRAGMAS:
            await connection.execute(pragma)
        await connection.commit()
        await apply_migrations(connection, MIGRATIONS_DIR)
    except BaseException:
        # A half-initialised connection must not escape, including on cancellation, or the
        # file stays locked for the lifetime of the process.
        await connection.close()
        raise
    return connection
