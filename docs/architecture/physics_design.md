# Physics Design (PyBullet)

Configuration

- Gravity: (0, 0, -9.8), fixed dt (e.g., 1/240 s)
- Self-collision enabled for humanoids
- Low, simple friction enabled by default; tunable via config
  - Lateral friction: small non-zero default to approximate no-gi mats (see `configuration.md`)
  - Rolling/spinning friction: default to 0.0
- Joint limits sourced from URDF/MJCF; centralized access for safety checks
- Default action mode: torque control (normalized to [-1, 1] and scaled/clipped)

Stability

- Clamp torques/forces; avoid extreme impulses
- Use fixed base for plane; ensure humanoids initialized above ground with small randomization
- Optional per-joint torque limits derived from URDF effort limits when available

Contacts

- Access inter-body contact points each step; summarize into fixed-length vector (see `observations_actions.md`)
- Optional filtering by link pairs (e.g., arm vs. neck/head) for reward logic and logging
- Draw debug contact markers in GUI when visualization is enabled

Determinism

- Use direct mode in headless runs; fix seeds for any randomization
- Keep dynamics and solver settings constant across runs; log all physics parameters
