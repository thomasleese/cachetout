from datetime import timedelta
from time import sleep

import pytest

from cachetout.backends.memory import MemoryBackend
from cachetout.functools import cache


@pytest.fixture
def backend() -> MemoryBackend:
    return MemoryBackend()


def test_call_count(backend):
    call_count = 0

    @cache(name="test_call_count", backend=backend)
    def expensive_function(x, y) -> int:
        nonlocal call_count
        call_count += 1
        return x + y

    result1 = expensive_function(1, 2)
    assert result1 == 3
    assert call_count == 1

    result2 = expensive_function(1, 2)
    assert result2 == 3
    assert call_count == 1

    result3 = expensive_function(3, 4)
    assert result3 == 7
    assert call_count == 2


def test_kwargs(backend):
    @cache(name="test_kwargs", backend=backend)
    def greet(name, greeting="Hello") -> str:
        return f"{greeting}, {name}!"

    result1 = greet("Alice")
    assert result1 == "Hello, Alice!"

    result2 = greet("Alice")
    assert result2 == "Hello, Alice!"

    result3 = greet("Alice", greeting="Hi")
    assert result3 == "Hi, Alice!"

    result4 = greet(name="Alice", greeting="Hi")
    assert result4 == "Hi, Alice!"


def test_complex_return(backend):
    @cache(name="test_complex_return", backend=backend)
    def get_data() -> dict[str, int]:
        return {"a": 1, "b": 2}

    result = get_data()
    assert result == {"a": 1, "b": 2}
    assert isinstance(result, dict)


def test_no_name(backend):
    @cache(backend=backend)
    def my_function() -> int:
        return 42

    assert my_function() == 42
    assert my_function() == 42


def test_expiration(backend):
    call_count = 0

    @cache(
        name="test_expiration", backend=backend, expires_in=timedelta(milliseconds=50)
    )
    def timed_function() -> int:
        nonlocal call_count
        call_count += 1
        return call_count

    result1 = timed_function()
    assert result1 == 1
    assert call_count == 1

    result2 = timed_function()
    assert result2 == 1
    assert call_count == 1

    sleep(0.06)

    result3 = timed_function()
    assert result3 == 2
    assert call_count == 2
