.PHONY: help

help: ## helper
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

.DEFAULT_GOAL := help

setup-dev:
	chmod +x ./setup && ./setup

lint:
	pre-commit run --all-files

lint-black:
	black aziona

lint-flake8:
	flake8 aziona

lint-isort:
	isort aziona