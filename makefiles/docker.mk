# Docker-related Makefile targets
# This file contains all Docker and Docker Compose commands

.PHONY: docker-down docker-restart docker-logs docker-shell
.PHONY: docker-up-dev docker-up-prod docker-down-dev docker-restart-dev docker-logs-rtmp
.PHONY: docker-build docker-rebuild docker-clean
.PHONY: docker-env-setup docker-env-check

## Docker Compose Commands

docker-down:  ## Stop and remove containers
	docker compose down

docker-restart:  ## Restart containers
	docker compose restart

docker-logs:  ## Show Docker Compose logs
	docker compose logs -f

docker-shell:  ## Open shell in container
	docker compose exec $(SERVICE_NAME) /bin/bash

## Environment-Specific Commands

docker-up-dev:  ## Start development environment with local RTMP server (build included)
	docker compose --profile dev up --build -d
	@echo "✅ Development environment started"
	@echo "📺 RTMP server: rtmp://localhost:1935/live/test"
	@echo "🎬 Run demo: make demo"

docker-up-prod:  ## Start production environment for YouTube Live streaming (build included)
	docker compose up --build -d
	@echo "✅ Production environment started"
	@echo "🚀 Ready for YouTube Live streaming"
	@echo "⚙️  Configure .env with YouTube RTMP credentials"

docker-down-dev:  ## Stop all containers including RTMP server
	docker compose --profile dev down

docker-restart-dev:  ## Restart development environment (rebuild with new dependencies)
	docker compose --profile dev down
	docker compose --profile dev up --build -d
	@echo "✅ Development environment restarted"

docker-logs-rtmp:  ## Show RTMP server logs
	docker compose logs -f rtmp-server

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
down: docker-down  ## Alias for docker-down
restart: docker-restart  ## Alias for docker-restart
logs: docker-logs  ## Alias for docker-logs
shell: docker-shell  ## Alias for docker-shell
up-dev: docker-up-dev  ## Alias for docker-up-dev
up-prod: docker-up-prod  ## Alias for docker-up-prod
down-dev: docker-down-dev  ## Alias for docker-down-dev
restart-dev: docker-restart-dev  ## Alias for docker-restart-dev
logs-rtmp: docker-logs-rtmp  ## Alias for docker-logs-rtmp
build: docker-build  ## Alias for docker-build
rebuild: docker-rebuild  ## Alias for docker-rebuild
clean: docker-clean  ## Alias for docker-clean
env-setup: docker-env-setup  ## Alias for docker-env-setup
env-check: docker-env-check  ## Alias for docker-env-check
