# Milestones and Exit Criteria

- M1: UI-first physics prototype renders two humanoids; contacts accessible; simple GUI overlays for contacts; local web UI shows frames and can reset/seed/start/stop (Phase 1 exit)
- M2: Env step/reset returns typed observations; reward components logged; event annotations visible in GUI (Phase 2 exit)
  - Progress: Deterministic placeholder multi-agent environment scaffold implemented with dependency-free spaces; needs physics-derived observations, hierarchical rewards, and GUI surfacing of reward events.
- M3: PPO self-play trains for 100 iterations; no NaNs; rewards monotonic-ish (Phase 3 exit)
- M4: In evaluation, agent maintains top position (Δz > threshold) for ≥5 consecutive seconds in ≥50% of episodes; overlays confirm events; thresholds validated (Phase 4 exit)

- M2.5: Local web UI reachable at `http://127.0.0.1:<port>`; can reset/seed/start an episode; Playwright smoke test passes in CI
