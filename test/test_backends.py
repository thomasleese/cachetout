from datetime import UTC, datetime

import pytest
from freezegun import freeze_time

from cachetout.backends.memory import MemoryBackend


@pytest.fixture(params=[MemoryBackend], ids=["memory"])
def backend_factory(request):
    return request.param


@pytest.fixture
def backend(backend_factory):
    return backend_factory()


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
