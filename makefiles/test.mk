# Test-related Makefile targets
# This file contains all testing commands using pytest
# All tests run inside Docker container (the only supported environment)

.PHONY: test test-verbose test-v test-llm test-tts test-openai

## Test Commands
test:  ## Run all tests
	docker compose exec $(SERVICE_NAME) pytest

test-verbose:  ## Run tests with verbose output
	docker compose exec $(SERVICE_NAME) pytest -v -s

test-v: test-verbose  ## Short alias for test-verbose

test-llm:  ## Run LLM response tests only
	docker compose exec $(SERVICE_NAME) pytest tests/test_openai_adapter.py::TestOpenAIAdapter::test_chat_completions_basic -v -s

test-tts:  ## Run TTS voice generation tests only
	docker compose exec $(SERVICE_NAME) pytest tests/test_voice_maker.py -v -s

test-openai:  ## Run all OpenAI API tests (LLM + TTS)
	docker compose exec $(SERVICE_NAME) pytest tests/test_openai_adapter.py tests/test_voice_maker.py -v -s
