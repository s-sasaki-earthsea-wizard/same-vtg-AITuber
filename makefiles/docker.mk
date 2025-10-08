# Docker-related Makefile targets
# This file contains all Docker and Docker Compose commands

.PHONY: docker-up docker-start docker-down docker-restart docker-logs docker-shell
.PHONY: docker-build docker-rebuild docker-clean
.PHONY: docker-env-setup docker-env-check

## Docker Compose Commands
docker-up:  ## Start with Docker Compose (build included)
	docker compose up --build

docker-start:  ## Start with Docker Compose (no build)
	docker compose up

docker-down:  ## Stop and remove containers
	docker compose down

docker-restart:  ## Restart containers
	docker compose restart

docker-logs:  ## Show Docker Compose logs
	docker compose logs -f

docker-shell:  ## Open shell in container
	docker compose exec $(SERVICE_NAME) /bin/bash

## Docker Image Management
docker-build:  ## Build Docker image
	docker compose build

docker-rebuild:  ## Rebuild Docker image (no cache)
	docker compose build --no-cache

docker-clean:  ## Remove containers, unused images, and volumes
	docker compose down -v
	docker system prune -f

## Environment Setup
docker-env-setup:  ## Setup .env file from .env.example
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo ".env file created. Please edit it to set your API keys."; \
	else \
		echo ".env file already exists."; \
	fi

docker-env-check:  ## Check environment variables
	@echo "=== Environment Variables ==="
	@if [ -f .env ]; then \
		echo "OPENAI_API_KEY: $$(grep OPENAI_API_KEY .env | cut -d'=' -f2 | sed 's/"//g' | sed 's/your-openai-api-key/NOT SET/g')"; \
		echo "OBS_WS_PASSWORD: $$(grep OBS_WS_PASSWORD .env | cut -d'=' -f2 | sed 's/"//g' | sed 's/your-obs-websocket-password/NOT SET/g')"; \
		echo "OBS_WS_PORT: $$(grep OBS_WS_PORT .env | cut -d'=' -f2 | sed 's/"//g')"; \
		echo "YOUTUBE_VIDEO_ID: $$(grep YOUTUBE_VIDEO_ID .env | cut -d'=' -f2 | sed 's/"//g' | sed 's/your-youtube-video-id/NOT SET/g')"; \
	else \
		echo ".env file not found. Run 'make docker-env-setup' first."; \
	fi

## Convenience aliases (shorter names)
up: docker-up  ## Alias for docker-up
start: docker-start  ## Alias for docker-start
down: docker-down  ## Alias for docker-down
restart: docker-restart  ## Alias for docker-restart
logs: docker-logs  ## Alias for docker-logs
shell: docker-shell  ## Alias for docker-shell
build: docker-build  ## Alias for docker-build
rebuild: docker-rebuild  ## Alias for docker-rebuild
clean: docker-clean  ## Alias for docker-clean
env-setup: docker-env-setup  ## Alias for docker-env-setup
env-check: docker-env-check  ## Alias for docker-env-check
