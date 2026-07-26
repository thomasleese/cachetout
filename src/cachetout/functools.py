from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from functools import wraps
from inspect import signature
from typing import Any

from cachetout.backends.abc import Backend

from .cache import Cache

DEFAULT = object()


@dataclass
class Key:
    args: tuple[Any]
    kwargs: dict[str, Any]


def cache(*args, **kwargs):
    name: str | None = kwargs.get("name")
    app_name: str | None = kwargs.get("app_name")
    backend: Backend | None = kwargs.get("backend")
    expires_in: timedelta | None = kwargs.get("expires_in")

    def decorator(f):
        cache = Cache(name or f.__name__, app_name=app_name, backend=backend)
        sig = signature(f)

        @wraps(f)
        def wrapper(*args, **kwargs):
            key = Key(args, kwargs)

            value = cache.get(key, default=DEFAULT, type=sig.return_annotation)
            if value is DEFAULT:
                value = f(*args, **kwargs)

                if expires_in is not None:
                    expires_at = datetime.now(tz=UTC) + expires_in
                else:
                    expires_at = None

                cache.set(key, value, expires_at=expires_at)

            return value

        return wrapper

    if len(args) == 1 and callable(args[0]):
        return decorator(args[0])
    else:
        return decorator
