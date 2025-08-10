# Non-functional Requirements

Quality attributes

- Reproducibility: Fixed seeds, deterministic stepping, pinned toolchain
- Observability: Reward component logging, episode summaries, optional video capture, overlays for contacts and reward events
- Performance: Run on a single machine CPU; optional GPU for RL; step rate ≥ 240 Hz in headless mode; bound observation cost via fixed-K contact summary and short decay window
- Portability: Windows-first dev; Unix-friendly scripts
- Maintainability: Typed Python 3.12, linted/formatted, modular design
- Testability (UI): Local web UI is fully automatable; stable selectors via `data-testid`; deterministic hooks (reset/seed); headless execution in CI
- Accessibility (UI): Use semantic HTML and ARIA roles; controls have accessible names/labels
- Browser/CI: Chromium is the reference browser; tests run with Playwright for Python

Tooling

- Physics: PyBullet (default). Keep an adapter layer to allow MuJoCo later if desired.
- RL: Ray RLlib (torch). Configs captured in versioned files.
- Env: Gymnasium multi-agent compatibility wrapper as needed.
- Web: FastAPI backend; server-rendered templates with minimal JS (HTMX/Alpine.js). Playwright for Python for E2E.

Security and Safety

- No network access required; local-only by default
- Clamp actions, validate config, and guard against extreme dynamics
