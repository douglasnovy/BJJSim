from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import time
from collections.abc import Iterator
from pathlib import Path
from typing import Final

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

HTTPX_SPEC = importlib.util.find_spec("httpx")
UVICORN_SPEC = importlib.util.find_spec("uvicorn")
HAS_SERVER_DEPS = HTTPX_SPEC is not None and UVICORN_SPEC is not None

if HAS_SERVER_DEPS:
    import httpx

BASE_HOST: Final[str] = "127.0.0.1"
BASE_PORT: Final[int] = 8765
BASE_URL: Final[str] = f"http://{BASE_HOST}:{BASE_PORT}"


def _wait_for_server(url: str, timeout_s: float = 10.0) -> None:
    if not HAS_SERVER_DEPS:  # pragma: no cover - defensive guard
        raise RuntimeError("server dependencies are not installed")
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


@pytest.fixture(scope="session")  # type: ignore[misc]
def server_url() -> Iterator[str]:
    if not HAS_SERVER_DEPS:
        pytest.skip("uvicorn/httpx not installed; server fixture unavailable")

    env = os.environ.copy()
    env["UVICORN_WORKERS"] = "1"
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
