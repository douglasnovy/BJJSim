# Tests

Add tests alongside implementation. Use `pytest` and keep tests small and focused.

## UI End-to-End Tests

- Tooling: Playwright for Python (`pytest` plugin)
- Install browser once locally: `python -m pip install playwright pytest-playwright` then `python -m playwright install chromium`
- Run headless: `pytest -m e2e --maxfail=1 -q`
- CI runs headless against the local server (`127.0.0.1:<port>`). Tests should rely on `data-testid` selectors and semantic roles.
