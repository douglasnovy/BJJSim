# Environment Design (Gymnasium, Multi-agent) ✅ IMPLEMENTED

## API Implementation

- **Two agents**: `agent1`, `agent2` (Dict-based multi-agent environment)
- **reset(seed) -> (obs, info)** where `obs` is Dict[str, np.ndarray] per agent
- **step(actions) -> (obs, rewards, terminated, truncated, infos)** per Gymnasium v0.29
- **Deterministic seeding**: Environment supports seeded resets for reproducible testing

## Observation Space (per agent) - 90 dimensions

**ACTUAL IMPLEMENTATION:**
- **Own joint positions**: 12 dimensions (joint angles in radians, range [-π, π])
- **Own joint velocities**: 12 dimensions (angular velocities, range [-50, 50])
- **Opponent joint positions**: 12 dimensions (joint angles in radians, range [-π, π])  
- **Opponent joint velocities**: 12 dimensions (angular velocities, range [-50, 50])
- **Own base z-position**: 1 dimension (vertical position, range [-10, 10])
- **Opponent base z-position**: 1 dimension (vertical position, range [-10, 10])
- **Contact summary vector**: 40 dimensions (8 contacts × 5 features each)
  - Per contact: [link_pair_id, normal_force, rel_pos_x, rel_pos_y, rel_pos_z]
  - Range: [0, 1000] for forces, [-1000, 1000] for positions
- **Total**: 12 + 12 + 12 + 12 + 1 + 1 + 40 = **90 dimensions per agent**

⚠️ **PLACEHOLDER STATUS**: Joint efforts/torques are NOT included in observations (contrary to some design docs). Contact summary uses exponential moving average over recent steps.

## Action Space (per agent) - 12 dimensions

- **Continuous torque control**: 12 joints per agent (Box space [-1, 1])
- **Clipping**: Actions automatically clipped to [-1, 1] range
- **Physics scaling**: Torques scaled by `max_torque` config (default: ±100.0 Nm)
- **Space type**: `gymnasium.spaces.Dict` with per-agent `Box(-1, 1, (12,), float32)`

## Hierarchical Reward System

**IMPLEMENTED VALUES (from EnvConfig):**
- **Choke submission**: +30.0 (highest priority, sustained contact force > 50.0)
- **Joint hyperextension**: +20.0 (joint limits exceeded with tolerance 0.1 rad)
- **Top control**: +10.0 (z-position advantage > 0.1 for 5+ steps)
- **Contact control**: +5.0 (3+ active contacts sustained for 5+ steps) 
- **Energy penalty**: -0.1 per action magnitude (encourages efficiency)
- **Reward tracking**: Full component breakdown logged in `reward_history` and step `infos`

⚠️ **PLACEHOLDER STATUS**: 
- Choke detection uses heuristic contact force thresholds (line 398-414)
- Hyperextension detection is randomized (0.1% chance, line 419-423)
- Contact forces are simulated random data (line 302-311)

## Termination Conditions

- **Submission achieved**: Episode terminates when choke OR hyperextension sustained
  - Choke: Force > 50.0 for 10+ consecutive steps
  - Hyperextension: Random 0.1% chance per step (placeholder implementation)
- **Episode timeout**: 1000 steps maximum (`max_episode_steps`)
- **Physics instability**: Currently disabled (placeholder for future PyBullet integration)
- **Early termination**: Winning agent gets terminated=True, losing agent also terminated

⚠️ **PLACEHOLDER STATUS**: Hyperextension termination is purely random, not based on actual joint physics.

## Technical Implementation

**FULLY IMPLEMENTED:**
- **Type safety**: Full mypy compliance with proper type annotations
- **Error handling**: Clear ImportError for missing numpy/gymnasium dependencies  
- **Multi-agent API**: Proper Dict-based spaces and return values
- **Reward computation**: Complete hierarchical system with state tracking
- **Configuration**: Comprehensive EnvConfig with sensible defaults
- **Deterministic seeding**: Uses self.np_random for all random generation ensuring reproducible behavior
- **Action scaling**: Actions scaled from [-1, 1] to [-max_torque, max_torque] as documented
- **Observation bounds**: Contact positions properly bounded to [-1000, 1000] range

**PLACEHOLDER/STUBBED:**
- **Physics integration**: Uses DeterministicCounterAdapter (dummy physics)
- **Observations**: Random dummy values instead of actual physics state
- **Contact detection**: Simulated random contact forces and positions
- **Choke detection**: Heuristic based on contact force thresholds
- **Hyperextension**: Random chance instead of joint limit physics

## Development Status

**Phase 2 - Environment Framework** ✅ COMPLETE
- Multi-agent Gymnasium API implemented and tested
- Observation/action spaces defined and validated
- Reward system architecture implemented
- Configuration system working

**Phase 3 - Physics Integration** 🔄 NEXT
- Replace DeterministicCounterAdapter with PyBullet
- Implement real contact detection and force calculation  
- Add proper joint limit enforcement and hyperextension detection
- Replace dummy observations with actual physics state

## Usage Example

```python
from bjjsim.env import BJJMultiAgentEnv
import numpy as np

# Create environment with default config
env = BJJMultiAgentEnv()

# Reset with seed for determinism
obs, info = env.reset(seed=42)
print(f"Observation shapes: {env.observation_space}")
# Output: Dict('agent1': Box(90,), 'agent2': Box(90,))

# Sample actions and step
actions = {agent: np.random.uniform(-1, 1, 12) for agent in env.agents}
obs, rewards, terminated, truncated, infos = env.step(actions)
print(f"Step rewards: {rewards}")
print(f"Reward breakdown: {infos['agent1']['reward_components']}")

# Environment info
print(f"Episode step: {env.episode_step_count}")
print(f"Agents: {env.agents}")  # ['agent1', 'agent2']
```

**Verified Working:** ✅ Import paths, API calls, observation dimensions, action spaces all tested and functional.