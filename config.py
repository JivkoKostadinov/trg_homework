from pathlib import Path

# ── URLs ──────────────────────────────────────────────────────────────────────
TRG_HOME_URL: str = "https://www.trgint.com"

# ── Timeouts (milliseconds) ───────────────────────────────────────────────────
PAGE_LOAD_TIMEOUT: int = 30_000

# ── Output paths ──────────────────────────────────────────────────────────────
OUTPUT_DIR: Path = Path("output")
CORE_VALUES_JSON: Path = OUTPUT_DIR / "core_values.json"
IMAGES_DIR: Path = OUTPUT_DIR / "images"
