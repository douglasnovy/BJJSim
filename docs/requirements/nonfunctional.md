# Non-functional Requirements

Quality attributes

- Reproducibility: Fixed seeds, deterministic stepping, pinned toolchain
- Observability: Reward component logging, episode summaries, optional video capture
- Performance: Run on a single machine CPU; optional GPU for RL; step rate ≥ 240 Hz in headless mode
- Portability: Windows-first dev; Unix-friendly scripts
- Maintainability: Typed Python 3.12, linted/formatted, modular design

Tooling

- Physics: PyBullet (default). Keep an adapter layer to allow MuJoCo later if desired.
- RL: Ray RLlib (torch). Configs captured in versioned files.
- Env: Gymnasium multi-agent compatibility wrapper as needed.

Security and Safety

- No network access required; local-only by default
- Clamp actions, validate config, and guard against extreme dynamics
