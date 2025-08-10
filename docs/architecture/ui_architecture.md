# Web UI Architecture (Phase 1 Priority)

## Goals

- Provide a simple local web control panel to drive evaluation episodes, inspect metrics, and capture snapshots.
- Keep the stack lightweight, Python-first, and highly testable.

## Stack

- Backend: FastAPI (typed Pydantic schemas), hosting REST and WebSocket endpoints.
- Frontend: Server-rendered pages (Jinja2) with minimal HTMX/Alpine.js for interactivity. No heavy SPA required initially.
- Transport: WebSocket for live events/metrics; REST for control operations.

## Public API (initial)

- `POST /api/sim/reset` → reset environment with optional `{seed:int}`.
- `POST /api/sim/start` → start a seeded evaluation episode.
- `POST /api/sim/stop` → stop current episode.
- `GET  /api/sim/state` → JSON snapshot of high-level state/metrics.
- `GET  /api/frames/current` → latest rendered frame (JPEG/PNG) with overlays when enabled.
- `WS   /ws/events` → stream of telemetry/events (reward components, contact counts, termination reasons).

All request/response bodies must be defined as typed models and versioned.

## Phase 1 Implementation Notes

- UI-first: wire the UI to the physics adapter with simple scripted motions before RL is integrated.
- Determinism hooks: explicit `{seed:int}` and `reset` ensure reproducible e2e tests.
- Frame cadence: 2–5 Hz preview to bound CPU; on-demand still image endpoint for tests.

## Pages (initial)

- Dashboard: start/stop/reset, seed entry, live metrics, and latest frame preview.
- Config: view current config; limited safe edits behind a form with server-side validation.

## Testability Hooks

- Every interactive control has a `data-testid` attribute (e.g., `data-testid="btn-start"`).
- Server offers `reset`/`seed` endpoints for deterministic e2e.
- Stable routes and IDs; avoid dynamic, index-based IDs in HTML.

## Performance/Constraints

- Optimized for local use; Chromium is the reference browser for e2e.
- Frame preview is periodic (e.g., 2–5 Hz) to keep bandwidth/CPU low; real-time streaming is not required initially.
