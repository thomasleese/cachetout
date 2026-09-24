# Changelog

## Unreleased

- Cache keys are no longer deleted from the store on retrieval if they’ve expired.
  This ensures that a read operation will never perform a write operation.

## v0.1.0

- First release.
