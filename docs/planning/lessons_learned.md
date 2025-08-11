# Lessons Learned

- Activating the venv via PowerShell can collide with file locks when forcing removal. Prefer reusing `.venv` unless absolutely necessary.
- Use `response_model` and return Pydantic models to keep contracts tight and mypy-friendly.
- Keep endpoints small and deterministic; this made stepping logic trivial to test.
- For Windows CI/local, prefer ASCII-only logs to avoid encoding surprises.
- Exposing a tiny metrics block via existing state endpoints helps catch regressions without adding infra.
- When adding new endpoints, mirror types in tests; returning a dedicated `MetricsResponse` simplified validation and kept type hints strict.
- Keep Web API docs synchronized with behavior. Documenting the WebSocket as a stream (hello then periodic state) avoids UI test confusion.
- For visual verification without heavy OCR, encode deterministic markers in images. We store `step % 256` in pixel (0,0)'s red channel and draw a lightweight text overlay; tests read the pixel to assert correctness.

- CI tips: e2e tests require Playwright browsers. Ensure the workflow installs Chromium (`python -m playwright install chromium`) before running `pytest`.
