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


def test_config_get_and_update() -> None:
    app = create_app()
    client = TestClient(app)

    # Default config
    res = client.get("/api/config")
    assert res.status_code == 200
    cfg: dict[str, Any] = res.json()
    assert isinstance(cfg["preview_hz"], int)
    assert cfg["preview_hz"] >= 1
    assert isinstance(cfg["max_steps_per_episode"], int)

    # Update config
    res = client.post("/api/config", json={"preview_hz": 5, "max_steps_per_episode": 3})
    assert res.status_code == 200
    cfg2: dict[str, Any] = res.json()
    assert cfg2["preview_hz"] == 5
    assert cfg2["max_steps_per_episode"] == 3

    # Respect max_steps_per_episode by auto-stopping
    res = client.post("/api/sim/start", json={})
    assert res.status_code == 200
    res = client.post("/api/sim/step", json={"num_steps": 2})
    assert res.status_code == 200
    state: dict[str, Any] = res.json()
    assert state["episode_running"] is True
    assert state["step"] == 2
    # Next step should stop at or beyond limit
    res = client.post("/api/sim/step", json={"num_steps": 1})
    state2: dict[str, Any] = res.json()
    assert state2["step"] >= 3
    assert state2["episode_running"] is False


def test_readyz_true_when_templates_exist() -> None:
    app = create_app()
    client = TestClient(app)

    res = client.get("/readyz")
    assert res.status_code == 200
    payload: dict[str, Any] = res.json()
    # Should be true because templates dir exists in repo
    assert payload["ready"] is True
