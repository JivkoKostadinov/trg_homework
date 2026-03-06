import logging
import shutil
from collections.abc import Generator
from typing import Any

import pytest
from playwright.sync_api import Browser, BrowserContext, BrowserType, Page

import config
from pages.page_objects.life_at_trg_page import LifeAtTRGPage

logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def clean_output() -> None:
    if config.OUTPUT_DIR.exists():
        shutil.rmtree(config.OUTPUT_DIR)


@pytest.fixture()
def life_at_trg_page(
    browser_type: BrowserType,
    browser_type_launch_args: dict[str, Any],
) -> Generator[LifeAtTRGPage, None, None]:
    # ── BEFORE test: open browser ──────────────────────────────────────────────
    browser: Browser = browser_type.launch(
        **browser_type_launch_args,
        args=["--start-maximized"],
    )
    context: BrowserContext = browser.new_context(no_viewport=True)
    page: Page = context.new_page()
    browser_label = browser_type_launch_args.get("channel") or browser_type.name
    logger.info("[setup] Browser opened: %s", browser_label)

    yield LifeAtTRGPage(page)

    # ── AFTER test: close browser ──────────────────────────────────────────────
    logger.info("[teardown] Browser closed: %s", browser_label)
    context.close()
    browser.close()
