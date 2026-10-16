
SHELL := /bin/bash

.PHONY: lint types test security arch check

lint:
	ruff check . && ruff format --check .

types:
	mypy

test:
	python -m pytest --ignore=tests/test_lab_vulnerable.py --cov=src/queenbee --cov-fail-under=90

security:
	bandit -q -r src -c pyproject.toml
	python -m pip_audit -r <(python -c "import tomllib; p=tomllib.load(open('pyproject.toml','rb')); print('\n'.join(p['project']['optional-dependencies']['dev']))")

arch:
	PYTHONPATH=src lint-imports

check: lint types test security arch
