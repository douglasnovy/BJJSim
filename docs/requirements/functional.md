# Functional Requirements

1. Physics Simulation
   - Load two rigid humanoid URDFs with self-collision enabled
   - Configure gravity, time step, and dynamics (initially zero friction)
   - Provide per-step state access: joint positions/velocities, base pose, contacts

2. Environment API (Multi-agent Gymnasium)
   - Two agents with symmetric observations/actions
   - Observation includes own + opponent kinematics and recent contact summary
   - Action is continuous torque/position control per joint (configurable)
   - Step/reset/close semantics compatible with RLlib

3. Rewarding and Termination
   - Hierarchical rewards: top control, control via multiple contacts, joint hyperextension, choke; energy penalty each step
   - Terminate on submission condition or timeout
   - Configurable thresholds with sensible defaults

4. Training and Evaluation
   - PPO-based self-play using RLlib with policy mapping per agent
   - Headless training; GUI visualization toggle for debugging
   - Checkpointing and reproducible seeds; basic evaluation loop

5. Instrumentation
    - Log episode stats and reward components separately
    - Deterministic mode for reproducibility (fixed seeds, fixed dt)
