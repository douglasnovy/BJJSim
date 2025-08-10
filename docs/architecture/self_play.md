# Self-Play and Training (RLlib PPO)

Setup

- Two policies (`agent1`, `agent2`) mapped to agents
- PPO with torch backend; configurable workers and rollout length
- Periodic checkpointing; evaluation episodes with GUI optional

Opponent sampling

- Start with symmetric latest policies
- Optionally introduce past checkpoint sampling later to stabilize learning

Visualization & logging

- Enable periodic GUI evaluation episodes with on-screen annotations of reward events
- Log per-component rewards and contact stats; emit CSV/Parquet for offline review

Key hyperparameters (initial)

- Clip param, entropy coeff, learning rate, vf clip, GAE λ
- Observation/Reward normalization off initially; consider later

Reproducibility

- Fixed trainer and env seeds; deterministic env stepping
