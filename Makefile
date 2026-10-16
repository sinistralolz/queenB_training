
.PHONY: lint types test security arch check

lint:
	ruff check . && ruff format --check .

types:
	mypy

test:
	python -m pytest --ignore=tests/test_lab_vulnerable.py --cov=src/queenbee --cov-fail-under=90

security:
	bandit -q -r src -c pyproject.toml
	python -m pip_audit --no-deps -r /dev/null

arch:
	PYTHONPATH=src lint-imports

check: lint types test security arch
