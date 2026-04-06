.PHONY: format
format:
	uv run ruff format src/
	uv run ruff check src/ --select I --fix   # fix only isort


.PHONY: lint
lint:
	uv run ruff check src/


.PHONY: type-check
type-check:
	uv run ty check src/