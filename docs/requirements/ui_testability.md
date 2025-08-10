# UI Testability Requirements

This project will ship with a locally hosted web UI that is fully automatable by the project itself. UI testability is a first-class requirement.

## Goals

- Ensure every user-visible and interactive behavior can be tested automatically with Python-based tools.
- Keep selectors stable and semantic to minimize brittle tests.
- Support fast, deterministic, headless execution in CI.

## Test Strategy

- End-to-end tests: Playwright for Python as the default tool. Headless by default; headed mode optional for debugging.
- Component/contract tests: Exercise server-side handlers (FastAPI) with typed request/response schemas and dependency injection for fakes.
- Accessibility checks: Basic automated checks (landmarks, roles, labels) integrated into the e2e suite.

## Selector and Semantics Policy

- Every interactive element must include a stable `data-testid` attribute.
- Prefer semantic HTML and ARIA roles; tests should first target roles/names, then `data-testid` for specificity.
- Avoid selectors that depend on CSS classes or DOM structure.

## Determinism and Fixtures

- Provide a test mode with fixed seeds and deterministic environment stepping.
- Expose a server endpoint to reset state and seed the simulation for repeatable UI tests.
- Supply lightweight server-side fakes/mocks for long-running operations where practical.

## Coverage Targets (initial)

- Smoke flow: open UI, start a seeded evaluation episode, observe basic metrics → 100% pass in CI.
- Critical controls (start/stop/reset/seed entry) → 100% covered by e2e.
- Error paths (invalid config, server errors) → at least one test per class of error.

## CI Integration

- E2E runs headless against the local server on `127.0.0.1`.
- Tests produce junit XML and HTML traces for debugging failures.

## Tooling

- Python 3.12, typed everywhere.
- `pytest` + `pytest-playwright` (or `playwright` plugin) for e2e.
- `ruff`/`black`/`mypy` for code quality; UI test code must pass the same linters.
- ASCII-only logs and outputs to simplify CI parsing.
