# Lessons Learned

- Activating the venv via PowerShell can collide with file locks when forcing removal. Prefer reusing `.venv` unless absolutely necessary.
- Use `response_model` and return Pydantic models to keep contracts tight and mypy-friendly.
- Keep endpoints small and deterministic; this made stepping logic trivial to test.
- For Windows CI/local, prefer ASCII-only logs to avoid encoding surprises.
 - Exposing a tiny metrics block via existing state endpoints helps catch regressions without adding infra.
