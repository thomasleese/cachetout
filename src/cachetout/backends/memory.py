from datetime import UTC, datetime
from threading import Lock

from .abc import Backend


class MemoryBackend(Backend):
    def __init__(self):
        self._lock = Lock()
        self._data: dict[bytes, bytes] = {}
        self._expirations: dict[bytes, datetime] = {}

    def __contains__(self, key: bytes) -> bool:
        with self._lock:
            try:
                self._data[key]
            except KeyError:
                return False
            else:
                try:
                    expires_at = self._expirations[key]
                except KeyError:
                    return True
                else:
                    return expires_at >= datetime.now(tz=UTC)

    def __delitem__(self, key: bytes) -> None:
        with self._lock:
            del self._data[key]
            self._delete_expiration(key)

    def get(self, key: bytes, *, default: bytes | None = None) -> bytes | None:
        with self._lock:
            value = self._data.get(key, default)

            try:
                expires_at = self._expirations[key]
            except KeyError:
                pass
            else:
                if expires_at < datetime.now(tz=UTC):
                    value = default

        return value

    def set(
        self, key: bytes, value: bytes, *, expires_at: datetime | None = None
    ) -> None:
        with self._lock:
            self._data[key] = value

            if expires_at is not None:
                self._expirations[key] = expires_at
            else:
                self._delete_expiration(key)

    def _delete_expiration(self, key: bytes):
        try:
            del self._expirations[key]
        except KeyError:
            pass
