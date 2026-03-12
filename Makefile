.PHONY: test test-headed test-ff test-screenshots test-video test-parallel lint typecheck

test:
	poetry run pytest

test-headed:
	poetry run pytest --headed --slowmo 500

test-ff:
	poetry run pytest --browser firefox

test-screenshots:
	poetry run pytest --screenshot=only-on-failure

test-video:
	poetry run pytest --video=retain-on-failure

test-parallel:
	poetry run pytest --browser chromium --browser firefox -n 2

lint:
	poetry run pre-commit run -a

typecheck:
	poetry run mypy .
