from __future__ import annotations

import os
from typing import Any

import pytest

pytest.importorskip("playwright.sync_api", reason="Playwright not installed")
from playwright.sync_api import Page, sync_playwright  # type: ignore  # noqa: E402


def test_dashboard_smoke(server_url: str) -> None:
    # Skip in environments without browsers installed
    if os.environ.get("CI") is None and not os.environ.get("PLAYWRIGHT_BROWSERS_INSTALLED"):
        pytest.skip("Playwright browsers not installed locally")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page: Page = browser.new_page()
        page.goto(server_url + "/")

        # Controls present
        assert page.get_by_test_id("btn-start").is_visible()
        assert page.get_by_test_id("btn-reset").is_visible()
        assert page.get_by_test_id("btn-step").is_visible()

        # Start episode and step once
        page.get_by_test_id("btn-start").click()
        page.get_by_test_id("btn-step").click()

        # Verify metrics text updates eventually
        page.wait_for_timeout(500)
        running_text = page.locator("#val-running").inner_text()
        step_text = page.locator("#val-step").inner_text()
        assert running_text in {"yes", "no"}
        # Step should be an integer string
        assert step_text.isdigit()

        browser.close()


