from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from time import monotonic
from typing import Final

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from starlette.websockets import WebSocket


class ResetRequest(BaseModel):
    seed: int | None = Field(default=None, ge=0)


class StartRequest(BaseModel):
    seed: int | None = Field(default=None, ge=0)


class StepRequest(BaseModel):
    """Request body for stepping the simulation.

    Allows stepping a positive number of ticks in one call to support
    deterministic, controllable progression during prototyping.
    """

    num_steps: int = Field(default=1, ge=1, le=1000)


class StateResponse(BaseModel):
    episode_running: bool = False
    last_seed: int | None = None
    step: int = 0
    metrics: dict[str, float] = Field(default_factory=dict)


class HealthResponse(BaseModel):
    status: str
    version: str


class ReadinessResponse(BaseModel):
    ready: bool


class MetricsResponse(BaseModel):
    episodes_started: float
    total_steps: float
    steps_per_second: float


@dataclass
class _ServerState:
    episode_running: bool = False
    last_seed: int | None = None
    step: int = 0
    # Metrics tracking (internal counters/time). Exposed via StateResponse.metrics
    total_steps_count: int = 0
    episodes_started_count: int = 0
    last_step_monotonic: float | None = None
    steps_ema_sps: float = 0.0


TEMPLATES_DIR: Final[Path] = Path(__file__).parent / "templates"


class AppConfig(BaseModel):
    """Mutable runtime configuration exposed to the UI.

    This is intentionally small and safe to change at runtime.
    """

    preview_hz: int = Field(default=2, ge=1, le=30, description="Frame preview frequency (Hz)")
    max_steps_per_episode: int = Field(default=1000, ge=1, le=100_000)


class AppConfigUpdate(BaseModel):
    preview_hz: int | None = Field(default=None, ge=1, le=30)
    max_steps_per_episode: int | None = Field(default=None, ge=1, le=100_000)


