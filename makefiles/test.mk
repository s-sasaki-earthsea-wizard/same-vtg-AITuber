# Test-related Makefile targets
# This file contains all testing commands using pytest

.PHONY: docker-test docker-test-verbose

## Test Commands
docker-test:  ## Run tests inside Docker container
	docker compose exec $(SERVICE_NAME) pytest

docker-test-verbose:  ## Run tests with verbose output in Docker
	docker compose exec $(SERVICE_NAME) pytest -v -s

docker-test-llm:  ## Run LLM response tests only
	docker compose exec $(SERVICE_NAME) pytest tests/test_openai_adapter.py::TestOpenAIAdapter::test_chat_completions_basic -v -s

## Convenience aliases
test: docker-test  ## Alias for docker-test
test-verbose: docker-test-verbose  ## Alias for docker-test-verbose
test-v: docker-test-verbose  ## Short alias for docker-test-verbose
test-llm: docker-test-llm  ## Alias for docker-test-llm
