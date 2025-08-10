# Notes for the next AI Agent

- Branch: `feat/docs-config-endpoints-tests`
- Changes: API handlers return Pydantic models; routes specify `response_model`.
- Tests: Added readiness assertion; ensured step auto-stop covered.
- Docs: Updated Web API; added ADR-0005 and lessons learned.

Updates in this iteration

- App version now comes from `bjjsim.__version__`; current version: `0.0.2`.
- `GET /api/sim/state` includes a minimal `metrics` block: `{ episodes_started, total_steps, steps_per_second }` (EMA).

Suggested next tasks

- Promote metrics to a dedicated `/api/metrics` endpoint and render a small metrics widget on `index.html`.
- Introduce a simple in-memory event log and expand WS to stream periodic state updates.
- Start stubbing a physics adapter interface with types and unit tests.

Completed in this iteration

- Added `GET /api/metrics` returning `{ episodes_started, total_steps, steps_per_second }`.
- Updated `index.html` to poll and display server metrics.
- Added unit test `test_metrics_endpoint` and updated Web API docs.
