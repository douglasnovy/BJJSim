# Open Questions / TBD

- Humanoid model: Which URDF and joint mapping will we standardize on? Link IDs for neck/arms?
- Reward thresholds: Exact z-height delta for "top", number of contacts for "control", force thresholds for chokes
- Hyperextension detection: Joint-specific safe limits vs. generic margins; per-joint weighting
- Termination: Timeout length, tap-out criteria, stability checks to avoid false positives
- Observation: Contact encoding limit and decay window; include opponent base orientation?
- Action space: Torque vs. position control; action scaling and clipping
- Curriculum: When to introduce friction or constraints; randomization ranges for initial poses
- Self-play strategy: Exact PPO settings; opponent sampling (latest vs. past checkpoints)
- Determinism: What elements remain nondeterministic and how do we bound them?
- Licensing: Project license selection (MIT/BSD/Apache-2.0?)
