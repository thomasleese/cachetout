from abc import ABC, abstractmethod
from datetime import datetime


class Backend(ABC):
    @abstractmethod
    def __contains__(self, key: bytes) -> bool: ...

    @abstractmethod
    def __delitem__(self, key: bytes) -> None: ...

    @abstractmethod
    def get(self, key: bytes, *, default: bytes | None = None) -> bytes | None: ...

    @abstractmethod
    def set(
        self, key: bytes, value: bytes, *, expires_at: datetime | None = None
    ) -> None: ...
