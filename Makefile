.PHONY: venv install dev-install test run docker-build docker-run lint format typecheck

venv:
	python3 -m venv .venv

install:
	. .venv/bin/activate && pip install -r requirements.txt

dev-install:
	. .venv/bin/activate && pip install -r requirements-dev.txt && pre-commit install

test:
	. .venv/bin/activate && pytest -q

run:
	. .venv/bin/activate && uvicorn valuation_service.main:app --app-dir src --reload --port 8000

lint:
	. .venv/bin/activate && ruff check src tests

format:
	. .venv/bin/activate && ruff format src tests

typecheck:
	. .venv/bin/activate && mypy src

docker-build:
	docker build -t valuation-service:latest .

docker-run:
	docker run -p 8000:8000 valuation-service:latest
