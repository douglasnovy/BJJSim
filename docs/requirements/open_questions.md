# Open Questions / TBD

- Humanoid model: Select a standard, well-supported model and document joint/link mapping (neck/arms). Candidate: DeepMind Control Suite Humanoid (MJCF) port for PyBullet.
- Reward thresholds: Confirm initial defaults for top/control/choke; validate via visualization.
- Hyperextension detection: Prefer joint-specific safe limits derived from model; define per-joint margins.
- Termination: Timeout length and robust tap-out detection; stability checks to avoid false positives.
- Observation: Fix contact K=8 and decay window D=3 initially; revisit after profiling. Opponent yaw excluded initially.
- Action space: Default to torque control; define scaling/clipping per joint; keep position control as future option.
- Curriculum: Start with small non-zero lateral friction and allow annealing schedule; define pose randomization ranges.
- Self-play strategy: Start with latest-vs-latest; add historical checkpoint sampling later as needed.
- Determinism: Enumerate remaining nondeterministic sources and log seeds/configs.
- Licensing: Adopt PolyForm Noncommercial 1.0.0 to allow contributions while disallowing commercial use.
