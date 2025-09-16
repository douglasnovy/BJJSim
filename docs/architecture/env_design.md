# Environment Design (Multi-agent Placeholder)

## Current Implementation (Phase 2 Scaffold)

- **Agents**: Two symmetric agents (`agent1`, `agent2`) exposed via a lightweight `DictSpace` wrapper that mirrors Gymnasium's mapping semantics without requiring external dependencies.
- **Physics backend**: Defaults to the deterministic `DeterministicCounterAdapter`. Real PyBullet integration remains a future milestone.
- **Seeding**: `reset(seed=...)` uses Python's `random.Random` seeded from either the provided value or a pseudo-random draw. Identical seeds yield identical observations for repeatability.
- **Episode accounting**: Tracks both per-episode step count and cumulative steps across the life of the environment instance.

## Observation Space (per agent)

- **Shape**: 12-dimensional vector of Python `float`s (configurable via `EnvConfig.observation_dim`).
- **Structure**:
  1. Episode step count (float)
  2. Physics adapter step count (float)
  3. Agent index (0 for `agent1`, 1 for `agent2`)
  4. Remaining dimensions filled with deterministic pseudo-random values drawn from a uniform distribution in `[observation_low, observation_high]` for quick prototyping.
- **Bounds**: `[-1000, 1000]` by default; configurable in `EnvConfig`.
- **Status**: Placeholder values — no real kinematics or contact data yet.

## Action Space (per agent)

- **Shape**: 6-dimensional vector (configurable via `EnvConfig.action_dim`).
- **Bounds**: `[-1, 1]` clipped per component by the `ContinuousSpace` helper.
- **Usage**: Actions are currently consumed only for reward shaping (energy penalty) and forwarded to the physics adapter as a fixed number of deterministic steps.

## Reward System (per agent)

- **Components**:
  - `step_reward`: Constant positive reward (default `0.1`) encouraging progress through the episode.
  - `energy_penalty`: Negative value proportional to the L2 norm of the agent's action vector (`-energy_penalty_scale * ||a||`).
- **Total reward**: Sum of the components above; stored in the per-agent `infos[agent]["reward_components"]` mapping for instrumentation.
- **Status**: Minimal scaffolding. Hierarchical BJJ-specific rewards (top control, submissions, etc.) are not implemented yet.

## Termination & Truncation

- **Truncation**: Episodes truncate once `episode_step_count >= max_episode_steps` (default 200). The environment stops issuing further steps until `reset` is called.
- **Termination**: No submission/instability termination conditions implemented yet.

## API Summary

- `reset(seed=None)` → `(observations, infos)` with deterministic seeding and per-agent metadata (`step`, `seed`, `physics_step`).
- `step(actions)` → `(observations, rewards, terminated, truncated, infos)` using the deterministic physics adapter and reward scaffolding described above.
- `close()` → Stops the physics adapter defensively.

## Known Gaps / Next Steps

- Replace placeholder observation values with real physics state (joint poses, velocities, contact summaries).
- Expand the reward system with hierarchical BJJ components and proper termination events (submissions, loss of control, etc.).
- Integrate a PyBullet-backed `PhysicsAdapter` once Phase 3 kicks off, including torque scaling and safety checks.
- Add richer instrumentation (episode metrics, rolling averages) once observations/rewards are physically grounded.

## Usage Example

```python
from bjjsim.env import BJJMultiAgentEnv

env = BJJMultiAgentEnv()
obs, info = env.reset(seed=42)
print(obs["agent1"])  # 12-dim placeholder observation as a list of floats

zero_actions = {agent: [0.0] * env.config.action_dim for agent in env.agents}
obs, rewards, terminated, truncated, infos = env.step(zero_actions)
print(rewards["agent1"], infos["agent1"]["reward_components"])
```
