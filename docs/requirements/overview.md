# Requirements Overview

Goal: Build a Python-based multi-agent self-play simulation to explore emergent BJJ-like behaviors via simplified rigid-body physics and reinforcement learning. No explicit position teaching; behaviors emerge from physics and rewards.

Key components

- Physics: PyBullet with rigid humanoids, fixed time step, initially zero friction
- Environment: Custom multi-agent Gymnasium environment with typed observations/actions
- Rewards: Hierarchical — staying on top > control > joint hyperextension > choke; energy penalty; terminate on submission
- RL: Self-play using Ray RLlib (PPO, torch); GUI for debugging; headless training

Scope (initial)

- Minimal prototype (two humanoids) that supports potential BJJ positions via general physics (no hard-coded moves)
- Deterministic stepping, guardrails against obvious reward exploits

Out of scope (initial)

- Soft-body tissue, detailed finger articulation, real-time multiplayer, distributed training at scale

References

- See `architecture/` docs for design details and `planning/roadmap.md` for phased delivery.
