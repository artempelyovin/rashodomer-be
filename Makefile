SHELL := /bin/bash
PROJECT_DIR ?= $(shell git rev-parse --show-toplevel)


.PHONY: format
format:
	uv run ruff format $(PROJECT_DIR)/src  # run `black`
	uv run ruff check $(PROJECT_DIR)/src --select I --fix   # run `isort`


.PHONY: lint
lint:
	uv run ruff check $(PROJECT_DIR)/src/
	uv run mypy $(PROJECT_DIR)/src/
