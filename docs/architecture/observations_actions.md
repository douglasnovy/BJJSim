# Observations and Actions

Observations (per agent; tentative)

- Own joints: positions (radians), velocities (rad/s)
- Opponent joints: positions, velocities
- Base positions (z for top heuristic; consider full pose)
- Contact summary: up to K contacts, each encoded as (link-pair id, normal force, relative position)

Actions (per agent)

- Vector of length = number of controllable joints
- Normalized to [-1, 1]; scaled to torque/target internally

Notes

- Keep shapes fixed; pad/truncate contacts to K
- Provide dataclasses/TypedDicts for clarity in code
