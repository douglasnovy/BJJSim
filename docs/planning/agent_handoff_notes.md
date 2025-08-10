# Notes for the next AI Agent

- Branch: `feat/docs-config-endpoints-tests`
- Changes: API handlers return Pydantic models; routes specify `response_model`.
- Tests: Added readiness assertion; ensured step auto-stop covered.
- Docs: Updated Web API; added ADR-0005 and lessons learned.

Suggested next tasks

- Add minimal `/api/metrics` with typed payload and small UI widget on `index.html`.
- Introduce a simple in-memory event log and expand WS to stream periodic state updates.
- Start stubbing physics adapter interface with types.
