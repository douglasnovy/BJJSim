# BJJSim

Brazilian Jiu-Jitsu multi-agent self-play simulation. This repository will host a Python 3.12, type-hinted, research-grade environment to explore emergent BJJ-like behaviors via simplified rigid-body physics and reinforcement learning self-play.

Status: Documentation scaffolding and project structure only. No executable code yet.

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
├── src/ (to be added when implementation starts)
├── tests/ (to be added with first code)
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

This will create a virtual environment, install dev tooling (ruff/black/mypy/pre-commit/pytest), and install pre-commit hooks.

Tooling policies

- Python 3.12, strict type hints (mypy), ruff for linting, black for formatting
- Pre-commit hooks must pass before merging

## Contributing

See `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`.

## License

PolyForm Noncommercial 1.0.0. See `LICENSE`.
