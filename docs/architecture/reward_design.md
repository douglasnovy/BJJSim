# Reward Design (Hierarchical)

Priorities (highest to lowest)

1. Choke (+30)
2. Joint hyperextension (+20)
3. Staying on top (+10)
4. Control via multiple contacts (+5)
5. Energy penalty per step (-0.1)

Definitions

- Top: Agent base z-position > opponent z-position by δ while in contact for τ steps
- Control: At least N distinct link contacts sustained for τ steps
- Hyperextension: Opponent joint angle beyond [low-ε, high+ε] configured per joint
- Choke: Arm link contacting opponent neck link with force > F for τ steps

Anti-exploit guardrails

- Reward shaping with hysteresis and minimum durations (τ) to avoid chattering
- Penalize repetitive self-collisions or non-progress states (e.g., lying still)
- Clip extreme per-step rewards; log each component separately
- Visual verification: enable GUI overlays that annotate detected events (top/control/choke) frame-by-frame

Curriculum

- Start with top/control; enable submission rewards after stability achieved
- Increase lateral friction gradually from near-zero to small non-zero

Tuning notes

- Track false positives; verify with link-name-based contact filters
- Maintain per-component moving averages; export CSV for offline analysis
