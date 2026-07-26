from datetime import datetime
from typing import TypeVar

import msgspec.msgpack
import platformdirs

from .backends.abc import Backend
from .backends.sqlite import SQLiteBackend

K = TypeVar("K")
V = TypeVar("V")


class Cache:
    def __init__(
        self, name: str, app_name: str | None = None, backend: Backend | None = None
    ):
        self.name = name

        if backend is not None:
            self.backend = backend
        else:
            base_path = platformdirs.user_cache_path(app_name or name)
            path = base_path / f"{name}.db"
            path.parent.mkdir(parents=True, exist_ok=True)
            self.backend = SQLiteBackend(path=path)

        self.encoder = msgspec.msgpack.Encoder()

    def get(self, key: K, *, type: type[V], default: V | None = None) -> V | None:
        encoded_key = self.encoder.encode(key)

        value = self.backend.get(encoded_key)
        if value is None:
            return default

        return msgspec.msgpack.decode(value, type=type)

    def set(self, key: K, value: V, *, expires_at: datetime | None = None) -> None:
        encoded_key = self.encoder.encode(key)
        encoded_value = self.encoder.encode(value)

        self.backend.set(encoded_key, encoded_value, expires_at=expires_at)

    def delete(self, key: K) -> bool:
        encoded_key = self.encoder.encode(key)
        return self.backend.delete(encoded_key)
