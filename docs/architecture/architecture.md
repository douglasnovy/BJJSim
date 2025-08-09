# Architecture Overview

Components

- Physics Engine Adapter (PyBullet): Loads humanoids, steps simulation, exposes typed state
- Environment Adapter (Gymnasium): Multi-agent API, observation/action spaces, reward/termination
- Training Orchestrator (RLlib): PPO configuration, self-play setup, checkpointing, evaluation
- Visualization: Optional GUI toggle, optional video capture and on-screen annotations
- Instrumentation: Reward component logging and episode stats

Key design choices

- Rigid-body physics with small, simple lateral friction by default (no-gi mats approximation)
- Hierarchical rewards to impart priorities without hand-coding moves
- Deterministic stepping (fixed dt) and bounded action magnitudes
- Adapter layer boundaries so we can change physics engine or RL library later

Data flow

1. Training loop computes actions using policies
2. Environment adapter applies actions via physics adapter
3. Physics computes next state and contacts
4. Environment computes rewards/termination and returns observations
