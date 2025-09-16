# Architecture Overview

Components

- Physics Engine Adapter (PyBullet): Loads humanoids, steps simulation, exposes typed state
- Environment Adapter (Gymnasium): Multi-agent API, observation/action spaces, reward/termination
- Training Orchestrator (RLlib): PPO configuration, self-play setup, checkpointing, evaluation
- Visualization: Optional GUI toggle, optional video capture and on-screen annotations
- Web UI Control Panel: Local FastAPI-served pages to control evaluation episodes and view metrics/frames
- Instrumentation: Reward component logging and episode stats

Near-term implementation: FastAPI UI skeleton in `src/bjjsim/web/` plus an initial Gymnasium environment (`bjjsim.env`) exposing deterministic placeholder observations/rewards for testing.

Key design choices

- Rigid-body physics with small, simple lateral friction by default (no-gi mats approximation)
- Hierarchical rewards to impart priorities without hand-coding moves
- Deterministic stepping (fixed dt) and bounded action magnitudes
- Adapter layer boundaries so we can change physics engine or RL library later
- Local web UI instead of desktop GUI to enable robust, automated UI testing in Python

Data flow

1. Training loop computes actions using policies
2. Environment adapter applies actions via physics adapter
3. Physics computes next state and contacts
4. Environment computes rewards/termination and returns observations
