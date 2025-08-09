# Configuration Knobs

Environment

- time_step: float (default: 1/240)
- max_steps_per_episode: int (default: 2000)
- gui: bool (default: false)
- seed: int

Physics

- friction_lateral: float (default: 0.0)
- friction_spinning: float (default: 0.0)
- friction_rolling: float (default: 0.0)
- torque_scale: float (default: 200.0)
- init_pose_jitter: float (default: 0.02)

Rewards

- top_delta_z: float (default: 0.10)
- top_min_steps: int (default: 5)
- control_min_contacts: int (default: 4)
- control_min_steps: int (default: 5)
- hyperextension_margin: float (default: 0.10)
- choke_force_threshold: float (default: 50.0)
- choke_min_steps: int (default: 5)
- energy_penalty_per_step: float (default: -0.1)
- rewards: {top: 10.0, control: 5.0, hyperextension: 20.0, choke: 30.0}

Self-play / Training

- framework: str (default: torch)
- num_workers: int (default: 4)
- rollout_fragment_length: int (default: 200)
- train_batch_size: int (default: 4000)
- lr: float (default: 3e-4)
- entropy_coeff: float (default: 0.0)
- seed: int

Notes

- Capture these in a typed config (e.g., Pydantic model) when implementation begins.
