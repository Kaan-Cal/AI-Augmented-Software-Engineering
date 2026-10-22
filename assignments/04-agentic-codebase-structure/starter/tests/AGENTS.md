
# Scoped Agent Instructions — Tests

These instructions apply to files inside the `tests/` directory.

## Testing Guidelines

1. Test application behavior through FastAPI's public HTTP API using `TestClient`.
2. Cover both successful operations and failure or edge cases.
3. Keep tests independent; do not rely on test execution order.
4. Verify HTTP status codes and relevant response data.
5. Avoid testing private implementation details or internal helper functions.
6. Preserve the behavior covered by the original `test_main.py`.
7. Use clear, descriptive test names.
8. Do not modify application code merely to make a failing test pass.
9. Run the complete test suite using `python -m pytest` after changes.

## Custom Alias Feature

For the custom alias task, verify:

- A valid custom alias is accepted.
- The returned short code matches the requested alias.
- The custom alias redirects to the correct original URL.
- Reusing an existing alias returns HTTP 409 Conflict.
- Creating a link without an alias continues to work.

Keep tests focused on observable API behavior.
