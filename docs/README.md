# BJJSim Documentation

## End-to-end tests (Playwright)

- Install package and tools: `pwsh -ExecutionPolicy Bypass -File ../scripts/setup.ps1`
- Install browsers: `python -m playwright install --with-deps chromium`
- Run tests: `pytest -q`

Notes:

- The smoke test starts a local uvicorn subprocess and drives the dashboard.
- Locally, if browsers are not installed, the test is skipped; in CI ensure installation step runs.

This folder is the canonical source of truth for requirements, architecture, and planning. Start with `requirements/overview.md` and proceed to architecture and planning as needed.

## Structure

- `requirements/`: What the system must do and constraints
- `architecture/`: How we will design and implement it
- `planning/`: Roadmap, milestones, risks, and decisions (ADRs)
