"""
Unit tests for OpenAI API adapter.

These tests verify the integration with OpenAI API services:
- Chat completion (LLM response generation)
- Text-to-speech (TTS voice synthesis)

Note: These are integration tests that make actual API calls to OpenAI.
Ensure OPENAI_API_KEY is set in .env before running.
"""

import os
import pytest
from api.openai_adapter import OpenAIAdapter


class TestOpenAIAdapter:
    """Test suite for OpenAIAdapter class"""

    @pytest.fixture
    def adapter(self):
        """Create OpenAIAdapter instance for testing"""
        return OpenAIAdapter()

    def test_api_key_is_configured(self):
        """Verify that OPENAI_API_KEY is configured"""
        api_key = os.getenv("OPENAI_API_KEY")
        assert api_key is not None, "OPENAI_API_KEY is not set in .env"
        assert len(api_key) > 0, "OPENAI_API_KEY is empty"

    def test_chat_completions_basic(self, adapter):
        """Test basic chat completion functionality"""
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello, World!' in Japanese."}
        ]

        response = adapter.chat_completions(messages)

        # Verify response is not empty
        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 0

        print(f"\n[Chat Completion Response]\n{response}")

    def test_chat_completions_with_character(self, adapter):
        """Test chat completion with character-specific prompt"""
        messages = [
            {"role": "system", "content": "あなたは語尾が「のじゃ」な強気なおじさんです"},
            {"role": "user", "content": "今日の天気はどうですか？"}
        ]

        response = adapter.chat_completions(messages)

        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 0

        print(f"\n[Character Chat Response]\n{response}")

    def test_create_voice(self, adapter):
        """Test TTS voice synthesis functionality"""
        test_text = "こんにちは、AIチューバーです。"

        audio_bytes = adapter.create_voice(test_text)

        # Verify audio data is returned
        assert audio_bytes is not None
        assert isinstance(audio_bytes, bytes)
        assert len(audio_bytes) > 0

        # Audio file should have reasonable size (at least 1KB for short text)
        assert len(audio_bytes) > 1000, f"Audio data too small: {len(audio_bytes)} bytes"

        print(f"\n[TTS Response] Generated {len(audio_bytes)} bytes of audio data")

    def test_create_message_helper(self, adapter):
        """Test create_message helper method"""
        message = adapter.create_message("user", "Test content")

        assert message["role"] == "user"
        assert message["content"] == "Test content"
        assert "role" in message
        assert "content" in message


if __name__ == "__main__":
    # Allow running tests directly with: python test_openai_adapter.py
    pytest.main([__file__, "-v", "-s"])
