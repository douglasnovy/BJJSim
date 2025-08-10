# Web API: UI Endpoints

Reference for local UI endpoints exposed by the FastAPI app during Phase 1.

See also: `docs/architecture/ui_architecture.md`.

```
POST /api/sim/reset   { seed?: int>=0 }
POST /api/sim/start   { seed?: int>=0 }
POST /api/sim/stop    {}
POST /api/sim/step    { num_steps: int>=1 }
GET  /api/sim/state   -> JSON state
GET  /api/frames/current -> image/png
WS   /ws/events       -> single hello message then close
```
