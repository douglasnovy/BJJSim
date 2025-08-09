# Observations and Actions

Observations (per agent; initial)

- Own joints: positions (radians), velocities (rad/s)
- Opponent joints: positions, velocities (optionally downsampled)
- Base: z-position for top heuristic; yaw may be added later if needed
- Contact summary vector (computationally bounded):
  - Fixed-size K entries (default K=8)
  - Per-entry encoding: `(link_pair_id, normal_force, rel_pos_x, rel_pos_y, rel_pos_z)`
  - Sorted by descending normal force; pad with zeros when fewer than K
  - Optional exponential decay/EMA over last D steps (default D=3) for stability

Actions (per agent)

- Torque control by default
- Vector length = number of controllable joints
- Normalized to [-1, 1]; scaled to per-joint torque limits; clipped to safe bounds

Notes

- Keep tensor shapes fixed; pad/truncate contacts to K
- Provide typed configuration for `K` and decay window `D`
- Maintain mapping tables for link names to IDs for reproducible contact encoding
