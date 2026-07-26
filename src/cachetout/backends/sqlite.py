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

    def get(self, key: bytes, *, default: bytes | None = None) -> bytes | None:
        self.cursor.execute("SELECT value, expires_at FROM cache WHERE key = ?", (key,))
        row = self.cursor.fetchone()

        if row is None:
            return default

        value, expires_at_isoformat = row

        if expires_at_isoformat is not None and datetime.fromisoformat(
            expires_at_isoformat
        ) < datetime.now(tz=UTC):
            self.delete(key)
            return default

        return value

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

    def delete(self, key: bytes) -> bool:
        self.cursor.execute("DELETE FROM cache WHERE key = ?", (key,))
        self.connection.commit()
        return self.cursor.rowcount > 0
