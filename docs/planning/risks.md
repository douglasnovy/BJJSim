# Risks and Mitigations

- Physics instability or reward hacking
  - Mitigate with fixed dt, action clipping, hysteresis, curriculum
- Non-emergence of meaningful behaviors
  - Iterate reward shaping, curriculum, contact filters; consider MuJoCo if needed
- Performance on CPU-only machines
  - Keep models small; headless mode; reduce workers; batch appropriately
- Reproducibility drift
  - Pin seeds, versions, and configs; log all knobs
