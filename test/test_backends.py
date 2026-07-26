import tempfile
from collections.abc import Generator
from datetime import UTC, datetime
from pathlib import Path

import pytest
from freezegun import freeze_time

from cachetout.backends.memory import MemoryBackend
from cachetout.backends.sqlite import SQLiteBackend


def memory_backend_generator() -> Generator[MemoryBackend]:
    yield MemoryBackend()


def sqlite_backend_generator() -> Generator[SQLiteBackend]:
    with tempfile.TemporaryDirectory() as temporary_directory:
        yield SQLiteBackend(path=Path(temporary_directory) / "test.db")


BACKENDS = {"memory": memory_backend_generator, "sqlite": sqlite_backend_generator}


@pytest.fixture(params=BACKENDS.values(), ids=list(BACKENDS.keys()))
def backend(request):
    yield from request.param()


def test_get_set_delete(backend) -> None:
    assert backend.get(b"key", default=b"default") == b"default"

    backend.set(b"key", b"value")

    assert backend.get(b"key") == b"value"

    assert backend.delete(b"key")

    assert backend.get(b"key") is None


def test_expiration(backend) -> None:
    with freeze_time("2020-01-01 12:00:00"):
        backend.set(
            b"key", b"value", expires_at=datetime(2020, 1, 1, 12, 5, tzinfo=UTC)
        )

    with freeze_time("2020-01-01 12:04:59"):
        assert backend.get(b"key") == b"value"

    with freeze_time("2020-01-01 12:05:00"):
        assert backend.get(b"key") == b"value"

    with freeze_time("2020-01-01 12:05:01"):
        assert backend.get(b"key") is None
