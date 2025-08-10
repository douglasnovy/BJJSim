# Roadmap

Phase 0 — Scaffolding (this PR)

- Repo structure, docs, tooling (ruff/black/mypy/pre-commit)

Phase 1 — UI-First Physics Prototype

- Two humanoids in PyBullet; deterministic stepping; contact readout; GUI toggle
- Local web UI (FastAPI + Jinja2) with start/stop/reset/seed; periodic frame preview with overlays
- Select standard humanoid model and publish link/joint mapping
- Exit: Deterministic stepping validated; contact summary extraction works; UI smoke test passes headless

Phase 2 — Environment and Rewards

- Multi-agent Gymnasium env; observation/action spaces; hierarchical reward components with logging
- Web UI control panel (local) with start/stop/reset/seed; periodic frame preview; Playwright test scaffolding
- Exit: Random-policy rollouts run; reward components tracked; UI smoke test passes headless

Phase 3 — Self-Play Baseline

- RLlib PPO training scripts; checkpointing; simple evaluation loop
- Exit: Training runs for N iterations without instability; rewards trend sensible

Phase 4 — Evaluation and Iteration

- Metrics, videos, curriculum tweaks, reduce false positives

Phase 5 — Extensions

- Friction scheduling; improved models; opponent sampling; engine abstraction
