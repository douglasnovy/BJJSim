# BJJSim

Brazilian Jiu-Jitsu multi-agent self-play simulation. This repository will host a Python 3.12, type-hinted, research-grade environment to explore emergent BJJ-like behaviors via simplified rigid-body physics and reinforcement learning self-play.

Status: **Phase 2 In Progress** 🚧 - Phase 1's UI-first physics prototype is complete, and an initial multi-agent environment skeleton now ships with deterministic placeholder observations/rewards for integration testing without external dependencies.

Next focus: Phase 2 — Environment and Rewards - Replace placeholder observations with physics data, add richer reward components, and expose termination signals beyond episode length.

## What we're building

- Two rigid humanoids in PyBullet interact under simplified physics
- A custom multi-agent environment designed to align with Gymnasium semantics once the full dependency stack is available
- Hierarchical rewards prioritizing: staying on top > control > joint hyperextension > choke
- Self-play training with RLlib PPO (torch), GUI for debugging and headless for training

## Optional dependencies

The repository vendors only standard-library code to keep tests runnable in constrained environments. Installing the following extras unlocks additional features and tests:

- `fastapi`, `uvicorn`, `pydantic`, `jinja2`, `httpx`, `pillow`: required for the dashboard API and Playwright smoke test
- `gymnasium`, `numpy`: bring the environment closer to the long-term Gymnasium API plan
- `playwright`, `pytest-playwright`: enable browser-driven end-to-end tests

When these packages are absent, the related tests are skipped while core physics and environment unit tests continue to run.

## Documentation (Sphinx)

- Build once:
  - `pip install -r docs/requirements.txt`
  - `sphinx-build -b html docs docs/_build/html`
- Live-reload (optional):
  - `pip install -r docs/requirements.txt`
  - `sphinx-autobuild docs docs/_build/html`
- Windows scripts:
  - Build: `pwsh -ExecutionPolicy Bypass -File .\scripts\docs-build.ps1`
  - Serve (live): `pwsh -ExecutionPolicy Bypass -File .\scripts\docs-serve.ps1`

## Run the local web UI (prototype)

```powershell
pwsh -ExecutionPolicy Bypass -File .\scripts\setup.ps1
pwsh -ExecutionPolicy Bypass -File .\scripts\serve-quick.ps1
```

Once started, the app provides these initial endpoints:

- `GET /` — dashboard page
- `POST /api/sim/reset` — reset with optional `{seed:int}`
- `POST /api/sim/start` — start episode
- `POST /api/sim/stop` — stop episode
- `POST /api/sim/step` — advance by `{num_steps:int>=1}` while running
- `GET /api/sim/state` — current state
  - Includes `metrics`: `{ episodes_started, total_steps, steps_per_second }`
- `GET /api/frames/current` — placeholder PNG frame (will show live frames in Phase 1)
- `GET /api/metrics` — lightweight server metrics
- `WS  /ws/events` — WebSocket stream: initial `hello` then periodic `state` updates
- `GET /healthz` — health probe with version
- `GET /readyz` — readiness probe
- `GET /api/config` — fetch runtime config
- `POST /api/config` — update runtime config fields
- `GET /api/events` — recent in-memory server events (for debugging/UI)

## End-to-end tests (Playwright)

- Install project tooling: `pwsh -ExecutionPolicy Bypass -File .\scripts\setup.ps1`
- Install browsers: `python -m playwright install --with-deps chromium`
- Run all tests: `pytest -q`

Notes:

- The E2E smoke test launches a local uvicorn subprocess and drives the dashboard when the optional web stack is installed.
- Locally, if browsers or FastAPI dependencies are not installed, the related tests are skipped. In CI, ensure the install step runs.

### Troubleshooting

- No module named `uvicorn`:
  - Ensure the virtual environment is active: `.\.venv\Scripts\Activate.ps1`
  - Install the project and deps: `pip install -e .`
  - Or re-run setup: `pwsh -ExecutionPolicy Bypass -File .\scripts\setup.ps1`

## Repository structure

```text
.
├── docs/
│   ├── README.md
│   ├── index.md
│   ├── conf.py
│   ├── requirements/
│   │   ├── overview.md
│   │   ├── functional.md
│   │   ├── nonfunctional.md
│   │   ├── assumptions.md
│   │   ├── open_questions.md
│   │   └── glossary.md
│   ├── architecture/
│   │   ├── architecture.md
│   │   ├── env_design.md
│   │   ├── physics_design.md
│   │   ├── reward_design.md
│   │   └── self_play.md
│   └── planning/
│       ├── roadmap.md
│       ├── milestones.md
│       ├── risks.md
│       └── decisions/
│           └── ADR-0001-initial-architecture.md
├── scripts/
│   ├── setup.ps1
│   ├── docs-build.ps1
│   └── docs-serve.ps1
├── src/
│   └── bjjsim/
│       ├── __init__.py
│       ├── env/
│       │   └── __init__.py
│       ├── physics/
│       │   ├── __init__.py
│       │   └── adapter.py
│       └── web/
│           ├── __init__.py
│           ├── app.py
│           └── templates/
│               └── index.html
├── tests/
│   ├── README.md
│   ├── conftest.py
│   ├── test_e2e_smoke.py
│   ├── test_env.py
│   ├── test_physics_adapter.py
│   └── test_web_app.py
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── pyproject.toml
├── .pre-commit-config.yaml
└── .gitignore
```

## Quickstart (docs)

- Start in `docs/requirements/overview.md` for the end-to-end requirements and mapping
- See `docs/architecture/architecture.md` for the system design
- Track priorities in `docs/planning/roadmap.md`

## Development setup (Windows PowerShell)

```powershell
pwsh -ExecutionPolicy Bypass -File .\scripts\setup.ps1
```

This will create a virtual environment, install dev tooling (ruff/mypy/pytest/pre-commit), and install pre-commit hooks.

Tooling policies

- Python 3.12, strict type hints (mypy), Ruff for linting and formatting
- Pre-commit hooks must pass before merging
- All logs/output use ASCII only

## Contributing

See `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`.

## License

PolyForm Noncommercial 1.0.0. See `LICENSE`.
