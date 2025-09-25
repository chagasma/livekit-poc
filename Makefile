.PHONY: help setup dev console docker clean

help:
	@echo "Available commands:"
	@echo "  setup    - Install dependencies and download models"
	@echo "  dev      - Run agent in development mode"
	@echo "  console  - Run agent in console mode"
	@echo "  docker   - Run agent with Docker"
	@echo "  clean    - Clean cache and temp files"

setup:
	uv sync
	uv run src/main.py download-files

dev:
	uv run src/main.py dev

console:
	uv run src/main.py console

docker:
	cd docker && docker-compose up --build

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	docker system prune -f