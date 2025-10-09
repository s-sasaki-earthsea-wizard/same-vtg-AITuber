"""
Unit tests for VoiceMaker TTS functionality.

These tests verify the voice generation pipeline:
- VoiceMaker.make_voice_tts() orchestration
- VoiceMaker.make_voice_openai() OpenAI TTS integration
- Audio file generation and format validation

Note: These are integration tests that make actual API calls to OpenAI.
Ensure OPENAI_API_KEY is set in .env before running.
"""

import os
import pytest
import tempfile
import soundfile
from pathlib import Path
from live.VoiceMaker import VoiceMaker, VoiceIO


class TestVoiceMaker:
    """Test suite for VoiceMaker class"""

    def test_make_voice_tts_generates_audio(self):
        """Test that make_voice_tts generates valid audio data"""
        test_text = "音声生成のテストです。"

        voice_io = VoiceMaker.make_voice_tts(test_text)

        # Verify VoiceIO structure
        assert voice_io is not None
        assert "data" in voice_io
        assert "sample_rate" in voice_io

        # Verify audio data properties
        assert voice_io["data"] is not None
        assert len(voice_io["data"]) > 0, "Audio data is empty"
        assert voice_io["sample_rate"] > 0, "Sample rate must be positive"

        # Typical sample rates: 16000, 22050, 24000, 44100, 48000
        assert voice_io["sample_rate"] in [16000, 22050, 24000, 44100, 48000], \
            f"Unexpected sample rate: {voice_io['sample_rate']}"

        print(f"\n[TTS Audio] Generated {len(voice_io['data'])} samples at {voice_io['sample_rate']}Hz")

    def test_make_voice_openai_generates_audio(self):
        """Test that make_voice_openai generates valid audio data"""
        test_text = "OpenAI TTSのテストです。"

        voice_io = VoiceMaker.make_voice_openai(test_text)

        # Verify VoiceIO structure
        assert voice_io is not None
        assert "data" in voice_io
        assert "sample_rate" in voice_io
        assert len(voice_io["data"]) > 0

        print(f"\n[OpenAI TTS] Generated {len(voice_io['data'])} samples")

    def test_make_voice_tts_with_japanese_text(self):
        """Test TTS with Japanese text to verify encoding handling"""
        japanese_texts = [
            "こんにちは、世界！",
            "バーチャルテックガレージへようこそ。",
            "今日はいい天気ですね。"
        ]

        for text in japanese_texts:
            voice_io = VoiceMaker.make_voice_tts(text)

            assert voice_io is not None
            assert len(voice_io["data"]) > 0, f"Failed to generate audio for: {text}"

        print(f"\n[Japanese TTS] Successfully generated audio for {len(japanese_texts)} texts")

    def test_make_voice_tts_with_english_text(self):
        """Test TTS with English text"""
        test_text = "Hello, this is a test of the text to speech system."

        voice_io = VoiceMaker.make_voice_tts(test_text)

        assert voice_io is not None
        assert len(voice_io["data"]) > 0

        print(f"\n[English TTS] Generated {len(voice_io['data'])} samples")

    def test_voice_io_can_be_written_to_file(self):
        """Test that VoiceIO can be successfully written to a WAV file"""
        test_text = "ファイル書き込みのテストです。"

        voice_io = VoiceMaker.make_voice_tts(test_text)

        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            tmp_path = Path(tmp_file.name)

        try:
            # Write audio to file
            soundfile.write(str(tmp_path), voice_io["data"], voice_io["sample_rate"])

            # Verify file was created and has content
            assert tmp_path.exists(), "Audio file was not created"
            assert tmp_path.stat().st_size > 1000, "Audio file is too small"

            # Verify file can be read back
            data, sample_rate = soundfile.read(str(tmp_path))
            assert len(data) > 0
            assert sample_rate == voice_io["sample_rate"]

            print(f"\n[File Write] Successfully wrote {tmp_path.stat().st_size} bytes to {tmp_path.name}")

        finally:
            # Cleanup
            if tmp_path.exists():
                tmp_path.unlink()

    def test_consecutive_tts_calls(self):
        """Test that multiple consecutive TTS calls work correctly"""
        texts = [
            "最初の音声です。",
            "二番目の音声です。",
            "三番目の音声です。"
        ]

        voice_ios = []
        for text in texts:
            voice_io = VoiceMaker.make_voice_tts(text)
            assert voice_io is not None
            assert len(voice_io["data"]) > 0
            voice_ios.append(voice_io)

        # Verify all generations succeeded
        assert len(voice_ios) == len(texts)

        print(f"\n[Consecutive TTS] Successfully generated {len(voice_ios)} audio samples")

    def test_save_voice_to_file(self):
        """Test that save_voice_to_file creates valid WAV files"""
        test_text = "ファイル保存のテストです。"

        voice_io = VoiceMaker.make_voice_tts(test_text)

        # Create temporary file path
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            tmp_path = Path(tmp_file.name)

        try:
            # Save voice to file using new method
            VoiceMaker.save_voice_to_file(voice_io, str(tmp_path))

            # Verify file was created and has content
            assert tmp_path.exists(), "Audio file was not created"
            assert tmp_path.stat().st_size > 1000, "Audio file is too small"

            # Verify file can be read back
            data, sample_rate = soundfile.read(str(tmp_path))
            assert len(data) > 0
            assert sample_rate == voice_io["sample_rate"]

            print(f"\n[save_voice_to_file] Successfully wrote {tmp_path.stat().st_size} bytes")

        finally:
            # Cleanup
            if tmp_path.exists():
                tmp_path.unlink()

    def test_save_voice_to_file_with_long_audio(self):
        """Test saving longer audio files"""
        test_text = "これは長い音声ファイルのテストです。複数の文章を含んでいます。音声合成の品質を確認します。"

        voice_io = VoiceMaker.make_voice_tts(test_text)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            tmp_path = Path(tmp_file.name)

        try:
            VoiceMaker.save_voice_to_file(voice_io, str(tmp_path))

            # Verify file size is reasonable for longer audio
            file_size = tmp_path.stat().st_size
            assert file_size > 5000, f"Audio file too small: {file_size} bytes"

            print(f"\n[Long Audio] Saved {file_size} bytes ({len(voice_io['data'])} samples)")

        finally:
            if tmp_path.exists():
                tmp_path.unlink()


if __name__ == "__main__":
    # Allow running tests directly with: python test_voice_maker.py
    pytest.main([__file__, "-v", "-s"])
