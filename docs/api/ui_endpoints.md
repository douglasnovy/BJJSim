# Web API: UI Endpoints

Reference for local UI endpoints exposed by the FastAPI app during Phase 1.

See also: `docs/architecture/ui_architecture.md`.

```text
POST /api/sim/reset   { seed?: int>=0 }
POST /api/sim/start   { seed?: int>=0 }
POST /api/sim/stop    {}
POST /api/sim/step    { num_steps: int>=1 } ; auto-stops when >= max_steps_per_episode
GET  /api/sim/state   -> {
  episode_running: bool,
  last_seed: int|null,
  step: int,
  metrics: { episodes_started: float, total_steps: float, steps_per_second: float }
}
GET  /api/metrics     -> { episodes_started: float, total_steps: float, steps_per_second: float }
GET  /api/frames/current -> image/png
  - Testing hook: pixel (0,0) encodes the current step in its red channel as `step % 256`; a text overlay "step: N" is also drawn.
WS   /ws/events       -> streams: initial { type: "hello", ... } followed by periodic { type: "state", ... }
GET  /healthz         -> { status: "ok", version: string }
GET  /readyz          -> { ready: boolean }
GET  /api/config      -> { preview_hz: int, max_steps_per_episode: int }
POST /api/config      { preview_hz?: int, max_steps_per_episode?: int } -> updated config
GET  /api/events      -> { events: [ { type: string, ts: float, payload: object } ] }
```
