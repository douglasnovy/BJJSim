from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from starlette.templating import Jinja2Templates


class ResetRequest(BaseModel):
    seed: int | None = Field(default=None, ge=0)


class StartRequest(BaseModel):
    seed: int | None = Field(default=None, ge=0)


class StateResponse(BaseModel):
    episode_running: bool = False
    last_seed: int | None = None
    step: int = 0
    metrics: dict[str, float] = Field(default_factory=dict)


@dataclass
class _ServerState:
    episode_running: bool = False
    last_seed: int | None = None
    step: int = 0


TEMPLATES_DIR: Final[Path] = Path(__file__).parent / "templates"


def create_app() -> FastAPI:
    app = FastAPI(title="BJJSim UI", version="0.0.1")

    templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
    state = _ServerState()

    @app.get("/", response_class=HTMLResponse)  # type: ignore[misc]
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

    @app.post("/api/sim/reset")  # type: ignore[misc]
    def reset(req: ResetRequest) -> JSONResponse:
        state.episode_running = False
        state.step = 0
        if req.seed is not None:
            state.last_seed = req.seed
        return JSONResponse(StateResponse.model_validate(state.__dict__).model_dump())

    @app.post("/api/sim/start")  # type: ignore[misc]
    def start(req: StartRequest) -> JSONResponse:
        if state.episode_running:
            raise HTTPException(status_code=409, detail="episode already running")
        if req.seed is not None:
            state.last_seed = req.seed
        state.episode_running = True
        state.step = 0
        return JSONResponse(StateResponse.model_validate(state.__dict__).model_dump())

    @app.post("/api/sim/stop")  # type: ignore[misc]
    def stop() -> JSONResponse:
        state.episode_running = False
        return JSONResponse(StateResponse.model_validate(state.__dict__).model_dump())

    @app.get("/api/sim/state")  # type: ignore[misc]
    def get_state() -> JSONResponse:
        return JSONResponse(StateResponse.model_validate(state.__dict__).model_dump())

    # Placeholder frame endpoint: returns 204 for now.
    @app.get("/api/frames/current")  # type: ignore[misc]
    def get_frame() -> JSONResponse:
        return JSONResponse({"detail": "no frame available"}, status_code=204)

    # Mount static if needed later
    app.mount("/static", StaticFiles(directory=str(TEMPLATES_DIR)), name="static")

    return app
