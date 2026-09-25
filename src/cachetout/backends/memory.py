from datetime import UTC, datetime
from threading import Lock

from .abc import Backend, Value


class MemoryBackend(Backend):
    """A backend that stores values in memory.

    Values are lost when the backend is destroyed.
    """

    def __init__(self):
        """Create an empty backend."""
        self._lock = Lock()
        self._data: dict[bytes, bytes] = {}
        self._expirations: dict[bytes, datetime] = {}

    def __contains__(self, key: bytes) -> bool:
        """Return whether the backend contains an unexpired value for the key."""
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
        """Remove the given key from the backend."""
        with self._lock:
            del self._data[key]
            self._delete_expiration(key)

    def __getitem__(self, key: bytes) -> bytes:
        """Return the value for the given key.

        Raises `KeyError` if the key is missing or expired.
        """
        with self._lock:
            value = self._data[key]

            try:
                expires_at = self._expirations[key]
            except KeyError:
                pass
            else:
                if expires_at < datetime.now(tz=UTC):
                    raise KeyError(key)

            return value

    def __setitem__(self, key: bytes, value: Value) -> None:
        """Store the given value against the given key."""
        with self._lock:
            self._data[key] = value[0]

            expires_at = value[1]
            if expires_at is not None:
                self._expirations[key] = expires_at
            else:
                self._delete_expiration(key)

    def _delete_expiration(self, key: bytes):
        try:
            del self._expirations[key]
        except KeyError:
            pass
