# ADR-0004: UI-First Execution, Multi-Agent Wrapper, Config System, Storage Layout, RLlib Pin

Context

- We want to validate project viability quickly by seeing humanoids load and move visually before integrating RL.
- Several foundational choices were left to execution: multi-agent API wrapper, config mechanism, storage layout, RLlib version pin.

Decision

1) UI-first Phase 1

- Prioritize a working local web UI that can reset/seed/start an episode and show frames with overlays.
- Physics adapter + simple scripted motions for shaking out rendering/contacts before RL.

1) Multi-agent API wrapper

- Use a thin Gymnasium-compatible multi-agent wrapper now (as planned). Keep boundaries so PettingZoo can be added later if beneficial.
- Rationale: Minimal surface area and fewer moving parts while we validate physics and the UI. PettingZoo adds value in ecosystem compatibility but is optional at this stage.

1) Configuration system

- Use Pydantic v2 typed config as the source of truth, with layered overrides: defaults → YAML file(s) → environment variables.
- Rationale: Strong typing and validation from Pydantic; YAML is ergonomic for experiments; env vars make CI/runtime overrides easy.

1) Storage layout

- Use `runs/<YYYYmmdd-HHMMSS_or_label>/` as the root per run.
  - `checkpoints/` (RLlib checkpoints)
  - `metrics/` (CSV/Parquet summaries, JSON logs)
  - `frames/` (periodic JPEG/PNG snapshots)
  - `videos/` (optional MP4)
  - `config.yaml` (frozen effective configuration)
- Rationale: Predictable structure that scales across experiments and simplifies CI artifact collection.

1) RLlib/Gymnasium versions

- Initial pins: `ray[default,rllib]==2.9.3`, `gymnasium==0.29.1`, `torch==2.4.*`.
- Rationale: Stable Ray 2.x with Gymnasium 0.29 multi-agent compatibility and current PyTorch. We will adjust if compatibility issues arise during implementation.

Consequences

- Faster feedback via UI-first flow reduces risk before RL investment.
- Gymnasium wrapper keeps implementation simple and swappable.
- Typed configs ensure safety and clarity; YAML/env layers enable flexible execution.
- Standardized run artifacts ease analysis and automation.
- Version pins improve reproducibility and reduce dependency drift.

Status

- Accepted.
