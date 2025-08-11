from __future__ import annotations

import os
import subprocess
import sys
import time
from collections.abc import Iterator
from typing import Final

import httpx
import pytest


BASE_HOST: Final[str] = "127.0.0.1"
BASE_PORT: Final[int] = 8765
BASE_URL: Final[str] = f"http://{BASE_HOST}:{BASE_PORT}"


def _wait_for_server(url: str, timeout_s: float = 10.0) -> None:
    start = time.monotonic()
    while time.monotonic() - start < timeout_s:
        try:
            r = httpx.get(f"{url}/api/sim/state", timeout=1.0)
            if r.status_code == 200:
                return
        except Exception:
            pass
        time.sleep(0.1)
    raise RuntimeError("Server did not become ready in time")


@pytest.fixture(scope="session")
def server_url() -> Iterator[str]:
    env = os.environ.copy()
    env["UVICORN_WORKERS"] = "1"
    # Start uvicorn as a subprocess using the app factory
    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "bjjsim.web.app:create_app",
            "--factory",
            "--host",
            BASE_HOST,
            "--port",
            str(BASE_PORT),
        ],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        _wait_for_server(BASE_URL, timeout_s=15.0)
        yield BASE_URL
    finally:
        try:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except Exception:
                proc.kill()
        except Exception:
            pass


