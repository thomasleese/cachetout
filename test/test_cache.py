from dataclasses import dataclass

import pytest

from cachetout.backends.memory import MemoryBackend
from cachetout.cache import Cache


@pytest.fixture
def cache() -> Cache:
    backend = MemoryBackend()
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

    with pytest.raises(KeyError):
        cache.get(key, type=_type)

    assert cache.get(key, type=_type, default=None) is None
    assert cache.get(key, type=_type, default="default") == "default"

    cache.set(key, value)

    assert key in cache
    assert cache.get(key, type=_type) == value

    del cache[key]

    assert key not in cache
    assert cache.get(key, type=_type, default=None) is None
