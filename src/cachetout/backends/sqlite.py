import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from .abc import Backend


class SQLiteBackend(Backend):
    create_table_sql = """
                       CREATE TABLE IF NOT EXISTS cache(
                           key BLOB PRIMARY KEY NOT NULL,
                           value BLOB NOT NULL,
                           expires_at TIMESTAMP
                       )
                       """

    def __init__(self, *, path: Path):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

        self.cursor.execute(self.create_table_sql)
        self.connection.commit()

    def __contains__(self, key: bytes) -> bool:
        sql = "SELECT 1 FROM cache WHERE key = ? AND (expires_at IS NULL OR expires_at >= ?)"
        parameters = (key, datetime.now(tz=UTC).isoformat())

        self.cursor.execute(sql, parameters)
        return self.cursor.fetchone() is not None

    def __delitem__(self, key: bytes) -> None:
        sql = "DELETE FROM cache WHERE key = ?"
        parameters = (key,)

        self.cursor.execute(sql, parameters)
        self.connection.commit()

        if self.cursor.rowcount == 0:
            raise KeyError(key)

    def get(self, key: bytes, *, default: bytes | None = None) -> bytes | None:
        sql = "SELECT value FROM cache WHERE key = ? AND (expires_at IS NULL OR expires_at >= ?)"
        parameters = (key, datetime.now(tz=UTC).isoformat())

        self.cursor.execute(sql, parameters)
        row = self.cursor.fetchone()

        if row is None:
            return default

        return row[0]

    def set(
        self, key: bytes, value: bytes, *, expires_at: datetime | None = None
    ) -> None:
        expires_at_isoformat = (
            expires_at.isoformat() if expires_at is not None else None
        )

        self.cursor.execute(
            """
            INSERT INTO cache (key, value, expires_at)
            VALUES (?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET value = ?, expires_at = ?
            """,
            (key, value, expires_at_isoformat, value, expires_at_isoformat),
        )
        self.connection.commit()
