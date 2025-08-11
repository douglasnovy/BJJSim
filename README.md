# BJJSim

Brazilian Jiu-Jitsu multi-agent self-play simulation. This repository will host a Python 3.12, type-hinted, research-grade environment to explore emergent BJJ-like behaviors via simplified rigid-body physics and reinforcement learning self-play.

Status: UI skeleton implemented with FastAPI; basic endpoints and unit tests passing. Placeholder PNG frame endpoint and WebSocket skeleton added. Documentation scaffolded and building clean.

Current branch target: Phase 1 stepping scaffold — adds typed `POST /api/sim/step` to advance a deterministic counter while an episode is running, plus UI and tests. Also adds lightweight server metrics in `GET /api/sim/state`.

## What we're building

- Two rigid humanoids in PyBullet interact under simplified physics
- A custom multi-agent Gymnasium environment (observations/actions/rewards well-defined)
- Hierarchical rewards prioritizing: staying on top > control > joint hyperextension > choke
- Self-play training with RLlib PPO (torch), GUI for debugging and headless for training

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

- The E2E smoke test launches a local uvicorn subprocess and drives the dashboard.
- Locally, if browsers are not installed, the E2E test is skipped. In CI, ensure the install step runs.

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
│       └── web/
│           ├── __init__.py
│           ├── app.py
│           └── templates/
│               └── index.html
├── tests/
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
