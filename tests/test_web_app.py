from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient

from bjjsim.web.app import create_app


def test_reset_and_state_roundtrip() -> None:
    app = create_app()
    client = TestClient(app)

    # Initial state
    res = client.get("/api/sim/state")
    assert res.status_code == 200
    state: dict[str, Any] = res.json()
    assert state["episode_running"] is False
    assert state["step"] == 0

    # Reset with seed
    res = client.post("/api/sim/reset", json={"seed": 123})
    assert res.status_code == 200
    state = res.json()
    assert state["episode_running"] is False
    assert state["last_seed"] == 123
    assert state["step"] == 0

    # Start uses same or provided seed
    res = client.post("/api/sim/start", json={})
    assert res.status_code == 200
    state = res.json()
    assert state["episode_running"] is True

    # Stop ends episode
    res = client.post("/api/sim/stop")
    assert res.status_code == 200
    state = res.json()
    assert state["episode_running"] is False


def test_frame_endpoint_png() -> None:
    app = create_app()
    client = TestClient(app)

    res = client.get("/api/frames/current")
    assert res.status_code == 200
    assert res.headers.get("content-type") == "image/png"
    body = res.content
    # PNG signature
    assert body.startswith(b"\x89PNG\r\n\x1a\n")


def test_ws_events_skeleton() -> None:
    app = create_app()
    client = TestClient(app)

    with client.websocket_connect("/ws/events") as ws:
        data = ws.receive_json()
        assert data.get("type") == "hello"
        assert "episode_running" in data
        assert "step" in data


def test_step_endpoint_advances_when_running() -> None:
    app = create_app()
    client = TestClient(app)

    # Not running -> 409 on step
    res = client.post("/api/sim/step", json={"num_steps": 3})
    assert res.status_code == 409

    # Start then step
    res = client.post("/api/sim/start", json={})
    assert res.status_code == 200
    res = client.post("/api/sim/step", json={"num_steps": 5})
    assert res.status_code == 200
    state: dict[str, Any] = res.json()
    assert state["episode_running"] is True
    assert state["step"] == 5

    # Another step
    res = client.post("/api/sim/step", json={"num_steps": 2})
    state = res.json()
    assert state["step"] == 7


def test_health_and_ready_endpoints() -> None:
    app = create_app()
    client = TestClient(app)

    res = client.get("/healthz")
    assert res.status_code == 200
    payload: dict[str, Any] = res.json()
    assert payload["status"] == "ok"
    assert isinstance(payload["version"], str)
    assert len(payload["version"]) > 0

    res = client.get("/readyz")
    assert res.status_code == 200
    payload2: dict[str, Any] = res.json()
    assert "ready" in payload2
