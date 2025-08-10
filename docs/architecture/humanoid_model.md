# Humanoid Model Selection

Choice

- Use the DeepMind Control Suite Humanoid MJCF (PyBullet-compatible port) checked into:
  - `src/bjsim/assets/humanoids/dm_control_humanoid/humanoid.xml`
- The loader will accept a model registry key (e.g., `dm_control_humanoid`) to enable future swaps without code changes.

Rationale

- Broad research adoption, stable kinematics, well-defined joint limits.
- Avoids custom meshes/limits; accelerates experimentation and validation.

Swapability

- Model selection is abstracted by a typed registry mapping keys → asset paths and expected link/joint schemas.
- On load, we validate required links/joints exist; code consumes stable logical names (e.g., `neck`, `torso`, `upper_arm_l`).

Requirements

- Document canonical link names and IDs for torso, head/neck, upper/lower arms (L/R), upper/lower legs (L/R), hands/feet if present.
- Capture joint effort limits and torque scaling per joint for safe torque control.
- Provide a typed mapping in code that resolves names to IDs at load and validates against the model.

Next Steps

- Import model and verify in PyBullet (visual and direct modes).
- Export link/joint mapping and add to documentation.
- Add basic tests asserting required links and expected counts.
