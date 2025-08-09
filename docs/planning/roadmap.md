# Roadmap

Phase 0 — Scaffolding (this PR)

- Repo structure, docs, tooling (ruff/black/mypy/pre-commit)

Phase 1 — Physics Prototype

- Two humanoids in PyBullet; deterministic stepping; contact readout; GUI toggle
- Exit: Deterministic stepping validated; contact summary extraction works

Phase 2 — Environment and Rewards

- Multi-agent Gymnasium env; observation/action spaces; hierarchical reward components with logging
- Exit: Random-policy rollouts run; reward components tracked

Phase 3 — Self-Play Baseline

- RLlib PPO training scripts; checkpointing; simple evaluation loop
- Exit: Training runs for N iterations without instability; rewards trend sensible

Phase 4 — Evaluation and Iteration

- Metrics, videos, curriculum tweaks, reduce false positives

Phase 5 — Extensions

- Friction scheduling; improved models; opponent sampling; engine abstraction
