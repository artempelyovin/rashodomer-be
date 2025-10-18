SHELL := /bin/bash
PROJECT_DIR ?= $(shell git rev-parse --show-toplevel)


.PHONY: format
format:
	poetry run ruff format $(PROJECT_DIR)/src  # run `black`
	poetry run ruff check $(PROJECT_DIR)/src --select I --fix   # run `isort`


.PHONY: lint
lint:
	poetry run ruff check $(PROJECT_DIR)/src/
	poetry run mypy $(PROJECT_DIR)/src/
