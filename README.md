# Playwright TRG End-to-end Tests

## About

End-to-end test suite for [trgint.com](https://www.trgint.com) using Playwright and pytest.
Two focused tests navigate to the **Life At TRG** page, scrape the Core Values section,
count exclamation marks, save results to JSON, and download each card image.

## Project Structure

```
task_three/
├── config.py                          # URL, timeout, and output path constants
├── conftest.py                        # Fixtures: browser lifecycle, output cleanup, page object
├── pytest.ini                         # pytest defaults (browser, headed mode, log level)
├── pyproject.toml                     # Poetry dependencies and tool configuration
├── Makefile                           # Task runner shortcuts (test, lint, typecheck)
├── .pre-commit-config.yaml            # Pre-commit hooks (black, isort, flake8, mypy, pylint)
├── helpers/
│   └── random_data.py                 # Test data generators (e.g. random_full_name)
├── pages/
│   ├── locators/
│   │   └── life_at_trg_locators.py    # All CSS/role/XPath selectors for the Life At TRG page
│   └── page_objects/
│       └── life_at_trg_page.py        # Page Object with navigation, scraping, and I/O methods
├── tests/
│   └── test_life_at_trg.py            # Two focused tests: core values scrape/JSON + image download
└── output/                            # Generated at runtime (gitignored)
    ├── core_values.json               # Scraped core values + exclamation mark count
    └── images/                        # Downloaded core-value card images (named after headlines)
```

The project follows the **Page Object Pattern**: selectors live in `locators/`, page behaviour
in `page_objects/`, test logic in `tests/`, and reusable test data generators in `helpers/`.

## What the Tests Do

### `test_core_values_extracted_and_saved`

1. Navigates `trgint.com → Careers → Life At TRG`
2. Scrolls to the **Core Values** section
3. Extracts each card's headline and description — asserts both are non-empty
4. Counts all `!` characters across every headline and description
5. Saves results to `output/core_values.json`
6. Verifies the JSON contains the correct number of entries and exclamation mark count

### `test_core_values_images_downloaded`

1. Navigates `trgint.com → Careers → Life At TRG`
2. Scrolls to the **Core Values** section
3. Extracts each card's headline and image URL
4. Downloads each card image to `output/images/` named after its headline
5. Verifies the downloaded file count matches the number of core values
6. Verifies each filename corresponds to the correct core value headline

**Sample output (`output/core_values.json`):**
```json
{
  "core_values": [
    { "headline": "Whatever it takes!", "description": "..." },
    { "headline": "We work together.",  "description": "..." },
    { "headline": "We make an impact.", "description": "..." },
    { "headline": "Passion is our fuel.", "description": "..." }
  ],
  "exclamation_mark_count": 2
}
```

## Setup & Usage

[Poetry](https://python-poetry.org/) is used for dependency management. All `make` commands
run inside the Poetry venv automatically — no manual activation needed.

### One-time setup

```bash
pip install poetry                   # 1. Install Poetry
poetry install                       # 2. Install project dependencies
poetry run playwright install        # 3. Install Playwright browsers
pre-commit install                   # 4. Install pre-commit hooks (optional)
```

> To activate the venv manually (Poetry 2.0+): `poetry env activate`

### Running tests

```bash
make test          # run all tests (Chromium, headed)
make test-headed   # run with slow-motion for debugging
make test-ff       # run on Firefox
```

### Code quality

```bash
make lint          # run all pre-commit hooks (black, isort, flake8, mypy, pylint)
make typecheck     # run mypy only
```

### Artifacts

```bash
make test-screenshots  # capture screenshots on failure
make test-video        # record video
```

Results are saved to `test-results/` by default.

### Parallel execution

```bash
make test-parallel
```
