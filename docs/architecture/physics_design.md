# Physics Design (PyBullet)

Configuration

- Gravity: (0, 0, -9.8), fixed dt (e.g., 1/240 s)
- Self-collision enabled for humanoids
- Zero friction initially; configurable later
- Joint limits sourced from URDF; centralized access for safety checks

Stability

- Clamp torques/forces; avoid extreme impulses
- Use fixed base for plane; ensure humanoids initialized above ground with small randomization

Contacts

- Access inter-body contact points each step; summarize into fixed-length vector
- Optional filtering by link pairs (e.g., arm vs. neck)

Determinism

- Use direct mode in headless runs; fix seeds for any randomization
