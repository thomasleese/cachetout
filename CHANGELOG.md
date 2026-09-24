# Changelog

## Unreleased

- Cache keys are no longer deleted from the store on retrieval if they’ve expired.
  This ensures that a read operation will never perform a write operation.
- The `in` and `not in` operator is now supported on both the backend classes and the
  `Cache` class, providing a faster way of determining presence as it avoids decoding
  the value.

## v0.1.0

- First release.
