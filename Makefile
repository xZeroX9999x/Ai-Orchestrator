.PHONY: help install install-dev lint format type test cov clean build \
        docker-build docker-up docker-down pre-commit-install

PYTHON ?= python
PACKAGE = ai_orchestrator

help: ## Mostrar esta ayuda
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Instalar el paquete
	$(PYTHON) -m pip install -e .

install-dev: ## Instalar con dependencias de desarrollo
	$(PYTHON) -m pip install -e ".[dev]"

lint: ## Ejecutar ruff check
	ruff check .

format: ## Formatear con ruff
	ruff format .
	ruff check --fix .

type: ## Type checking con mypy
	mypy $(PACKAGE)

test: ## Ejecutar tests
	pytest

cov: ## Tests con coverage report
	pytest --cov=$(PACKAGE) --cov-report=term-missing --cov-report=html

clean: ## Limpiar artefactos de build y caches
	rm -rf build dist *.egg-info
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} +

build: clean ## Construir sdist y wheel
	$(PYTHON) -m build

docker-build: ## Construir imagen Docker
	docker build -t ai-orchestrator:latest .

docker-up: ## Levantar stack con docker compose
	docker compose up -d

docker-down: ## Bajar stack
	docker compose down

pre-commit-install: ## Instalar hooks de pre-commit
	pre-commit install

all: format lint type test ## Pipeline completa de validación local
