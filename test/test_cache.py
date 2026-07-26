from dataclasses import dataclass

import pytest

from cachetout.backends.memory import MemoryBackend
from cachetout.cache import Cache

backend = MemoryBackend()


@pytest.fixture
def cache() -> Cache:
    return Cache("cache", backend=backend)


@dataclass
class DummyDataclass:
    name: str
    value: int


@pytest.mark.parametrize(
    "key,value",
    [
        ("int", 123),
        ("str", "string"),
        ("dataclass", DummyDataclass("value", 123)),
        (["a", "b"], 123),
    ],
    ids=["int", "str", "dataclass", "list"],
)
def test_get_set_delete(cache: Cache, key, value) -> None:
    _type = type(value)

    assert cache.get(key, default="default", type=_type) == "default"

    cache.set(key, value)

    assert cache.get(key, type=_type) == value

    assert cache.delete(key)

    assert cache.get(key, type=_type) is None
