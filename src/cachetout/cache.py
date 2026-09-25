from datetime import datetime
from typing import TypeVar, cast, overload

import msgspec.msgpack
import platformdirs

from .backends.abc import Backend
from .backends.sqlite import SQLiteBackend

K = TypeVar("K")
V = TypeVar("V")


class _DefaultRaise:
    """Sentinel type for the default `default` value of Cache.get."""


DEFAULT_RAISE = _DefaultRaise()


class Cache:
    """A persistent cache that stores values in a named backend."""

    def __init__(
        self, name: str, app_name: str | None = None, backend: Backend | None = None
    ):
        """Create a cache with the given name.

        If `backend` is not given, a SQLite backend is created inside the
        user cache directory for `app_name` (or `name` if no app name is
        given).
        """
        self.name = name

        if backend is not None:
            self.backend = backend
        else:
            base_path = platformdirs.user_cache_path(app_name or name)
            path = base_path / f"{name}.db"
            path.parent.mkdir(parents=True, exist_ok=True)
            self.backend = SQLiteBackend(path=path)

        self.encoder = msgspec.msgpack.Encoder()

    def __contains__(self, key: K) -> bool:
        """Return whether the cache contains the given key."""
        encoded_key = self.encoder.encode(key)
        return encoded_key in self.backend

    def __delitem__(self, key: K) -> None:
        """Remove the given key from the cache."""
        encoded_key = self.encoder.encode(key)
        del self.backend[encoded_key]

    @overload
    def get(self, key: K, *, type: type[V]) -> V: ...

    @overload
    def get(self, key: K, *, type: type[V], default: V) -> V: ...

    def get(
        self, key: K, *, type: type[V], default: V | _DefaultRaise = DEFAULT_RAISE
    ) -> V:
        """Return the value for the given key, decoded as `type`.

        If the key is missing and `default` is given, return `default`;
        otherwise raise `KeyError`.
        """
        encoded_key = self.encoder.encode(key)

        try:
            value = self.backend[encoded_key]
        except KeyError:
            if default is DEFAULT_RAISE:
                raise
            else:
                return cast(V, default)
        else:
            return msgspec.msgpack.decode(value, type=type)

    def set(self, key: K, value: V, *, expires_at: datetime | None = None) -> None:
        """Store the given value against the given key.

        If `expires_at` is given, the value can no longer be retrieved
        after that time.
        """
        encoded_key = self.encoder.encode(key)
        encoded_value = self.encoder.encode(value)

        self.backend[encoded_key] = (encoded_value, expires_at)
