.PHONY: test test-headed test-ff lint typecheck

test:
	poetry run pytest

test-headed:
	poetry run pytest --headed --slowmo 500

test-ff:
	poetry run pytest --browser firefox

lint:
	poetry run pre-commit run -a

typecheck:
	poetry run mypy .
