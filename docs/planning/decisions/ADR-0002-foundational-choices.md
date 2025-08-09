# ADR-0002: Foundational Choices (Friction, Control, Model, Visualization, License)

Context

- Planning review identified key decisions needed before implementation: friction model, humanoid selection, action control mode, observation contact strategy, visualization/logging, and licensing.

Decision

- Physics friction: Default to small, simple lateral friction to approximate no-gi mats; spinning/rolling = 0.0; configurable and can be annealed.
- Control mode: Torque control by default with normalized [-1, 1] actions scaled/clipped per joint.
- Humanoid model: Use a well-supported humanoid MJCF/URDF commonly used in research (e.g., DeepMind Control Suite Humanoid MJCF port for PyBullet). Document link-name to ID mapping for neck/arms/torso.
- Observation contacts: Fixed-size K=8 contact summary with optional EMA over D=3 steps; sorted by normal force; link-pair IDs maintained in a canonical table.
- Visualization & logging: Treat as first-class. Provide GUI overlays for contacts and reward event annotations; log per-component rewards and contact stats for offline analysis.
- License: PolyForm Noncommercial 1.0.0 to enable contributions while disallowing commercial use.

Consequences

- Small friction reduces degenerate sliding while keeping physics simple and fast.
- Torque control aligns with potential future transfer to real humanoids; requires careful torque limits.
- Standard humanoid model accelerates development; we avoid reinventing meshes/limits.
- Bounded contact encoding keeps observations cheap and scalable across millions of steps.
- Early visualization reduces reward hacking risk and accelerates debugging.
- Noncommercial license encourages open collaboration without commercial exploitation.

Status

- Accepted.
