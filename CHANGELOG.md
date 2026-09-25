# Changelog

## v0.3.0

- API documentation is now included for the public classes, functions and methods.

## v0.2.0

- Cache keys are no longer deleted from the store on retrieval if they’ve expired.
  This ensures that a read operation will never perform a write operation.
- The `in` and `not in` operator is now supported on both the backend classes and the
  `Cache` class, providing a faster way of determining presence as it avoids decoding
  the value.
- Deleting keys now requires the use of the `del` statement and raises a `KeyError` if
  the key doesn't exist to delete.
- `Cache.get` now raises a `KeyError` if the key doesn’t exist, unless a `default` is
  passed in to the call.

## v0.1.0

- First release.
