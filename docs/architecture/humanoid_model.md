# Humanoid Model Selection

Choice

- Use a well-supported research humanoid model from MJCF/URDF, specifically the DeepMind Control Suite Humanoid MJCF (or a faithful URDF/MJCF port compatible with PyBullet).

Rationale

- Broad adoption in research, stable kinematics, and well-defined joint limits.
- Avoids building custom meshes/limits; accelerates experimentation.

Requirements

- Document canonical link names and IDs for torso, head/neck, upper/lower arms (L/R), upper/lower legs (L/R), hands/feet if present.
- Capture joint effort limits and torque scaling per joint for safe torque control.
- Provide a mapping table in code (typed) that resolves names to IDs at load time and validates against the model.

Next Steps

- Import model and verify in PyBullet (visual and in direct mode).
- Export link/joint mapping and add to documentation.
- Add basic tests that assert presence of required links and expected counts.
