# ADR-0006: Physics Adapter Interface

Status: Accepted

## Context

We need a minimal, typed interface to decouple the web UI and future training code from the underlying physics engine. Early phases rely on deterministic stepping to validate UI flow and test scaffolding while we design the PyBullet integration.

## Decision

- Introduce `PhysicsAdapter` as a `Protocol` with `reset`, `start`, `stop`, `step`, and read-only properties `step_count` and `last_seed`.
- Provide `DeterministicCounterAdapter` for current scaffolding and tests.
- Wire the adapter into the FastAPI app so that stepping and seeding flow through the adapter.

## Consequences

- The UI and tests no longer depend on local state increments only; they interact via an adapter, easing replacement with a real physics backend.
- The adapter is small enough to implement quickly for PyBullet while preserving type safety.

## Alternatives Considered

- Keep counters in the web app only: simple but makes replacement harder and mixes concerns.
- Define a larger interface now: premature; we prefer incremental evolution with tight tests.
