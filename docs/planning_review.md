# BJJSim Project Plan Review

**Date:** 2025-08-09
**Reviewer:** Jules, AI Agent

## 1. Overall Assessment

The BJJSim project is in an excellent state for the planning phase. The documentation-first approach is commendable and provides a strong foundation for development. The project structure, goals, and initial technical choices (PyBullet, Gymnasium, RLlib) are sound and well-aligned with the research objectives.

This review highlights critical considerations and decision points that should be addressed before or during the initial development phases to mitigate risks and ensure the project's success.

## 2. Critical Issues & Areas for Attention

These are areas that I recommend focusing on, as they pose the most significant risks or have the largest impact on the project's outcome.

### 2.1. The "Zero Friction" Assumption

The decision to start with zero friction is a significant one.

* **Impact:** While this simplifies the physics model and may help avoid certain local optima in the learning process, it fundamentally changes the nature of the physical interaction. Brazilian Jiu-Jitsu is heavily reliant on friction (e.g., grips, positional control).
* **Attention Needed:** The emergent behaviors in a zero-friction environment may not resemble BJJ. The project should have a clear hypothesis about what is expected to emerge from this simplified model and a clear plan for how and when to introduce friction. This is the most critical physics-related assumption and should be validated early.

### 2.2. Humanoid Model (URDF) Selection

The choice of the humanoid model (URDF) is a foundational decision that currently blocks development.

* **Impact:** The URDF defines the agent's body, its joints, and their limits. It directly impacts the observation and action spaces, the physics simulation, and the definitions of rewards (e.g., identifying "neck" or "arm" links).
* **Attention Needed:** This decision must be made at the very beginning of **Phase 1**. I recommend selecting a standard, well-tested humanoid URDF and explicitly mapping its link names/IDs to the concepts in the glossary (e.g., "neck link", "torso").

### 2.3. Observation Space Complexity

The "contact summary vector" is a clever way to handle a variable number of contacts, but its implementation is critical.

* **Impact:** A high-dimensional, sparse, or noisy observation space can dramatically slow down or prevent learning. The size (`K`), encoding, and temporal decay of this vector are crucial hyperparameters.
* **Attention Needed:** It may be prudent to start with a very simple contact representation (e.g., just a boolean "is_contacting" flag and the number of contact points) before moving to a more complex summary vector. This allows for incremental complexity and easier debugging.

### 2.4. Reward Hacking Potential

The hierarchical reward system is well-designed, but the risk of "reward hacking" (agents finding unintended ways to maximize rewards) is ever-present and the primary challenge in this domain.

* **Impact:** An agent might learn to, for example, rapidly "tap" the opponent's neck for the choke reward without establishing a legitimate hold, or oscillate its Z-axis position to farm the "top control" reward.
* **Attention Needed:** The planned anti-exploit guardrails (hysteresis, minimum durations) are essential. I recommend investing heavily in visualization and detailed logging from day one to continuously monitor for and diagnose these behaviors.

## 3. Decisions to be Made

The `open_questions.md` document is excellent. This section formalizes those questions and adds others based on my review, structured by priority. I recommend recording the answers in a new ADR file.

### 3.1. Immediate Project-Level Decisions

* **Project License:** What open-source license will the project use (e.g., MIT, BSD, Apache 2.0)? This should be decided before any code is written.
* **Definition of Success:** What specific, measurable behaviors will define success for M4 ("Evidence of top/control behavior")? For example: "Agent A, when facing the latest policy, achieves and maintains top position for at least 5 consecutive seconds in over 50% of evaluation episodes."

### 3.2. Phase 1 (Physics) Decisions

* **Humanoid URDF:**
  * Which specific URDF file will be the standard?
  * What are the canonical names/IDs for the critical links (e.g., torso, head/neck, left/right upper/lower arms)?
* **Action Space Control:**
  * Will the initial implementation use **Torque Control** or **Position Control**? This is a critical decision affecting physics stability and learning.
* **Friction Model:**
  * Confirm the "zero friction" approach for the initial prototype.
  * What is the specific trigger or milestone that will prompt the introduction of friction in a later phase?

### 3.3. Phase 2 (Environment & Rewards) Decisions

* **Observation Space Parameters:**
  * What is the initial value for `K` (the contact summary limit)?
  * How will contact force/position be encoded?
  * Will the opponent's full base orientation (not just Z-position) be included in the observation?
* **Reward & Termination Thresholds:**
  * The values in `configuration.md` are a great start. Please confirm these initial defaults for all reward and termination parameters (`z-height delta`, `min_contacts`, `force_thresholds`, `max_steps_per_episode`, etc.).
* **Hyperextension Logic:**
  * Will the system use a generic safety margin for all joints or define specific, safe operational ranges for each joint individually?

### 3.4. Phase 3 (Self-Play) Decisions

* **PPO Hyperparameters:**
  * Confirm the initial set of PPO hyperparameters from `configuration.md`.
* **Opponent Sampling:**
  * For the baseline, will agents train strictly against the most recent version of the opponent policy, or will a form of historical checkpoint sampling be used from the start?

## 4. Decisions Applied (2025-08-09)

* Friction: Adopt small non-zero lateral friction by default (rolling/spinning 0.0); configurable and eligible for annealing.
* Humanoid model: Use a standard research humanoid (DM Control Humanoid MJCF or compatible port) and document link/joint mapping.
* Action control: Torque control by default; normalized actions scaled/clipped per joint.
* Observation contacts: Fixed K=8 top-k contacts with optional EMA over D=3 steps.
* Visualization/logging: Treat as first-class; GUI overlays showing contacts and reward events.
* Licensing: PolyForm Noncommercial 1.0.0.
