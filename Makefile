SHELL := /bin/bash

build:
	bash build.sh

run_local:
	docker-compose -f docker-compose.dev.yml up

run_prod:
	docker-compose -f docker-compose.prod.yml up --build

lint:
	source venv/bin/activate && ruff check .

lint-fix:
	source venv/bin/activate && ruff check . --fix