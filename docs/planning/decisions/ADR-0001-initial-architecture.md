# ADR-0001: Initial Architecture and Tooling

Context

- Need a fast path to a working self-play physics prototype with strong Python 3.12 typing and tooling

Decision

- Physics: PyBullet (rigid-body), Gymnasium env adapter, RLlib PPO (torch)
- Tooling: ruff/mypy/pre-commit/pytest; Windows PowerShell setup script
- Documentation-first: requirements/architecture/planning before code

Consequences

- Faster prototyping; may need engine abstraction if switching to MuJoCo later
- Strong typing upfront reduces refactor cost
