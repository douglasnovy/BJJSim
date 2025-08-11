# Contributing to BJJSim

Thank you for helping build an open, rigorous BJJ self-play simulation.

## Development standards

- Python 3.12 only
- Type hints required everywhere (public and private). CI enforces `mypy --strict`.
- Style: `ruff` (lint and format). Pre-commit hooks must pass.
- Tests: `pytest`. Add tests for new behavior. Prefer small, focused tests.
- Documentation: Update relevant docs under `docs/` with each change.

## Workflow

1. Create an issue describing the change.
2. Create a branch: `feature/<short-description>`.
3. Run `pre-commit install` once, then commit frequently.
4. Ensure `ruff`, `mypy`, and `pytest` are green locally.
5. Open a PR linking the issue and updating docs.

## Code organization

- `src/bjjsim/` for package code
- `tests/` for tests mirroring module structure
- `scripts/` for developer utilities (no library imports from here)
- `docs/` for requirements, architecture, planning

## Type hints

- Prefer `typing` and `collections.abc` over `typing_extensions` (Python 3.12).
- Use `TypedDict`/`Protocol` for structured dicts and interfaces.
- Avoid `Any`; when unavoidable, encapsulate and document the boundary.

## Commits and PRs

- Conventional commits recommended: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`
- Keep PRs small and focused. Include a short motivation and design notes.
