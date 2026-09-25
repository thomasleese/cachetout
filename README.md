# Cachetout

A persistent, type-safe caching library for Python.

## Installation

```shell
$ pip install cachetout
```

## Usage

```python
from cachetout import Cache

cache = Cache("my_app_cache")

cache.set("user:123", {"name": "Alice", "age": 30})

user = cache.get("user:123", type=dict)
print(user)  # {'name': 'Alice', 'age': 30}

del cache["user:123"]
```

For more examples, including the `cache` decorator, serialisation, and
expiration, see the [documentation].

[documentation]: https://thomas.leese.io/cachetout/

## Development

### Tests

```shell
$ uv run pytest
```

### Linting

```shell
$ uv run ruff format
$ uv run ruff check
$ uv run ty check
```
