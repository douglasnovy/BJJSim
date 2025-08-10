# ADR-0003: Local Web UI with Built-In UI Automation

## Context

Manual desktop GUIs are costly to test and maintain. We want UI interactions to be fully testable within this project using Python tooling and to run deterministically in CI.

## Decision

- Implement a local web UI served by the backend (FastAPI) instead of a desktop GUI.
- Adopt Playwright for Python as the primary end-to-end UI testing tool.
- Enforce `data-testid` on all interactive elements; prefer semantic roles and accessible names.
- Provide deterministic test hooks: reset/seed endpoints; headless Chromium as the reference browser.

## Consequences

- Lower ongoing QA cost through stable selectors and deterministic flows.
- Simplifies distribution (local web server; no native GUI dependencies).
- Adds minimal backend scope (HTTP/WS endpoints) and a lightweight templated frontend.

## Status

Accepted.
