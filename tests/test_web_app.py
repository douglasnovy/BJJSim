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
    assert isinstance(state.get("metrics"), dict)

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

    # Verify step encoding in top-left pixel red channel after stepping
    assert client.post("/api/sim/start", json={}).status_code == 200
    assert client.post("/api/sim/step", json={"num_steps": 5}).status_code == 200
    res2 = client.get("/api/frames/current")
    assert res2.status_code == 200
    from io import BytesIO

    from PIL import Image

    img = Image.open(BytesIO(res2.content))
    pixel = img.getpixel((0, 0))
    # Handle both grayscale (single value) and RGB (tuple) cases
    if isinstance(pixel, (int, float)):
        r = int(pixel)
        g = b = 0
    elif isinstance(pixel, tuple) and len(pixel) >= 3:
        r, g, b = pixel[:3]  # Take first 3 values in case of RGBA
    else:
        # Default fallback if pixel format is unexpected
        r = g = b = 0
    assert r == 5 % 256
    assert g == 0 and b == 0


def test_ws_events_streaming() -> None:
    app = create_app()
    client = TestClient(app)

    with client.websocket_connect("/ws/events") as ws:
        # First message is hello
        data = ws.receive_json()
        assert data.get("type") == "hello"
        assert "episode_running" in data
        assert "step" in data
        # Next message should be a state update
        data2 = ws.receive_json()
        assert data2.get("type") == "state"
        assert "metrics" in data2


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
    assert isinstance(state.get("metrics", {}).get("total_steps"), int | float)

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


def test_metrics_endpoint() -> None:
    app = create_app()
    client = TestClient(app)

    # Initial metrics
    res = client.get("/api/metrics")
    assert res.status_code == 200
    m: dict[str, Any] = res.json()
    assert set(m.keys()) == {"episodes_started", "total_steps", "steps_per_second"}
    e0 = m["episodes_started"]
    t0 = m["total_steps"]

    # Start and step should change metrics
    assert client.post("/api/sim/start", json={}).status_code == 200
    assert client.post("/api/sim/step", json={"num_steps": 2}).status_code == 200
    m2: dict[str, Any] = client.get("/api/metrics").json()
    assert m2["episodes_started"] >= e0
    assert m2["total_steps"] >= t0


def test_readyz_true_when_templates_exist() -> None:
    app = create_app()
    client = TestClient(app)

    res = client.get("/readyz")
    assert res.status_code == 200
    payload: dict[str, Any] = res.json()
    # Should be true because templates dir exists in repo
    assert payload["ready"] is True


def test_events_endpoint_basic() -> None:
    app = create_app()
    client = TestClient(app)

    # Perform a sequence of actions that emit events
    assert client.post("/api/sim/reset", json={"seed": 42}).status_code == 200
    assert client.post("/api/sim/start", json={}).status_code == 200
    assert client.post("/api/sim/step", json={"num_steps": 3}).status_code == 200
    # Query events
    res = client.get("/api/events")
    assert res.status_code == 200
    body: dict[str, Any] = res.json()
    assert isinstance(body.get("events"), list)
    types = [e.get("type") for e in body["events"]]
    # Ensure recent actions are present
    assert any(t == "reset" for t in types)
    assert any(t == "start" for t in types)
    assert any(t == "step" for t in types)
