.PHONY: help setup dev console docker clean

SESSION ?= base-native-audio

help:
	@echo "Available commands:"
	@echo "  setup    - Install dependencies and download models"
	@echo "  dev      - Run agent in development mode"
	@echo "  console  - Run agent in console mode"
	@echo "  docker   - Run agent with Docker"
	@echo "  clean    - Clean cache and temp files"
	@echo ""
	@echo "Available sessions:"
	@echo "  - base-native-audio (default)"
	@echo "  - base-stt_llm_tts"
	@echo "  - test-elevenlabs-tts"
	@echo "  - test-openai-tts"
	@echo "  - test-gpt-4o-transcribe-stt"
	@echo ""
	@echo "Usage: make dev SESSION=test-elevenlabs-tts"

setup:
	uv sync
	uv run src/main.py download-files

dev:
	uv run src/main.py dev -$(SESSION)

console:
	uv run src/main.py console -$(SESSION)

docker:
	cd docker && docker-compose up --build

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	docker system prune -f