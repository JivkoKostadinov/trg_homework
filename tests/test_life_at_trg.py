import json
import logging

import config
from pages.page_objects.life_at_trg_page import LifeAtTRGPage

logger = logging.getLogger(__name__)


def test_core_values_extracted_and_saved(life_at_trg_page: LifeAtTRGPage) -> None:
    # ── 1. Navigation ──────────────────────────────────────────────────────────
    life_at_trg_page.navigate_to_life_at_trg()

    # ── 2. Scroll to Core Values ───────────────────────────────────────────────
    life_at_trg_page.scroll_to_core_values()

    # ── 3. Extract core values ─────────────────────────────────────────────────
    core_values = life_at_trg_page.get_core_values()
    assert len(core_values) > 0, "No core values were found on the page"
    for cv in core_values:
        assert cv["headline"], f"Empty headline in core value: {cv}"
        assert cv["description"], f"Empty description for: {cv['headline']!r}"
        logger.info("  Core value: [%s] — %s...", cv["headline"], cv["description"][:60])

    # ── 4. Count exclamation marks ─────────────────────────────────────────────
    exclamation_count = life_at_trg_page.count_exclamation_marks(core_values)
    assert exclamation_count >= 0, "Exclamation mark count must be a non-negative integer"
    logger.info("Exclamation marks found: %d", exclamation_count)

    # ── 5. Save core values to JSON ────────────────────────────────────────────
    life_at_trg_page.save_core_values_json(
        core_values, exclamation_count, config.CORE_VALUES_JSON
    )
    assert (
        config.CORE_VALUES_JSON.exists()
    ), f"JSON file was not created at {config.CORE_VALUES_JSON}"

    saved = json.loads(config.CORE_VALUES_JSON.read_text())
    assert len(saved["core_values"]) == len(core_values), (
        f"JSON contains {len(saved['core_values'])} entries, expected {len(core_values)}"
    )
    assert saved["exclamation_mark_count"] == exclamation_count, (
        f"JSON exclamation_mark_count {saved['exclamation_mark_count']} "
        f"does not match counted value {exclamation_count}"
    )
    logger.info("JSON verified: %d core values, %d exclamation marks", len(saved["core_values"]), exclamation_count)


def test_core_values_images_downloaded(life_at_trg_page: LifeAtTRGPage) -> None:
    # ── 1. Navigation ──────────────────────────────────────────────────────────
    life_at_trg_page.navigate_to_life_at_trg()

    # ── 2. Scroll to Core Values ───────────────────────────────────────────────
    life_at_trg_page.scroll_to_core_values()

    # ── 3. Extract core values ─────────────────────────────────────────────────
    core_values = life_at_trg_page.get_core_values()
    assert len(core_values) > 0, "No core values were found on the page"

    # ── 4. Download images ─────────────────────────────────────────────────────
    life_at_trg_page.download_images(core_values, config.IMAGES_DIR)

    downloaded = list(config.IMAGES_DIR.glob("*"))
    assert len(downloaded) == len(
        core_values
    ), f"Expected {len(core_values)} images, found {len(downloaded)}"

    # ── 5. Verify filenames match core value headlines ─────────────────────────
    downloaded_stems = {f.stem for f in downloaded}
    for cv in core_values:
        expected_stem = LifeAtTRGPage.headline_to_filename(cv["headline"])
        assert expected_stem in downloaded_stems, (
            f"No image file found for headline {cv['headline']!r} "
            f"(expected filename stem: {expected_stem!r})"
        )
        logger.info("  Filename verified: %s", expected_stem)
