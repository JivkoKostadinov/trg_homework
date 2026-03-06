import json
import logging
import re
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import Locator, Page, expect

import config
from pages.locators.life_at_trg_locators import LifeAtTRGLocators

logger = logging.getLogger(__name__)


class LifeAtTRGPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        # Role-based locators (DOM interaction deferred until action is called)
        self.careers_link: Locator = page.get_by_role(
            "link",
            name=LifeAtTRGLocators.CAREERS_LINK_NAME,
        )
        self.life_at_trg_link: Locator = page.get_by_role(
            "link",
            name=LifeAtTRGLocators.LIFE_AT_TRG_LINK_NAME,
        )
        self.core_values_heading: Locator = page.get_by_role(
            "heading",
            name=LifeAtTRGLocators.CORE_VALUES_HEADING_NAME,
        )

    def _follow_link(self, locator: Locator, error_msg: str) -> None:
        expect(locator.first).to_be_visible()
        href = locator.first.get_attribute("href")
        assert href is not None, error_msg
        self.page.goto(href)

    def navigate_to_life_at_trg(self) -> None:
        logger.info("Navigating to %s", config.TRG_HOME_URL)
        self.page.goto(config.TRG_HOME_URL)
        self._follow_link(self.careers_link, "Careers link href not found")
        logger.info("Navigated to Careers page")
        self._follow_link(self.life_at_trg_link, "Life At TRG link href not found")
        expect(self.core_values_heading.first).to_be_visible(
            timeout=config.PAGE_LOAD_TIMEOUT
        )
        logger.info("Life At TRG page loaded")

    def scroll_to_core_values(self) -> None:
        logger.info("Scrolling to Core Values section")
        self.core_values_heading.first.scroll_into_view_if_needed()
        expect(self.core_values_heading.first).to_be_in_viewport()

    def get_core_values(self) -> list[dict[str, str]]:
        # ── 1. Locate the card section ─────────────────────────────────────────
        section = self.page.locator(LifeAtTRGLocators.CORE_VALUES_SECTION)

        # ── 2. Collect all card-level headings ─────────────────────────────────
        all_headings = section.get_by_role("heading").all()
        card_headings = [
            h
            for h in all_headings
            if not re.search(r"core\s+values", h.inner_text().strip(), re.IGNORECASE)
        ]

        # ── 3. Extract data from each card ─────────────────────────────────────
        core_values = []
        for heading in card_headings:
            headline = heading.inner_text().strip()

            # Find the card container: among all section descendants that contain
            # an image AND this heading's exact text, `.last` gives the innermost
            # (most specific) match in document order — i.e. the individual card,
            # not the grid wrapper that encloses all cards.
            card = (
                section.locator(LifeAtTRGLocators.CARD_CONTAINER)
                .filter(has=self.page.get_by_role("heading", name=headline, exact=True))
                .last
            )

            description = (
                card.locator(LifeAtTRGLocators.CARD_DESCRIPTION)
                .first.inner_text()
                .strip()
            )
            image_src = (
                card.locator(LifeAtTRGLocators.CARD_IMAGE).first.get_attribute("src")
                or ""
            )

            core_values.append(
                {
                    "headline": headline,
                    "description": description,
                    "image_src": image_src,
                }
            )

        logger.info("Extracted %d core values", len(core_values))
        return core_values

    @staticmethod
    def count_exclamation_marks(core_values: list[dict[str, str]]) -> int:
        """Count all '!' characters across every headline and description."""
        return sum(
            cv["headline"].count("!") + cv["description"].count("!")
            for cv in core_values
        )

    @staticmethod
    def headline_to_filename(headline: str) -> str:
        """Convert a headline string to a safe, lowercase filename stem."""
        clean = re.sub(r"[^\w\s]", "", headline)
        return re.sub(r"\s+", "_", clean).strip("_").lower()

    @staticmethod
    def get_image_extension(url: str) -> str:
        """
        Derive the image file extension from a URL.
        Handles Wix CDN paths such as:
          .../media/abc_image.jpg/v1/fill/...
        """
        valid = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"}
        for segment in urlparse(url).path.split("/"):
            ext = Path(segment).suffix.lower()
            if ext in valid:
                return ext
        return ".jpg"

    def download_images(
        self, core_values: list[dict[str, str]], output_dir: Path
    ) -> None:
        """Download every core-value image and name the file after its headline."""
        output_dir.mkdir(parents=True, exist_ok=True)
        for cv in core_values:
            if not cv["image_src"]:
                logger.warning("Skipping image for %r — no image src found", cv["headline"])
                continue
            ext = self.get_image_extension(cv["image_src"])
            filename = self.headline_to_filename(cv["headline"]) + ext
            req = urllib.request.Request(
                cv["image_src"], headers={"User-Agent": "Mozilla/5.0"}
            )
            try:
                with urllib.request.urlopen(req) as response:
                    (output_dir / filename).write_bytes(response.read())
                logger.info("Downloaded: %s", filename)
            except urllib.error.HTTPError as exc:
                logger.warning(
                    "Skipping image for %r — HTTP %s: %s",
                    cv["headline"],
                    exc.code,
                    cv["image_src"],
                )
            except urllib.error.URLError as exc:
                logger.warning(
                    "Skipping image for %r — network error: %s",
                    cv["headline"],
                    exc.reason,
                )

    @staticmethod
    def save_core_values_json(
        core_values: list[dict[str, str]],
        exclamation_count: int,
        output_path: Path,
    ) -> None:
        """Persist core values and exclamation count to JSON."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "core_values": [
                {"headline": cv["headline"], "description": cv["description"]}
                for cv in core_values
            ],
            "exclamation_mark_count": exclamation_count,
        }
        output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
        logger.info(
            "Saved %d core values to %s (exclamation marks: %d)",
            len(core_values),
            output_path,
            exclamation_count,
        )
