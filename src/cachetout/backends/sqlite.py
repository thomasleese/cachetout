import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from .abc import Backend, Value


class SQLiteBackend(Backend):
    """A backend that stores values in a SQLite database file."""

    create_table_sql = """
                       CREATE TABLE IF NOT EXISTS cache(
                           key BLOB PRIMARY KEY NOT NULL,
                           value BLOB NOT NULL,
                           expires_at TIMESTAMP
                       )
                       """

    def __init__(self, *, path: Path):
        """Create a backend connected to the database at the given path."""
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

        self.cursor.execute(self.create_table_sql)
        self.connection.commit()

    def __contains__(self, key: bytes) -> bool:
        """Return whether the backend contains an unexpired value for the key."""
        sql = "SELECT 1 FROM cache WHERE key = ? AND (expires_at IS NULL OR expires_at >= ?)"
        parameters = (key, datetime.now(tz=UTC).isoformat())

        self.cursor.execute(sql, parameters)
        return self.cursor.fetchone() is not None

    def __delitem__(self, key: bytes) -> None:
        """Remove the given key from the backend.

        Raises `KeyError` if the key is missing.
        """
        sql = "DELETE FROM cache WHERE key = ?"
        parameters = (key,)

        self.cursor.execute(sql, parameters)
        self.connection.commit()

        if self.cursor.rowcount == 0:
            raise KeyError(key)

    def __getitem__(self, key: bytes) -> bytes:
        """Return the value for the given key.

        Raises `KeyError` if the key is missing or expired.
        """
        sql = "SELECT value FROM cache WHERE key = ? AND (expires_at IS NULL OR expires_at >= ?)"
        parameters = (key, datetime.now(tz=UTC).isoformat())

        self.cursor.execute(sql, parameters)
        row = self.cursor.fetchone()

        if row is None:
            raise KeyError(key)
        else:
            return row[0]

    def __setitem__(self, key: bytes, value: Value) -> None:
        """Store the given value against the given key."""
        expires_at_isoformat = value[1].isoformat() if value[1] is not None else None

        sql = """
            INSERT INTO cache (key, value, expires_at)
            VALUES (?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET value = ?, expires_at = ?
        """

        parameters = (
            key,
            value[0],
            expires_at_isoformat,
            value[0],
            expires_at_isoformat,
        )

        self.cursor.execute(sql, parameters)
        self.connection.commit()