def create_app() -> FastAPI:
    # Import locally to avoid any possibility of import cycles during app startup.
    from bjjsim import __version__ as pkg_version

    app = FastAPI(title="BJJSim UI", version=pkg_version)

    templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
    state = _ServerState()
    config = AppConfig()

    def index(request: Request) -> HTMLResponse:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "episode_running": state.episode_running,
                "last_seed": state.last_seed,
                "step": state.step,
            },
        )

    def _build_metrics() -> dict[str, float]:
        return {
            "episodes_started": float(state.episodes_started_count),
            "total_steps": float(state.total_steps_count),
            "steps_per_second": float(state.steps_ema_sps),
        }

    def _to_state_response() -> StateResponse:
        return StateResponse(
            episode_running=state.episode_running,
            last_seed=state.last_seed,
            step=state.step,
            metrics=_build_metrics(),
        )

    def _update_steps_per_second(num_steps: int) -> None:
        now = monotonic()
        if state.last_step_monotonic is None:
            state.last_step_monotonic = now
            return
        dt = now - state.last_step_monotonic
        # Guard against zero/negative time deltas due to clock peculiarities.
        if dt <= 1e-9:
            state.last_step_monotonic = now
            return
        instantaneous_sps = float(num_steps) / dt
        # Exponential moving average for stability
        alpha = 0.5
        state.steps_ema_sps = (1 - alpha) * state.steps_ema_sps + alpha * instantaneous_sps
        state.last_step_monotonic = now

    def reset(req: ResetRequest) -> StateResponse:
        state.episode_running = False
        state.step = 0
        if req.seed is not None:
            state.last_seed = req.seed
        # Reset per-episode timing; leave global counters intact
        state.last_step_monotonic = None
        state.steps_ema_sps = 0.0
        return _to_state_response()

    def start(req: StartRequest) -> StateResponse:
        if state.episode_running:
            raise HTTPException(status_code=409, detail="episode already running")
        if req.seed is not None:
            state.last_seed = req.seed
        state.episode_running = True
        state.step = 0
        state.episodes_started_count += 1
        state.last_step_monotonic = None
        state.steps_ema_sps = 0.0
        return _to_state_response()

    def stop() -> StateResponse:
        state.episode_running = False
        return _to_state_response()

    def get_state() -> StateResponse:
        return _to_state_response()

    def get_metrics() -> MetricsResponse:
        m = _build_metrics()
        return MetricsResponse(**m)

    def do_step(req: StepRequest) -> StateResponse:
        if not state.episode_running:
            raise HTTPException(status_code=409, detail="episode not running")
        # For now, a deterministic counter; physics integration will replace this.
        state.step += req.num_steps
        state.total_steps_count += req.num_steps
        _update_steps_per_second(req.num_steps)
        if state.step >= config.max_steps_per_episode:
            # Auto-stop when reaching max steps per episode
            state.episode_running = False
        return _to_state_response()

    # Placeholder frame endpoint: returns 204 for now.
    def get_frame() -> Response:
        """
        Return a tiny placeholder PNG to enable UI smoke tests.

        The image is a 1x1 opaque black PNG. Replaced with real frames in Phase 1.
        """
        png_bytes = (
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde"
            b"\x00\x00\x00\x0cIDAT\x08\xd7c\xf8\xff\xff?\x00\x05\xfe\x02\xfeA\x8d\x1d\x89\x00\x00\x00\x00IEND\xaeB`\x82"
        )
        return Response(content=png_bytes, media_type="image/png")

    async def ws_events(ws: WebSocket) -> None:
        """Minimal WebSocket endpoint for future live telemetry.

        For now, accepts the connection and sends a single hello event.
        """
        await ws.accept()
        await ws.send_json(
            {
                "type": "hello",
                "episode_running": state.episode_running,
                "step": state.step,
            }
        )
        await ws.close()

    def healthz() -> HealthResponse:
        # Import locally to avoid any possibility of import cycles during app startup.
        from bjjsim import __version__ as pkg_version

        return HealthResponse(status="ok", version=pkg_version)

    def readyz() -> ReadinessResponse:
        # Basic readiness: templates directory exists and is accessible.
        is_ready = TEMPLATES_DIR.exists()
        return ReadinessResponse(ready=is_ready)

    # Config API
    def get_config() -> AppConfig:
        return config

    def update_config(req: AppConfigUpdate) -> AppConfig:
        if req.preview_hz is not None:
            config.preview_hz = req.preview_hz
        if req.max_steps_per_episode is not None:
            config.max_steps_per_episode = req.max_steps_per_episode
        return config

    # Config page
    def config_page(request: Request) -> HTMLResponse:
        return templates.TemplateResponse(
            "config.html",
            {
                "request": request,
                "config": config.model_dump(),
            },
        )

    # Mount static if needed later
    app.mount("/static", StaticFiles(directory=str(TEMPLATES_DIR)), name="static")

    # Register routes explicitly to keep mypy happy with decorators
    app.add_api_route("/", index, methods=["GET"], response_class=HTMLResponse)
    app.add_api_route("/api/sim/reset", reset, methods=["POST"], response_model=StateResponse)
    app.add_api_route("/api/sim/start", start, methods=["POST"], response_model=StateResponse)
    app.add_api_route("/api/sim/stop", stop, methods=["POST"], response_model=StateResponse)
    app.add_api_route("/api/sim/step", do_step, methods=["POST"], response_model=StateResponse)
    app.add_api_route("/api/sim/state", get_state, methods=["GET"], response_model=StateResponse)
    app.add_api_route("/api/metrics", get_metrics, methods=["GET"], response_model=MetricsResponse)
    app.add_api_route("/api/frames/current", get_frame, methods=["GET"], response_class=Response)
    app.add_api_websocket_route("/ws/events", ws_events)
    app.add_api_route("/healthz", healthz, methods=["GET"], response_model=HealthResponse)
    app.add_api_route("/readyz", readyz, methods=["GET"], response_model=ReadinessResponse)
    app.add_api_route("/api/config", get_config, methods=["GET"], response_model=AppConfig)
    app.add_api_route("/api/config", update_config, methods=["POST"], response_model=AppConfig)
    app.add_api_route("/config", config_page, methods=["GET"], response_class=HTMLResponse)

    return app
