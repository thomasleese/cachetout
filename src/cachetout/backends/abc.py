from abc import ABC, abstractmethod
from datetime import datetime

type Value = tuple[bytes, datetime | None]


class Backend(ABC):
    @abstractmethod
    def __contains__(self, key: bytes) -> bool: ...

    @abstractmethod
    def __delitem__(self, key: bytes) -> None: ...

    @abstractmethod
    def __getitem__(self, key: bytes) -> bytes: ...

    @abstractmethod
    def __setitem__(self, key: bytes, value: Value) -> None: ...
