from datetime import UTC, datetime
from threading import Lock


class MemoryBackend:
    def __init__(self):
        self._lock = Lock()
        self._data: dict[bytes, bytes] = {}
        self._expirations: dict[bytes, datetime] = {}

    def get(self, key: bytes, *, default: bytes | None = None) -> bytes | None:
        with self._lock:
            value = self._data.get(key, default)

            try:
                expires_at = self._expirations[key]
                if expires_at < datetime.now(tz=UTC):
                    self._delete(key)
                    value = None
            except KeyError:
                pass

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

    def delete(self, key: bytes) -> bool:
        with self._lock:
            return self._delete(key)

    def _delete(self, key: bytes) -> bool:
        try:
            del self._data[key]
            self._delete_expiration(key)
            return True
        except KeyError:
            return False

    def _delete_expiration(self, key: bytes):
        try:
            del self._expirations[key]
        except KeyError:
            pass
