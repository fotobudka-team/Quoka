SHELL := /bin/bash

build:
	bash build.sh

run_local:
	docker-compose -f docker-compose.dev.yml up

run_prod:
	docker-compose -f docker-compose.prod.yml up --build

lint:
	source venv/bin/activate && ruff check src/

lint-fix:
	source venv/bin/activate && black . && ruff check src/ --fix