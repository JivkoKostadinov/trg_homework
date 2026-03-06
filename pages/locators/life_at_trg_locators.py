import re
from typing import Final


class LifeAtTRGLocators:  # pylint: disable=too-few-public-methods
    # ── Navigation (role-based) ────────────────────────────────────────────────

    # TRG main site — "Careers" link in the top navigation
    CAREERS_LINK_NAME: Final[str] = "Careers"

    # Careers portal — "Life At TRG" (or "#Life At TRG") nav link
    LIFE_AT_TRG_LINK_NAME: Final[re.Pattern[str]] = re.compile(
        r"Life\s+At\s+TRG", re.IGNORECASE
    )

    # Life At TRG page — "Core Values" section heading
    CORE_VALUES_HEADING_NAME: Final[re.Pattern[str]] = re.compile(
        r"Core\s+Values", re.IGNORECASE
    )

    # ── Core Values section — XPath / CSS selectors ────────────────────────────

    # The card section is the first <section> sibling that follows the intro section
    # which contains the Core Values heading
    CORE_VALUES_SECTION: Final[str] = 'section:has-text("Core Values") + section'

    # Any descendant of the section that contains an image — used as the candidate
    # pool when searching for a specific card by heading text (see get_core_values).
    CARD_CONTAINER: Final[str] = "*:has(img[src])"

    # Description paragraph inside a card
    CARD_DESCRIPTION: Final[str] = "p"

    # Image element inside a card
    CARD_IMAGE: Final[str] = "img[src]"
