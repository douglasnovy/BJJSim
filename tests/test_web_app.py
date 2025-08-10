from __future__ import annotations

import sys
from typing import Any
import pytest
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
    if sys.platform.startswith("win"):
        pytest.skip("WS test flaky on Windows runners")
    app = create_app()
    client = TestClient(app)

    with client.websocket_connect("/ws/events") as ws:
        data = ws.receive_json()
        assert data.get("type") == "hello"
        assert "episode_running" in data
        assert "step" in data
