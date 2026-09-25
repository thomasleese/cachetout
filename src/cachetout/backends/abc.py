from abc import ABC, abstractmethod
from datetime import datetime

type Value = tuple[bytes, datetime | None]


class Backend(ABC):
    """A storage backend that maps encoded keys to encoded values."""

    @abstractmethod
    def __contains__(self, key: bytes) -> bool:
        """Return whether the backend contains the given key."""

    @abstractmethod
    def __delitem__(self, key: bytes) -> None:
        """Remove the given key from the backend."""

    @abstractmethod
    def __getitem__(self, key: bytes) -> bytes:
        """Return the value for the given key.

        Raises `KeyError` if the key is missing or expired.
        """

    @abstractmethod
    def __setitem__(self, key: bytes, value: Value) -> None:
        """Store the given value against the given key."""
