# Environment Design (Gymnasium, Multi-agent)

API

- Two agents: `agent1`, `agent2`
- `reset(seed) -> (obs, info)` where `obs` is a dict per agent
- `step(actions) -> (obs, rewards, terminated, truncated, infos)` per Gymnasium v0.29

Observation space (per agent)

- Own joint positions/velocities; base pose (position + orientation if needed)
- Opponent joint positions/velocities; opponent base pose
- Contact summary vector (fixed-length, e.g., top-k contacts with position/force/time decay)

Action space (per agent)

- Continuous vector per controllable joint
- Control mode configurable: torque or position control
- Clipped to [-1, 1], scaled inside physics adapter

Termination

- Submission condition met (hyperextension/choke) or timeout steps

Type hints

- All public functions and data structures annotated strictly; mypy must pass
