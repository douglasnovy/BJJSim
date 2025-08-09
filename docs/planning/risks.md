# Risks and Mitigations

- Physics instability or reward hacking
  - Mitigate with fixed dt, action clipping, hysteresis, curriculum
  - Add early visualization overlays and detailed logging of reward events
- Non-emergence of meaningful behaviors
  - Iterate reward shaping, curriculum, contact filters; consider MuJoCo if needed
- Performance on CPU-only machines
  - Keep models small; headless mode; reduce workers; batch appropriately
  - Bound observation cost with fixed K contact summary and short decay window
- Reproducibility drift
  - Pin seeds, versions, and configs; log all knobs
