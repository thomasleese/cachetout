# Cachetout

A persistent, type-safe caching library for Python.

## Installation

```shell
pip install cachetout
```

## Usage

### `Cache` class

```python
from cachetout import Cache

# Create a cache (uses SQLite backend by default)
cache = Cache("my_app_cache")

# Store a value
cache.set("user:123", {"name": "Alice", "age": 30})

# Retrieve a value
user = cache.get("user:123", type=dict)
print(user)  # {'name': 'Alice', 'age': 30}

# Delete a value
cache.delete("user:123")
```

### `cache` decorator

```python
from datetime import timedelta
from cachetout import cache

@cache(expires_in=timedelta(hours=1))
def fetch_user_data(user_id: int) -> dict:
    # This function will only be called once per user_id per hour
    print("Fetching data from API...")
    return {"id": user_id, "data": "..."}

# First call: fetches from source
result1 = fetch_user_data(123)

# Second call with same args: returns cached result
result2 = fetch_user_data(123)
```

### Serialisation

The library uses [msgspec] for serialisation, which respects the Python type hints:

```python
from dataclasses import dataclass
from cachetout import Cache

@dataclass
class User:
    id: int
    name: str
    email: str

cache = Cache("user_cache")

# Store a dataclass instance
user = User(id=1, name="Alice", email="alice@example.com")
cache.set("user_1", user)

# Retrieve with type hint
retrieved: User = cache.get("user_1", type=User)
print(retrieved.name)  # "Alice"
```

[msgspec]: https://msgspec.dev/

### Expiration

Set expiration when storing values:

```python
from datetime import datetime, timedelta, UTC
from cachetout import Cache

cache = Cache("temp_cache")

# Expire in 1 hour
cache.set("temp_data", "value", expires_at=datetime.now(tz=UTC) + timedelta(hours=1))

# Or use timedelta with decorator
@cache(expires_in=timedelta(minutes=30))
def get_stock_price(symbol: str) -> float:
    return fetch_from_api(symbol)
```

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
